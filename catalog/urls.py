from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('brands/<slug:brand_slug>/', views.get_brand, name='brand'),
    path('categories/<slug:category_slug>/', views.get_category, name='category'),
]
