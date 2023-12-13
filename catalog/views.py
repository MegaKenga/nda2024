from django.shortcuts import render
from catalog.models import Category, Brand, Product


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.visible.filter(parent=None).order_by('name')
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    products = Product.objects.filter(brand=brand)
    category_ids = set()
    for product in products:
        category_ids.add(product.category.id)
    categories = Category.objects.filter(pk__in = list(category_ids))
    context = {'categories': categories, 'brand': brand, 'products': products}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    parent = None
    if category.parent is not None:
        parent = Category.objects.get(pk=category.parent)
    children = Category.objects.filter(parent=category.pk)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'parent': parent, 'children': children, 'products': products}
    return render(request, 'catalog/category.html', context=context)
