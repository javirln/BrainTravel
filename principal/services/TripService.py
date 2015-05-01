# -*- coding: latin-1 -*-

from django.db.models import Q, Count, Sum

from principal.models import Trip, Traveller, Comment, Assessment, Scorable, Feedback, Venue


# author: Javi
def searchTrip(title):
    trip_list = []
    if title and title != " ":
        trip_list = Trip.objects.filter(Q(name__icontains=title, state='ap', planified=False)
                                        | Q(city__icontains=title, state='ap', planified=False)
                                        | Q(country__icontains=title, state='ap', planified=False)).order_by('likes')
    return trip_list


def find_planed_trips_by_traveller(traveller_id):
    res = Trip.objects.filter(Q(traveller=traveller_id) & Q(planified=True))
    return res


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


# author: David
def list_my_trip(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller, planified=False).filter(~Q(state='df'))
    return trips


# author: David
def list_trip_draft(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller, planified=False, state='df')
    return trips


# author: Juane
def list_trip_approved(id_traveller):
    trips = Trip.objects.all().filter(traveller=id_traveller, planified=False, state='ap')
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
    trip.name = form.cleaned_data['name']
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
    to_check = Trip.objects.get(id=trip_id)
    if to_check.state == "ap":
        user = Traveller.objects.get(id=user_id)
        score_trip = Scorable.objects.get(id=trip_id)
        score_user = Scorable.objects.get(id=user_id)
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
            num = scorable_math[0].rating_sum
            if num is None:
                num = 0
            number = scorable_math[0].rating_number
            scorable_instance.rating = int(num) + int(rate_value) / (int(number) + 1)
            score_user.rating += int(num) + int(rate_value) / (int(number) + 1)
            score_user.save()
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


# author: Javi Rodriguez
def send_feedback(user_id, venue_id, lead_time, duration_time, description):
    user = Traveller.objects.get(id=user_id)
    venue = Venue.objects.get(id=venue_id)
    feedback_instance = Feedback(
        description=description,
        leadTime=lead_time,
        duration=duration_time,
        traveller=user,
        usefulCount=0,
        venues=venue
    )
    feedback_instance.save()


# author: Javi Rodriguez
def value_tip(id_tip, id_venue):
    tip = Feedback.objects.get(id=id_tip, venues=id_venue)
    new_count = tip.usefulCount + 1
    tip.usefulCount = new_count
    tip.save()


# author: Javi Rodriguez
def stats():
    travellers_travelling = Traveller.objects.annotate(num_trips=Count('trip')).order_by('-num_trips')
    travellers_publishing = Traveller.objects.annotate(num_trips=Count('trip')) \
        .filter(trip__planified=False).order_by('-num_trips')
    best_trips = Trip.objects.filter(judges__likes=True).annotate(num_judges=Count('judges')).order_by('-num_judges')
    most_liked_trips = Trip.objects.filter(planified=False).annotate(num_likes=Count('likes')).order_by('-num_likes')
    most_useful_tips = Feedback.objects.annotate(num_useful=Count('usefulCount')).order_by('-num_useful')
    result = {'travellers_travelling': travellers_travelling, 'travellers_publishing': travellers_publishing,
              'best_trips': best_trips, 'most_liked_trips': most_liked_trips, 'most_useful_tips': most_useful_tips}
    return result