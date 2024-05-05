from celery import shared_task


@shared_task()
def send_feedback_email_task(message_to_send):
    message_to_send.send(fail_silently=False)
