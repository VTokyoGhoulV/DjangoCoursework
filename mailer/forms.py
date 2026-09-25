from django import forms

from mailer.models import Recipient


# Recipient

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'
