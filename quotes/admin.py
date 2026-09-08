from django.contrib import admin
from .models import PartRequest, Quote, Shop


@admin.register(PartRequest)
class PartRequestAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'vehicle_make',
        'vehicle_model',
        'vehicle_year',
        'part_name',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'vehicle_make',
        'created_at',
    )

    search_fields = (
        'customer_name',
        'phone_number',
        'vin_number',
        'vehicle_make',
        'vehicle_model',
        'part_name',
    )


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        'shop_name',
        'part_request',
        'price',
        'availability',
        'is_accepted',
        'created_at',
    )

    list_filter = (
        'availability',
        'is_accepted',
        'created_at',
    )

    search_fields = (
        'shop_name',
        'part_request__customer_name',
        'part_request__vehicle_make',
        'part_request__vehicle_model',
        'part_request__part_name',
    )


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'shop_name',
        'phone_number',
        'email',
        'location',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'location',
    )

    search_fields = (
        'shop_name',
        'phone_number',
        'email',
        'location',
    )