from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<brand_id>', views.get_brand, name='brand'),
    path('units/<unit_id>', views.get_unit, name='unit'),
    path('categories/<category_id>', views.get_category, name='category'),
    path('<brand_id>/<category_id>', views.get_product_with_offers, name='offer'),
]
