from django.urls import path
from files import views


urlpatterns = [
    path('<file_path>', views.serve_file, name='serve_file' )
]
