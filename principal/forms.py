# -*- coding: latin-1 -*-
from django import forms
from django_summernote.widgets import SummernoteWidget
from bootstrap3_datetime.widgets import DateTimePicker


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
        ('pe', 'PENDING'),
        ('df', 'DRAFT')
    ))


# david
class TripEditForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))

    startDate = forms.DateField(label="Start date",
                                widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                               "pickTime": False}))

    endDate = forms.DateField(label="End date",
                              widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                             "pickTime": False}))

    publishedDescription = forms.CharField(label='Published Description', widget=SummernoteWidget())
