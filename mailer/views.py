from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, View

from mailer.forms import RecipientForm, MessageForm, MailerForm
from mailer.models import Recipient, Message, Mailer, MailerAttempt
from mailer.services import send_mailing


# Create your views here.

# Recipient
class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/create_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipient/update_recipient.html"
    context_object_name = "recipient"

    def get_success_url(self):
        return reverse("detail_recipient", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "recipient/delete_recipient.html"
    context_object_name = "recipient"
    success_url = reverse_lazy("list_recipients")

    def get_queryset(self):
        return Recipient.objects.filter(owner=self.request.user)


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipient/list_recipient.html"
    context_object_name = "recipients"

    def get_queryset(self):
        if self.request.user.has_perm("mailer.view_recipient"):
            return Recipient.objects.all()

        return Recipient.objects.filter(owner=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = "recipient/detail_recipient.html"
    context_object_name = "recipient"

    def get_queryset(self):
        if self.request.user.has_perm("mailer.view_recipient"):
            return Recipient.objects.all()

        return Recipient.objects.filter(owner=self.request.user)


# Message
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "message/create_message.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse("detail_message", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "message/update_message.html"
    context_object_name = "message"

    def get_success_url(self):
        return reverse("detail_message", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "message/delete_message.html"
    context_object_name = "message"
    success_url = reverse_lazy("list_messages")

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "message/list_message.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "message/detail_message.html"
    context_object_name = "message"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["recipient"].queryset = Recipient.objects.filter(owner=self.request.user)
        form.fields["message"].queryset = Message.objects.filter(owner=self.request.user)

        return form


class MailerUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailer
    form_class = MailerForm
    template_name = "mailer/update_mailer.html"
    context_object_name = "mailer"

    def get_success_url(self):
        return reverse("detail_mailer", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        return Mailer.objects.filter(owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["recipient"].queryset = Recipient.objects.filter(owner=self.request.user)
        form.fields["message"].queryset = Message.objects.filter(owner=self.request.user)

        return form


class MailerDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailer
    template_name = "mailer/delete_mailer.html"
    context_object_name = "mailer"
    success_url = reverse_lazy("list_mailers")

    def get_queryset(self):
        return Mailer.objects.filter(owner=self.request.user)


class MailerListView(LoginRequiredMixin, ListView):
    model = Mailer
    template_name = "mailer/list_mailer.html"
    context_object_name = "mailers"

    def get_queryset(self):
        if self.request.user.has_perm("mailer.view_mailer"):
            obj = Mailer.objects.all()
        else:
            obj = Mailer.objects.filter(owner=self.request.user)

        for i in obj:
            i.update_status()

        return obj


class MailerDetailView(LoginRequiredMixin, DetailView):
    model = Mailer
    template_name = "mailer/detail_mailer.html"
    context_object_name = "mailer"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.update_status()
        return obj

    def get_queryset(self):
        if self.request.user.has_perm("mailer.view_mailer"):
            return Mailer.objects.all()

        return Mailer.objects.filter(owner=self.request.user)


class MailerSendView(LoginRequiredMixin, View):

    def post(self, request, pk):
        mailer = get_object_or_404(Mailer, pk=pk, owner=self.request.user)
        try:
            send_mailing(mailer.pk)
        except ValueError as error:
            messages.error(request, str(error))

        return redirect("detail_mailer", pk=pk)


class MailerDisableView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "mailer.disable_mailer"

    def post(self, request, pk):
        mailer = get_object_or_404(Mailer, pk=pk)
        mailer.is_enabled = False
        mailer.save(update_fields=["is_enabled"])
        mailer.update_status()

        return redirect("detail_mailer", pk=pk)


@login_required
def statistic(request):
    attempts = MailerAttempt.objects.filter(mailing__owner=request.user)
    successful_attempts = attempts.filter(status="Успешно").count()
    unsuccessful_attempts = attempts.filter(status="Не успешно").count()
    return render(request, "mailer/statistic.html",
                  {"successful_attempts": successful_attempts, "unsuccessful_attempts": unsuccessful_attempts})
