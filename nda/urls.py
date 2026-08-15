"""
URL configuration for nda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap

from nda.sitemap import sitemaps
from nda import settings
from nda.views import custom_404, custom_500
import catalog.views, core.views


urlpatterns = [
    path('', catalog.views.IndexView.as_view(), name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls')),
    path('catalog/', include('catalog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('debug/', include('debug_toolbar.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('privacy/', core.views.PrivacyView.as_view(), name='privacy'),
    path('soglasie-obrabotka-dannyh/', core.views.AcceptPolicyView.as_view(), name='accept_policy'),
    path('contacts/', core.views.ContactsView.as_view(), name='contacts'),
    path('work/', core.views.WorkView.as_view(), name='work'),
    path('karta-saita/', core.views.SiteMapView.as_view(), name='site_map'),
    path('certificates/', core.views.BrandsWithCertificatesView.as_view(), name='brands_with_certificates'),
    path('brand/<int:pk>/certificates/', core.views.BrandCertificatesDetailView.as_view(),name='brand_certificates'),
    path('files/', include('files.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404
handler500 = custom_500
