from django.core.mail import EmailMessage
from datetime import datetime

from django.template.loader import render_to_string

from nda.settings import EMAIL_HOST_USER, RECIPIENT_EMAIL
from nda_email.forms import ContactForm


template_for_nda = 'cart/message_for_nda.html'
template_for_customer = 'cart/message_for_customer.html'


class EmailSender:
    def get_message_data(self, request, template, subject, offers):
        form = ContactForm(request.POST, request.FILES)
        message_to_send = None
        if form.is_valid():
            customer_email = form.cleaned_data['email']
            customer_phone = form.cleaned_data['phone_number']
            customer_message = form.cleaned_data['message']
            letter = render_to_string(
                template,
                {'customer_message': customer_message, 'customer_email': customer_email,
                 'customer_phone': customer_phone, 'offers': offers}
            )
            if template == template_for_nda:
                message_to_send = EmailMessage(subject, letter, EMAIL_HOST_USER, [RECIPIENT_EMAIL])
            elif template == template_for_customer:
                message_to_send = EmailMessage(subject, letter, EMAIL_HOST_USER, [customer_email])
            if request.FILES:
                company_details = request.FILES['company_details']
                message_to_send.attach(company_details.name, company_details.read(), company_details.content_type)
            return message_to_send

    def __send_email(self, message_to_send):
        message_to_send.send(fail_silently=False)

    def send_submitted_order(self, request, offers):
        subject = f'Заказ с сайта {datetime.now().strftime("%Y-%m-%d %H:%M:%S.")}'
        template = template_for_nda
        message_to_send = self.get_message_data(request, template, subject, offers)
        self.__send_email(message_to_send)

    def send_message_to_customer(self, request, offers):
        subject = f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M:%S.")}'
        template = template_for_customer
        message_to_send = self.get_message_data(request, template, subject, offers)
        self.__send_email(message_to_send)
