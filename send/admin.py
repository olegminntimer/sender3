from django.contrib import admin

from send.models import Recipient, Message, Newsletter, AttemptToSend


# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "comment")
    list_filter = ("email",)
    search_fields = (
        "email",
        "name",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "letter_body")
    list_filter = ("subject",)
    search_fields = ("subject", "letter_body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = (
        "first_dispatch",
        "end_of_sending",
        "status",
        "message",
    )
    list_filter = ("status",)
    search_fields = ("status", "message")


@admin.register(AttemptToSend)
class AttemptToSendAdmin(admin.ModelAdmin):
    list_display = (
        "attempt",
        "status",
        "mail_server_response",
        "newsletter",
    )
    list_filter = ("status",)
    search_fields = ("status",)
