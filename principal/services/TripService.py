# -*- coding: latin-1 -*-

from django.db.models import Q

from principal.models import Trip, Traveller, Comment


# author: Javi
def searchTrip(title):
    trip_list = []
    if title and title != " ":
        trip_list = Trip.objects.filter(name__icontains=title, state='ap').order_by('likes')
    return trip_list


# author: Juane
def list_all_by_state(user):
    # List of all trips ordered by their status
    if user.has_perm('administrator'):
        result = Trip.objects.order_by('state')
    else:
        result = False
    return result


# author: Juane
def update_state(user, form):
    # Update the status of a trip
    if user.has_perm('administrator'):
        result = Trip.objects.get(id=form.cleaned_data['id'])
        result.state = form.cleaned_data['state']
    else:
        result = False
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
    return


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
    if trip.state == 'ap':
        comment = Comment(
            description=comment_text,
            trip=trip,
            traveller=traveller,
        )
        comment.save()
        

# david
# comprobar algo?
# se borra en cascada
# TODO
def delete(trip):
    trip.delete()