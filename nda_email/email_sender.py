from django.core.mail import send_mail
from nda.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL


class EmailSender:
    def send_submit_cart(self, customer_email, subject, message):
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
            recipient_list=[RECIPIENT_EMAIL, customer_email]  # todo: send message to customer as well
        )
        