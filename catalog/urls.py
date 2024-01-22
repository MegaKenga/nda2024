from django.urls import path
from . import views

urlpatterns = [
    path('brands/<slug:brand_slug>', views.get_brand, name='brand'),
    path('categories/<slug:category_slug>', views.get_category, name='category'),
    path('<slug:brand_slug>/<slug:category_slug>', views.get_product_with_offers, name='offer'),
]
