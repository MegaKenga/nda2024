from .models import Brand

def brands_processor(request):
    brands = Brand.visible.all().order_by('name')
    return {
        'brands': brands
    }
