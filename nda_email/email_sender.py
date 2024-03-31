from django.core.mail import send_mail
from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL


class EmailSender:
    def send_submit_cart(self, payload):
        send_mail(
            subject=payload['subject'],
            message=payload['msg'],
            from_email=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            recipient_list=[RECIPIENT_EMAIL]  # todo: send message to customer as well
        )
