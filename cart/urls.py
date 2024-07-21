from django.urls import path

from cart import views


urlpatterns = [
    # path('', views.cart_detail, name='cart_detail'),
    path('add/<offer_id>/', views.cart_add, name='cart_add'),
    path('cart_modal', views.cart_modal, name='cart_modal'),
    path('cart_submit', views.cart_submit, name='cart_submit'),
    path('remove/<offer_id>/', views.cart_remove, name='cart_remove'),
    # path('success/', views.ContactSuccessView.as_view(), name="success"),
    # path('clear', views.cart_clear, name='clear')
]
