from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Recipient


class RecipientListView(ListView):
    model = Recipient

    def get_context_data(self, **kwargs):
        recipients = Recipient.objects.all()
        context = super().get_context_data(**kwargs)
        context['recipients'] = recipients
        return context

class RecipientCreateView(CreateView):
    model = Recipient
    fields = ['email', 'name', 'comment']
    template_name = 'recipient_form.html'
    success_url = reverse_lazy('recipient_list')
