from datetime import datetime
from .models import WidgetAlert, WidgetAdvertisement


def current_year_processor(request):
    return {'current_year': datetime.now().year}


def alerts_processor(request):
    alert = WidgetAlert.visible.all()
    return {
        'alert': alert
    }


def advertisement_processor(request):
    advert = WidgetAdvertisement.visible.all()
    return {
        'advert': advert
    }

