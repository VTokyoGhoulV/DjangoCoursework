from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View

from mailer.forms import RecipientForm, MessageForm, MailerForm
from mailer.models import Recipient, Message, Mailer, MailerAttempt
from mailer.services import send_mailing


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


# Mailer
class MailerCreateView(LoginRequiredMixin, CreateView):
    model = Mailer
    form_class = MailerForm
    template_name = "mailer/create_mailer.html"
    context_object_name = "mailer"

    def get_success_url(self):
        return reverse("detail_mailer", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailerUpdateView(UpdateView):
    model = Mailer
    form_class = MailerForm
    template_name = "mailer/update_mailer.html"
    context_object_name = "mailer"

    def get_success_url(self):
        return reverse("detail_mailer", kwargs={"pk": self.object.pk})


class MailerDeleteView(DeleteView):
    model = Mailer
    template_name = "mailer/delete_mailer.html"
    context_object_name = "mailer"
    success_url = reverse_lazy("list_mailers")


class MailerListView(ListView):
    model = Mailer
    template_name = "mailer/list_mailer.html"
    context_object_name = "mailers"

    def get_queryset(self):
        obj = Mailer.objects.all()
        for i in obj:
            i.update_status()

        return obj


class MailerDetailView(DetailView):
    model = Mailer
    template_name = "mailer/detail_mailer.html"
    context_object_name = "mailer"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj


class MailerSendView(View):

    def post(self, request, pk):
        try:
            send_mailing(pk)
        except ValueError as error:
            messages.error(request, str(error))

        return redirect("detail_mailer", pk=pk)


@login_required
def statistic(request):
    attempts = MailerAttempt.objects.filter(mailing__owner=request.user)
    successful_attempts = attempts.filter(status="Успешно").count()
    unsuccessful_attempts = attempts.filter(status="Не успешно").count()
    return render(request, "mailer/statistic.html",
                  {"successful_attempts": successful_attempts, "unsuccessful_attempts": unsuccessful_attempts})
