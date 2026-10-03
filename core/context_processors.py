from datetime import datetime
from .models import WidgetAlert, WidgetAdvertisement


def current_year_processor(request):
    return {'current_year': datetime.now().year}


def alerts_processor(request):
    return {
        'alert': WidgetAlert.visible.order_by('-id').first()
    }


def advertisement_processor(request):
    return {
        'advert': WidgetAdvertisement.visible.select_related('product', 'product__brand').order_by('-id').first()
    }
