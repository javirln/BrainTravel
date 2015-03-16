# -*- coding: latin-1 -*-
"""Aquí se colocan las vistas relacionadas con el Modelo 1"""
'''@author dcjosej'''

import json

from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render_to_response, render
from django.template.context import RequestContext
from django.views.generic.edit import CreateView

from principal.forms import LoginForm
from principal.models import Traveller
from principal.services import TravellerService


def sign_in(request):
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
					result = render(request, 'signin.html', {'message': message})
			else:
				message = 'Wrong user or password' 
				result = render(request, 'signin.html', {'message': message})

		else:
			result = render(request, 'signin.html', {'form': form})
	else:
		next = request.GET.get('next', '/')
		result = render(request, 'signin.html', {'next': next})
	
	return result
	
	

def create_traveller(request):
	data = json.loads(request.body)
	return HttpResponse(data)
	
	
	
'''def register_traveller(request):
	res = None
	if request.method == "POST":
		form = TravellerRegistrationForm(request.POST)
		if form.is_valid():
			try:
				traveller = TravellerService.create()
				TravellerService.save(traveller)
			except Exception as e:
				return HttpResponse("ESO NO SE PUEDE! POR DIOS!")'''
