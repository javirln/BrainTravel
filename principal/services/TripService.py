# -*- coding: latin-1 -*-

from django.db.models import Q, Count, Sum

from principal.models import Trip, Traveller, Comment, Assessment, Scorable


# author: Javi
def searchTrip(title):
    trip_list = []
    if title and title != " ":
        trip_list = Trip.objects.filter(name__icontains=title, state='ap').order_by('likes')
    return trip_list


# author: Juane
def list_trip_administrator(user):
    assert user.has_perm('principal.administrator')
    result = Trip.objects.all().filter(~Q(planified=True) & ~Q(state='df')).order_by('-state')
    return result


# author: Juane
def update_state(user, form):
    assert user.has_perm('principal.administrator')
    result = Trip.objects.get(id=form.cleaned_data['id'])
    result.state = form.cleaned_data['state']
    return result


# author: Juane
def save(trip):
    trip.save()


# david
def list_my_trip(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller).filter(~Q(state='df'))
    return trips


# david
def list_my_trip_draft(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller, state='df')
    return trips


# david
def create(form, user_id):
    traveller = Traveller.objects.get(id=user_id)
    trip = Trip()
    trip.publishedDescription = form.cleaned_data['publishedDescription']
    trip.startDate = form.cleaned_data['startDate']
    trip.endDate = form.cleaned_data['endDate']
    trip.coins = 0
    trip.likes = 0
    trip.dislikes = 0
    trip.traveller = traveller
    trip.city = form.cleaned_data['city']
    trip.country = form.cleaned_data['country']
    return trip


# author: Juane
def increase_like(trip):
    likes = trip.likes
    trip.likes = likes + 1
    return trip


# author: Juane
def increase_dislike(trip):
    dislikes = trip.dislikes
    trip.dislikes = dislikes + 1
    return trip


# author: Juane
def decrement_like(trip):
    likes = trip.likes
    trip.likes = likes - 1
    return trip


# author: Juane
def decrement_dislike(trip):
    dislikes = trip.dislikes
    trip.dislikes = dislikes - 1
    return trip


# david
def save_secure(trip):
    if trip.startDate > trip.endDate:
        pass
    else:
        trip.save()


# author: Javi Rodriguez
def submit_comment(user_id, comment_text, trip_id):
    traveller = Traveller.objects.get(id=user_id)
    trip = Trip.objects.get(id=trip_id)
    results = {'state': True, 'ownership': True}
    if trip.state == 'ap':
        if traveller.id != trip.traveller.id:
            comment = Comment(
                description=comment_text,
                trip=trip,
                traveller=traveller,
            )
            comment.save()
            return results
        else:
            results['ownership'] = False
            return results
    else:
        results['state'] = False
        return results


# david
def delete(request, trip):
    assert request.user.id == trip.traveller.id
    trip.delete()


# author: Javi Rodriguez
def send_assessment(user_id, rate_value, trip_id, rate_text):
    user = Traveller.objects.get(id=user_id)
    score_trip = Scorable.objects.get(id=trip_id)
    occurrences_same_traveller = Assessment.objects.all().filter(traveller=user_id, scorable_id=trip_id).count()
    scorable_instance = Scorable.objects.get(id=trip_id)
    scorable_math = Scorable.objects.filter(id=trip_id).annotate(rating_number=Count('rating'),
                                                                 rating_sum=Sum('rating'))
    if 0 == occurrences_same_traveller:
        comment = Assessment(
            score=rate_value,
            comment=rate_text,
            traveller=user,
            scorable=score_trip
        )
        comment.save()
        scorable_instance.rating = scorable_math[0].rating_sum + rate_value / scorable_math[0].rating_number + 1
        scorable_instance.save()
        return True
    return False


# author: Juane
def find_one(trip_id):
    try:
        trip = Trip.objects.get(id=trip_id)
    except Trip.DoesNotExist:
        assert False
    return trip


# author: Juane
def list_my_trip_approved(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller, state='ap')
    return trips