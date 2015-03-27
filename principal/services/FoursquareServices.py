# -*- coding: latin-1 -*-
import threading

import foursquare

from principal.models import Category, Venue


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
def search_by_section(city, section):
    # section = One of food, drinks, coffee, shops, arts, outdoors, sights, trending or specials, nextVenues
    # (venues frequently visited after a given venue)
    # or topPicks (a mix of recommendations generated without a query from the user).
    response = client.venues.explore(params={'near': city, 'section': section})
    print(response)


def apply_weighting(category, weighting):
    # devolvera los sitios que tienen esa categoria aplicandole previamente el peso al rating de los sitios
    pass


# 1º parametro = categorias que ha puntuado el usuario
def planificador(dict_category_weighting, number_days, another_category=""):
    list_categories_and_options = []
    for categoria in dict_category_weighting:
        # sacamos la ponderacion de dicha categoria
        weighting = dict_category_weighting[categoria]
        print(weighting)
        list_categories_and_options.append(apply_weighting(categoria, weighting))

    com = Planificador()
    com.run_all(list_categories_and_options)


class Planificador():
    def __init__(self):
        self.lock = threading.Lock()
        self.lista = []

    @staticmethod
    def worker(count):
        # sleep(random() * 5)
        print "Este es el %s trabajo que hago hoy para Genbeta Dev" % count

    def anyadir(self, obj):
        self.lock.acquire()
        self.lista.append(obj)
        self.lock.release()
        print(self.lista)

    def apply_weighting(self, category, weighting):
        category_fs = Category.objects.filter(name=category)
        all_venue_category = Venue.objects.filter(id_foursquare=category_fs.id_foursquare)
        # todo asegurarse de los valores
        if weighting == "a lot of":
            for categoria in all_venue_category:
                categoria.scorable.rating *= 1.6

        if weighting == "many of":
            for categoria in all_venue_category:
                categoria.scorable.rating *= 1.4

        if weighting == "never":
            for categoria in all_venue_category:
                categoria.scorable.rating *= 0.01


    # 1º parametro = dict categorias:puntuacion del usuario
    def ejecute(self, dict_category_weighting):
        list_categories_and_options = []
        for categoria in dict_category_weighting:
            # sacamos la ponderacion de dicha categoria
            weighting = dict_category_weighting[categoria]
            print(weighting)
            list_categories_and_options.append(apply_weighting(categoria, weighting))

    def obtener(self, ):
        self.lock.acquire()
        obj = self.lista.pop()
        self.lock.release()
        print(obj + "asda")
        return obj

    def run_all(self, list_categories):
        th1 = threading.Thread(target=self.anyadir, args=("1",))
        th2 = threading.Thread(target=self.anyadir, args=("2",))
        th3 = threading.Thread(target=self.obtener)
        th1.start()
        th2.start()
        th3.start()
        # for i in range(3):
        # t = threading.Thread(target=worker, args=(i,))
        # threads.append(t)
        # t.start()


def test_hilos():
    list_categories_and_options = []
    com = Planificador()
    com.run_all(list_categories_and_options)














