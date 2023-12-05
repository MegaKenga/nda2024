from django.shortcuts import render
from catalog.models import Category, ProductCategory, Product


def index(request):
    categories = Category.objects.filter(parent=None)
    context = {'categories': categories}
    return render(request, 'catalog/index.html', context=context)


def get_category_or_product(request, category_id):
    if ProductCategory.category == category_id:
        product_id = ProductCategory.objects.filter(category=category_id)
        product = Product.objects.filter(id=product_id)
        context = {'product': product}
        return render(request, 'catalog/product.html', context=context)
    else:
        category = Category.objects.filter(parent=category_id)
        context = {'category': category}
        return render(request, 'catalog/category.html', context=context)
