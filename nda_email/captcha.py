import json
import sys

import requests

from nda.settings import YACAPTCHA_SERVER


def get_client_ip(request):
    """получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def verify_yandex_captcha(token, client_ip):
    resp = requests.post(
       "https://smartcaptcha.cloud.yandex.ru/validate",
       data={
          "secret": YACAPTCHA_SERVER,
          "token": token,
          "ip": client_ip
       },
       timeout=1
    )
    server_output = resp.content.decode()
    if resp.status_code != 200:
       print(f"Allow access due to an error: code={resp.status_code}; message={server_output}", file=sys.stderr)
       return True
    return json.loads(server_output)["status"] == "ok"
