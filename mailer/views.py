from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailer.forms import RecipientForm
from mailer.models import Recipient


# Create your views here.

# Recipient
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "create_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "update_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "delete_recipient.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("list_recipients")


class RecipientListView(ListView):
    model = Recipient
    template_name = "list_recipient.html"
    context_object_name = "recipients"


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "detail_recipient.html"
    context_object_name = "recipient"
