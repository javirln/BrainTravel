# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from principal.forms import PlanForm
from principal.models import Trip, Feedback, Category
from principal.services import FoursquareServices, TravellerService, CoinService,\
    VenueService
from principal.services.FoursquareServices import categories_initializer, init_fs
from principal.utils import BrainTravelUtils
from principal.views.Coinviews import buy_coins


client = init_fs()


@permission_required('principal.traveller')
def show_planning(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)
        assert trip.traveller.id == request.user.id
        return render_to_response('show_planning.html', {'trip': trip}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('principal.traveller')
def foursquare_request(request):
    try:
        if request.method == 'GET':
                categories_initializer()
        else:
            return redirect('/')
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


@permission_required('principal.traveller')
def foursquare_list_venues(request):
    try:
        assert request.user.has_perm('principal.traveller')
        traveller = TravellerService.find_one(request.user.id)
        list_cat = Category.objects.all()
        # categories = Category.objects.raw('SELECT * FROM category')
        if request.POST:
            form = PlanForm(request.POST)
            list_constrains = request.POST.getlist('rests')

            if form.is_valid():
                days = int(form.cleaned_data['days'])
                coins_cost = CoinService.check_coins(days)
                if CoinService.check_coins_available(traveller, coins_cost) is False:
                    BrainTravelUtils.save_error(request, _("Insufficient coins available"))
                    return buy_coins(request)
                city = form.cleaned_data['city']

                limit = 0
                if days <= 3:
                    limit = 20
                elif 3 < days <= 7:
                    limit = 40

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

                all_venues = FoursquareServices.filter_and_save(items_venues)
                all_food = FoursquareServices.filter_and_save(items_food, food=True)
                
                all_venues = FoursquareServices.save_data(all_venues)
                all_food = FoursquareServices.save_data(all_food)

                # Llamada al nuevo algoritmo
                plan_venues = FoursquareServices.get_plan(list_constrains, items_venues, days)
                plan_food = FoursquareServices.get_plan_food(list_constrains, items_food, days, items_venues[0])
                # Filter and save
                selected_venues = FoursquareServices.filter_and_save(plan_venues[0])
                selected_food = FoursquareServices.filter_and_save(plan_food, food=True)
                
                trip = FoursquareServices.create_trip(form, coins_cost, request, selected_venues, plan_venues[1],
                                                      selected_food, all_venues, all_food)

                traveller.coins -= coins_cost
                traveller.save()
                FoursquareServices.create_history(trip)

                return redirect("/show_planning/" + str(trip.id) + "/")
            # si no es valido el form devolvemos a editar
            return render_to_response('plan_creation.html', {'form': form, 'traveller': traveller, 'list_cat': list_cat}, context_instance=RequestContext(request))
        else:
            form = PlanForm()
            return render_to_response('plan_creation.html', {'form': form, 'traveller': traveller, 'list_cat': list_cat}, context_instance=RequestContext(request))

    except:
        # print traceback.format_exc()
        return render_to_response('error_planning.html', context_instance=RequestContext(request))


def retrieve_venue(request, id_venue):
    if request.method == 'GET':
        try:
            venue = FoursquareServices.retrieve_venues(id_venue)
            trips = Feedback.objects.filter(Q(venues=id_venue)).order_by("usefulCount")
            is_visited = VenueService.is_visited_by_user(request, venue.id) 
            paginator = Paginator(trips, 10)
            page = request.GET.get('page')
            try:
                trips = paginator.page(page)
            except PageNotAnInteger:
                trips = paginator.page(1)
            except EmptyPage:
                trips = paginator.page(paginator.num_pages)

            return render_to_response('venue_details.html', {"venue": venue, "trips": trips, "is_visited":is_visited}, context_instance=RequestContext(request))

        except:
            return render_to_response('error.html', context_instance=RequestContext(request))