from django.contrib import admin
from .models import LotSize, Lot, LotPriceIds

# Register your models here.
admin.site.register(LotSize)
admin.site.register(Lot)
admin.site.register(LotPriceIds)
