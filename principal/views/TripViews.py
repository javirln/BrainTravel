# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from principal.models import Trip, Comment
from principal.services import TripService
from principal.forms import TripUpdateStateForm


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
def list_all_by_state(request):
    trips = TripService.list_all_by_state(request.user)
    if trips is not False:
        paginator = Paginator(trips, 1)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_list.html', {'trips': trips}, context_instance=RequestContext(request))
    else:
        msg_errors = ["You must login!"]
        return render_to_response('signin.html', {'msg_errors': msg_errors})


@login_required()
def update_state(request):
    if request.POST:
        trip_form = TripUpdateStateForm(request.POST)
        if trip_form.is_valid():
            trip = TripService.update_state(request.user, trip_form)
            if trip is not False:
                TripService.save(trip)
                return redirect(list_all_by_state)
            else:
                msg_errors = ["You must login!"]
                return render_to_response('signin.html', {'msg_errors': msg_errors})
    return redirect(list_all_by_state)
