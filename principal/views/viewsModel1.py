# -*- coding: iso-8859-1 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext

"""Aquí se colocan las vistas relacionadas con el Modelo 1"""

def metodo1(request):
	print "hola"
	return render_to_response('signin.html', {}, context_instance=RequestContext(request))
