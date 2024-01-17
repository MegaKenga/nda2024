from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('catalog/brands/<slug:brand_slug>', views.get_brand, name='brand'),
    # path('catalog/categories/<slug:category_slug>', views.get_category, name='category'),
    path('<slug:category_slug>', views.category_m2m, name='category_m2m'),
    # path('catalog/<slug:brand_slug>/<slug:category_slug>', views.get_product_with_offers, name='offer'),
]
