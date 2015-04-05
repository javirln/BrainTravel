# -*- coding: latin-1 -*-

# david
import pprint
from datetime import date, datetime
import traceback

from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from principal.forms import PlanForm
from principal.models import Trip
from principal.services import TravellerService
from principal.services import FoursquareServices
from principal.services.FoursquareServices import init_fs, categories_initializer, search_by_category
from principal.services.FoursquareServices import init_fs, test_plan


client = init_fs()


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


def foursquare_list_venues(request):
    try:
        assert request.user.has_perm('principal.traveller')
        traveller = TravellerService.find_one(request.user.id)
        if request.POST:
            form = PlanForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['startDate']
                days = int(form.cleaned_data['days'])
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

                selected_venues_with_photos = FoursquareServices.save_photo(selected_venues)
                selected_food_with_photos = FoursquareServices.save_photo(selected_food)


                # Descomentar vista de prueba para ver los resultados
                # return [selected_food_with_photos, selected_food_with_photos]
                trip = FoursquareServices.create_trip(form, request, selected_venues_with_photos, selected_food_with_photos)
                return render_to_response('show_planning.html',
                                          {'venues': selected_venues_with_photos, 'food': selected_food_with_photos},
                                          context_instance=RequestContext(request))
            # si no es valido el form devolvemos a editar
            return render_to_response('plan_creation.html', {'form': form, 'traveller':traveller}, context_instance=RequestContext(request))
        else:
            form = PlanForm()
            return render_to_response('plan_creation.html', {'form': form, 'traveller':traveller}, context_instance=RequestContext(request))
    except:
        print traceback.format_exc()
        return render_to_response('error.html', context_instance=RequestContext(request))