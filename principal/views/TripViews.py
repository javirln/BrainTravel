# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.models import Trip, Comment
from principal.services import TripService
from django.utils.translation import ugettext as _

def search_trip(request):
    if request.method == 'GET':
        title = request.GET.get('title', False)
        trip_result = None
        try:
            trip_result = TripService.searchTrip(title)
            return render_to_response('search.html', {'trip_result': trip_result},
                                      context_instance=RequestContext(request))
        except Exception as e:
            return HttpResponse(e)


def public_trip_details(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    comments = Comment.objects.filter(trip=trip_id)
    return render_to_response('public_trip_details.html', {'trip': trip, 'comments': comments},
                              context_instance=RequestContext(request))

@login_required()
def trip_list_all(request):
    if request.user.is_authenticated() and request.user.has_perm('administrator'):
        trips = TripService.list_trip_all()
        return render_to_response('trip_list.html', {'trips': trips}, content_type=RequestContext(request))
    else:
        return render_to_response('index.html')