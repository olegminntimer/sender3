from datetime import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from send.models import AttemptToSend


@staticmethod
def start_of_mailing(newsletter):
    newsletter.date_and_time_of_first_dispatch = timezone.now()
    newsletter.status = "Запущена"
    newsletter.save()

    subject = newsletter.message.subject
    message = newsletter.message.letter_body
    recipients = [recipient.email for recipient in newsletter.recipients.all()]
    for recipient in recipients:
        ats = AttemptToSend(
            date_and_time_of_attempt=timezone.now(),
            mail_server_response="",
            newsletter=newsletter,
        )
        try:
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                [recipient,]
            )
        except Exception as e:
            ats.status = "Не успешно"
            ats.mail_server_response = str(e),
        else:
            ats.status = "Успешно"
