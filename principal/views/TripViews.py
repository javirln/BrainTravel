# -*- coding: latin-1 -*-
from principal.models import Trip
from principal.services import TripService
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http.response import HttpResponse

def search_trip(request):
	if request.method == 'GET':
		city = request.GET.get('city', False)
		trip_result = None
		try:
			trip_result = TripService.searchTrip(city)
			return render_to_response('search.html', {'trip_result': trip_result}, context_instance=RequestContext(request))
		except Exception as e:
			return HttpResponse(e)