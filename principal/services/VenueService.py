from django.core.context_processors import request
from django.db.models.query_utils import Q

from principal.models import Venue


def is_visited_by_user(request, venue_id):
    return Venue.objects.filter(Q(day__trip__traveller__id=request.user.id) & Q(id = venue_id)).exists()
    