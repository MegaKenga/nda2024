from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<brand_id>', views.get_brand, name='brand'),
    path('categories/<category_id>', views.get_category, name='category'),
    path('categories/<category_id>/<product_id>', views.get_offer, name='offer'),
]
