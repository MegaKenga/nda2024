from django.urls import path
from cart import views


urlpatterns = [
    path('', views.cart_detail_2, name='cart_detail'),
    path('add/<offer_id>/', views.cart_add_2, name='cart_add'),
    path('remove/<offer_id>/', views.cart_remove, name='cart_remove'),
]
