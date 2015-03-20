# -*- coding: latin-1 -*-

from principal.models import Trip


def searchTrip(title):
    trip_list = []
    if title and title != " ":
        trip_list = Trip.objects.filter(name__icontains=title).order_by('likes')
    return trip_list


def list_all_by_state(user):
    # List of all trips ordered by their status
    if user.has_perm('administrator'):
        result = Trip.objects.order_by('state')
    else:
        result = False
    return result


def update_state(user, form):
    # Update the status of a trip
    if user.has_perm('administrator'):
        result = Trip.objects.get(id=form.cleaned_data['id'])
        result.state = form.cleaned_data['state']
    else:
        result = False
    return result


def save(trip):
    trip.save()


# david
def list_my_trip(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller)
    return trips

