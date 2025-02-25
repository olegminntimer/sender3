from django.forms import ModelForm, BooleanField

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
        fields = ("date_and_time_of_end_of_sending", "message", "recipients")


class NewsletterBlockForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ("status",)


class AttemptToSendForm(StyleFormMixin, ModelForm):
    class Meta:
        model = AttemptToSend
        fields = ("status",)
