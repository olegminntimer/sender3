from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import RecipientForm, MessageForm
from .models import Recipient, Newsletter, Message


def main_view(request):
    recipients = Recipient.objects.all()
    newsletters = Newsletter.objects.all()
    context = {
        'recipients': recipients,
        'newsletters': newsletters,
    }
    return render(request, 'send/main.html', context)


class RecipientListView(ListView):
    model = Recipient

    def get_context_data(self, **kwargs):
        recipients = Recipient.objects.all()
        context = super().get_context_data(**kwargs)
        context["recipients"] = recipients
        return context


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy("send:recipient_list")


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
        messages = Message.objects.all()
        context = super().get_context_data(**kwargs)
        context["messages"] = messages
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("send:message_list")


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


