from django.forms import ModelForm, BooleanField

from send.models import Recipient, Message, Newsletter


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


class RecipientManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Recipient
        exclude = '__all__'


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ("owner",)


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        exclude = ("owner",)
