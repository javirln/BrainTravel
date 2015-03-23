# -*- coding: latin-1 -*-

import foursquare

_client_id = "TWYKUP301GVPHIAHBPYFQQT0PJGZ0O2B24HQ3RUGLUFSLP1E"
_client_secret = "TDNQ441CNLDJZKC3UJYDERT2MNDWN1E2CX1550CW1OXPEST2"


def auth_request():
    # Construct the client object
    client = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret,
                                   redirect_uri='http://127.0.0.1:8000/auth_fs')

    # Build the authorization url for your app
    auth_uri = client.oauth.auth_url()
    print(auth_uri)
    return auth_uri


def auth_catch(auth_code):
    # Construct the client object
    clients = foursquare.Foursquare(client_id=_client_id, client_secret=_client_secret,
                                    redirect_uri='http://127.0.0.1:8000/auth_fs')

    # Interrogate foursquare's servers to get the user's access_token
    access_token = clients.oauth.get_token(auth_code)

    # Apply the returned access token to the client
    clients.set_access_token(access_token)

    # Get the user's data
    # user = client.users()
    print(access_token)
    client = foursquare.Foursquare(access_token=access_token, version='20111215')
    print(client)
    respuesta = client.Tips('4b5e662a70c603bba7d790b4')
    print(respuesta)



