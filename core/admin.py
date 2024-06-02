from django.contrib import admin
from core.models import MainPage
from catalog.admin_filters import RelatedOnlyDropdownFilter


class MainPageAdmin(admin.ModelAdmin):
    list_display = (
        'advert_name',
        'advert_category',
        'advert_text',
        'advert_image',
        'status'
    )
    list_editable = ('advert_text', )
    list_filter = ('advert_name', ('advert_category', RelatedOnlyDropdownFilter), 'status')
    fields = [
        'advert_name',
        'advert_category',
        'advert_text',
        'advert_image',
        'status'
    ]
    autocomplete_fields = ['advert_category']
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['advert_name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('advert_category')


admin.site.register(MainPage, MainPageAdmin)
