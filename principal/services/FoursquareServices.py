# -*- coding: latin-1 -*-
import pprint
import threading
import traceback

import pprint
import datetime

import foursquare

from principal.models import Category, Venue, Trip, Day, VenueDay
from principal.services import TravellerService
from django.db.models.fields import Empty


_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"
client = None


def init_fs():
    # Construct the client object
    global client
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret)


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
            counter =counter + 1
    # Devolvemos 8 viajes por dias
    print ("Hay " + str((counter+1)) + " sitios repetidos")
    return all_venues[0:(amount_sites * days)]


def save_photo(venues_selected):
    venues_selected_with_photos = []
    for v in venues_selected:
        venue = client.venues(v.id_foursquare)
        photo = ""
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
    #     obj = self.lista.pop()
    #     self.lock.release()
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


def create_trip(tripForm, request, selected_venues_with_photos, selected_food_with_photos):
    start_date = tripForm.cleaned_data['startDate']
    days = int(tripForm.cleaned_data['days'])
    country = tripForm.cleaned_data['country']
    city = tripForm.cleaned_data['city']
    end_date = start_date + datetime.timedelta(days=days)

    trip = Trip(name=str(days) + " days in " + city, publishedDescription="", state='ap',
                startDate=start_date, endDate=end_date, planified=True, coins=0,
                traveller=TravellerService.find_one(request.user.id),
                city=city, country=country)



    # ------------- Relationships --------------#
    trip.save()
    for num_day in range(1, days + 1):
        # si no es la primera iteracion sumamos "days" a la fecha
        if num_day == 1:
            date=start_date
        else:
            date = start_date + datetime.timedelta(days=num_day-1)

        day = Day(numberDay=num_day, trip=trip, date=date)
        day.save()
        for numero in range(1, 9):
            venue_day = VenueDay(order=numero, day=day, venue=selected_venues_with_photos.pop(0))
            venue_day.save()

        for numero_comida in range(1, 4):
            venue_day = VenueDay(order=numero_comida, day=day, venue=selected_food_with_photos.pop(0))
            venue_day.save()

    return trip