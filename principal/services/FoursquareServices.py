# -*- coding: iso-8859-1 -*-
from datetime import datetime
import json
from math import radians, sin, cos, sqrt, asin
import pprint
import traceback
import urllib2
from django.utils.translation import ugettext as _
from django.db.models import Avg
from django.db.models.query_utils import Q
import foursquare

from BrainTravel import constants
from principal.models import Category, Venue, Trip, Day, VenueDay, CoinHistory, \
    Feedback
from principal.services import TravellerService


_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"
client = None


def init_fs():
    # Construct the client object
    global client
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret)
    categories_initializer()


def categories_initializer():
    """This functions belongs to populate_db but since there is no instance
     of Foursquare there, this function will be used."""
    categories = client.venues.categories()
    Category.objects.all().delete()
    for row in categories['categories']:
        cat = Category(
            id_foursquare=row['id'],
            name=row['pluralName']
        )
        cat.save()
        for child in row['categories']:
            cat1 = Category(
                id_foursquare=child['id'],
                name=child['pluralName']
            )
            cat1.save()
            for grand_child in child['categories']:
                cat2 = Category(
                    id_foursquare=grand_child['id'],
                    name=grand_child['pluralName']
                )
                cat2.save()


# devuelve: un dict,con una lista llamada groups, que contiene un dict, qe contiene lista llamada items ordenada x rating
def search_by_category(city, category):
    # A term to be searched against a venue's tips, category, etc.
    response = client.venues.explore(params={'near': city, 'query': category})
    print(response)


# devuelve lista ordenada por rating (hay que asegurarse mas)
def search_by_section(city, section, limit=40):
    # section = One of food, drinks, coffee, shops, arts, outdoors, sights, trending or specials, nextVenues
    # (venues frequently visited after a given venue)
    # or topPicks (a mix of recommendations generated without a query from the user).
    response = client.venues.explore(params={'near': city, 'section': section, 'limit': limit})
    # pp = pprint.PrettyPrinter()
    # pp.pprint(response)
    return response


def get_categories(fs_categories):
    res = []
    for category in fs_categories:
        res.append(Category.objects.get(id_foursquare=category['id']))
    return res


def filter_and_save(items, food=False):
    # Days contiene la longitud del viaje en dias
    all_venues = []
    id_list = []
    counter = 0
    for item in items:
        venue = item['venue']
        id = venue['id']
        if id not in id_list:
            id_list.append(id)
            if not Venue.objects.filter(id_foursquare=id).exists():
                categories = get_categories(venue['categories'])
                venue = Venue(name=venue['name'],
                              id_foursquare=id,
                              latitude=venue['location']['lat'],
                              longitude=venue['location']['lng'],
                              is_food=food)
                venue.save()
                venue.categories.add(*categories)
                all_venues.append(venue)
            else:
                venue = Venue.objects.get(id_foursquare=id)
                all_venues.append(venue)
        else:
            # print("ID repetido: " + id)
            # print("Venue repetido: " + venue['name'])
            counter = counter + 1
    # Devolvemos 8 viajes por dias
    return all_venues


# autor david.
# Si tiene el venue hours lo guarda
# def save_hours(venue_time):
# timeframe = venue_time['timeframes']
# for time in timeframe:
# day = time['days']
#
# pass


def save_data(venues_selected):
    venues_selected_with_photos = []
    print "Venues para guardar " + str(len(venues_selected))
    for v in venues_selected:
        if v.photo is not None and v.photo is not "":
            venues_selected_with_photos.append(v)
        else:
            venue = client.venues(v.id_foursquare)
            photo = ""
            # if 'hours' in venue['venue']:
            #     save_hours(venue['venue']['hours'])
            # elif 'popular' in venue['venue'] and not 'hours' in venue['venue']:
            #     save_hours(venue['venue']['popular'])

            if len(venue['venue']['photos']['groups']) != 0:
                photo = venue['venue']['photos']['groups'][0]['items'][0]
                photo_url = photo['prefix'] + str(photo['width']) + "x" + str(photo['height']) + photo['suffix']
                v.photo = photo_url
            v.save()
            venues_selected_with_photos.append(v)
    return venues_selected_with_photos


