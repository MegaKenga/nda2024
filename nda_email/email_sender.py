import base64
from datetime import datetime
from time import sleep

from django.template.loader import render_to_string

from nda.settings import RECIPIENT_EMAIL
from nda_email.forms import ContactForm
from nda_email.tasks import send_email_task, send_email_with_file_task


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
        file = form.cleaned_data['company_details']
        file_name, file_base64 = None, None
        if file:
            file_name = form.cleaned_data['company_details'].name
            file_base64 = base64.b64encode(file.read()).decode()
        return customer_email, customer_phone, customer_message, file_name, file_base64

    @classmethod
    def create_message(cls, to_recipient, request, offers):
        template = TEMPLATES.get(to_recipient)
        subject = SUBJECTS.get(to_recipient)
        if template is None:
            raise ValueError(f'No template for recipient {to_recipient}')
        customer_email, customer_phone, customer_message, file_name, file_base64 = cls.get_message_data(request)
        html_message = render_to_string(
            template,
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        email_address = customer_email if to_recipient == 'customer' else RECIPIENT_EMAIL
        if file_base64:
            send_email_with_file_task.delay(file_base64, file_name, email_address, subject, html_message)
        else:
            send_email_task.delay(email_address, subject, html_message)

    @classmethod
    def send_submitted_order(cls, request, offers):
        cls.create_message('nda', request, offers)

    @classmethod
    def send_message_to_customer(cls, request, offers):
        cls.create_message('customer', request, offers)
