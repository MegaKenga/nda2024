from django.shortcuts import render


def custom_404(request, exception):
    return render(request, 'page404.html', status=404)
