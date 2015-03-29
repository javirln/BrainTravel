# -*- coding: latin-1 -*-

import pprint

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
def search_by_section(city, section, limit=40):
    # section = One of food, drinks, coffee, shops, arts, outdoors, sights, trending or specials, nextVenues
    # (venues frequently visited after a given venue)
    # or topPicks (a mix of recommendations generated without a query from the user).
    response = client.venues.explore(params={'near': city, 'section': section, 'limit':limit})
    #pp = pprint.PrettyPrinter()
    #pp.pprint(response)
    return response



def get_categories(fs_categories):
    res = []
    for category in fs_categories:
        res.append(Category.objects.get(id_foursquare=category['id']))
    return res


def filter_and_save(items, days, food=False):
    #Days contiene la longitud del viaje en dias
    all_venues = []
    id_list = []
    amount_sites = 8
    counter = 0
    if food:
        amount_sites = 3 #En el caso que estemos seleccionando sitios para comer, solo elegimos 3 por dia
    for item in items:
        venue = item['venue'] 
        id = venue['id']
        if id not in id_list:
            id_list.append(id)
            if not Venue.objects.filter(id_foursquare = id).exists():
                categories = get_categories(venue['categories'])
                venue = Venue(name=venue['name'], 
                              id_foursquare=id, 
                              latitude=venue['location']['lat'], 
                              longitude=venue['location']['lng'])
                venue.save()
                venue.categories.add(*categories)
                all_venues.append(venue)
            else:
                venue = Venue.objects.get(id_foursquare=id)
                all_venues.append(venue)
            
    #Devolvemos 8 viajes por dias
    return all_venues[0:(amount_sites*days)]

def save_photo(venues_selected):
    venues_selected_with_photos = []
    for v in venues_selected:
        venue= client.venues(v.id_foursquare)
        photo = venue['venue']['photos']['groups'][0]['items'][0]
        photo_url = photo['prefix'] + str(photo['width']) + "x" + str(photo['height']) +photo['suffix']
        v.photo = photo_url
        v.save()
        venues_selected_with_photos.append(v)
    return venues_selected_with_photos
            
        
    
    
    
    
    

