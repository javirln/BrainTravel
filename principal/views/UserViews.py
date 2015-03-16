# -*- coding: latin-1 -*-
"""Aquí se colocan las vistas relacionadas con el Modelo 1"""
'''@author dcjosej'''

import json

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render_to_response, render
from django.template.context import RequestContext
from django.views.generic.edit import CreateView
from django_ajax.decorators import ajax

from principal.forms import LoginForm, TravellerRegistrationForm
from principal.models import Traveller
from principal.services import TravellerService


def sign_in(request):
	registerForm = TravellerRegistrationForm()
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect("/")
				else:
					message = 'Your account is desactivated' 
					result = render_to_response('signin.html', {'message': message, 'registerForm': registerForm}, context_instance=RequestContext(request))
			else:
				message = 'Wrong user or password' 
				result = render_to_response('signin.html', {'message': message, 'registerForm': registerForm}, context_instance=RequestContext(request))

		else:
			result = render_to_response('signin.html', {'form': form, 'registerForm': registerForm}, context_instance=RequestContext(request))
	else:
		next = request.GET.get('next', '/')
		result = render_to_response('signin.html', {'next': next, 'registerForm': registerForm}, context_instance=RequestContext(request))
	
	return result
	
	
def create_traveller(request):
	data = request.POST
	form = TravellerRegistrationForm(data)
	response = {'success' : form.is_valid()}
	
	if form.is_valid():
		traveller = TravellerService.create(form)
		TravellerService.save(traveller)
	
	return HttpResponse(json.dumps(response))
	
	
