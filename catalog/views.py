from django.shortcuts import render
from catalog.models import Category, Brand, Unit, Offer


def index(request):
    brands = Brand.visible.all().order_by('name')
    units = Unit.objects.filter(parent=None)
    context = {'brands': brands, 'units': units}
    return render(request, 'index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    categories = Category.visible.filter(brand=brand_id).filter(parent=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


def get_unit(request, unit_id):
    unit = Unit.objects.get(pk=unit_id)
    sub_units = Unit.visible.filter(parent=unit_id)
    categories = Category.visible.filter(unit=unit_id)
    context = {'unit': unit, 'sub_units': sub_units, 'categories': categories}
    return render(request, 'catalog/unit.html', context=context)


def get_category(request, category_id):
    category = Category.visible.get(pk=category_id)
    try:
        brand = Brand.visible.get(id=category.brand_id)
    except Brand.DoesNotExist:
        brand = None
    parent = category.parent
    if parent is None:
        parent = None
    children = Category.visible.filter(parent=category.id)
    context = {'category': category, 'parent': parent, 'brand': brand, 'children': children}
    return render(request, 'catalog/category.html', context=context)


def get_product_with_offers(request, brand_id, category_id):
    offers = Offer.visible.filter(category=category_id)
    category = Category.visible.get(id=category_id)
    context = {'offers': offers, 'category': category}
    return render(request, 'catalog/offer.html', context=context)
