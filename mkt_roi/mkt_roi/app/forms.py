from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django.forms import ModelForm
from app.models import MKTOffLine


# Create the form class.
class MediosOffLineForm(ModelForm):
    class Meta:
        model = MKTOffLine
        fields = '__all__'