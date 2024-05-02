from django.urls import path
from django.views.decorators.cache import cache_page

from catalog import views

urlpatterns = [
    path('brands/<slug:brand_slug>', cache_page(60)(views.BrandView.as_view()), name='brand'),
    path('categories/<slug:category_slug>', cache_page(60)(views.CategoryView.as_view()), name='category'),
    path('<slug:brand_slug>/<slug:category_slug>', cache_page(60)(views.OfferView.as_view()), name='offer'),
    path('search/', views.SiteSearchView.as_view(), name='search_page'),
]
