# -*- coding: latin-1 -*-

"""Aquí se colocan los servicios relacionados con el Model1"""
from django.contrib.auth.models import User

from principal.models import Traveller

def create(form):
    
    res = Traveller(first_name=form.cleaned_data['first_name'],
                    email=form.cleaned_data['email'],
                    username=form.cleaned_data['email'])
    res.user_permissions.add('traveller.traveller')
    res.is_active = False;
    return res


def save(traveller):
    traveller.save()


# author: Juane
def find_one(traveller_id):
    try:
        traveller = Traveller.objects.get(id=traveller_id)
    except Traveller.DoesNotExist:
        assert False

    return traveller