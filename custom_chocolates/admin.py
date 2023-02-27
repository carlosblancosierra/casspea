from django.contrib import admin
from .models import ChocolateDesignLayer, ChocolateDesign, UserChocolateDesign, ChocolateDesignBase

# Register your models here.
admin.site.register(ChocolateDesignLayer)
admin.site.register(ChocolateDesignBase)

admin.site.register(UserChocolateDesign)


class ChocolateDesignModelAdmin(admin.ModelAdmin):
    filter_horizontal = (
                         'layer1_options',
                         'layer2_options',
                         'layer3_options',
                         'base_options',
                         )


admin.site.register(ChocolateDesign, ChocolateDesignModelAdmin)
