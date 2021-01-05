from django import forms
from .models import *
from django.forms.models import inlineformset_factory

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
