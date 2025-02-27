from django.forms import ModelForm, BooleanField, ChoiceField

from send.models import Recipient, Message, Newsletter, AttemptToSend


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class RecipientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        exclude = ("owner",)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ("end_of_sending", "message", "recipients")


class NewsletterBlockForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ("status",)


class AttemptToSendForm(StyleFormMixin, ModelForm):
    class Meta:
        model = AttemptToSend
        fields = ("mail_server_response",)


class AttemptToSendNewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = AttemptToSend
        fields = ("mail_server_response",)

class AttemptToSendSearchForm(ModelForm):
    newsletter = ChoiceField()

    class Meta:
        model = AttemptToSend
        fields = ['newsletter']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['newsletter'].choices = [(newsletter.id, newsletter.date_and_time_of_first_dispatch) for newsletter in Newsletter.objects.all()]
