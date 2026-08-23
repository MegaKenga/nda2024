from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView
from django.urls import resolve
from django.db.models import Q, Prefetch, Count
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from files.views import import_from_excel
from files.models import ModelFile, ModelImage, InstructionsFile, CatalogFile
from core.models import MainPageInfoBlock
from catalog.models import Category, Brand, Offer, Product
from cart.forms import CartAddProductForm


SEARCH_QUERY_PARAM = 'q'


def breadcrumbs_path(category):
    parents = category.parents.prefetch_related('parents').select_related('brand').all()
    breadcrumbs = []
    while len(parents) > 0:
        parents_path = [parent for parent in parents if parent.brand is not None]
        if parents_path:
            breadcrumbs.insert(0, parents_path[0])
            parents = parents_path[0].parents.all()
        else:
            parents_path = [parent for parent in parents if parent.brand is None]
            breadcrumbs.insert(0, parents_path[0])
            parents = parents_path[0].parents.all()
    return breadcrumbs


class IndexView(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name
        context['brands'] = Brand.visible.all().order_by('name')
        context['categories'] = Category.visible.filter(brand=None)
        context['ads'] = MainPageInfoBlock.visible.all()
        return context


class CategoryView(TemplateView):
    model = Category
    template_name = 'catalog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name

        category = get_object_or_404(Category.visible.select_related('brand').order_by('place'),slug=self.kwargs['category_slug'])
        context['brand'] = category.brand
        context['category'] = category
        context['categories'] = Category.visible.filter(parents=category).select_related('brand').order_by('place')
        context['products'] = Product.visible.filter(parents=category).select_related('brand').order_by('place')
        context['breadcrumbs'] = breadcrumbs_path(category)
        return context


class BrandView(TemplateView):
    model = Category
    template_name = 'catalog/brand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_path = self.request.path_info
        match = resolve(current_path)
        current_url_name = match.url_name
        context['current_url_name'] = current_url_name

        brand = get_object_or_404(Brand.visible, slug=self.kwargs['brand_slug'])
        context['categories'] = Category.visible.filter(parents=None, brand=brand).select_related('brand').order_by('place')
        context['products'] = Product.visible.filter(brand=brand).exclude(parents__brand=brand).select_related('brand').order_by('place')
        context['brand'] = brand
        return context


class OfferView(TemplateView):
    template_name = 'catalog/offer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = get_object_or_404(Product.visible.select_related('brand', 'specialist'), slug=self.kwargs['product_slug'])
        brand=get_object_or_404(Brand.visible.filter(pk=product.brand.id), slug=self.kwargs['brand_slug'])
        uploaded_file = None
        if self.request.method == 'POST':
            uploaded_file = import_from_excel(self.request, product_id=product.id)
        context['product'] = product
        context['brand'] = brand
        context['offers'] = Offer.visible.filter(product=product).order_by('place')
        context['images'] = ModelImage.objects.filter(product=product)
        context['certificates'] = ModelFile.objects.filter(product=product)
        context['breadcrumbs'] = breadcrumbs_path(product)
        context['cart_product_form'] = CartAddProductForm()
        context['specialist'] = product.specialist
        context['youtube_link'] = product.youtube_link
        context['rutube_link'] = product.rutube_link
        context['keywords'] = product.keywords
        context['title'] = product.title
        context['instructions'] = InstructionsFile.objects.filter(product=product)
        context['catalogs'] = CatalogFile.objects.filter(product=product)
        context['uploaded_file'] = uploaded_file

        return context


class SiteSearchView(ListView):
    model = Product
    template_name = 'core/search.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get(SEARCH_QUERY_PARAM, '').strip()
        qs = super().get_queryset()
        if len(query) < 3:
            messages.error(self.request, message='Слишком короткий запрос. Попробуйте увеличить количество символов в запросе')
            return qs.none()

        related_offers = Prefetch(
            'offer',
            queryset=Offer.visible.filter(name__icontains=query) or Offer.visible.filter(text_description__icontains=query),
            to_attr='related_offers')
        qs = (
            qs.filter(Q(name__icontains=query) | Q(offer__name__icontains=query) | Q(offer__text_description__icontains=query))
            .prefetch_related(related_offers).distinct()
        )
        if len(qs) == 0:
            messages.error(self.request, message='По вашему запросу ничего не найдено. Попробуйте изменить запрос и попробовать снова')
            return qs.none()
        return qs.filter(status='PUBLISHED')


class DuplicatesView(LoginRequiredMixin, TemplateView):
    template_name = 'core/duplicates.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        get_duplicates = Offer.visible.values('name').annotate(Count('name')).order_by().filter(name__count__gt=1).values_list('name', flat=True)
        duplicates = Offer.visible.filter(name__in=get_duplicates).order_by('name')
        context['duplicates'] = duplicates
        return context
