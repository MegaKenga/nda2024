from django.urls import path
from . import views


urlpatterns = [
    path('instructions/<file_path>', views.serve_file, name='serve_file'),
]
