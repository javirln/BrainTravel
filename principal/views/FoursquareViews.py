# -*- coding: latin-1 -*-

# david
from django.http import HttpResponse
from django.shortcuts import redirect

from principal.services.FoursquareServices import init_fs, categories_initializer, search_by_category


client = init_fs()


def foursquare_request(request):
    if request.method == 'GET':
        try:
            # categories_initializer()
            search_by_category("sevilla", "coffee")
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('/')