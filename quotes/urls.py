from django.urls import path
from . import views


urlpatterns = [
    # =====================================================
    # CUSTOMER
    # =====================================================

    # Request a spare part
    path(
        '',
        views.request_part,
        name='request_part'
    ),

    # Request success page
    path(
        'success/<uuid:public_id>/',
        views.request_success,
        name='request_success'
    ),

    # Private customer request page
    path(
        'request/<uuid:public_id>/',
        views.request_detail,
        name='request_detail'
    ),

    # Reopen expired request
    path(
        'request/<uuid:public_id>/reopen/',
        views.reopen_request,
        name='reopen_request'
    ),

    # Accept supplier quotation
    path(
        'request/<uuid:public_id>/quote/<int:quote_id>/accept/',
        views.accept_quote,
        name='accept_quote'
    ),

    # Submit customer review
    path(
        'request/<uuid:public_id>/review/',
        views.submit_review,
        name='submit_review'
    ),

    # Track customer request
    path(
        'track/',
        views.track_request,
        name='track_request'
    ),

    # =====================================================
    # SHOP
    # =====================================================

    # Shop registration
    path(
        'shop/register/',
        views.shop_register,
        name='shop_register'
    ),

    # Shop login
    path(
        'shop/login/',
        views.shop_login,
        name='shop_login'
    ),

    # Shop logout
    path(
        'shop/logout/',
        views.shop_logout,
        name='shop_logout'
    ),

    # Shop dashboard
    path(
        'shop/dashboard/',
        views.shop_dashboard,
        name='shop_dashboard'
    ),

    # Shop reviews
    path(
        'shop/reviews/',
        views.shop_reviews,
        name='shop_reviews'
    ),

    # Submit / update quotation
    path(
        'shop/request/<int:request_id>/quote/',
        views.submit_quote,
        name='submit_quote'
    ),

    # Mark accepted order as completed
    path(
        'shop/request/<int:request_id>/complete/',
        views.mark_completed,
        name='mark_completed'
    ),
]