from django import template

from core.models import MainPage


register = template.Library()


@register.inclusion_tag('core/components/advertisement_on_main.html')
def ad_query():
    ads = MainPage.visible.all()
    return {'ads': ads}
