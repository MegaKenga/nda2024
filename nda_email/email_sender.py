from datetime import datetime

from django.template.loader import render_to_string

from nda.settings import RECIPIENT_EMAIL, TEMPORARY_UPLOAD_ROOT, TEMPORARY_UPLOAD_URL, EMAIL_HOST_USER

from nda_email.forms import ContactForm
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage


TEMPORARY_STORAGE = FileSystemStorage(location=TEMPORARY_UPLOAD_ROOT, base_url=TEMPORARY_UPLOAD_URL)


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
        return customer_email, customer_phone, customer_message, file

    @classmethod
    def create_message(cls, request, offers):
        customer_email, customer_phone, customer_message, file = cls.get_message_data(request)
        html_message_for_nda = render_to_string(
            'cart/message_for_nda.html',
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        html_message_for_customer = render_to_string(
            'cart/message_for_customer.html',
            {'customer_message': customer_message, 'customer_email': customer_email,
             'customer_phone': customer_phone, 'offers': offers}
        )
        email_for_nda = EmailMessage(f'Заказ с сайта от {datetime.now().strftime("%Y-%m-%d %H:%M.")}',
                                     html_message_for_nda, EMAIL_HOST_USER, [RECIPIENT_EMAIL])
        email_for_customer = EmailMessage(f'Ваш заказ от {datetime.now().strftime("%Y-%m-%d %H:%M.")}',
                                          html_message_for_customer, EMAIL_HOST_USER, [customer_email])
        if file is not None:
            storaged_file = TEMPORARY_STORAGE.save(file.name, file)
            storaged_file_path = TEMPORARY_STORAGE.path(storaged_file)
            email_for_nda.attach_file(storaged_file_path)
            email_for_customer.attach_file(storaged_file_path)
        email_for_nda.send(fail_silently=False)
        email_for_customer.send(fail_silently=False)

    @classmethod
    def send_submitted_order_and_customer_reply(cls, request, offers):
        cls.create_message(request, offers)
