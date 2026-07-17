from django.views.generic import TemplateView, ListView, DetailView
from django.urls import resolve


from catalog.models import Brand, Product
from files.models import ModelFile

import datetime


class BrandsWithCertificatesView(ListView):
    model = Brand
    template_name = 'core/certificates.html'
    context_object_name = 'brands'

    def get_queryset(self):
        queryset = super().get_queryset()
        brands_with_certs = set(Brand.visible.filter(product__modelfile__isnull=False))
        return queryset.filter(id__in=[b.id for b in brands_with_certs])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name
        current_year = datetime.datetime.now().year
        context['current_year'] = current_year
        return context


class BrandCertificatesDetailView(DetailView):
    model = Brand
    template_name = 'core/brand_certificates_detail.html'
    context_object_name = 'brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name

        brand = self.object
        products = Product.visible.filter(brand=brand)
        certificates = ModelFile.objects.filter(product__in=products)

        context['products'] = products
        context['certificates'] = certificates
        context['brands'] = Brand.visible.all().order_by('name')

        current_year = datetime.datetime.now().year
        context['current_year'] = current_year
        return context


class WorkView(TemplateView):
    template_name = 'core/work.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name

        context['brands'] = Brand.visible.all().order_by('name')

        current_year = datetime.datetime.now().year
        context['current_year'] = current_year
        return context


class PrivacyView(WorkView):
    template_name = 'core/privacy.html'


class ContactsView(WorkView):
    template_name = 'core/contacts.html'


class SiteMapView(WorkView):
    template_name = 'core/sitemap.html'

    def get_context_data(self, **kwargs):
        from core.sitemap_tree import build_sitemap_nodes

        context = super().get_context_data(**kwargs)
        context['sitemap_nodes'] = build_sitemap_nodes()
        return context
