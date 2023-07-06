from django.contrib import admin
from .models import Discount

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'stripe_id', 'amount', 'type', 'max_uses')
    list_filter = ('type',)
    search_fields = ('title', 'code',)
