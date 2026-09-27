from datetime import timedelta

from django import forms
from django.utils import timezone

from mailer.models import Recipient, Message, Mailer


# Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'
        widgets = {
            "email": forms.EmailInput(attrs={'class': 'form-control'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
            "comment": forms.Textarea(attrs={'class': 'form-control'}),
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
        fields = '__all__'


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
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        starting_time = cleaned_data.get('start_time')
        ending_time = cleaned_data.get('end_time')
        time_validator(starting_time, ending_time)

        return cleaned_data
