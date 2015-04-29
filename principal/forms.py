# -*- coding: latin-1 -*-
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from paypal.standard.forms import PayPalPaymentsForm
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from validators import password_validator
from principal.models import Traveller


def user_exist_validator(value):
    if User.objects.exists(username=value):
        raise ValidationError(_('Already exists a user with that email!'))


# Formulario de login
class LoginForm(forms.Form):
    username = forms.EmailField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '254',
                'placeholder': 'Email address'
            }
        )
    )
    password = forms.CharField(
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '32',
                'placeholder': 'Password'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                self.add_error('username', "Your account is desactivated")
        else:
            self.add_error('username', "Wrong email or password")

        return self.cleaned_data


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
    city = forms.CharField(label='City', widget=forms.TextInput())
    country = forms.CharField(label='Country', widget=forms.TextInput())
    startDate = forms.DateField(label="Start date", widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
    endDate = forms.DateField(label="End date", widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))

    publishedDescription = forms.CharField(label='Published Description',
                                           widget=forms.Textarea(attrs={'id': 'summernote'}))

    name = forms.CharField(label='Name', widget=forms.TextInput())

    def clean(self):
        name = self.cleaned_data['name']
        if len(name) > 150:
            self.add_error('name', _("Message length too long"))
        start_date = self.data['startDate']
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        end_date = self.data['endDate']
        end_date = datetime.strptime(end_date, '%d/%m/%Y').date()
        if start_date > datetime.now().date():
            self.add_error('startDate', "Must be a date in the past")
        if start_date > end_date:
            self.add_error('startDate', "Incorrect logic date")
            self.add_error('endDate', "Incorrect logic date")
        if end_date > datetime.now().date():
            self.add_error('endDate', "Must be a date in the past")

        return self.cleaned_data


# david
class PlanForm(forms.Form):
    city = forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control', }))
    country = forms.CharField(label='Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    startDate = forms.DateField(label="starDate", widget=forms.TextInput(attrs={'class': 'datepicker form-control'}))
    days = forms.CharField(label='Days', widget=forms.NumberInput(attrs={'min': 0, 'max': 7, 'class': 'form-control'}))

    def clean(self):
        start_date = self.data['startDate']
        start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
        if start_date < datetime.now().date():
            self.add_error('startDate', "Must be a date in the future")
        return self.data


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
                if self.cleaned_data.get('photo').size > 2 * 1024 * 1024:
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


# @author: Juane
class CommentForm(forms.Form):
    id_trip = forms.IntegerField(
        widget=forms.HiddenInput
    )
    comment = forms.CharField(
        required=True,
        min_length=3,
        max_length=254,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'required': 'required',
                'maxlength': '254',
                'minlength': '3',
                'rows': '3',
                'style': 'resize: none;'
            }
        )
    )
