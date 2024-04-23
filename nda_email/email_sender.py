from django.core.mail import send_mail
from datetime import datetime

from django.template.loader import render_to_string

from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL
from nda_email.forms import ContactForm


class EmailSender:
    def __send_email(self, subject, message, recipient_list):
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            recipient_list=recipient_list
        )

    def send_submitted_order(self, request, offers):
        subject = f'Заказ с сайта {datetime.now().strftime("%Y-%m-%d %H:%M:%S.")}'
        recipient_list = [RECIPIENT_EMAIL]
        form = ContactForm(request.POST)
        if form.is_valid():
            customer_email = form.cleaned_data['email']
            customer_phone = form.cleaned_data['phone_number']
            customer_message = form.cleaned_data['message']
            message = render_to_string(
                'cart/message_for_nda.html',
                {'customer_message': customer_message, 'customer_email': customer_email,
                    'customer_phone': customer_phone, 'offers': offers}
            )
            self.__send_email(subject, message, recipient_list)

    def send_message_to_customer(self, request, offers):
        form = ContactForm(request.POST)
        subject = f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M:%S.")}'
        if form.is_valid():
            customer_email = form.cleaned_data['email']
            customer_phone = form.cleaned_data['phone_number']
            customer_message = form.cleaned_data['message']
            message = render_to_string(
                'cart/message_for_customer.html',
                {'customer_message': customer_message, 'customer_email': customer_email,
                 'customer_phone': customer_phone, 'offers': offers}
            )
            recipient_list = [customer_email]
            self.__send_email(subject, message, recipient_list)
