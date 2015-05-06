from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from principal.models import Judges, Trip, Traveller, CoinHistory
from principal.services import JudgeServices, TripService, CoinService

# author: Juane
@login_required()
def judge(request, trip_id, like):
    try:
        assert request.user.has_perm("principal.traveller")
        trip = Trip.objects.get(id=trip_id)
        assert trip.state == 'ap'
    except AssertionError:
        return render_to_response('error.html')

    if like == '0':
        like = False
    else:
        like = True

    traveller = Traveller.objects.get(id=request.user.id)
    list_judges = Judges.objects.filter(trip_id=trip_id, traveller_id=traveller.id)

    if len(list_judges) == 0:
        judge1 = JudgeServices.create(trip, traveller, like)
        JudgeServices.save(judge1)
        if like:
            trip = TripService.increase_like(trip, traveller.id)
        else:
            trip = TripService.increase_dislike(trip)
    else:
        judge1 = list(list_judges)[0]
        if judge1.like is like:
            JudgeServices.delete(judge1)
            if like:
                trip = TripService.decrement_like(trip)
            else:
                trip = TripService.decrement_dislike(trip)
        else:
            judge2 = JudgeServices.update(judge1, like)
            JudgeServices.save(judge2)
            if like:
                trip = TripService.increase_like(trip)
                trip = TripService.decrement_dislike(trip)
            else:
                trip = TripService.increase_dislike(trip)
                trip = TripService.decrement_like(trip)
    TripService.save(trip)
    return HttpResponseRedirect('/public_trip_details/' + trip_id)