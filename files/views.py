
from django.http import HttpResponse


def serve_file(request, file_path):
    print('serving file', file_path)
    return HttpResponse('im serving')