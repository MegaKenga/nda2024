from django.urls import path

from cart import views


urlpatterns = [
    path('add/<offer_id>/', views.cart_add, name='cart_add'),
    path('cart_modal', views.cart_modal, name='cart_modal'),
    path('cart_submit', views.cart_submit, name='cart_submit'),
    path('physical_cart_submit', views.physical_cart_submit, name='physical_cart_submit'),
    path('remove/<offer_id>/', views.cart_remove, name='cart_remove'),
    path('mail_submit', views.mail_submit, name='mail_submit'),
    path('call_submit', views.call_submit, name='call_submit'),
    path('success', views.success, name='success'),
]
