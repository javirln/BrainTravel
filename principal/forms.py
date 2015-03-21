# -*- coding: latin-1 -*-
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django_summernote.widgets import SummernoteWidget


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()


# author: Juane
class TripUpdateStateForm(forms.Form):
    id = forms.IntegerField()
    state = forms.ChoiceField(choices=(
        ('ap', 'APPROVED'),
        ('re', 'REJECTED'),
        ('pe', 'PENDING')
    ))


# david
class TripEditForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput())
    country = forms.CharField(label='Country', widget=forms.TextInput())
    startDate = forms.DateTimeField(label='Start Date', widget=forms.DateInput())
    endDate = forms.DateTimeField(label='End Date', widget=forms.DateInput)
    # prueba2 = forms.DateField(
    #     widget=DateTimePicker(options={"format": "YYYY-MM-DD",
    #                                    "pickTime": False}))
    publishedDescription = forms.CharField(label='Published Description', widget=SummernoteWidget())