# autor: david
def create_trip(tripForm, coins_cost, request, selected_venues_with_photos, indexes_venues, selected_food_with_photos,
                all_venues, all_food):
    days = int(tripForm.cleaned_data['days'])
    country = tripForm.cleaned_data['country']
    city = tripForm.cleaned_data['city']

    trip = Trip(name=str(days) + " days in " + city, publishedDescription="", state='ap',
                planified=True, coins=coins_cost,
                traveller=TravellerService.find_one(request.user.id),
                city=city, country=country)
    trip.save()

    trip.possible_venues.add(*(set(all_venues) - set(selected_venues_with_photos)))
    trip.possible_venues.add(*(set(all_food) - set(selected_food_with_photos)))

    for num_day in range(1, days + 1):
        day = Day(numberDay=num_day, trip=trip)
        day.save()

        day_venues = []
        if num_day == 1:
            day_venues = selected_venues_with_photos[0: indexes_venues[num_day - 1]]
        elif num_day == len(indexes_venues) + 1:
            day_venues = selected_venues_with_photos[indexes_venues[num_day - 2]:]
        else:
            day_venues = selected_venues_with_photos[indexes_venues[num_day - 2]: indexes_venues[num_day - 1]]

        # enumerate devuelve el elemento sobre el que se esta iterando y el indice que ocupa
        for idx, venue in enumerate(day_venues):
            # venue = selected_venues_with_photos.pop(0)
            # leadtime_average = venue.feedback_set.aggregate(Avg('leadTime')).values()[0]
            # if leadtime_average is None:
            # 2 horas
            # leadtime_average = 120

            # time_spent -= leadtime_average
            venue_day = VenueDay(order=idx, day=day, venue=venue)
            venue_day.save()

            # nos ahorramos un for
            if idx < 3:
                venue_day = VenueDay(order=idx, day=day, venue=selected_food_with_photos.pop(0))
                venue_day.save()

                # Si el tiempo a gastar es 0 o menor, pasamos a un dia nuevo
                # if time_spent <= 0:
                # print("Se agoto el tiempo: " + str(time_spent))
                # break
                # print("tiempo restante: " + str(time_spent))
    return trip


# author: Javi Rodriguez
def retrieve_venues(id_venue):
    venue = Venue.objects.get(id=id_venue)
    return venue


# autor: david
def create_history(trip):
    coin_history = CoinHistory(amount=trip.coins, concept=trip.name, date=datetime.now(),
                               traveller=trip.traveller, trip=trip)
    coin_history.save()


def calculate_distance(lat1, lon1, list_venue):
    list_distances = []
    for venue in list_venue:
        lat2 = venue['venue']['location']['lat']
        lon2 = venue['venue']['location']['lng']
        dLat = (lat2 - lat1) ** 2
        dLon = (lon2 - lon1) ** 2

        c = sqrt(dLat + dLon) * 1000
        list_distances.append(c)
    return list_distances


# Autor: david
def get_venues_order(list_constrains, lat_centre, lng_centre, list_venues):
    # obtengo la primera qe es la que tiene mayor puntuacion en FS
    destinations = ""
    map_const = {}
    is_google = True
    for const in list_constrains:
        if len(const) != 0:
            split = const.split(":")
            cat = Category.objects.filter(id_foursquare=split[0]).first()
            id_category_fs = cat.id_foursquare
            if split[1] == "Mucho":
                split[1] = constants.NUMBER_A_LOT_OF
            elif split[1] == "Poco":
                split[1] = constants.NUMBER_SOME_OF
            elif split[1] == "Nada":
                split[1] = constants.NUMBER_ANYTHING_OF
            else:
                raise ValueError(_('Input value incorrect'))
            map_const[id_category_fs] = split[1]

    for venue in list_venues:
        lat = venue['venue']['location']['lat']
        lng = venue['venue']['location']['lng']

        # 107 caracteres son fijos y obligatorios
        if len(destinations) < (2024 - 107):
            destinations = destinations + str(lat) + "," + str(lng) + "|"
        else:
            break

    destinations = destinations[:-1]

    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(lat_centre) + "," + str(lng_centre) \
          + "&destinations=" + destinations + "&language=es-ES&sensor=false"

    print (url)
    response = urllib2.urlopen(url)
    data = json.load(response)
    list_durations = []
    count = 0
    if data['status'] == "OVER_QUERY_LIMIT":
        elements = calculate_distance(lat_centre, lng_centre, list_venues)
        print("Elementos distancia mi metodo privado " + str(len(elements)))
        is_google = False
    else:
        elements = data['rows'][0]['elements']
    print ("Usamos google? " + str(is_google))

    for element in elements:
        if is_google:
            if element['status'] != "OK":
                print("El estado del elemento es: " + str(element['status']))
                print "No se puede trazar un camino entre el origen y el destino. Pasamos de la mierda de destino este"
                continue
        # son metros
        # distance = element['distance']['value']
        # son segundos
        # duration = element['duration']['value']
        venue_actual = list_venues[count]
        if is_google:
            try:
                tiempo = element['duration']['value']
            except Exception as e:
                pprint.pprint(element)
                raise e
        else:
            tiempo = element

        tupla = ()
        # recorremos el mapa y vemos si coincide el id_FS de la vista con el del algoritmo
        for rest in map_const:
            if rest in venue_actual['venue']['categories'][0]['id']:
                # Aqui entra si coincide el id_FS con el id_categoria_venue

                # Este IF ES PARA  los venues que estan muy cercas pero no quieres ver.
                # si esta a menos 1min, la distancia es 0 y eso al multiplicar sigue siendo 0
                if map_const[rest] == constants.NUMBER_ANYTHING_OF:
                    tiempo = int(tiempo) + map_const[rest]
                else:
                    tiempo = int(tiempo) * map_const[rest]

        tupla = (venue_actual, tiempo)
        list_durations.append(tupla)
        count += 1
    list_durations.sort(key=lambda x: x[1])
    print "Venues ordenados con longitud: " + str(len(list_durations))
    return list_durations


