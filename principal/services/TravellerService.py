# -*- coding: latin-1 -*-

"""Aquí se colocan los servicios relacionados con el Model1"""
from django.contrib.auth.models import User

from principal.models import Traveller


def create(form):
    
    user_account = User.objects.create_user(username=form.cleaned_data['email'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password1'])
    
    user_account.save()
    
    res = Traveller(user_account=user_account,
                    firstName=form.cleaned_data['first_name'],
                    lastName=form.cleaned_data['last_name'],
                    genre=form.cleaned_data['genre'],
                    coins=0, recommendations=0)
    
    return res


def save(traveller):
    traveller.save()
