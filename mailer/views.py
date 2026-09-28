from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailer.forms import RecipientForm, MessageForm
from mailer.models import Recipient, Message


# Create your views here.

# Recipient
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/create_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/update_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipient/delete_recipient.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("list_recipients")


class RecipientListView(ListView):
    model = Recipient
    template_name = "recipient/list_recipient.html"
    context_object_name = "recipients"


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = "recipient/detail_recipient.html"
    context_object_name = "recipient"


# Message
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message/create_message.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse("detail_message", kwargs={"pk": self.object.pk})


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "message/update_message.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse("detail_message", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "message/delete_message.html"
    context_object_name = "message"
    success_url = reverse_lazy("list_messages")


class MessageListView(ListView):
    model = Message
    template_name = "message/list_message.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "message/detail_message.html"
    context_object_name = "message"
