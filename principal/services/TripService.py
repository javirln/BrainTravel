# -*- coding: latin-1 -*-
from django.db.models import Q, Count, Avg, Sum
from principal.models import Trip, Traveller, Assessment, Scorable, Feedback, Venue, Likes, CoinHistory, Comment


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


# david
def save_secure(trip):
    if trip.startDate > trip.endDate:
        pass
    else:
        trip.save()


# david
def delete(request, trip):
    assert request.user.id == trip.traveller.id
    trip.delete()


# author: Juane
def construct_assessment(user_id, assessment_form):

    # Obtener los valores del formulario
    comment = assessment_form.cleaned_data['comment']
    trip_id = assessment_form.cleaned_data['id_trip']
    score = assessment_form.cleaned_data['score']

    # Validaciones
    trip = Trip.objects.get(id=trip_id)
    assert trip.state == "ap"
    assert trip.traveller.id != user_id
    assert trip.planified is False
    occurrences_same_traveller = Assessment.objects.all().filter(traveller=user_id, scorable_id=trip_id).count()
    assert 0 == occurrences_same_traveller

    # Obtener el viajero
    traveller = Traveller.objects.get(id=user_id)

    # Obtener el viaje puntuable
    score_trip = Scorable.objects.get(id=trip_id)

    # Crear la valoracion
    assessment = Assessment(
        score=score,
        comment=comment,
        traveller=traveller,
        scorable=score_trip
    )

    # Guardar la valoracion en la base de datos
    assessment.save()

    # Calcular y guardar el rating del viaje
    scorable_instance = Scorable.objects.get(id=trip_id)
    average_score = Assessment.objects.filter(scorable_id=scorable_instance.id).aggregate(average_score=Avg('score'))
    scorable_instance.rating = round(average_score["average_score"], 2)
    scorable_instance.save()

    # Calcular y guardar la reputacion
    average_reputation = Trip.objects.filter(traveller_id=trip.traveller.id).aggregate(average_rating=Avg('rating'))
    traveller = Traveller.objects.get(id=trip.traveller.id)
    traveller.reputation = round(average_reputation["average_rating"], 2)
    traveller.save()


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
def value_tip(tip, user):
    new_count = tip.usefulCount + 1
    tip.usefulCount = new_count
    tip.save()
    
    #guardar la relacion entre like y feedback
    likes_instance = Likes(
        useful=True,
        traveller=user,
        feedback=tip
    )
    
    likes_instance.save()


# author: Javi Rodriguez
def stats():
    travellers_travelling = Traveller.objects.annotate(num_trips=Count('trip')).order_by('-num_trips')[:5]
    travellers_publishing = Traveller.objects.annotate(num_trips=Count('trip')).filter(Q(trip__planified=False) & ~Q(num_trips = 0)).order_by(
        '-num_trips')[:5]
    best_trips = Trip.objects.filter(judges__likes=True).annotate(num_judges=Count('judges')).order_by('-num_judges')[:5]
    most_liked_trips = Trip.objects.filter(Q(planified=False) & Q(state='ap')).annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]
    most_useful_tips = Feedback.objects.annotate(num_useful=Count('usefulCount')).order_by('-num_useful')[:5]
    most_visited_venues = Venue.objects.annotate(num_visit=Count('day__trip')).order_by('-num_visit')[:5]
    result = {'travellers_travelling': travellers_travelling, 'travellers_publishing': travellers_publishing,
              'best_trips': best_trips, 'most_liked_trips': most_liked_trips, 'most_useful_tips': most_useful_tips, 'most_visited_venues': most_visited_venues}
    return result
