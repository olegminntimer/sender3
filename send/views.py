from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from config.settings import DEFAULT_FROM_EMAIL
from .forms import RecipientForm, MessageForm, NewsletterForm, NewsletterBlockForm, AttemptToSendNewsletterForm
from .models import Recipient, Newsletter, Message, AttemptToSend
from .servicies import get_recipients_from_cache, get_messages_from_cache


def main_view(request):
    if request.user.is_superuser:
        recipients = get_recipients_from_cache
        newsletters = Newsletter.objects.all()
        newsletters_launched = Newsletter.objects.filter(status='launched')
        context = {
            'recipients': recipients,
            'newsletters': newsletters,
            'newsletters_launched': newsletters_launched,
        }
        return render(request, 'send/main.html', context)
    if request.user:
        recipients = Recipient.objects.filter(owner=request.user.id)
        newsletters = Newsletter.objects.filter(owner=request.user.id)
        newsletters_launched = Newsletter.objects.filter(owner=request.user.id, status='launched')
        context = {
            'recipients': recipients,
            'newsletters': newsletters,
            'newsletters_launched': newsletters_launched,
        }
        return render(request, 'send/main.html', context)


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.can_view_recipient'):
            context["recipients"] = get_recipients_from_cache
            return context
        context["recipients"] = Recipient.objects.filter(owner=self.request.user)
        return context

class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return RecipientForm
        else:
            raise PermissionDenied


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("send:recipient_list")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.can_view_message'):
            context["messages"] = get_messages_from_cache
            return context
        context["messages"] = Message.objects.filter(owner=self.request.user)
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("send:message_list")


class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter
    context_object_name = 'newsletters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.can_view_newsletter'):
            context["newsletters"] = Newsletter.objects.all()
            return context
        context["newsletters"] = Newsletter.objects.filter(owner=self.request.user)
        return context


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")


class NewsletterBlockView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterBlockForm
    success_url = reverse_lazy("send:newsletter_list")


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy("send:newsletter_list")


class SendNewsletterView(LoginRequiredMixin, View):

    def post(self, request, pk):
        # Получаем объект рассылки
        newsletter = Newsletter.objects.get(pk=pk, owner=request.user)
        message = newsletter.message
        recipients = newsletter.recipients.all()
        mail_server_response = None

        # Отправляем сообщения каждому получателю
        for recipient in recipients:
            try:
                send_mail(
                    message.subject,
                    message.letter_body,
                    DEFAULT_FROM_EMAIL,
                    [recipient.email],
                )
                AttemptToSend.objects.create(
                    status="Успешно", mail_server_response=f"Успешно отправлено на {recipient.email}", newsletter=newsletter
                )
            except Exception as e:
                mail_server_response = f"Письмо не отправлено на {recipient.email}: {e}"
                AttemptToSend.objects.create(status="Не успешно", mail_server_response=mail_server_response, newsletter=newsletter)
        # Отправляем сообщение об успехе и перенаправляем
        if AttemptToSend.objects.filter(newsletter=newsletter).order_by("id").first().status == "Успешно":
            messages.success(request, f"Письмо успешно отправлено на {recipient.email}")
        else:
            messages.warning(request, mail_server_response)
        newsletter.status = "FINISHED"
        newsletter.save()
        return redirect("send:newsletter_list")


class AttemptToSendListView(LoginRequiredMixin, ListView):
    model = AttemptToSend
    context_object_name = 'attempttosends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempttosends'] = AttemptToSend.objects.select_related('newsletter')
        return context
# class AttemptToSendListView(ListView):
#     model = AttemptToSend
#     template_name = 'send/attempttosend_list.html'
#     context_object_name = 'attempttosends'
#
#     def get_queryset(self):
#         newsletter_id = self.kwargs.get('newsletter_pk')
#         print(newsletter_id)
#         if newsletter_id:
#             return get_attempttosend_from_newsletter(newsletter_id)
#         else:
#             return AttemptToSend.objects.none()
#
#     def get(self, request, *args, **kwargs):
#         form = AttemptToSendSearchForm()
#         return render(request, self.template_name, {'form': form, 'attempttosends': self.get_queryset()})
#
#
#     def post(self, request, *args, **kwargs):
#         form = AttemptToSendSearchForm(request.POST)
#         if form.is_valid():
#             newsletter_id = form.cleaned_data['newsletter']
#             return self.get_queryset(newsletter_id)
#         else:
#             return render(request, self.template_name, {'form': form})

class AttemptToSendCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    form_class = AttemptToSendNewsletterForm
    success_url = reverse_lazy("send:newsletter_list")

    def form_valid(self, form):
        # form.instance.owner = self.request.user
        start_of_mailing(self)
        # form.instance.newsletter = self.request.newsletters.get(str(self.kwargs.get("id")))
        # sys.stdout.write(str(self.request.user))
        return super().form_valid(form)

