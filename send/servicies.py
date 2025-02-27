from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from django.core.cache import cache
from send.models import Recipient, Message


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
