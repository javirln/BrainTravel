# -*- coding: latin-1 -*-
from bootstrap3_datetime.widgets import DateTimePicker
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django_summernote.widgets import SummernoteWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from paypal.standard.forms import PayPalPaymentsForm
from django import forms

from principal.models import Traveller


def user_exist_validator(value):
    if User.objects.exists(username=value):
        raise ValidationError(_('Already exists a user with that email!'))


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField(validators=[user_exist_validator])


# author: Juane
class TripUpdateStateForm(forms.Form):
    State = (
        ('ap', 'APPROVED'),
        ('re', 'REJECTED'),
        ('pe', 'PENDING'),
        ('df', 'DRAFT')
    )
    id = forms.IntegerField(widget=forms.HiddenInput)
    state = forms.ChoiceField(label='state', choices=State, widget=forms.Select(attrs={'class': 'form-control'}))


# david
class TripEditForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))

    startDate = forms.DateField(label="Start date",
                                widget=DateTimePicker(attrs={'class': 'form-control'}, options={"format": "YYYY-MM-DD",
                                                                                                "pickTime": False}))

    endDate = forms.DateField(label="End date",
                              widget=DateTimePicker(attrs={'class': 'form-control'}, options={"format": "YYYY-MM-DD",
                                                                                              "pickTime": False}))

    publishedDescription = forms.CharField(label='Published Description',
                                           widget=SummernoteWidget(attrs={'class': 'form-control'}))

# david
class PlanForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))

    startDate = forms.DateField(label="Start date",
                                widget=DateTimePicker(attrs={'class': 'form-control'}, options={"format": "YYYY-MM-DD",
                                                                                                "pickTime": False}))
    days = forms.CharField(label='Days', widget=forms.NumberInput(attrs={'min':0, 'max':7, 'class': 'form-control'}))

# author: Juane
class TravellerEditProfileForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    Genre = (
        ('MA', 'MALE'),
        ('FE', 'FEMALE')
    )
    first_name = forms.CharField(label='first name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='last name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(label='genre', choices=Genre, widget=forms.Select(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='photo')


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


class FormPaypalOwn(PayPalPaymentsForm):
    def get_image(self):
        return "https://www.paypalobjects.com/webstatic/en_US/btn/btn_checkout_pp_142x27.png";
