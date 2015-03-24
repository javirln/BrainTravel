# -*- coding: latin-1 -*-

import foursquare
from principal.models import Category

_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"
client = None


def auth_request():
    # Construct the client object
    global client
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret,
                                   redirect_uri='http://127.0.0.1:8000/auth_fs')

    # Build the authorization url for your app
    auth_uri = client.oauth.auth_url()
    print(auth_uri)
    return auth_uri


def auth_catch(auth_code):
    global client
    # Construct the client object
    clients = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret,
                                    redirect_uri='http://127.0.0.1:8000/auth_fs', lang='en')

    # Interrogate foursquare's servers to get the user's access_token
    access_token = clients.oauth.get_token(auth_code)

    # Apply the returned access token to the client
    clients.set_access_token(access_token)

    # Get the user's data
    # user = client.users()
    print(access_token)
    client = foursquare.Foursquare(access_token=access_token, version='20120609', lang='en')
    print(client)
    respuesta = client.Tips('4b5e662a70c603bba7d790b4')
    print(respuesta)
    #categories_initializer()


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