from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('category/<category_id>/', views.get_category_or_product),
]