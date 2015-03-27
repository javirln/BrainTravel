# -*- coding: latin-1 -*-

# david
from django.http import HttpResponse
from django.shortcuts import redirect

from principal.services.FoursquareServices import init_fs, search_by_category, test_hilos


client = init_fs()


def foursquare_request(request):
    if request.method == 'GET':
        try:
            # categories_initializer()
            # search_by_category("sevilla", "coffee")
            test_hilos()
        except Exception as e:
            return HttpResponse(e)
    else:
        return redirect('/')