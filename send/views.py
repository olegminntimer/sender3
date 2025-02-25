from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .forms import RecipientForm, MessageForm, NewsletterForm, NewsletterBlockForm, AttemptToSendForm
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


class AttemptToSendListView(LoginRequiredMixin, ListView):
    model = AttemptToSend
    context_object_name = 'attempttosends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.can_view_newsletter'):
            context["attempttosends"] = AttemptToSend.objects.all()
            return context
        context["attempttosends"] = AttemptToSend.objects.filter(owner=self.request.user)
        return context


class AttemptToSendCreateView(LoginRequiredMixin, CreateView):
    model = AttemptToSend
    form_class = AttemptToSendForm
    success_url = reverse_lazy("send:newsletter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        start_of_mailing(form.instance.newsletter)
        # form.instance.newsletter = self.request.newsletters.get(str(self.kwargs.get("id")))
        return super().form_valid(form)

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