# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.forms import TripEditorForm, TripCreateForm
from principal.models import Trip, Comment
from principal.services import TripService


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
    is_edit = False
    if trip.traveller.id == request.user.id:
        is_edit = True
    return render_to_response('public_trip_details.html',
                              {'trip': trip, 'comments': comments, 'traveller_edit': is_edit},
                              context_instance=RequestContext(request))


@login_required()
def trip_list_all(request):
    if request.user.is_authenticated() and request.user.has_perm('administrator'):
        trips = TripService.list_trip_all()
        return render_to_response('trip_list.html', {'trips': trips}, content_type=RequestContext(request))
    else:
        return render_to_response('index.html')


# david
@login_required()
def list_all_by_traveller(request):
    if request.user.is_authenticated():
        trips = TripService.list_my_trip(request.user.id)
        return render_to_response('list_my_trip.html', {'trips': trips}, content_type=RequestContext(request))
    else:
        return render_to_response('index.html')


# david
@login_required()
def trip_create(request):
    user_id = request.user.id
    if request.POST:
        form = TripCreateForm(request.POST)
        if form.is_valid():
            trip_new = TripService.create(form, user_id)
            trip_new.save()
            return HttpResponseRedirect('/list_my_trips/')
    else:
        form = TripCreateForm()

    return render_to_response('trip_edit.html', {"form": form, "create": True},
                              context_instance=RequestContext(request))


# david
@login_required()
def trip_edit(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if trip.traveller.id != request.user.id:
        return render_to_response('index.html', context_instance=RequestContext(request))

    if request.POST:
        form = TripEditorForm(request.POST)
        if form.is_valid():
            trip.publishedDescription = form.cleaned_data['publishedDescription']
            trip.save()
            return HttpResponseRedirect('/list_my_trips/')
    else:
        data = {'startDate': trip.startDate, 'endDate': trip.endDate}
        form = TripEditorForm(initial=data)

    return render_to_response('trip_edit.html', {"form": form, "trip": trip, "create": False},
                              context_instance=RequestContext(request))
