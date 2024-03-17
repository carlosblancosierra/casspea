from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active', 'sold_out')
    list_filter = ('active', 'sold_out')
    search_fields = ('title', 'description')


admin.site.register(Product, ProductAdmin)
