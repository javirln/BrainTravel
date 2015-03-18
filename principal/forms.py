    # -*- coding: latin-1 -*-
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()