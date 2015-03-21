# -*- coding: latin-1 -*-
"""Aquí se colocan las vistas relacionadas con el Modelo 1"""
'''@author dcjosej'''

import hashlib
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse, \
    HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django.template.context import RequestContext

from principal.forms import LoginForm, TravellerRegistrationForm
from principal.services import TravellerService, UserService
from principal.views import EmailViews
from principal.utils import BrainTravelUtils


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
                    result = render_to_response('signin.html', {'message': message, 'registerForm': registerForm},
                                                context_instance=RequestContext(request))
            else:
                message = 'Wrong user or password'
                result = render_to_response('signin.html', {'message': message, 'registerForm': registerForm},
                                            context_instance=RequestContext(request))

        else:
            result = render_to_response('signin.html', {'form': form, 'registerForm': registerForm},
                                        context_instance=RequestContext(request))
    else:
        next = request.GET.get('next', '/')
        result = render_to_response('signin.html', {'next': next, 'registerForm': registerForm},
                                    context_instance=RequestContext(request))

    return result


@login_required()
def system_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def create_traveller(request):
    data = request.POST
    form = TravellerRegistrationForm(data)
    response = {'success': form.is_valid()}

    if form.is_valid():
        traveller = TravellerService.create(form)
        rand_password = BrainTravelUtils.id_generator()
        traveller.set_password(rand_password)
        traveller.save()

        EmailViews.send_email_confirmation(traveller, rand_password)
    # traveller = TravellerService.create(form)
    # TravellerService.save(traveller)

    return HttpResponse(json.dumps(response))


def confirm_account(request):
    username = request.GET['username']
    hash1 = hashlib.sha256(username).hexdigest()
    hash2 = request.GET['hash']
    if hash1 == hash2:
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        password = request.GET['rand_password']
        user_logged = authenticate(username=user.username, password=password)
        login(request, user_logged)
        return HttpResponseRedirect("/")
    else:
        return HttpResponse("Hash not math!! :(")
