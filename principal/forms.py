# -*- coding: latin-1 -*-
from django import forms
from django.contrib.auth.hashers import check_password
from django_summernote.widgets import SummernoteWidget
from bootstrap3_datetime.widgets import DateTimePicker

from principal.models import Traveller


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


# author: Juane
class TravellerEditProfileForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    Genre = (
        ('MA', 'MALE'),
        ('FE', 'FEMALE')
    )
    first_name = forms.CharField(label='first name', widget=forms.TextInput)
    last_name = forms.CharField(label='last name', widget=forms.TextInput)
    genre = forms.ChoiceField(label='genre', choices=Genre, widget=forms.Select)
    # photo = forms.ImageField(label='photo')


# author: Juane
class TravellerEditPasswordForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    old_password = forms.CharField(label='Old password', max_length=30, widget=forms.PasswordInput)
    password = forms.CharField(label='New password', max_length=30, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='New password repeat', max_length=30, widget=forms.PasswordInput)

    def clean(self):
        traveller = Traveller.objects.get(id=self.cleaned_data.get('id'))
        old_password = self.cleaned_data.get('old_password')

        if not check_password(old_password, traveller.password):
            self.add_error('old_password', "Wrong password")

        if self.cleaned_data.get('password') != self.cleaned_data.get('password_repeat'):
            self.add_error('password_repeat', "Password do not match")
        return self.cleaned_data
