from django.contrib import admin
from django.urls import path, reverse

from core.models import MainPageInfoBlock
from core import media_optimizer_views
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


admin.site.register(MainPageInfoBlock, MainPageInfoBlockAdmin)

"""Админка оптимизатора медиа файлов"""

_original_get_urls = admin.site.get_urls
_original_get_app_list = admin.site.get_app_list


def _optimizer_admin_urls():
    wrap = admin.site.admin_view
    return [
        path(
            'media-optimizer/',
            wrap(media_optimizer_views.media_optimizer_admin_page),
            name='core_media_optimizer',
        ),
        path(
            'media-optimizer/start/',
            wrap(media_optimizer_views.media_optimizer_start),
            name='core_media_optimizer_start',
        ),
        path(
            'media-optimizer/stop/',
            wrap(media_optimizer_views.media_optimizer_stop),
            name='core_media_optimizer_stop',
        ),
        path(
            'media-optimizer/reset/',
            wrap(media_optimizer_views.media_optimizer_reset),
            name='core_media_optimizer_reset',
        ),
        path(
            'media-optimizer/status/',
            wrap(media_optimizer_views.media_optimizer_status),
            name='core_media_optimizer_status',
        ),
        path(
            'media-optimizer/report/',
            wrap(media_optimizer_views.media_optimizer_report),
            name='core_media_optimizer_report',
        ),
    ]


def custom_get_urls():
    return _optimizer_admin_urls() + _original_get_urls()


def custom_get_app_list(request, app_label=None):
    app_list = _original_get_app_list(request, app_label=app_label)
    if request.user.is_staff:
        app_list.append({
            'name': 'Инструменты',
            'app_label': 'tools',
            'app_url': reverse('admin:core_media_optimizer'),
            'has_module_perms': True,
            'models': [{
                'name': 'Оптимизация изображений',
                'object_name': 'MediaOptimizer',
                'admin_url': reverse('admin:core_media_optimizer'),
                'view_only': True,
            }],
        })
    return app_list


admin.site.get_urls = custom_get_urls
admin.site.get_app_list = custom_get_app_list
