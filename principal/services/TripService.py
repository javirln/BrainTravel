# -*- coding: latin-1 -*-

from principal.models import Trip

def searchTrip(title):
	if not title or " " in title:
		title = "null"
	trip_list = Trip.objects.filter(name__icontains=title).order_by('likes')
	return trip_list


def list_trip_all():

    trips = Trip.objects.order_by('approved')
    return trips