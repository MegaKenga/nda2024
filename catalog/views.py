from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView

from catalog.models import Category, Brand, Offer


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.visible.all().order_by('name')
        context['categories'] = Category.visible.filter(parents=None).filter(brand=None)
        return context


class CategoryView(TemplateView):
    model = Category
    template_name = 'catalog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.visible.prefetch_related('parents').select_related('brand').get(slug=self.kwargs['category_slug'])
        parents = category.parents.all()
        breadcrumbs = []
        while len(parents) > 0:
            brand_parents = [parent for parent in parents if parent.brand is not None]
            if len(brand_parents) > 1:
                raise ValueError('We don\'t expect multiple brand parents')
            if len(brand_parents) == 1:
                breadcrumbs.insert(0, brand_parents[0])
            parents = brand_parents[0].parents.all()
        context['brand'] = category.brand
        context['category'] = category
        context['breadcrumbs'] = breadcrumbs
        return context


class BrandView(TemplateView):
    model = Category
    template_name = 'catalog/brand.html'

    def get_queryset(self):
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brand = get_object_or_404(Brand.visible, slug=self.kwargs['brand_slug'])
        context['categories'] = Category.visible.filter(parents=None, brand=brand).select_related('brand')
        context['brand'] = brand
        return context


class OfferView(TemplateView):
    model = Offer
    template_name = 'catalog/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category.visible, slug=self.kwargs['category_slug'])
        context['category'] = category
        context['offers'] = Offer.visible.filter(category=category.id).select_related('category')
        return context
