import json
import sys

import generics
from django.conf import settings
import requests
from django.http import JsonResponse


def get_client_ip(request):
    """получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def check_captcha(token,request):
    """проверка токена капчи"""
    guest_ip = str(get_client_ip(request))
    resp = requests.get(
        "https://captcha-api.yandex.ru/validate",
        {
            "secret": settings.YACAPCHA_SERVER,
            "token": token,
            "ip": guest_ip  # Нужно передать IP пользователя.
                               # Как правильно получить IP зависит от вашего фреймворка и прокси.
                               # Например, в Flask это может быть request.remote_addr
        },
        timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
        print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
        return True
    return json.loads(server_output)["status"] == "ok"


# class RequestWithCapchaCreateAPI(generics.CreateAPIView):
#     """общий класс для проверки каппчи"""
#     def create(self, request, *args, **kwargs):
#         captcha_token = request.POST['smart-token']
#         if check_captcha(captcha_token, request):
#             return super().create(request, *args, **kwargs)
#         else:
#             return JsonResponse({'status': 'false', 'message': 'ROBOT'}, status=423)
