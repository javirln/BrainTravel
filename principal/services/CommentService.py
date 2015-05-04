from principal.models import Trip, Traveller, Comment


# author: Juane
def construct_comment(user_id, comment_form):
    traveller = Traveller.objects.get(id=user_id)
    trip = Trip.objects.get(id=comment_form.cleaned_data['id_trip'])
    comment = Comment(
        description=comment_form.cleaned_data['comment'],
        trip=trip,
        traveller=traveller,
    )
    return comment


# author: Juane
def save(user_id, comment):
    assert comment.trip.state == 'ap'
    assert comment.traveller.id == user_id
    comment.save()


