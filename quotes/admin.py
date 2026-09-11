from django.contrib import admin

from .models import (
    PartRequest,
    Quote,
    Shop,
    Notification,
    NotificationRead,
)


# =========================================================
# PART REQUEST ADMIN
# =========================================================

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


# =========================================================
# QUOTE ADMIN
# =========================================================

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


# =========================================================
# SHOP ADMIN
# =========================================================

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


# =========================================================
# NOTIFICATION ADMIN
# =========================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'shop',
        'is_global',
        'notification_type',
        'created_at',
    )

    list_filter = (
        'is_global',
        'notification_type',
        'created_at',
    )

    search_fields = (
        'title',
        'message',
        'shop__shop_name',
    )


# =========================================================
# NOTIFICATION READ ADMIN
# =========================================================

@admin.register(NotificationRead)
class NotificationReadAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'notification',
        'shop',
    )