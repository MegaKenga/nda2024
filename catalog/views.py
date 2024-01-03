from django.shortcuts import render
from catalog.models import Category, Brand, ProductGroup, Offer


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.objects.filter(parent=None).filter(brand=None)
    context = {'brands': brands, 'categories': categories}
    return render(request, 'index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    categories = Category.visible.filter(brand=brand_id).filter(parent=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


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
    products_groups = ProductGroup.visible.filter(categories=category.id)
    context = {'category': category, 'parent': parent, 'brand': brand, 'children': children, 'products_groups': products_groups}
    return render(request, 'catalog/category.html', context=context)


def get_product_with_offers(request, brand_id, product_group_id):
    offers = Offer.visible.filter(product_group=product_group_id)
    product_group = ProductGroup.visible.get(id=product_group_id)
    context = {'offers': offers, 'product_group': product_group}
    return render(request, 'catalog/offer.html', context=context)
