from django.shortcuts import render
from catalog.models import Category, Brand, Product


"""Не до конца понимаю этот метод, надо разобрать будет."""
def find_root(categories, category_id):
    category = next((category for category in categories if category.id == category_id), None)
    parent = category
    while parent.parent is not None:
        parent = parent.parent
    return parent
"""/ Не до конца понимаю этот метод, надо разобрать будет."""


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.visible.filter(parent=None).order_by('name')
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_id):
    brand = Brand.objects.get(pk=brand_id)
    products = Product.objects.filter(brand=brand_id)
    all_categories = Category.objects.all()
    category_ids = set()
    for product in products:
        category_ids.add(product.category.id)
    product_categories = Category.objects.filter(pk__in=category_ids)
    root_categories = set()
    for category in product_categories:
        root_categories.add(find_root(all_categories, category.id))
    context = {'categories': root_categories, 'brand': brand, 'products': products}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    parent = None
    if category.parent is not None:
        parent = category.parent
    children = Category.objects.filter(parent=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'parent': parent, 'children': children, 'products': products}
    return render(request, 'catalog/category.html', context=context)


def get_category_by_brand(request, brand_id, category_id):
    category = Category.objects.get(pk=category_id)
    parent = None
    if category.parent is not None:
        parent = category.parent
    #children = Category.objects.filter(parent=category_id)
    products = Product.objects.filter(category=category)
    children_ids = set()
    for product in products:
        children_ids.add(product.category.id)
    children = Category.objects.filter(parent__in=children_ids)
    context = {'category': category, 'parent': parent, 'brand_id': brand_id, 'children': children, 'products': products}
    return render(request, 'catalog/category.html', context=context)
