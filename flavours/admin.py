from django.contrib import admin

# Register your models here.
from .models import Flavour, PreBuildFlavour, Allergen


class FlavourModelAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "valentines_flavour"]

    class Order:
        model = Flavour


admin.site.register(Flavour, FlavourModelAdmin)
admin.site.register(PreBuildFlavour)
admin.site.register(Allergen)
