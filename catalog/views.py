from django.shortcuts import render, get_object_or_404, get_list_or_404
from catalog.models import Category, Brand, Offer


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.visible.filter(parents=None).filter(brand=None)
    context = {'brands': brands, 'categories': categories}
    return render(request, 'index.html', context=context)


def get_category(request, category_slug):
    category = Category.visible.get(slug=category_slug)
    parents = category.parents.all()
    breadcrumbs = []
    while len(parents) > 0:
        brand_parents = [parent for parent in parents if parent.brand is not None]
        if len(brand_parents) > 1:
            raise ValueError('We don\'t expect multiple brand parents')
        if len(brand_parents) == 1:
            breadcrumbs.insert(0, brand_parents[0])
        parents = brand_parents[0].parents.all()
    context = {'category': category, 'breadcrumbs': breadcrumbs}
    return render(request, 'catalog/category.html', context=context)


def get_brand(request, brand_slug):
    brand = get_object_or_404(Brand.visible, slug=brand_slug)
    categories = get_list_or_404(Category.visible, brand=brand.id, parents=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


def get_product_with_offers(request, brand_slug, category_slug):
    category = get_object_or_404(Category.visible, slug=category_slug)
    offers = Offer.visible.filter(category=category.id)
    context = {'offers': offers, 'category': category}
    return render(request, 'catalog/offer.html', context=context)
