# -*- coding: latin-1 -*-

"""Aquí se colocan los servicios relacionados con el Model1"""
from django.contrib.auth.models import User

from principal.models import Traveller


def create(traveller_registration_form):
    
    user_account = User.objects.create_user(username=traveller_registration_form.email,
                                            email=traveller_registration_form.email,
                                            password=traveller_registration_form.password1)
    
    res = Traveller(user_account = user_account,
                    first_name=traveller_registration_form.first_name,
                    last_name=traveller_registration_form.last_name,
                    genre = traveller_registration_form.genre)
    
    return res


def save(traveller):
    traveller.save()