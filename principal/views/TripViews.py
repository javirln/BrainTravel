# -*- coding: latin-1 -*-
import traceback

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from principal.models import Judges
from principal.forms import TripEditForm
from principal.models import Trip, Comment
from principal.services import TripService, TravellerService
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
    if trip.traveller.id == request.user.id or trip.state == 'ap' or request.user.has_perm('principal.administrator'):
        judges = Judges.objects.filter(trip_id=trip_id, traveller_id=request.user.id)
        if len(judges) == 0:
            judge = None
        else:
            judge = list(judges)[0]
        # is_edit = True
        data = {'id': trip.id, 'state': trip.state}
        form = TripUpdateStateForm(initial=data)
        return render_to_response('public_trip_details.html',
                                  {'trip': trip, 'comments': comments, 'traveller_edit': True,
                                   'judge': judge, 'form': form}, context_instance=RequestContext(request))
    else:
        BrainTravelUtils.save_error(request)
        return render_to_response('search.html', {}, context_instance=RequestContext(request))


# author: Juane
@login_required()
def list_trip_administrator(request):
    try:
        trips = TripService.list_trip_administrator(request.user)
    except AssertionError:
        return render_to_response('error.html')
    paginator = Paginator(trips, 2)
    page = request.GET.get('page')
    try:
        trips = paginator.page(page)
    except PageNotAnInteger:
        trips = paginator.page(1)
    except EmptyPage:
        trips = paginator.page(paginator.num_pages)
    return render_to_response('trip_list.html', {'trips': trips}, context_instance=RequestContext(request))


# author: Juane
@login_required()
def update_state(request, trip_id):
    try:
        assert request.user.has_perm('principal.administrator')
        if request.POST:
            trip_form = TripUpdateStateForm(request.POST)
            if trip_form.is_valid():
                trip = TripService.update_state(request.user, trip_form)
                assert str(trip.scorable_ptr_id) == trip_id
                TripService.save(trip)
                BrainTravelUtils.save_success(request, 'Trip successfully updated')
                return redirect(list_trip_administrator)
        else:
            return redirect(public_trip_details(request, trip_id))
    except AssertionError:
        return render_to_response('error.html')


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
        return render_to_response('trip_list.html', {'trips': trips},
                                  context_instance=RequestContext(request))


# david
@login_required()
def list_all_by_traveller_draft(request):
    trips = TripService.list_my_trip_draft(request.user.id)
    if trips is not False:
        paginator = Paginator(trips, 5)
        page = request.GET.get('page')
        try:
            trips = paginator.page(page)
        except PageNotAnInteger:
            trips = paginator.page(1)
        except EmptyPage:
            trips = paginator.page(paginator.num_pages)
        return render_to_response('trip_list.html', {'trips': trips}, context_instance=RequestContext(request))


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
                return redirect('/trip/mylist/1')
            elif "save" in request.POST and request.POST['save'] == "Publish Trip":
                trip_new.state = "pe"
                TripService.save_secure(trip_new)
                return redirect('/trip/mylist/2')

            return redirect('/trip/mylist/0')

    else:
        data = {}
        form = TripEditForm(initial=data)

    return render_to_response('trip_edit.html', {"form": form, "create": True},
                              context_instance=RequestContext(request))


# david
@login_required()
def trip_edit(request, trip_id):
    try:
        assert request.user.has_perm('principal.traveller')
        trip = Trip.objects.get(id=trip_id)
        assert trip.traveller.id == request.user.id
        if request.POST:
            form = TripEditForm(request.POST)
            if form.is_valid():
                trip.publishedDescription = form.cleaned_data['publishedDescription']
                trip.city = form.cleaned_data['city']
                trip.startDate = form.cleaned_data['startDate']
                trip.endDate = form.cleaned_data['endDate']
                trip.country = form.cleaned_data['country']
                if 'save' in request.POST and request.POST['save'] == "Save draft":
                    trip.state = "df"
                    TripService.save_secure(trip)
                    return redirect('/trip/mylist/1')
                elif 'save' in request.POST and request.POST['save'] == "Publish Trip":
                    trip.state = "pe"
                    TripService.save_secure(trip)
                    return redirect('/trip/mylist/2')

            if 'delete' in request.POST:
                TripService.delete(request, trip)
                return redirect('/trip/mylist/3')

        else:
            data = {'city': trip.city, 'publishedDescription': trip.publishedDescription, 'country': trip.country,
                    'startDate': trip.startDate, 'endDate': trip.endDate}
            form = TripEditForm(initial=data)

        return render_to_response('trip_edit.html',
                                  {"form": form, "trip": trip, "can_delete": True, "create": False},
                                  context_instance=RequestContext(request))
    except AssertionError:
        print(traceback.format_exc())
        return render_to_response('error.html')


# author: Javi Rodriguez
@login_required()
def comment_trip(request):
    try:
        comment = request.POST['text-comment']
        user_id = request.user.id
        trip_id = request.POST['trip-id']
        url = request.path.split("/")
        res = TripService.submit_comment(user_id, comment, trip_id)
        if res['state'] == False:
            BrainTravelUtils.save_warning(request, 'This trip is pending of the approval by an administrator.')
            return HttpResponseRedirect("/" + url[1] + "/" + trip_id)
        elif res['ownership'] == False:
            BrainTravelUtils.save_warning(request, 'You cannot comment your own trip!')
        elif res['state'] == True and res['ownership'] == True:
            BrainTravelUtils.save_success(request, 'Your comment has been saved!')
        return HttpResponseRedirect("/" + url[1] + "/" + trip_id)
    except:
        msg_errors = ["Something went wrong..."]
        return render_to_response('public_trip_details.html', {'msg_errors': msg_errors})


# author: Javi Rodriguez
@login_required()
def send_assessment(request):
    try:
        user_id = request.user.id
        rate_text = request.POST['text-rate-description']
        trip_id = request.POST['trip-id']
        rate_value = request.POST['rate-value']
        url = request.path.split("/")
        res = TripService.send_assessment(user_id, rate_value, trip_id, rate_text)
        if res == False:
            BrainTravelUtils.save_warning(request, 'You already voted this trip!')
        else:
            BrainTravelUtils.save_success(request, 'Your vote has been saved!')
        return HttpResponseRedirect("/" + url[1] + "/" + trip_id)
    except:
        msg_errors = ["Something went wrong..."]
        return render_to_response('public_trip_details.html', {'msg_errors': msg_errors})


# author: Juane
@login_required()
def list_trip_approved_by_profile(request, profile_id):
    try:
        assert request.user.has_perm('principal.traveller')
        traveller = TravellerService.find_one(profile_id)
        trips = TripService.list_my_trip_approved(traveller.id)
        return render_to_response('trip_list.html', {'trips': trips}, context_instance=RequestContext(request))
    except AssertionError:
        return render_to_response('error.html')