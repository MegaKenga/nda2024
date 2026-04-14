from django.template.loader import render_to_string

from catalog.models import Product
from nda_email.temporary_storage import temporary_storage
from nda_email.forms import ContactForm, PhysicalContactForm, MailForm, CallForm
from nda_email.tasks import send_order_emails_task, send_request_for_email_task, send_request_for_call_task


def check_if_form_is_valid_and_get_data(request, form):
    if not form.is_valid():
        raise ValueError('Cannot send email, form is invalid')
    customer_email = form.cleaned_data['email']
    customer_phone = form.cleaned_data['phone_number']
    customer_message = form.cleaned_data['message']
    company_name = form.cleaned_data['company_name'] if 'company_name' in request.POST else None
    inn = form.cleaned_data['inn'] if 'inn' in request.POST else None
    name = form.cleaned_data['name']
    file = request.FILES['company_details'] if 'company_details' in request.FILES else None
    if file:
        print ("FILE!!!!")
    else:
        print("NO FILE")
    return customer_email, customer_phone, company_name, inn, name, file, customer_message


def check_if_offers_and_generate_messages(offers, file, context, customer_email):
    if offers:
        context['offers'] = offers
        product_id = offers[0].product_id # product нужен для сохранения ссылки на страницу товара в письме
        product = Product.objects.get(id=product_id)
        context['product'] = product
    html_order_message_for_nda = render_to_string(
        'nda_email/order_message_for_nda.html',
        context
    )
    html_order_message_for_customer = render_to_string(
        'nda_email/order_message_for_customer.html',
        context
    )
    storaged_file = None
    if file is not None:
        storaged_file = temporary_storage.save(file.name, file)
    send_order_emails_task.delay(html_order_message_for_nda, html_order_message_for_customer, customer_email, storaged_file)


class CompanyOrderEmailSender:  # Класс для отправки писем от имени юридических лиц
    @staticmethod
    def get_message_data(request):
        form = ContactForm(request.POST, request.FILES)
        data = check_if_form_is_valid_and_get_data(request, form)
        return data

    @classmethod
    def send_messages(cls, request, offers):
        customer_email, customer_phone, company_name, inn, name, file, customer_message = cls.get_message_data(request)
        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'company_name': company_name,
            'inn': inn,
            'name': name,
        }
        check_if_offers_and_generate_messages(offers, file, context, customer_email)


class PhysicalPersonOrderSender:  # Класс для отправки писем от имени физических лиц
    @staticmethod
    def get_message_data(request):
        form = PhysicalContactForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')
        data = check_if_form_is_valid_and_get_data(request, form)
        return data

    @classmethod
    def send_messages(cls, request, offers):
        customer_email, customer_phone, customer_message, file, name, inn, company_name = cls.get_message_data(request)
        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'name': name,
        }
        check_if_offers_and_generate_messages(offers, file, context, customer_email)

class MailRequestFormEmailSender:
    @staticmethod
    def get_message_data(request):
        form = MailForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('Cannot send email, form is invalid')
        customer_email = form.cleaned_data['email']
        customer_phone = form.cleaned_data['phone_number']
        company_name = form.cleaned_data['company_name']
        inn = form.cleaned_data['inn']
        name = form.cleaned_data['name']
        file = request.FILES['company_details'] if 'company_details' in request.FILES else None
        customer_message = form.cleaned_data['message']
        return customer_email, customer_phone, company_name, inn, name, file, customer_message

    @classmethod
    def send_messages(cls, request, offers=None):
        customer_email, customer_phone, company_name, inn, name, file, customer_message = cls.get_message_data(request)

        context = {
            'customer_message': customer_message,
            'customer_email': customer_email,
            'customer_phone': customer_phone,
            'company_name': company_name,
            'inn': inn,
            'name': name,
        }

        html_message_for_nda = render_to_string('nda_email/request_mail_message_for_nda.html', context)
        html_message_for_customer = render_to_string('nda_email/request_mail_message_for_customer.html', context)

        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)

        send_request_for_email_task.delay(html_message_for_nda, html_message_for_customer, customer_email, storaged_file)


class CallRequestFormEmailSender:  # Renamed class
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
    def send_messages(cls, request, offers=None): # offers не передается
        name, customer_phone, customer_message, file = cls.get_message_data(request)

        context = {
            'name': name,
            'customer_phone': customer_phone,
            'customer_message': customer_message,
        }
        storaged_file = None
        if file is not None:
            storaged_file = temporary_storage.save(file.name, file)
        html_message_for_nda = render_to_string('nda_email/request_call_message_for_nda.html', context)
        send_request_for_call_task.delay(html_message_for_nda, storaged_file)
