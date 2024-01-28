from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from catalog.models import Category, Brand, Offer


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.visible.all().order_by('name')
        context['categories'] = Category.visible.filter(parents=None).filter(brand=None)
        return context


class CategoryView(ListView):
    model = Category
    template_name = 'catalog/category.html'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.visible.prefetch_related('parents').select_related('brand').get(slug=self.kwargs['category_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BrandView(ListView):
    model = Category
    template_name = 'catalog/brand.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.visible.select_related('brand').filter(parents=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = get_object_or_404(Brand.visible, slug=self.kwargs['brand_slug'])
        return context


class OfferView(ListView):
    model = Offer
    template_name = 'catalog/offer.html'
    context_object_name = 'offers'

    def get_queryset(self):
        category = Category.visible.get(slug=self.kwargs['category_slug'])
        return Offer.visible.select_related('category').filter(category=category.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category.visible, slug=self.kwargs['category_slug'])
        return context
