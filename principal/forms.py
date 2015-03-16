# -*- coding: latin-1 -*-
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
'''class TravellerRegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'form-control'}), max_length=50)
    last_name = forms.CharField(max_length=50)
    genre = forms.ChoiceField('MALE', 'FEMALE')
    email = forms.EmailField()
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    
    def clean(self):
        if self.password1 != self.password2:
            raise ValidationError("Passwords must be the same!")
        super().clean()'''