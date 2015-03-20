# -*- coding: latin-1 -*-
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()


class TripEditorForm(forms.Form):
    # id = forms.CharField(widget=forms.HiddenInput)
    publishedDescription = forms.CharField(label='Published Description', widget=forms.Textarea)

    startDate = forms.DateTimeField(label='Start Date', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    endDate = forms.DateTimeField(label='End Date', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
