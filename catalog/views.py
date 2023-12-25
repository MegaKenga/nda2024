from django.shortcuts import render
from catalog.models import Category, Brand, Product, Offer


def index(request):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.filter(parent=None).filter(brand=None)
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    categories = Category.objects.filter(brand=brand_id).filter(parent=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    try:
        brand = Brand.objects.get(id=category.brand_id)
    except Brand.DoesNotExist:
        brand = None
    parent = category.parent
    if parent is None:
        parent = None
    children = Category.objects.filter(parent=category.id)
    products = Product.objects.filter(categories=category.id)
    context = {'category': category, 'parent': parent, 'brand': brand, 'children': children, 'products': products}
    return render(request, 'catalog/category.html', context=context)


def get_offer(request, brand_id, product_id):
    offers = Offer.objects.filter(product=product_id)
    product = Product.objects.get(id=product_id)
    brand = Brand.objects.get(pk=brand_id)
    context = {'offers': offers, 'product_id': product, 'brand_id': brand}
    return render(request, 'catalog/offer.html', context=context)
