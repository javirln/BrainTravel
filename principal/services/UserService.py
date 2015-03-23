# -*- coding: latin-1 -*-
"""Aquí se colocan los servicios relacionados con el Model1"""
from django.contrib.auth.models import User

from principal.models import Traveller
from principal.utils import BrainTravelUtils


def create(form):
    user_account = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], BrainTravelUtils.id_generator())
    user_account.is_active = False
    user_account.save()
    return user_account
