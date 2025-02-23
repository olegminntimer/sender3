import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Permission

from users.forms import UserRegisterForm, UserForm
from users.models import CustomUser

from config.settings import EMAIL_HOST_USER


class UserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        # Назначение разрешений
        add_recipient_permission = Permission.objects.get(codename='add_recipient')
        change_recipient_permission = Permission.objects.get(codename='change_recipient')
        delete_recipient_permission = Permission.objects.get(codename='delete_recipient')
        view_recipient_permission = Permission.objects.get(codename='view_recipient')

        add_newsletter_permission = Permission.objects.get(codename='add_newsletter')
        change_newsletter_permission = Permission.objects.get(codename='change_newsletter')
        delete_newsletter_permission = Permission.objects.get(codename='delete_newsletter')
        view_newsletter_permission = Permission.objects.get(codename='view_newsletter')

        add_message_permission = Permission.objects.get(codename='add_message')
        change_message_permission = Permission.objects.get(codename='change_message')
        delete_message_permission = Permission.objects.get(codename='delete_message')
        view_message_permission = Permission.objects.get(codename='view_message')

        user.user_permissions.add(add_recipient_permission, change_recipient_permission, delete_recipient_permission, \
                                  view_recipient_permission, add_newsletter_permission, change_newsletter_permission, \
                                  delete_newsletter_permission, view_newsletter_permission, add_message_permission, \
                                  change_message_permission, delete_message_permission, view_message_permission)

        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy("users:user_list")


class UserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        if not self.request.user.has_perm('users.view_customuser'):
            return CustomUser.objects.none()
        return CustomUser.objects.all()


class UserDetailView(DetailView):
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy("users:user_list")
