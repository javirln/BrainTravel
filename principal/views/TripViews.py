# -*- coding: latin-1 -*-
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.models import Trip, Comment
from principal.services import TripService


def search_trip(request):
	if request.method == 'GET':
		title = request.GET.get('title', False)
		trip_result = None
		try:
			trip_result = TripService.searchTrip(title)
			return render_to_response('search.html', {'trip_result': trip_result}, context_instance=RequestContext(request))
		except Exception as e:
				return HttpResponse(e)
		
def public_trip_details(request, trip_id):
	trip = Trip.objects.get(id=trip_id)
	comments = Comment.objects.get(trip=trip_id)
	return render_to_response('public_trip_details.html', {'trip': trip, 'comments': comments}, context_instance=RequestContext(request))