# -*- coding: latin-1 -*-

import foursquare

# import oauth
# credentials = foursquare.OAuthCredentials(consumer_key, consumer_secret)
# fs = foursquare.Foursquare(credentials)
# user_token = oauth.OAuthToken(user_key, user_secret)
# credentials.set_access_token(user_token)
# print fs.user()
from foursquare.tests import BaseAuthenticatedEndpointTestCase

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


class test_fs():
    def auth_catch(self, auth_code):
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


class MultiEndpointTestCase(BaseAuthenticatedEndpointTestCase):
    """
    General
    """

    def test_multi(self):
        """Load up a bunch of multi sub-requests and make sure they process as expected"""
        self.api.users(multi=True)
        self.api.users.leaderboard(params={'neighbors': 5}, multi=True)
        # Throw a non-multi in the middle to make sure we don't create conflicts
        user_response = self.api.users()
        assert 'user' in user_response
        # Resume loading the multi sub-requests
        self.api.users.badges(multi=True)
        # Throw a call with multiple params in the middle to make sure it gets encoded correctly
        # and won't affect the other api calls that share the same http request
        self.api.pages.venues('1070527', params={'limit': 10, 'offset': 10}, multi=True)
        self.api.users.lists(params={'group': u'friends'}, multi=True)
        self.api.venues.categories(multi=True)
        self.api.checkins.recent(params={'limit': 10}, multi=True)
        self.api.tips(self.default_tipid, multi=True)
        self.api.lists(self.default_listid, multi=True)
        self.api.photos(self.default_photoid, multi=True)
        # We are expecting certain responses...
        expected_responses = (
            'user', 'leaderboard', 'badges', 'venues', 'lists', 'categories', 'recent', 'tip', 'list', 'photo',)
        # Make sure our utility functions are working
        assert len(self.api.multi) == len(expected_responses), u'{0} requests queued. Expecting {1}'.format(
            len(self.api.multi),
            len(expected_responses)
        )
        assert self.api.multi.num_required_api_calls == 2, u'{0} required API calls. Expecting 2'.format(
            self.api.multi.num_required_api_calls
        )
        # Now make sure the multi call comes back with what we want
        for response, expected_response in zip(self.api.multi(), expected_responses):
            assert expected_response in response, '{0} not in response'.format(expected_response)