def get_plan(list_constrains, fs_venues, num_days):
    origin = fs_venues[0]
    venues_ordered = get_venues_order(list_constrains, origin['venue']['location']['lat'],
                                      origin['venue']['location']['lng'],
                                      fs_venues)
    total_threshold = constants.DAY_THRESHOLD * num_days
    acum_time = 0  # Tiempo acumulado en cada iteración en segundos
    acum_time_per_day = 0
    index_days = []
    selected_venues = []

    selected_venues_ids = []  # Para controlar que no haya sitios repetidos
    i = 0
    for venue in venues_ordered:

        venue_fs_id = venue[0]['venue']['id']
        if venue_fs_id in selected_venues_ids:
            continue

        i += 1

        selected_venues.append(venue[0])
        selected_venues_ids.append(venue_fs_id)

        average_duration = constants.AVERAGE_TIME_PER_VENUE
        average_lead_time = constants.AVERAGE_LEAD_TIME

        time_travel = constants.AVERAGE_LEAD_TIME
        if venue[1] > time_travel:
            time_travel = venue[1]

        if Feedback.objects.filter(Q(venues__id_foursquare=venue_fs_id) & ~Q(leadTime=0)):
            average_lead_time = \
                Feedback.objects.filter(Q(venues__id_foursquare=venue_fs_id) & ~Q(leadTime=0)).aggregate(
                    Avg('leadTime')).values()[0]

        if Feedback.objects.filter(Q(venues__id_foursquare=venue_fs_id) & ~Q(duration=0)):
            average_duration = Feedback.objects.filter(Q(venues__id_foursquare=venue_fs_id) & ~Q(duration=0)).aggregate(
                Avg('duration')).values()[0]

        acum_time += time_travel + average_duration + average_lead_time
        acum_time_per_day += time_travel + average_duration + average_lead_time

        if acum_time_per_day >= constants.DAY_THRESHOLD:
            index_days.append(i)
            acum_time_per_day = 0
        if acum_time >= total_threshold:
            return (selected_venues, index_days)

    return (selected_venues, index_days)


def get_plan_food(list_constrains, fs_venues_food, num_days, origin):
    print("get_plan_food longitud venues NO ordenados " + str(len(fs_venues_food)))
    print("get_plan_food se necesitan estos sitios de comida " + str((num_days * 5) - 1))
    venues_ordered = get_venues_order(list_constrains, origin['venue']['location']['lat'],
                                      origin['venue']['location']['lng'],
                                      fs_venues_food)

    print("get_plan_food longitud venues ordenados " + str(len(venues_ordered)))

    selected_venues = []
    for idx, venue in enumerate(venues_ordered):
        selected_venues.append(venue[0])

        if idx >= ((num_days * 5) -1):
            break

    return selected_venues

