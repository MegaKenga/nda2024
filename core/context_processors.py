from datetime import datetime
from .models import WidgetAlert, WidgetAdvertisement


def current_year_processor(request):
    return {'current_year': datetime.now().year}


def alerts_processor(request):
    alert = WidgetAlert.visible.all()
    return {
        'alert_header': alert.header,
        'alert_text': alert.text
    }


def advertisement_processor(request):
    advert = WidgetAdvertisement.visible.all()
    return {
        'advert_header': advert.header,
        'advertisement_text': advert.text,
        'advert_category': advert.category,
        'advert_notes': advert.notes,
        'advert_image': advert.image
    }

