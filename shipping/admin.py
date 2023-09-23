from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ShippingType

admin.site.register(ShippingType)