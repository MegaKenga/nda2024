from django.shortcuts import render, get_object_or_404, get_list_or_404
from catalog.models import Category, Brand, Offer


def index(request):
    brands = Brand.visible.all().order_by('name')
    # units = Unit.visible.filter(parent=None)
    context = {'brands': brands,
               # 'units': units
               }
    return render(request, 'index.html', context=context)


def category_m2m(request, category_slug):
    category = get_object_or_404(Category.visible, slug=category_slug)
    brand = get_object_or_404(Brand.visible, pk=category.brand_id)
    context = {'category': category, 'brand': brand}
    return render(request, 'catalog/category_m2m.html', context=context)


def get_brand(request, brand_slug):
    brand = get_object_or_404(Brand.visible, slug=brand_slug)
    categories = get_list_or_404(Category.visible, brand=brand.id, parent=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_slug):
    category = get_object_or_404(Category.visible, slug=category_slug)
    brand = get_object_or_404(Brand.visible, pk=category.brand_id)
    parent = category.parent
    if parent is None:
        parent = None
    children = Category.visible.filter(parent=category.id)
    context = {'category': category, 'parent': parent, 'brand': brand, 'children': children}
    return render(request, 'catalog/category.html', context=context)


def get_product_with_offers(request, brand_slug, category_slug):
    category = get_object_or_404(Category.visible, slug=category_slug)
    offers = Offer.visible.filter(category=category.id)
    context = {'offers': offers, 'category': category}
    return render(request, 'catalog/offer.html', context=context)
