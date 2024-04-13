from django.core.mail import send_mail
from datetime import datetime
from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL


class EmailSender:
    def send_submit_cart(self, message):
        send_mail(
            subject=f'Заказ с сайта {datetime.now().strftime("%Y-%m-%d %H:%M:%S.")}',
            message=message,
            from_email=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            recipient_list=[RECIPIENT_EMAIL]  # todo: send message to customer as well
        )
        