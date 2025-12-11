from datetime import datetime
from django.core.mail import EmailMessage

from nda.settings import EMAIL_HOST_USER, RECIPIENT_EMAIL
from nda_email.temporary_storage import temporary_storage
from nda_email.models import OrderNumber


ORDERS_COUNTER = OrderNumber.objects.filter(id=1).first()

def form_email_and_send(subject_for_nda, subject_for_customer, html_message_for_nda, html_message_for_customer, customer_email, file_name):
    email_for_nda = EmailMessage(
        subject_for_nda,
        html_message_for_nda,
        EMAIL_HOST_USER,
        [RECIPIENT_EMAIL]
    )
    email_for_nda.content_subtype = "html"

    subject_for_customer = subject_for_customer
    email_for_customer = EmailMessage(
        subject_for_customer,
        html_message_for_customer,
        EMAIL_HOST_USER,
        [customer_email]
    )
    email_for_customer.content_subtype = "html"  # Добавляем для корректной отправки HTML
    if file_name is not None:
        storaged_file_path = temporary_storage.path(file_name)
        email_for_nda.attach_file(storaged_file_path)
        email_for_customer.attach_file(storaged_file_path)
        temporary_storage.delete(file_name)
    email_for_nda.send(fail_silently=False)
    email_for_customer.send(fail_silently=False)


def send_order_emails_task(html_message_for_nda, html_message_for_customer, customer_email, file_name):
    number=int(ORDERS_COUNTER.value) or None
    subject_for_nda = f'Заказ с сайта № {number} от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    subject_for_customer = f'Ваш заказ с сайта nda.ru № {number} от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    form_email_and_send(subject_for_nda, subject_for_customer, html_message_for_nda, html_message_for_customer, customer_email, file_name)
    try:
        ORDERS_COUNTER.value += 1
        ORDERS_COUNTER.save()
    except Exception as e:
        print(e)


def send_request_for_email_task(html_message_for_nda, html_message_for_customer, customer_email, file_name):
    subject_for_nda = f'Запрос обратного письма с сайта от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    subject_for_customer = f'Ваш запрос обратного письма с сайта nda.ru от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    form_email_and_send(subject_for_nda, subject_for_customer, html_message_for_nda, html_message_for_customer,
                        customer_email, file_name)


def send_request_for_call_task(html_message_for_nda):
    subject_for_nda = f'Запрос обратного звонка с сайта от {datetime.now().strftime("%Y-%m-%d %H:%M.")}'
    email_for_nda = EmailMessage(
        subject_for_nda,
        html_message_for_nda,
        EMAIL_HOST_USER,
        [RECIPIENT_EMAIL]
    )
    email_for_nda.content_subtype = "html"

    email_for_nda.send(fail_silently=False)
