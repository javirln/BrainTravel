# -*- coding: latin-1 -*-
from datetime import datetime
from bootstrap3_datetime.widgets import DateTimePicker
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from paypal.standard.forms import PayPalPaymentsForm
from django import forms
from validators import password_validator
from django.db.models.fields import BLANK_CHOICE_DASH

from principal.models import Traveller


def user_exist_validator(value):
    if User.objects.exists(username=value):
        raise ValidationError(_('Already exists a user with that email!'))


class LoginForm(forms.Form):
    username = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    email = forms.EmailField()
    
    def clean_email(self):
        cleaned_email = self.cleaned_data['email']
        if User.objects.filter(username=cleaned_email).exists():
            raise ValidationError(_('Already exists a user with that email!'))
        return cleaned_email


# author: Juane
class TripUpdateStateForm(forms.Form):
    State = (
        ('ap', 'APPROVED'),
        ('re', 'REJECTED'),
        ('pe', 'PENDING')
    )
    id = forms.IntegerField(widget=forms.HiddenInput)
    state = forms.ChoiceField(label='state', choices=State, widget=forms.Select(attrs={'class': 'form-control'}))


# david
class TripEditForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))

    startDate = forms.DateField(label="Start date",
                                widget=DateTimePicker(attrs={'required': True, 'class': 'form-control'},
                                                      options={"format": "YYYY-MM-DD",
                                                               "pickTime": False}))

    endDate = forms.DateField(label="End date",
                              widget=DateTimePicker(attrs={'required': True, 'class': 'form-control'},
                                                    options={"format": "YYYY-MM-DD",
                                                             "pickTime": False}))

    publishedDescription = forms.CharField(label='Published Description',
                                           widget=SummernoteWidget(attrs={'class': 'form-control'}))

    def clean(self):
        start_date = self.cleaned_data['startDate']
        end_date = self.cleaned_data['endDate']
        if start_date > datetime.now().date():
            self.add_error('startDate', "Must be a date in the past")
        if start_date > end_date:
            self.add_error('startDate', "Incorrect date")
            self.add_error('endDate', "Incorrect date")
        if end_date > datetime.now().date():
            self.add_error('endDate', "Must be a date in the past")

        return self.cleaned_data


# david
class PlanForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))

    startDate = forms.DateField(label="Start date",
                                widget=DateTimePicker(attrs={'class': 'form-control', 'required': True},
                                                      options={"format": "YYYY-MM-DD",
                                                               "pickTime": False}))
    days = forms.CharField(label='Days', widget=forms.NumberInput(attrs={'min': 0, 'max': 7, 'class': 'form-control'}))

    def clean(self):
        start_date = self.cleaned_data['startDate']

        if start_date < datetime.now().date():
            self.add_error('startDate', "Must be a date in the future")
        return self.cleaned_data


# author: Juane
class TravellerEditProfileForm(forms.Form):
    Genre = (
        ('MA', 'MALE'),
        ('FE', 'FEMALE')
    )
    id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput,
    )
    first_name = forms.CharField(
        label='first name',
        required=True,
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '254',
            }
        )
    )
    last_name = forms.CharField(
        label='last name',
        required=False,
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'maxlength': '254',
            }
        )
    )
    genre = forms.ChoiceField(
        label='genre',
        choices=BLANK_CHOICE_DASH + list(Genre),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    photo = forms.ImageField(
        label='photo',
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': 'image/png, image/jpeg, image/jpg',
            }
        ),
    )
    photo_clear = forms.BooleanField(
        label='photo_clear',
        required=False,
    )

    def clean(self):
        if self.cleaned_data.get('photo') and self.cleaned_data.get('photo_clear'):
            self.add_error('photo', "Please either submit a file or check the default image checkbox, not both")
        elif self.cleaned_data.get('photo'):
            content_types = ['image/png', 'image/jpg', 'image/jpeg']
            if self.cleaned_data.get('photo').content_type in content_types:
                if self.cleaned_data.get('photo').size > 2*1024*1024:
                    self.add_error('photo', "Image file too large ( > 2mb )")
            else:
                self.add_error('photo', "Not valid file type. Only PNG and JPG are supported")
        return self.cleaned_data


# author: Juane
class TravellerEditPasswordForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput
    )
    old_password = forms.CharField(
        label='Old password',
        required=True,
        # min_length=8,
        # max_length=32,
        # validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                # 'maxlength': '32',
                # 'minlength': '8',
                # 'pattern': '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$'
            }
        )
    )
    password = forms.CharField(
        label='New password',
        required=True,
        min_length=8,
        max_length=32,
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '32',
                'minlength': '8',
                'pattern': '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$',
            }
        )
    )
    password_repeat = forms.CharField(
        label='New password repeat',
        required=True,
        min_length=8,
        max_length=32,
        validators=[password_validator],
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '32',
                'minlength': '8',
                'pattern': '^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$',
                'data-match': '#id_password',
                'data-match-error': "Whoops, these don't match"
            }
        )
    )

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
