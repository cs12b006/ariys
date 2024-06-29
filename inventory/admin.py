from django.contrib import admin

from inventory.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock_quantity")
    search_fields = ("name", "description")
    list_filter = ("price",)

    fieldsets = (
        (None, {"fields": ("name", "description", "price", "stock_quantity")}),
        (
            "Advanced Options",
            {
                "classes": ("collapse",),
                "fields": ("created_at",),
            },
        ),
    )

    readonly_fields = ("created_at",)
