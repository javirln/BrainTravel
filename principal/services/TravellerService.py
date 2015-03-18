# -*- coding: latin-1 -*-

"""Aquí se colocan los servicios relacionados con el Model1"""
from django.contrib.auth.models import User

from principal.models import Traveller
from principal.utils import BrainTravelUtils


def create(form):
    
    res = Traveller(first_name=form.cleaned_data['first_name'],
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['email'])
    res.is_active = False;
    return res


def save(traveller):
    traveller.save()
