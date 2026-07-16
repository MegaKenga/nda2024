import secrets
from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden


def get_optimizer_token_from_request(request) -> str:
    token = request.GET.get('token') or request.POST.get('token') or ''
    if not token:
        token = request.headers.get('X-Media-Optimizer-Token', '')
    return token.strip()


def is_valid_optimizer_token(token: str) -> bool:
    expected = getattr(settings, 'MEDIA_OPTIMIZER_TOKEN', '') or ''
    if not expected or not token:
        return False
    return secrets.compare_digest(token, expected)


def has_media_optimizer_access(request) -> bool:
    if request.user.is_authenticated and request.user.is_staff:
        return True
    return is_valid_optimizer_token(get_optimizer_token_from_request(request))


def get_media_optimizer_actor(request) -> str:
    if request.user.is_authenticated and request.user.is_staff:
        return request.user.get_username()
    if has_media_optimizer_access(request):
        return 'token-access'
    return 'anonymous'


def append_optimizer_token(url: str, token: str) -> str:
    if not token:
        return url
    separator = '&' if '?' in url else '?'
    return f'{url}{separator}token={token}'


def media_optimizer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if has_media_optimizer_access(request):
            return view_func(request, *args, **kwargs)

        expected = getattr(settings, 'MEDIA_OPTIMIZER_TOKEN', '') or ''
        if not expected:
            message = (
                'Доступ запрещён. На сервере не задан MEDIA_OPTIMIZER_TOKEN '
                '(файл .env или env в корне проекта).'
            )
        else:
            message = (
                'Доступ запрещён. Укажите ключ в URL: '
                '/admin-tools/media-optimizer/?token=ВАШ_КЛЮЧ '
                'или войдите как staff-пользователь.'
            )

        return HttpResponseForbidden(message)

    return wrapper
