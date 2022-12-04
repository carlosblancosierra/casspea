from django.db import models

from addresses.models import Address
from carts.models import CartEntry
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
User = settings.AUTH_USER_MODEL

STATUS_CHOICES = (
    ('created', 'created'),
    ('cancelled', 'cancelled'),
    ('delivered', 'delivered'),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=120, blank=True, default="INICIADA", choices=STATUS_CHOICES)
    total = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    cart_entries = models.ManyToManyField(CartEntry, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.order_id:
            return self.order_id
        else:
            return self.id

    class Meta:
        ordering = ['-timestamp']

    def subtotal(self):
        subtotal = 0
        for entry in self.cart_entries.all():
            item_total = entry.sku_product.master.costo * entry.quantity
            subtotal += item_total
        return subtotal

    def total(self):
        return self.subtotal()

    def get_staff_url(self):
        return f"/orders/staff/{self.order_id}"

    def get_absolute_url(self):
        return f"/orders/{self.order_id}"


def post_save_order_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = "JM" + str(instance.id)
        instance.save()


post_save.connect(post_save_order_receiver, sender=Order)
