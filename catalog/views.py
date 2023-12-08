from django.shortcuts import render
from catalog.models import Category, Brand


def index(request):
    brands = Brand.visible.all().order_by('name')
    categories = Category.visible.filter(parent=None).order_by('name')
    context = {'brands': brands, 'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_id):
    pass


def get_category(request, category_id):
    pass
