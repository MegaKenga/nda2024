from django.contrib import admin

from core.models import MainPageInfoBlock, WidgetAlert, WidgetAdvertisement
from catalog.admin_filters import RelatedOnlyDropdownFilter


class MainPageInfoBlockAdmin(admin.ModelAdmin):
    list_display = (
        'block_name',
        'block_category',
        'block_text',
        'block_image',
        'status'
    )
    list_editable = ('block_text', )
    list_filter = ('block_name', ('block_category', RelatedOnlyDropdownFilter), 'status')
    fields = [
        'block_name',
        'block_header',
        'block_category',
        'block_text',
        'block_image',
        'status'
    ]
    autocomplete_fields = ['block_category']
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['block_name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('block_category')


class WidgetAlertAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'header',
        'text',
        'status'
    )
    list_editable = ('header', 'text', 'status' )
    list_filter = ('name', 'status')
    fields = [
        'name',
        'header',
        'text',
        'status'
    ]
    view_on_site = True
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']


class WidgetAdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'header',
        'product',
        'text',
        'notes',
        'status'
    )
    list_editable = ('header', 'text', 'notes', 'status' )
    list_filter = ('name', 'status')
    fields = [
         'name',
        'header',
        'product',
        'text',
        'notes',
        'image',
        'status'
    ]
    view_on_site = True
    autocomplete_fields = ['product']
    actions_on_bottom = True
    list_per_page = 25
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product')

admin.site.register(MainPageInfoBlock, MainPageInfoBlockAdmin)
admin.site.register(WidgetAlert, WidgetAlertAdmin)
admin.site.register(WidgetAdvertisement, WidgetAdvertisementAdmin)
