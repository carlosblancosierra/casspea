from django.contrib import admin
from .models import Order


# Register your models here.

class OrderModelAdmin(admin.ModelAdmin):
    list_display = ["order_id", "user", "status", "total", "timestamp"]

    search_fields = ["order_id"]
    list_filter = ["user", "status", "timestamp"]

    readonly_fields = ['cart_entries']


    class Order:
        model = Order


admin.site.register(Order, OrderModelAdmin)
