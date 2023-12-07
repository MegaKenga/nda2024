from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Brand


def page_not_found(request, exception):
    page404 = render(request, 'catalog/page404.html')
    return HttpResponseNotFound(page404)


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.visible.filter(parent=None).order_by('name')
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    context = {'brand': brand, 'brand_name': brand.name, 'brand_description': brand.description}
    return render(request, 'catalog/brand.html', context=context)


def get_category(request, category_id):
    category = get_object_or_404(Category, parent=category_id)
    context = {'category': category, 'category_name': category.name, 'category_description': category.description}
    return render(request, 'catalog/category.html', context=context)
