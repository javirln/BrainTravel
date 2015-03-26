# -*- coding: latin-1 -*-

# david
from django.http import HttpResponse
from django.shortcuts import redirect

from principal.services.FoursquareServices import init_fs, categories_initializer


client = init_fs()


def foursquare_request(request):
    if request.method == 'GET':
        try:
            categories_initializer()
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('/')