# -*- coding: latin-1 -*-

from principal.models import Trip, Traveller


def searchTrip(title):
    trip_list = []
    if title and title != " ":
        trip_list = Trip.objects.filter(name__icontains=title).order_by('likes')
    return trip_list


def list_trip_all():
    trips = Trip.objects.order_by('approved')
    return trips


# david
def list_my_trip(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller)
    return trips


def create(form, user_id):
    traveller = Traveller.objects.get(id=user_id)
    trip = Trip()
    trip.publishedDescription = form.cleaned_data['publishedDescription']
    trip.startDate = form.cleaned_data['startDate']
    trip.endDate = form.cleaned_data['endDate']
    trip.coins = 0
    trip.likes = 0
    trip.dislikes = 0
    trip.traveller = traveller
    trip.city = form.cleaned_data['city']
    trip.country = form.cleaned_data['country']
    return trip