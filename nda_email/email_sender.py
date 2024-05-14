import os
from datetime import datetime
from pathlib import Path
# from time import sleep

# from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

from nda import settings
from nda.settings import RECIPIENT_EMAIL, TEMPORARY_UPLOAD_ROOT, TEMPORARY_UPLOAD_URL, EMAIL_HOST_USER

from nda_email.forms import ContactForm
# from nda_email.tasks import send_email_task
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage


TEMPORARY_STORAGE = FileSystemStorage(location=TEMPORARY_UPLOAD_ROOT, base_url=TEMPORARY_UPLOAD_URL)

TEMPLATES = {
    'nda':      'cart/message_for_nda.html',
    'customer': 'cart/message_for_customer.html'
}

SUBJECTS = {
    'nda':      f'Заказ с сайта от {datetime.now().strftime("%Y-%m-%d %H:%M.")}',
    'customer': f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
}


class EmailSender:
    @staticmethod
    def get_message_data(request):
        form = ContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')
        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        # storaged_file = None
        # if file:
        #     storaged_file = TEMPORARY_STORAGE.save(file.name, file)
        return customer_email, customer_phone, customer_message, file

    @classmethod
    def create_message(cls, to_recipient, request, offers):
        template = TEMPLATES.get(to_recipient) if to_recipient in TEMPLATES \
            else ValueError(f'No template for recipient {to_recipient}')
        subject = SUBJECTS.get(to_recipient)if to_recipient in SUBJECTS \
            else ValueError(f'No subject for recipient {to_recipient}')
        customer_email, customer_phone, customer_message, file = cls.get_message_data(request)
        html_message = render_to_string(
            template,
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        email_address = customer_email if to_recipient == 'customer' else RECIPIENT_EMAIL
        # if file:
        #     # storaged_file_url = TEMPORARY_STORAGE.url(storaged_file)
        #     send_email_with_file_task.delay(file, email_address, subject, html_message)
        #     # sleep(10)
        #     # TEMPORARY_STORAGE.delete(storaged_file)
        # else:
        # send_email_task.delay(file, email_address, subject, html_message)
        email = EmailMessage(subject, html_message, EMAIL_HOST_USER, [email_address])
        if file is not None:
            file_name = 'company_details'
            storaged_file = TEMPORARY_STORAGE.save(file_name, file)
            storaged_file_url = TEMPORARY_STORAGE.url(storaged_file)
            print(storaged_file, storaged_file_url)

            email.attach_file(os.path.join(settings.BASE_DIR) + storaged_file_url)
        email.send(fail_silently=False)

    @classmethod
    def send_submitted_order_and_customer_reply(cls, request, offers):
        cls.create_message('nda', request, offers)
        cls.create_message('customer', request, offers)

    # @classmethod
    # def send_message_to_customer(cls, request, offers):
    #     cls.create_message('customer', request, offers)
