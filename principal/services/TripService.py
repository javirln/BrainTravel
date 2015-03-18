# -*- coding: latin-1 -*-

from principal.models import Trip, City

def searchTrip(city_name):
	city_name_id = City.objects.filter(name=city_name)
	trip_list = Trip.objects.filter(city=city_name_id).order_by('likes')
	return trip_list

def getCommentsFromTrip(trip):
	comments = Comment.objects.get(trip=trip).count()
	return comments