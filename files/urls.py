from django.urls import path

from files import views

urlpatterns = [
    path('<int:product_id>/add/', views.import_from_excel, name='offers_add'),
    path('<int:product_id>/delete/', views.delete_offers, name='offers_delete'),
]
