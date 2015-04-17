# -*- coding: iso-8859-1 -*-
import json
import threading
import traceback
import pprint
from math import radians, sin, cos, sqrt, asin
import urllib2
from datetime import datetime
from datetime import timedelta
from django.db.models import Avg
import foursquare

from principal.models import Category, Venue, Trip, Day, VenueDay, CoinHistory
from principal.services import TravellerService


_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"
client = None


def init_fs():
    # Construct the client object
    global client
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret)
    categories_initializer()


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6372.8  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dLon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # retorna en Km
    return R * c


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


def filter_and_save(items, days, food=False):
    # Days contiene la longitud del viaje en dias
    all_venues = []
    id_list = []
    amount_sites = 8
    counter = 0
    if food:
        amount_sites = 3  # En el caso que estemos seleccionando sitios para comer, solo elegimos 3 por dia
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
    print ("Hay " + str((counter + 1)) + " sitios repetidos")
    return all_venues[0:(amount_sites * days)]


# autor david.
# Si tiene el venue hours lo guarda
# def save_hours(venue_time):
# timeframe = venue_time['timeframes']
# for time in timeframe:
# day = time['days']
#
#     pass


def save_data(venues_selected):
    venues_selected_with_photos = []
    for v in venues_selected:
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


# 1º parametro = categorias que ha puntuado el usuario
def planificador(dict_category_weighting, number_days):
    com = Planificador(dict_category_weighting)
    com.ejecute()


class Planificador(threading.Thread):
    def __init__(self, dict_category_weighting):
        # self.lock = threading.Lock()
        threading.Thread.__init__(self)
        self.lista = []
        self.dict_category_weighting = dict_category_weighting

    # def anyadir(self, obj):
    # self.lock.acquire()
    # self.lista.append(obj)
    # self.lock.release()
    # print(self.lista)
    # def obtener(self, ):
    # self.lock.acquire()
    # obj = self.lista.pop()
    # self.lock.release()
    #     print(obj + "asda")
    #     return obj
    def apply_weighting(self, category, weighting):
        # category_bd = Category.objects.filter(name=category)
        all_venue_category = Venue.objects.filter(categories__name=category)

        # todo asegurarse de los valores
        if weighting == "a lot of":
            for categoria in all_venue_category:
                categoria.scorable_ptr.rating *= 1.6

        if weighting == "many of":
            for categoria in all_venue_category:
                categoria.scorable_ptr.rating *= 1.4

        if weighting == "never":
            for categoria in all_venue_category:
                categoria.scorable_ptr.rating *= 0.01

        # finalmente escribimos los resultados
        self.lista.extend(all_venue_category)

    # dict categorias:puntuacion del usuario
    def ejecute(self):
        actual = threading.active_count()
        for categoria in self.dict_category_weighting:
            print(threading.active_count())
            # sacamos la ponderacion de dicha categoria
            weighting = self.dict_category_weighting[categoria]
            th = threading.Thread(target=self.apply_weighting, args=(categoria, weighting,))
            # print(categoria)
            # print(weighting)
            th.start()
            # print("+1")
        #     lo uso para sincronizar los hilos
        while actual != threading.active_count():
            # esperamos a que todos los hilos terminen
            pass
        # Ordenados de mayor a menor rating
        self.lista.sort(cmpRating, reverse=True)
        pprint.pprint(self.lista)

        # for i in self.lista:
        #     print(i.scorable_ptr.name)
        #     print(i.scorable_ptr.rating)


# comparamos venue segun su rating
def cmpRating(venue1, venue2):
    """ Compara dos hoteles por su precio. """
    return cmp(venue1.scorable_ptr.rating, venue2.scorable_ptr.rating)


def test_plan():
    try:
        dict_categories_and_options = {'Castle': "a lot of", 'Stadium': "many of"}
        com = Planificador(dict_categories_and_options)
        com.ejecute()
        # while True:
        # if len(com.lista) != 0:
    except:
        traceback.print_exc()


# autor: david
def create_trip(tripForm, coins_cost, request, selected_venues_with_photos, selected_food_with_photos):
    start_date = tripForm.data['startDate']
    start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
    days = int(tripForm.cleaned_data['days'])
    country = tripForm.cleaned_data['country']
    city = tripForm.cleaned_data['city']
    end_date = start_date + timedelta(days=days)

    trip = Trip(name=str(days) + " days in " + city, publishedDescription="", state='ap',
                startDate=start_date, endDate=end_date, planified=True, coins=coins_cost,
                traveller=TravellerService.find_one(request.user.id),
                city=city, country=country)
    trip.save()

    for num_day in range(1, days + 1):
        # si no es la primera iteracion sumamos "days" a la fecha
        if num_day == 1:
            date = start_date
        else:
            date = start_date + timedelta(days=num_day - 1)

        day = Day(numberDay=num_day, trip=trip, date=date)
        day.save()

        # 24 - 8h (para dormir) - 3h para comer * 60 (lo pasamos a minutos)
        time_spent = 13 * 60
        for numero in range(1, 9):
            venue = selected_venues_with_photos.pop(0)
            leadtime_average = venue.feedback_set.aggregate(Avg('leadTime')).values()[0]
            if leadtime_average is None:
                # 2 horas
                leadtime_average = 120

            time_spent -= leadtime_average
            venue_day = VenueDay(order=numero, day=day, venue=venue)
            venue_day.save()

            # nos ahorramos un for
            if numero < 4:
                venue_day = VenueDay(order=numero, day=day, venue=selected_food_with_photos.pop(0))
                venue_day.save()
                # time_spent -= 1

            # Si el tiempo a gastar es 0 o menor, pasamos a un dia nuevo
            if time_spent <= 0:
                print("Se agoto el tiempo: " + str(time_spent))
                break
            print("tiempo restante: " + str(time_spent))
    return trip


#author: Javi Rodriguez
def retrieve_venues(id_venue):
    venue = Venue.objects.get(id=id_venue)
    return venue


# autor: david
def create_history(trip):
    coin_history = CoinHistory(amount=trip.coins, concept=trip.name, date=datetime.now(),
                               traveller=trip.traveller, trip=trip)
    coin_history.save()


def get_venues_order(centre, list_venues):
    # obtengo la primera qe es la que tiene mayor puntuacion en FS
    lat_centre = centre.latitude
    lng_centre = centre.longitude
    destinations = ""
    for venue in list_venues:
        lat = venue.latitude
        lng = venue.longitude

        # 107 caracteres son fijos y obligatorios
        if len(destinations) < (2024 - 107):
            destinations = destinations + str(lat) + "," + str(lng) + "|"
        else:
            break

    destinations = destinations[:-1]

    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(lat_centre) + "," + str(lng_centre) \
          + "&destinations=" + destinations + "&language=es-ES&sensor=false"
    print(url)
    print(len(url))

    response = urllib2.urlopen(url)
    data = json.load(response)
    list_distancias = []
    count = 0
    for element in data['rows'][0]['elements']:
        # son metros
        # distance = element['distance']['value']
        # son segundos
        # duration = element['duration']['value']
        tupla = (str(list_venues[count].id), element['duration']['value'])
        list_distancias.append(tupla)
        count += 1
    list_distancias.sort(key=lambda x: x[1])

    return list_distancias

















