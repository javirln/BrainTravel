# -*- coding: latin-1 -*-
from django import forms
from django_summernote.widgets import SummernoteWidget


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()


class TripEditorForm(forms.Form):
    # id = forms.CharField(widget=forms.HiddenInput)
    publishedDescription = forms.CharField(label='Published Description', widget=SummernoteWidget())

    startDate = forms.DateTimeField(label='Start Date', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    endDate = forms.DateTimeField(label='End Date', widget=forms.TextInput(attrs={'readonly': 'readonly'}))


class TripCreateForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput())
    country = forms.CharField(label='Country', widget=forms.TextInput())
    startDate = forms.DateTimeField(label='Start Date', widget=forms.TextInput())
    endDate = forms.DateTimeField(label='End Date', widget=forms.TextInput())
    publishedDescription = forms.CharField(label='Published Description', widget=SummernoteWidget())