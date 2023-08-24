from django.db import models

from addresses.models import Address
from carts.models import CartEntry
from discounts.models import Discount
from django.conf import settings
from django.db.models.signals import post_save
import json
from decimal import *
# Create your models here.
User = settings.AUTH_USER_MODEL

CREATED = 'created'
CANCELED = 'cancelled'
PAID = 'paid'
DELIVERED = 'delivered'

STATUS_CHOICES = (
    (CREATED, CREATED),
    (CANCELED, CANCELED),
    (DELIVERED, DELIVERED),
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True, null=True)
    gift_message = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    shipping_address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=120, blank=True, default="created", choices=STATUS_CHOICES)
    payment_status = models.CharField(max_length=120, blank=True)
    shipping_date = models.DateField(verbose_name="Shipping Date", null=True)
    cart_entries = models.ManyToManyField(CartEntry, blank=True)
    stripe_data = models.TextField(blank=True, null=True)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    staff_email_sent = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.order_id:
            return self.order_id
        else:
            return self.id

    class Meta:
        ordering = ['-timestamp']

    # def subtotal(self):
    #     subtotal = 0
    #     for entry in self.cart_entries.all():
    #         item_total = entry.sku_product.master.costo * entry.quantity
    #         subtotal += item_total
    #     return subtotal
    #
    # def total(self):
    #     return self.subtotal()

    def get_staff_url(self):
        return f"/orders/staff/{self.order_id}"

    def get_absolute_url(self):
        return f"/orders/client/{self.order_id}"

    @property
    def subtotal(self):
        entries = self.cart_entries.all()
        subtotal = Decimal(0)
        for entry in entries:
            subtotal += Decimal(entry.total)
        return subtotal

    @property
    def shipping_free(self):
        subtotal = self.subtotal
        if subtotal >= 45:
            return True
        else:
            return False

    @property
    def shipping_cost(self):
        if self.shipping_free:
            return 0
        else:
            return 5.99

    @property
    def total(self):
        return round(float(self.subtotal) + float(self.shipping_cost), 2)

    @property
    def is_paid(self):
        if self.payment_status == 'paid':
            return self.payment_status
        else:
            return 'unpaid'

    @property
    def stripe_description(self):
        if self.stripe_data:
            stripe_data = json.loads(self.stripe_data)
            return stripe_data['payment_intent']

    def discount_total(self, request):
        entries = self.cart_entries(request)
        raw_total = Decimal(0)
        for entry in entries:
            raw_total_entry = Decimal(entry.raw_total)
            raw_total += raw_total_entry
        return float(raw_total) - float(self.subtotal(request))


def post_save_order_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = "CP" + str(instance.id)
        instance.save()


post_save.connect(post_save_order_receiver, sender=Order)
