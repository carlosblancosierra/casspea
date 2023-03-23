from django.contrib import admin
from .models import \
    LayerColor, \
    ChocolateDesignLayerType, \
    ChocolateDesignLayer, \
    ChocolateDesignBase, \
    UserChocolateDesign, \
    ChocolateDesign

# Register your models here.
admin.site.register(LayerColor)

admin.site.register(ChocolateDesignLayerType)


class ChocolateDesignLayerModelAdmin(admin.ModelAdmin):
    list_display = ["type", "color", "updated"]

    search_fields = ["type", "color"]
    list_filter = ["type", "color"]

    class Order:
        model = ChocolateDesignLayer


admin.site.register(ChocolateDesignLayer, ChocolateDesignLayerModelAdmin)

admin.site.register(ChocolateDesignBase)


class UserChocolateDesignModelAdmin(admin.ModelAdmin):
    list_display = ["design", "user", "timestamp", "featured"]

    search_fields = ["design", "user"]
    list_filter = ["design", "featured"]

    class Order:
        model = UserChocolateDesign


admin.site.register(UserChocolateDesign, UserChocolateDesignModelAdmin)


class ChocolateDesignModelAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'layer1_options',
        'layer2_options',
        'layer3_options',
        'base_options',
    )


admin.site.register(ChocolateDesign, ChocolateDesignModelAdmin)
