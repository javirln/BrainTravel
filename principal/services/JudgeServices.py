# -*- coding: latin-1 -*-

from principal.models import Judges


# author: Juane
def create(trip, traveller, like):
    judge = Judges()
    judge.trip = trip
    judge.traveller = traveller
    judge.like = like
    return judge


# author: Juane
def update(judge, like):
    judge.like = like
    return judge


# author: Juane
def save(judge):
    return judge.save()


# author: Juane
def delete(judge):
    judge.delete()