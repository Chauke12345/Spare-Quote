from django.urls import path
from . import views



urlpatterns = [

    # =====================================================
    # CUSTOMER
    # =====================================================

    path(
        '',
        views.request_part,
        name='request_part'
    ),

    path(
        'shop-request/<int:shop_id>/',
        views.request_part,
        name='shop_request_part'
    ),

    path(
        'success/<uuid:public_id>/',
        views.request_success,
        name='request_success'
    ),

    path(
        'request/<uuid:public_id>/',
        views.request_detail,
        name='request_detail'
    ),

    path(
        'request/<uuid:public_id>/reopen/',
        views.reopen_request,
        name='reopen_request'
    ),

    path(
        'request/<uuid:public_id>/quote/<int:quote_id>/accept/',
        views.accept_quote,
        name='accept_quote'
    ),

    path(
        'request/<uuid:public_id>/review/',
        views.submit_review,
        name='submit_review'
    ),

    path(
        'track/',
        views.track_request,
        name='track_request'
    ),

# =====================================================
# SHOP
# =====================================================

path(
    'shop/login/',
    views.shop_login,
    name='shop_login'
),

path(
    'shop/logout/',
    views.shop_logout,
    name='shop_logout'
),

path(
    'shop/dashboard/',
    views.shop_dashboard,
    name='shop_dashboard'
),

path(
    'shop/change-password/',
    views.shop_change_password,
    name='shop_change_password'
),

path(
    'shop/reviews/',
    views.shop_reviews,
    name='shop_reviews'
),

path(
    'shop/request/<int:request_id>/quote/',
    views.submit_quote,
    name='submit_quote'
),

path(
    'shop/request/<int:request_id>/complete/',
    views.mark_completed,
    name='mark_completed'
),

path(
    'shop/notification/<int:notification_id>/read/',
    views.mark_notification_read,
    name='mark_notification_read'
),

path(
    'shop/support/',
    views.shop_support,
    name='shop_support'
),

    # =====================================================
    # ADMIN
    # =====================================================

    path(
        'sparequote-admin/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'sparequote-admin/shop/<int:shop_id>/access/',
        views.update_shop_access,
        name='update_shop_access'
    ),

    path(
        'sparequote-admin/support/<int:ticket_id>/update/',
        views.update_support_ticket,
        name='update_support_ticket'
    ),


    # =====================================================
    # QR CODES
    # =====================================================

    path(
        'qr/marketplace/',
        views.marketplace_qr,
        name='marketplace_qr'
    ),

    path(
        'qr/shop/<int:shop_id>/',
        views.private_shop_qr,
        name='private_shop_qr'
    ),

    path(
    'request-done/',
    views.request_done,
    name='request_done'
),

]