from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, BooleanField

from send.forms import StyleFormMixin
from users.models import CustomUser


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2",)


class UserForm(StyleFormMixin, ModelForm):
    class Meta:
        model = CustomUser
        fields = ("is_active",)
