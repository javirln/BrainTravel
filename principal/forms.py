# -*- coding: latin-1 -*-
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django_summernote.widgets import SummernoteWidget
from paypal.standard.forms import PayPalPaymentsForm

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
    
    
class FormPaypalOwn(PayPalPaymentsForm):
    def get_image(self):
        return "https://www.paypalobjects.com/webstatic/en_US/btn/btn_checkout_pp_142x27.png";
