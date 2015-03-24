# -*- coding: latin-1 -*-

# david
from django.http import HttpResponse, HttpResponseRedirect

from principal.services.FoursquareServices import auth_request, auth_catch


def foursquare_request(request):
    if request.method == 'GET':
        try:
            url_fs_request = auth_request()
            return HttpResponseRedirect(url_fs_request)
        except Exception as e:
            return HttpResponse(e)
    else:
        pass


def foursquare_code(request):
    if request.method == 'GET':
        try:
            auth_code = request.GET.get('code').encode("utf-8")
            auth_catch(auth_code)
        except Exception as e:
            return HttpResponse(e)



