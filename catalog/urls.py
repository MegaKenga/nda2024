from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/brands/<slug:brand_slug>', views.get_brand, name='brand'),
    path('catalog/units/<slug:unit_slug>', views.get_unit, name='unit'),
    path('catalog/categories/<slug:category_slug>', views.get_category, name='category'),
    path('catalog/<slug:brand_slug>/<slug:category_slug>', views.get_product_with_offers, name='offer'),
]
