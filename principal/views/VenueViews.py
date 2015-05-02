from django.core import serializers
from django.db.models.query_utils import Q
from django.http.response import JsonResponse

from principal.models import Venue, Scorable


def venue_details_json(request, id_venue):
    venue = Venue.objects.get(id = id_venue)
    scorable = Scorable.objects.get(id = id_venue)
    res = serializers.serialize("json", [venue,] + [scorable,])
    return JsonResponse(res, safe=False)

def venues_to_change_json(request, id_trip):
    venues_to_change = Venue.objects.filter(~Q(day__trip__id=id_trip) & Q(id__in=[1234]))
    res = serializers.serialize("json", venues_to_change)
    return JsonResponse(res, safe=False)