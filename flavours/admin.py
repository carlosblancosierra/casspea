from django.contrib import admin

# Register your models here.
from .models import Flavour, PreBuildFlavour, Allergen

# Register your models here.
admin.site.register(Flavour)
admin.site.register(PreBuildFlavour)
admin.site.register(Allergen)