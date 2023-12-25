from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<brand_id>', views.get_brand, name='brand'),
    path('categories/<category_id>', views.get_category, name='category'),
    # path('categories/<category_id>/<product_id>', views.get_offer_by_category, name='offer_by_category'),
    # path('brands/<brand_id>/<category_id>/', views.get_category_by_brand, name='category_by_brand'),
    path('/<brand_id>/<product_id>', views.get_offer, name='offer'),
]
