from django.core.mail import EmailMessage
from datetime import datetime

from django.template.loader import render_to_string

from nda.settings import EMAIL_HOST_USER, RECIPIENT_EMAIL
from nda_email.forms import ContactForm


TEMPLATES = {
    'nda':      'cart/message_for_nda.html',
    'customer': 'cart/message_for_customer.html'
}


class EmailSender:

    @staticmethod
    def get_message_data(request, recipient, subject, offers):
        template = TEMPLATES.get(recipient)
        if template is None:
            raise ValueError(f'No template for recipient {recipient}')

        form = ContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')

        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        letter = render_to_string(
            template,
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        email_address = customer_email if recipient == 'customer' else RECIPIENT_EMAIL
        message_to_send = EmailMessage(subject, letter, EMAIL_HOST_USER, [email_address])
        if request.FILES:
            company_details = request.FILES['company_details']
            message_to_send.attach(company_details.name, company_details.read(), company_details.content_type)
        return message_to_send

    @staticmethod
    def __send_email(message_to_send):
        message_to_send.send(fail_silently=False)

    @classmethod
    def send_submitted_order(cls, form, offers):
        subject = f'Заказ с сайта {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
        message_to_send = cls.get_message_data(form, 'nda', subject, offers)
        cls.__send_email(message_to_send)

    @classmethod
    def send_message_to_customer(cls, form, offers):
        subject = f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
        message_to_send = cls.get_message_data(form, 'customer', subject, offers)
        cls.__send_email(message_to_send)
