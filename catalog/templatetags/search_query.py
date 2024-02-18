from django import template
from catalog.views import SEARCH_QUERY_PARAM

register = template.Library()


@register.simple_tag()
def search_query(request):
    search_query = request.GET.get(SEARCH_QUERY_PARAM, '')
    return search_query
