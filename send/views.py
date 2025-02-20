from sys import stdout

from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import RecipientForm, MessageForm, NewsletterForm
from .models import Recipient, Newsletter, Message


def main_view(request):
    if request.user:
        recipients = Recipient.objects.filter(owner=request.user.id)
        newsletters = Recipient.objects.filter(owner=request.user.id)
        context = {
            'recipients': recipients,
            'newsletters': newsletters,
        }
        return render(request, 'send/main.html', context)


class RecipientListView(ListView):
    model = Recipient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipients"] = Recipient.objects.filter(owner=self.request.user)
        return context

class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")


class RecipientDetailView(DetailView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")


class RecipientDeleteView(DeleteView):
    model = Recipient
    success_url = reverse_lazy("send:recipient_list")


class MessageListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(owner=self.request.user)
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")


class MessageDetailView(DetailView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("send:message_list")


class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        newsletters_owner = Newsletter.objects.filter(owner=self.request.user)
        context = super().get_context_data(**kwargs)
        context["newsletters"] = newsletters_owner
        return context


class NewsletterCreateView(CreateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")


class NewsletterDetailView(DetailView):
    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("send:newsletter_list")


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy("send:newsletter_list")
