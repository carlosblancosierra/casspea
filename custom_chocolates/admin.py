from django.contrib import admin
from .models import ChocolateDesignLayer, ChocolateDesign, UserChocolateDesign

# Register your models here.
admin.site.register(ChocolateDesignLayer)
admin.site.register(ChocolateDesign)
admin.site.register(UserChocolateDesign)
