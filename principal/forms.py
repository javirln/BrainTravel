# -*- coding: latin-1 -*-
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField(label=u"First Name", max_length=50, widget=forms.TextInput(attrs={'name': 'first_name'}))
    last_name = forms.CharField(label=u"Last Name", max_length=50, widget=forms.TextInput(attrs={'name': 'last_name'}))
    genre = forms.ChoiceField(choices=[('MA', 'MALE'), ('FE', 'FEMALE')], widget=forms.Select(attrs={'name': 'genre'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'name': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password1'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password2'}), label="Repeat password")
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
    
        if password1 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
    
        return self.cleaned_data

class SearchForm(forms.Form):
    search = forms.CharField()