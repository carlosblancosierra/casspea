from django.db import models
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from custom_chocolates.models import UserChocolateDesign
from discounts.models import Discount
from decimal import *
from django.dispatch import receiver

from boxes.models import Box
from shipping.models import ShippingType

User = settings.AUTH_USER_MODEL


# Create your models here.
class CartsManager(models.Manager):
    def new_or_get(self, request):

        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id).filter(active=True)

        if qs.count() == 1:
            new_object = False
            cart_obj = qs.first()

            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_object = True
            request.session['cart_id'] = cart_obj.id

        return cart_obj, new_object

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user

        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)

    shipping_type = models.ForeignKey(ShippingType, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CartsManager()

    def __unicode__(self):
        return "ID: {}. Total is ${}".format(self.id, self.total)

    @property
    def subtotal(self):
        entries = CartEntry.objects.filter(active=True, cart=self)
        subtotal = Decimal('0.00')
        for entry in entries:
            subtotal += Decimal(entry.total)
        return round(subtotal, 2)

    @property
    def shipping_free(self):
        subtotal = self.subtotal
        if subtotal >= 45:
            return True
        else:
            return False

    @property
    def shipping_cost(self):
        if not self.shipping_free and self.shipping_type:
            return self.shipping_type.cost
        else:
            return 0

    @property
    def total(self):
        return round(
            float(self.subtotal) +
            float(self.shipping_cost),
            2)


class CartEntryManager(models.Manager):

    def new(self, request, product, quantity):
        cart_obj, new_cart = Cart.objects.new_or_get(request)

        if quantity and int(quantity) > 0:
            return self.model.objects.create(
                product=product,
                cart=cart_obj,
                quantity=quantity
            )

    def entries(self, request):
        entries = []
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            entries = self.filter(active=True, cart__id=cart_id)
            for entry in entries:
                if entry.product.size.sold_out:
                    entry.active = False
                    entry.save()
        return entries.filter(active=True)

    def set_inactive(self, request, id):
        qs = self.filter(id=id)
        if len(qs) == 1:
            obj = qs.first()
            obj.active = False
            obj.save()
            # print(obj.active)

    def empty_cart(self, request):
        if not self.entries(request):
            return True
        return False

    def discount_total(self, request):
        entries = self.entries(request)
        if entries:
            raw_total = Decimal('0.00')
            cart = entries.first().cart
            for entry in entries:
                raw_total_entry = Decimal(entry.raw_total)
                raw_total += raw_total_entry
            discount_total = raw_total - Decimal(cart.subtotal)
            return round(float(discount_total), 2)
        return 0.00


class CartEntry(models.Model):
    quantity = models.PositiveIntegerField()

    # limit = models.Q(app_label='boxes', model='box')  # | models.Q(app_label='miapp', model='article')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    # total = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    user_chocolate_design = models.ForeignKey(
        UserChocolateDesign,
        related_name="custom_design",
        on_delete=models.PROTECT,
        blank=True,
        null=True)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartEntryManager()

    def __str__(self):
        return "{}".format(self.id)

    @property
    def total(self):
        return self.price * self.quantity

    @property
    def raw_total(self):
        return self.product.price * self.quantity

    @property
    def cart_boxes(self):
        entries = CartEntry.objects.filter(cart=self.cart, active=True)
        total = 0
        for entry in entries:
            if isinstance(entry.product, Box):
                total += entry.quantity
        return total

    @property
    def more_than_15_boxes(self):
        boxes = self.cart_boxes
        if boxes >= 15:
            return True

    @property
    def more_than_30_boxes(self):
        boxes = self.cart_boxes
        if boxes >= 30:
            return True

    @property
    def discounted_price(self):
        discount = self.cart.discount
        if discount:
            if discount.type == Discount.PERCENTAGE:
                price = float(self.product.price)
                discount = price * float(discount.amount / 100)
                return price - discount
        else:
            return None

    @property
    def has_discount(self):
        if self.cart.discount and self.product.size not in self.cart.discount.box_exclusions.all():
            return True
        else:
            return False

    @property
    def price(self):
        price = self.product.price
        if self.has_discount:
            return self.discounted_price
        else:
            return price

    @property
    def discount_total_str(self):
        discount = self.cart.discount
        if discount:
            return int(discount.amount)
        else:
            return None


@receiver(pre_save, sender=Cart)
def set_default_shipping_type(sender, instance, **kwargs):
    if instance.shipping_type is None:
        # Get the default shipping type (if it exists)
        default_shipping_type = ShippingType.objects.filter(default=True).first()
        if default_shipping_type:
            instance.shipping_type = default_shipping_type
