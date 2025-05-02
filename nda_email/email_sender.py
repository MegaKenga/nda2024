from django.template.loader import render_to_string

from nda_email.temporary_storage import temporary_storage
from nda_email.forms import ContactForm, PhysicalContactForm, MailForm, CallForm
from nda_email.tasks import send_emails_task


class LegalEntityEmailSender:  # Класс для отправки писем от имени юридических лиц
    @staticmethod
    def get_message_data(request):
        form = ContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')
        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        company_name = form.cleaned_data['company_name']
        inn = form.cleaned_data['inn']
        name = form.cleaned_data['name']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        return customer_email, customer_phone, customer_message, file, company_name, inn, name

    @classmethod
    def send_messages(cls, request, offers):
        customer_email, customer_phone, customer_message, file, company_name, inn, name = cls.get_message_data(request)
        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'company_name': company_name,
            'inn': inn,
            'name': name,
        }
        if offers:  
            context['offers'] = offers

        html_message_for_nda = render_to_string(
            'cart/../templates/cart/message_for_nda.html',
            context
        )
        html_message_for_customer = render_to_string(
            'cart/../templates/cart/message_for_customer.html',
            context
        )
        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)
        send_emails_task.delay(html_message_for_nda, html_message_for_customer, customer_email, storaged_file)


class PhysicalPersonEmailSender:  # Класс для отправки писем от имени физических лиц
    @staticmethod
    def get_message_data(request):
        form = PhysicalContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')

        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        name = form.cleaned_data['name']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None

        return customer_email, customer_phone, customer_message, file, name

    @classmethod
    def send_messages(cls, request, offers=None):
        customer_email, customer_phone, customer_message, file, name = cls.get_message_data(request)

        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'name': name,
        }

        if offers:  # Проверяем, не пуст ли список offers
            context['offers'] = offers

        html_message_for_nda = render_to_string(
            'cart/../templates/cart/message_for_nda.html',
            context
        )
        html_message_for_customer = render_to_string(
            'cart/../templates/cart/message_for_customer.html',
            context
        )

        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)

        send_emails_task.delay(html_message_for_nda, html_message_for_customer, customer_email, storaged_file)

class MailFormEmailSender:  
    @staticmethod
    def get_message_data(request):
        form = MailForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')

        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        company_name = form.cleaned_data['company_name']
        inn = form.cleaned_data['inn']
        name = form.cleaned_data['name']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        return customer_email, customer_phone, customer_message, company_name, inn, name, file

    @classmethod
    def send_messages(cls, request, offers=None):
        customer_email, customer_phone, customer_message, company_name, inn, name, file = cls.get_message_data(request)

        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'company_name': company_name,
            'inn': inn,
            'name': name,
            'offers': offers, # Убедитесь, что offers всегда передается в контекст
        }

        html_message_for_nda = render_to_string('cart/../templates/cart/message_for_nda.html', context)
        html_message_for_customer = render_to_string('cart/../templates/cart/message_for_customer.html', context)

        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)

        send_emails_task.delay(html_message_for_nda, html_message_for_customer, customer_email, storaged_file)


class CallFormEmailSender:  # Renamed class
    @staticmethod
    def get_message_data(request):
        form = CallForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')

        name = form.cleaned_data['name']
        customer_phone = form.cleaned_data['phone_number']
        customer_message = form.cleaned_data['message']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        return name, customer_phone, customer_message, file

    @classmethod
    def send_messages(cls, request): # offers не передается
        name, customer_phone, customer_message, file = cls.get_message_data(request)

        context = {
            'name': name,
            'customer_phone': customer_phone,
            'customer_message': customer_message,
        }

        html_message_for_nda = render_to_string('cart/../templates/cart/message_for_nda.html', context)
        html_message_for_customer = render_to_string('cart/../templates/cart/message_for_customer.html', context)

        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)

        send_emails_task.delay(html_message_for_nda, html_message_for_customer, name, storaged_file)    




