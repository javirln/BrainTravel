# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from principal.models import Judges
from principal.forms import TripEditForm
from principal.models import Trip, Comment
from principal.services import TripService
from principal.forms import TripUpdateStateForm
from principal.utils import BrainTravelUtils



# author: Javi
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


# author: Javi
def public_trip_details(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    comments = Comment.objects.filter(trip=trip_id)
    # is_edit = False
    if trip.traveller.id == request.user.id or trip.state == 'ap':
        judges = Judges.objects.filter(trip_id=trip_id, traveller_id=request.user.id)
        if len(judges) == 0:
            judge = None
        else:
            judge = list(judges)[0]
        # is_edit = True
        return render_to_response('public_trip_details.html',
                                  {'trip': trip, 'comments': comments, 'traveller_edit': True, 'judge': judge},
                                  context_instance=RequestContext(request))
    else:
        BrainTravelUtils.save_error(request)
        return render_to_response('search.html', {}, context_instance=RequestContext(request))


# author: Juane
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


# author: Juane
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


# david
@login_required()
def list_all_by_traveller(request, optional=0):
    if optional == "0":
        BrainTravelUtils.save_error(request)
    if optional == "1":
        BrainTravelUtils.save_success(request, "Successfully complete action")
    if optional == "2":
        BrainTravelUtils.save_success(request, "Your trip must be accept by a admin")
    if optional == "3":
        BrainTravelUtils.save_success(request, "Delete trip")

    trips = TripService.list_my_trip(request.user.id)
    if trips is not False:
        paginator = Paginator(trips, 5)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('list_my_trip.html', {'trips': trips},
                                  context_instance=RequestContext(request))


# david
@login_required()
def list_all_by_traveller_draft(request):
    trips = TripService.list_my_trip_draft(request.user.id)
    ss = len(trips)
    if trips is not False:
        paginator = Paginator(trips, 5)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('list_my_trip.html', {'trips': trips}, content_type=RequestContext(request))


# david
@login_required()
def trip_create(request):
    user_id = request.user.id
    if request.POST:
        form = TripEditForm(request.POST)
        if form.is_valid():
            trip_new = TripService.create(form, user_id)
            if "save" in request.POST and request.POST['save'] == "Save draft":
                trip_new.state = "df"
                TripService.save_secure(trip_new)
                return redirect('/Trip/list/1')
            elif "save" in request.POST and request.POST['save'] == "Publish Trip":
                trip_new.state = "pe"
                TripService.save_secure(trip_new)
                return redirect('/Trip/list/2')

            return redirect('/Trip/list/0')

    else:
        data = {'startDate': 'yyyy/mm/dd', 'endDate': 'yyyy/mm/dd'}
        form = TripEditForm(initial=data)

    return render_to_response('trip_edit.html', {"form": form, "create": True},
                              context_instance=RequestContext(request))


# david
@login_required()
def trip_edit(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    if trip.traveller.id != request.user.id:
        return render_to_response('index.html', context_instance=RequestContext(request))

    if request.POST:
        form = TripEditForm(request.POST)
        if form.is_valid():
            trip.publishedDescription = form.cleaned_data['publishedDescription']
            trip.city = form.cleaned_data['city']
            trip.startDate = form.cleaned_data['startDate']
            trip.endDate = form.cleaned_data['endDate']
            trip.country = form.cleaned_data['country']
            if "save" in request.POST and request.POST['save'] == "Save draft":
                trip.state = "df"
                TripService.save_secure(trip)
                return redirect('/Trip/list/1')
            elif "save" in request.POST and request.POST['save'] == "Publish Trip":
                trip.state = "pe"
                TripService.save_secure(trip)
                return redirect('/Trip/list/2')
            elif request.POST['delete'] == "Delete Trip":
                TripService.delete(trip)
                return redirect('/Trip/list/3')

            return redirect('/Trip/list/')
    else:
        data = {'city': trip.city, 'country': trip.country, 'startDate': trip.startDate, 'endDate': trip.endDate}
        form = TripEditForm(initial=data)

    return render_to_response('trip_edit.html', {"form": form, "trip": trip, "create": False},
                              context_instance=RequestContext(request))