from datetime import datetime
from time import sleep

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

from nda.settings import RECIPIENT_EMAIL, TEMPORARY_UPLOAD_ROOT, TEMPORARY_UPLOAD_URL
from nda_email.forms import ContactForm
from nda_email.tasks import send_email_task, send_email_with_file_task


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
        storaged_file = None
        if file:
            storaged_file = TEMPORARY_STORAGE.save(file.name, file)
        return customer_email, customer_phone, customer_message, storaged_file

    @classmethod
    def create_message(cls, to_recipient, request, offers):
        template = TEMPLATES.get(to_recipient)
        subject = SUBJECTS.get(to_recipient)
        if template or subject is None:
            raise ValueError(f'No template for recipient {to_recipient}')
        customer_email, customer_phone, customer_message, storaged_file = cls.get_message_data(request)
        html_message = render_to_string(
            template,
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        email_address = customer_email if to_recipient == 'customer' else RECIPIENT_EMAIL
        if storaged_file:
            storaged_file_url = TEMPORARY_STORAGE.url(storaged_file)
            send_email_with_file_task.delay(storaged_file_url, email_address, subject, html_message)
            # sleep(10)
            # TEMPORARY_STORAGE.delete(storaged_file)
        else:
            send_email_task.delay(email_address, subject, html_message)

    @classmethod
    def send_submitted_order(cls, request, offers):
        cls.create_message('nda', request, offers)

    @classmethod
    def send_message_to_customer(cls, request, offers):
        cls.create_message('customer', request, offers)
