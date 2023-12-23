from django.shortcuts import render
from catalog.models import Category, Brand, Product, Offer


def index(request):
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.filter(parent=None).order_by('name') & Category.objects.filter(brand=None)
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    categories = Category.objects.filter(brand=brand_id) & Category.objects.filter(parent=None)
    context = {'brand': brand, 'categories': categories}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    parent = category.parent
    if parent is None:
        parent = None
    children = Category.objects.filter(parent=category.id)
    products = Product.objects.filter(categories=category.id)
    context = {'category': category, 'parent': parent, 'children': children, 'products': products}
    return render(request, 'catalog/category.html', context=context)


def get_offer_by_category(request, category_id, product_id):
    items = Offer.objects.filter(product=product_id)
    category = Product.objects.filter(categories=category_id)
    context = {'items': items, 'category_id': category}
    return render(request, 'catalog/offer_by_category.html', context=context)


def get_category_by_brand(request, brand_id, category_id):
    brand = Brand.objects.get(pk=brand_id)
    category = Category.objects.get(pk=category_id)
    parent = category.parent
    if parent is None:
        parent = None
    children = Category.objects.filter(brand=brand_id) & Category.objects.filter(parent=category_id)
    products = Product.objects.filter(categories=category.id)
    context = {'brand': brand, 'category': category, 'parent': parent, 'children': children, 'products': products}
    return render(request, 'catalog/category_by_brand.html', context=context)


def get_offer_by_brand(request, brand_id, category_id, product_id):
    offers = Offer.objects.filter(product=product_id)
    brand = Brand.objects.get(pk=brand_id)
    product = Product.objects.get(categories=category_id)
    context = {'offers': offers, 'product_id': product, 'brand_id': brand}
    return render(request, 'catalog/offer_by_category.html', context=context)