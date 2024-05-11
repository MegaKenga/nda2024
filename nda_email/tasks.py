import base64
from time import sleep

from celery import shared_task

from django.core.mail import EmailMessage
from nda.settings import EMAIL_HOST_USER


@shared_task
def send_email_task(to_recipient, subject, html_message):
    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
    sleep(5)
    email.send(fail_silently=False)


@shared_task
def send_email_with_file_task(file_base64, file_name, to_recipient, subject, html_message):
    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
    decoded_file = base64.b64decode(file_base64)
    email.attach(file_name, decoded_file)
    sleep(5)
    email.send(fail_silently=False)


