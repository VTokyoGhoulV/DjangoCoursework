from datetime import timedelta

from django import forms
from django.utils import timezone

from mailer.models import Recipient, Message, Mailer


# Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = "__all__"
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "email": "Email",
            "name": "Имя",
            "comment": "Комментарий"
        }


# Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        widgets = {
            "topic": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "topic": "Тема",
            "message": "Сообщение"
        }


# Mailer

def time_validator(starting_time, ending_time):
    if starting_time and ending_time:
        if starting_time > ending_time:
            raise forms.ValidationError(
                "Дата начала рассылки не может быть позже конца рассылки."
            )

    if starting_time:
        if starting_time < timezone.now() - timedelta(minutes=1):
            raise forms.ValidationError(
                "Дата начала рассылки не может быть раньше текущей даты."
            )


class MailerForm(forms.ModelForm):
    class Meta:
        model = Mailer
        fields = "__all__"
        exclude = ["status"]
        widgets = {
            "start_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "class": "form-control"},
            ),
            "end_time": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local", "class": "form-control"},
            ),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipient": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "start_time": "Время начала рассылки",
            "end_time": "Время окончания рассылки",
            "message": "Сообщение",
            "recipient": "Получатель"
        }

    def clean(self):
        cleaned_data = super().clean()

        starting_time = cleaned_data.get("start_time")
        ending_time = cleaned_data.get("end_time")
        time_validator(starting_time, ending_time)

        return cleaned_data

