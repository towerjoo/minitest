from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=widgets.PasswordInput)

class SecretForm(forms.Form):
    answer = forms.CharField(max_length=100, required=True)
