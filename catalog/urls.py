from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<brand_id>', views.get_brand, name='brand'),
    path('categories/<category_id>', views.get_category, name='category'),
    path('<brand_id>/<product_group_id>', views.get_product_with_offers, name='offer'),
]
