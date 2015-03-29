# -*- coding: latin-1 -*-

# david
import pprint

from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext

from principal.services import FoursquareServices
from principal.services.FoursquareServices import init_fs, categories_initializer, search_by_category


client = init_fs()


def foursquare_request(request):
    if request.method == 'GET':
        try:
            # categories_initializer()
            search_by_category("sevilla", "coffee")
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('/')
    
    
def foursquare_list_venues(request):
    days = int(request.GET['days'])
    city = request.GET['city']
    limit = 40
    if days <= 3:
        limit = 10
    elif days > 3 and days <= 7:
        limit = 20
    
    
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
    
    
    #Descomentar vista de prueba para ver los resultados
    return [selected_food_with_photos, selected_food_with_photos]
    #return render_to_response('show_planning.html', {'venues': selected_venues_with_photos, 'food': selected_food_with_photos},
     #                         context_instance=RequestContext(request))
    
