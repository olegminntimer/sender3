from django.shortcuts import render
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import RecipientForm
from .models import Recipient, Newsletter



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