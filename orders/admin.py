from django.contrib import admin
from .models import Order


# Register your models here.

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["order_id", "user", "shipping_address_name", "payment_status", "shipping_date", "discount", "total", "timestamp", "staff_email_sent"]

    search_fields = ["order_id"]
    list_filter = ["user", "status", "timestamp"]

    readonly_fields = ['cart_entries']

    def shipping_address_name(self, obj):
        return obj.shipping_address.full_name

    class Order:
        model = Order


admin.site.register(Order, OrderModelAdmin)
