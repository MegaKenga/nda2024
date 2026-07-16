from django.urls import path

from core import media_optimizer_views

urlpatterns = [
    path('', media_optimizer_views.media_optimizer_page, name='media_optimizer'),
    path('start/', media_optimizer_views.media_optimizer_start, name='media_optimizer_start'),
    path('stop/', media_optimizer_views.media_optimizer_stop, name='media_optimizer_stop'),
    path('reset/', media_optimizer_views.media_optimizer_reset, name='media_optimizer_reset'),
    path('status/', media_optimizer_views.media_optimizer_status, name='media_optimizer_status'),
    path('report/', media_optimizer_views.media_optimizer_report, name='media_optimizer_report'),
]
