from django.utils import timezone

from config.settings import EMAIL_HOST_USER, CACHE_ENABLED
from django.core.mail import send_mail
from django.core.cache import cache
from send.models import AttemptToSend, Newsletter, Recipient, Message


@staticmethod
def get_recipients_from_cache():
    if CACHE_ENABLED:
        key = "recipients_list"
        recipients = cache.get(key)
        if recipients is None:
            recipients = Recipient.objects.all()
            cache.set(key, recipients)
        return recipients
    return Recipient.objects.all()

@staticmethod
def get_messages_from_cache():
    if CACHE_ENABLED:
        messages = Message.objects.all()
        key = "messages_list"
        messages = cache.get(key)
        if messages is None:
            messages = Message.objects.all()
            cache.set(key, messages)
        return messages
    return Message.objects.all()


@staticmethod
def start_of_mailing(newsletter):
    if isinstance(newsletter, Newsletter):
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
