from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<slug:brand_slug>', views.get_brand, name='brand'),
    path('units/<slug:unit_slug>', views.get_unit, name='unit'),
    path('categories/<slug:category_slug>', views.get_category, name='category'),
    path('<slug:brand_slug>/<slug:category_slug>', views.get_product_with_offers, name='offer'),
]
