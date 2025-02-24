from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .forms import RecipientForm, MessageForm, NewsletterForm, NewsletterBlockForm
from .models import Recipient, Newsletter, Message


def main_view(request):
    if request.user.is_superuser:
        recipients = Recipient.objects.all()
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
            context["recipients"] = Recipient.objects.all()
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
            context["messages"] = Message.objects.all()
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
