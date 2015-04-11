# -*- coding: latin-1 -*-

import pprint
from datetime import date, datetime
import traceback
from django.contrib.auth.decorators import permission_required

from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from principal.forms import PlanForm
from principal.models import Trip, Traveller
from principal.services import TravellerService
from principal.services import FoursquareServices
from principal.services.FoursquareServices import init_fs, categories_initializer, search_by_category
from principal.services.FoursquareServices import init_fs, test_plan
from principal.utils import BrainTravelUtils
from principal.views import TripViews
from principal.views.Coinviews import buy_coins


client = init_fs()


@permission_required('principal.traveller')
def show_planning(request, trip_id):
    trip = Trip.objects.get(pk=trip_id)
    if Traveller.objects.get(id=request.user.id) != trip.traveller:
        BrainTravelUtils.save_error(request, "This is not your trip")
        return TripViews.planned_trips(request)
    else:
        return render_to_response('show_planning.html', {'trip': trip}, context_instance=RequestContext(request))


@permission_required('principal.traveller')
def foursquare_request(request):
    if request.method == 'GET':
        try:
            categories_initializer()
            # search_by_category("sevilla", "coffee")
            # test_plan()
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('/')

# autor: david
def check_coins(days):
    if days <= 3:
        coins = 20
    elif 3 < days <= 7:
        coins = 40
    else:
        coins = 80
    return coins

def check_coins_available(traveller, coins_spent):
    coins_available = traveller.coins
    if coins_available < coins_spent:
        return False
    else:
        return True

@permission_required('principal.traveller')
def foursquare_list_venues(request):
    try:
        assert request.user.has_perm('principal.traveller')
        traveller = TravellerService.find_one(request.user.id)
        if request.POST:
            form = PlanForm(request.POST)
            if form.is_valid():
                days = int(form.cleaned_data['days'])
                if check_coins_available(traveller, check_coins(days)) is False:
                    BrainTravelUtils.save_error(request, "Insufficient coins available")
                    return buy_coins(request)
                start_date = form.cleaned_data['startDate']
                country = form.cleaned_data['country']
                city = form.cleaned_data['city']

                limit = 40
                if days <= 3:
                    limit = 15
                elif days > 3 and days <= 7:
                    limit = 25

                venues_sigths = FoursquareServices.search_by_section(city, "sights", limit=limit)
                venues_outdoors = FoursquareServices.search_by_section(city, "outdoors", limit=limit)
                venues_arts = FoursquareServices.search_by_section(city, "arts", limit=limit)
                venues_eat = FoursquareServices.search_by_section(city, "food")

                # List of all items
                items_venues = []
                items_food = []

                items_venues += venues_sigths['groups'][0]['items']
                items_venues += venues_outdoors['groups'][0]['items']
                items_venues += venues_arts['groups'][0]['items']

                items_food += venues_eat['groups'][0]['items']

                # Filter and save
                selected_venues = FoursquareServices.filter_and_save(items_venues, days=days)
                selected_food = FoursquareServices.filter_and_save(items_food, days=days, food=True)

                selected_venues_with_photos = FoursquareServices.save_data(selected_venues)
                selected_food_with_photos = FoursquareServices.save_data(selected_food)

                trip = FoursquareServices.create_trip(form, request, selected_venues_with_photos,
                                                      selected_food_with_photos)
                return show_planning(request, trip.id)
            # si no es valido el form devolvemos a editar
            return render_to_response('plan_creation.html', {'form': form, 'traveller': traveller},
                                      context_instance=RequestContext(request))
        else:
            form = PlanForm()
            return render_to_response('plan_creation.html', {'form': form, 'traveller': traveller},
                                      context_instance=RequestContext(request))

    except:
        print traceback.format_exc()
        return render_to_response('error.html', context_instance=RequestContext(request))
