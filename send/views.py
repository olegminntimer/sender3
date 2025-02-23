from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .forms import RecipientForm, MessageForm, NewsletterForm, RecipientManagerForm
from .models import Recipient, Newsletter, Message


def main_view(request):
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


class RecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    context_object_name = 'recipients'
    permission_required = 'send.view_recipient'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.view_recipient'):
            context["recipients"] = Recipient.objects.all()
            return context
        context["recipients"] = Recipient.objects.filter(owner=self.request.user)
        return context

class RecipientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")
    permission_required = 'send.add_recipient'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")
    permission_required = 'send.change_recipient'

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return RecipientForm
        if user.has_perm('send.view_recipient'):
            return RecipientManagerForm
        else:
            raise PermissionDenied


class RecipientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")
    permission_required = 'send.view_recipient'


class RecipientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy("send:recipient_list")
    permission_required = 'send.delete_recipient'


class MessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Message
    context_object_name = 'messages'
    permission_required = 'send.view_message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(owner=self.request.user)
        return context


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")
    permission_required = 'send.add_message'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")
    permission_required = 'send.change_message'


class MessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")
    permission_required = 'send.view_message'


class MessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy("send:message_list")
    permission_required = 'send.delete_message'


class NewsletterListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Newsletter
    context_object_name = 'newsletters'
    permission_required = 'send.view_newsletter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('send.view_newsletter'):
            context["newsletters"] = Newsletter.objects.all()
            return context
        context["newsletters"] = Newsletter.objects.filter(owner=self.request.user)
        return context


class NewsletterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")
    permission_required = 'send.add_newsletter'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")
    permission_required = 'send.change_newsletter'


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")
    permission_required = 'send.view_newsletter'


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    model = Newsletter
    success_url = reverse_lazy("send:newsletter_list")
    permission_required = 'send.delete_newsletter'
