from celery import shared_task

from django.core.mail import EmailMessage
from nda.settings import EMAIL_HOST_USER


@shared_task
def send_email_task(to_recipient, subject, html_message):
    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
    email.send(fail_silently=False)


@shared_task
def send_email_with_file_task(storaged_file_url, to_recipient, subject, html_message):
    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
    attachment = storaged_file_url
    email.attach(attachment)
    email.send(fail_silently=False)


