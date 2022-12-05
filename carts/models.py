from django.db import models
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
            print(obj.active)

    #
    # def new_or_update(self, request, sku_product_id, quantity):
    #
    #     if sku_product_id is not None:
    #         try:
    #             sku_product = SkuProduct.objects.get(sku=sku_product_id)
    #
    #         except SkuProduct.DoesNotExist:
    #             messages.error(request, "Error de producto")
    #             return redirect("carts:home")
    #
    #     cart, created = Cart.objects.new_or_get(request)
    #
    #     cart_entry = self.filter(cart=cart).filter(sku_product=sku_product)
    #
    #     if cart_entry.count() == 1:
    #         entry = cart_entry.first()
    #         if int(quantity) > 0:
    #             entry.quantity = quantity
    #             entry.save()
    #
    #         elif int(quantity) == 0:
    #             entry.delete()
    #
    #     elif cart_entry.count() > 1:
    #         raise MultipleObjectsReturned
    #
    #     else:
    #         entry = self.new(request, sku_product=sku_product, quantity=quantity)
    #
    # def add_or_remove_quantity(self, request, sku_product_id, quantity):
    #
    #     if sku_product_id is not None:
    #         try:
    #             sku_product = SkuProduct.objects.get(sku=sku_product_id)
    #
    #         except SkuProduct.DoesNotExist:
    #             messages.error(request, "Error de producto")
    #             return redirect("carts:home")
    #     cart, created = Cart.objects.new_or_get(request)
    #     cart_entry = self.filter(cart=cart).filter(sku_product=sku_product)
    #
    #     if cart_entry.count() == 1:
    #         entry = cart_entry.first()
    #         print(quantity)
    #         entry.quantity = entry.quantity + quantity
    #         entry.save()
    #
    #         if entry.quantity <= 0:
    #             entry.delete()
    #
    # def add_1(self, request, sku_product_id):
    #     self.add_or_remove_quantity(request, sku_product_id, 1)
    #
    # def remove_1(self, request, sku_product_id):
    #     self.add_or_remove_quantity(request, sku_product_id, -1)


class CartEntry(models.Model):
    quantity = models.PositiveIntegerField()

    # limit = models.Q(app_label='boxes', model='box')  # | models.Q(app_label='miapp', model='article')
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveIntegerField()
    product = GenericForeignKey('content_type', 'object_id')

    cart = models.ForeignKey(Cart, null=True, on_delete=models.CASCADE)
    total = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)

    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartEntryManager()

    def __str__(self):
        return "{}".format(self.id)


def pre_save_entry_receiver(sender, instance, *args, **kwargs):
    pass


pre_save.connect(pre_save_entry_receiver, sender=CartEntry)
