from django.contrib.auth.decorators import permission_required
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.models import Venue, Scorable


@permission_required('principal.traveller')
def venue_details_json(request, id_venue):
    venue = Venue.objects.get(id = id_venue)
    scorable = Scorable.objects.get(id = id_venue)
    res = serializers.serialize("json", [venue,] + [scorable,])
    return JsonResponse(res, safe=False)

@permission_required('principal.traveller')
def visited_venues(request):
    try:
        visited_venues = Venue.objects.filter(day__trip__traveller__id=request.user.id)
        paginator = Paginator(visited_venues, 12)
        page = request.GET.get('page')
        try:
            visited_venues = paginator.page(page)
        except PageNotAnInteger:
            visited_venues = paginator.page(1)
        except EmptyPage:
            visited_venues = paginator.page(paginator.num_pages)

        return render_to_response('my_visited_venues.html', {'visited_venues': visited_venues}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


def venues_to_change_json(request, id_trip):
    venues_to_change = Venue.objects.filter(~Q(day__trip__id=id_trip) & Q(id__in=[1234]))
    res = serializers.serialize("json", venues_to_change)
    return JsonResponse(res, safe=False)
