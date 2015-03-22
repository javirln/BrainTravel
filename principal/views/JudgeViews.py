from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from principal.models import Judges, Trip, Traveller
from principal.services import JudgeServices, TripService


@login_required()
def judge(request, trip_id, like):
    if like == '0':
        like = False
    else:
        like = True
    # if request.user.has_perm("traveller"):
    trip = Trip.objects.get(id=trip_id)
    assert trip.state == 'ap'
    traveller = Traveller.objects.get(id=request.user.id)
    list_judges = Judges.objects.filter(trip_id=trip_id, traveller_id=traveller.id)
    if len(list_judges) == 0:
        judge1 = JudgeServices.create(trip, traveller, like)
        JudgeServices.save(judge1)
        if like:
            trip1 = TripService.increase_like(trip)
            TripService.save(trip1)
        else:
            trip2 = TripService.increase_dislike(trip)
            TripService.save(trip2)
    else:
        judge1 = list(list_judges)[0]
        if judge1.like is like:
            JudgeServices.delete(judge1)
            if like:
                likes = trip.likes
                trip.likes = likes-1
                trip.save()
            else:
                dislikes = trip.dislikes
                trip.dislikes = dislikes-1
                trip.save()
        else:
            judge2 = JudgeServices.update(judge1, like)
            JudgeServices.save(judge2)
            if like:
                likes = trip.likes
                trip.likes = likes+1
                trip.save()
                dislikes = trip.dislikes
                trip.dislikes = dislikes-1
                trip.save()
            else:
                dislikes = trip.dislikes
                trip.dislikes = dislikes+1
                likes = trip.likes
                trip.likes = likes-1
                trip.save()
    return HttpResponseRedirect('/public_trip_details/'+trip_id)