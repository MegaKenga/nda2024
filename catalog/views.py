from django.shortcuts import render, get_object_or_404

from catalog.models import Brand


def index(request):
    brands = Brand.objects.all()
    context = {'brands': brands}
    return render(request, 'catalog/index.html', context=context)


def get_brand(request, brand_name):
    brand = get_object_or_404(Brand.objects.filter(name=brand_name))
    context = {'brand': brand, 'brand_name': brand.name}
    return render(request, 'catalog/brand.html', context=context)


def get_unit(request, unit_slug):
    unit = get_object_or_404(Unit.objects.filter(slug=unit_slug))
    context = {'unit': unit, 'unit_title': unit.title}
    return render(request, 'catalog/unit.html', context=context)