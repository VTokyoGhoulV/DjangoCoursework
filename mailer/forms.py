from django import forms

from mailer.models import Recipient, Message


# Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'


# Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
