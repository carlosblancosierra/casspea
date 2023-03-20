from django.db import models
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from custom_chocolates.models import UserChocolateDesign

from boxes.models import Box

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
    subtotal = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=15, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = CartsManager()

    def __unicode__(self):
        return "ID: {}. Total is ${}".format(self.id, self.total)


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
        return entries

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

    def cart_subtotal(self, request):
        entries = self.entries(request)
        total = 0
        for entry in entries:
            subtotal = entry.total
            total += subtotal
        return total

    def cart_boxes(self, request):
        entries = self.entries(request)
        boxes = 0
        for entry in entries:
            if entry.content_type == ContentType.objects.get_for_model(Box):
                boxes += entry.quantity

        print(boxes)
        return boxes

    def shipping_free(self, request):
        cart_subtotal = self.cart_subtotal(request)
        if cart_subtotal >= 45:
            return True
        else:
            return False

    def cart_shipping_cost(self, request):
        if self.shipping_free(request):
            return 0.00
        else:
            return 5.99

    def cart_total(self, request):
        cart_subtotal = float(self.cart_subtotal(request))
        cart_shipping_cost = float(self.cart_shipping_cost(request))
        total = cart_subtotal + cart_shipping_cost

        return round(total, 2)

    def more_than_15(self, request):
        boxes = self.cart_boxes(request)
        if boxes >= 15:
            return True
        return False

    def more_than_30(self, request):
        boxes = self.cart_boxes(request)
        if boxes >= 30:
            return True
        return False


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
    def cart_boxes(self):
        entries = CartEntry.objects.filter(cart=self.cart, active=True)
        total = 0
        for entry in entries:
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
        if self.more_than_30_boxes:
            return float(self.product.price) * 0.85
        elif self.more_than_15_boxes:
            return float(self.product.price) * 0.9
        else:
            return None

    @property
    def has_discount(self):
        if self.more_than_15_boxes or self.more_than_30_boxes:
            return True
        else:
            return False

    @property
    def price(self):
        price = self.product.price
        if self.discounted_price:
            return self.discounted_price
        else:
            return price