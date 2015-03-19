# -*- coding: latin-1 -*-

from principal.models import Trip


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