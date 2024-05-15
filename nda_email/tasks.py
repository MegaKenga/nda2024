from celery import shared_task

from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage

from nda.settings import EMAIL_HOST_USER, TEMPORARY_UPLOAD_ROOT, TEMPORARY_UPLOAD_URL


TEMPORARY_STORAGE = FileSystemStorage(location=TEMPORARY_UPLOAD_ROOT, base_url=TEMPORARY_UPLOAD_URL)

@shared_task
def send_email_task(file, to_recipient, subject, html_message):
    email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
    if file is not None:
        storaged_file = TEMPORARY_STORAGE.save(file.name, file)
        storaged_file_url = TEMPORARY_STORAGE.url(storaged_file)
        email.attach_file(storaged_file_url)
    email.send(fail_silently=False)


# @shared_task
# def send_email_with_file_task(file, to_recipient, subject, html_message):
#     email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [to_recipient])
#     storaged_file = TEMPORARY_STORAGE.save(file.name, file)
#     storaged_file_url = TEMPORARY_STORAGE.url(storaged_file)
#     email.attach_file(storaged_file_url)
#     email.send(fail_silently=False)

@shared_task
def send_emails_task(customer_email, customer_phone, customer_message, file_name):
