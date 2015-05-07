# -*- coding: iso-8859-1 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext

"""Aquí se colocan las vistas relacionadas con el Modelo 1"""

def metodo1(request):
	return render_to_response('signin.html', {}, context_instance=RequestContext(request))
