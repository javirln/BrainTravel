import hashlib
import django

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from principal.forms import LoginForm, TravellerRegistrationForm
from principal.services import TravellerService
from principal.utils import BrainTravelUtils
from principal.views import EmailViews
from django.utils.translation import ugettext as _


def sign_in(request):
    try:
        assert not request.user.has_perm('principal.traveller') and not request.user.has_perm('principal.administrator')
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                assert user.is_active
                login(request, user)
                return HttpResponseRedirect('/profile/'+str(user.id))
        else:
            form = LoginForm()
        registerForm = TravellerRegistrationForm()
        return render_to_response('signin.html', {'registerForm': registerForm, 'form': form}, context_instance=RequestContext(request))
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


def system_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def create_traveller(request):
    data = request.POST
    form = TravellerRegistrationForm(data)
    response = {}
    if form.is_valid():
        response['success'] = True
        traveller = TravellerService.create(form)
        rand_password = BrainTravelUtils.id_generator()
        traveller.set_password(rand_password)
        TravellerService.save(traveller)  # Aqui se asignan los permisos
        EmailViews.send_email_confirmation(traveller, rand_password)
    else:
        message = ""
        for field, errors in form.errors.items():
            for error in errors:
                message += error

        # response['errors'] = _(message)
        response['success'] = False
        response['error'] = _(message)
        # HttpResponse(json.dumps(response))

    return JsonResponse(response)


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


def cookies_policies(request):
    if django.utils.translation.get_language() == "es":
        return render_to_response('cookies_policies_es.html', {}, context_instance=RequestContext(request))
    if django.utils.translation.get_language() == "en":
        return render_to_response('cookies_policies_en.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('cookies_policies_en.html', {}, context_instance=RequestContext(request))


def about_us(request):
    if django.utils.translation.get_language() == "es":
        return render_to_response('about_us_es.html', {}, context_instance=RequestContext(request))
    if django.utils.translation.get_language() == "en":
        return render_to_response('about_us_en.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('about_us_en.html', {}, context_instance=RequestContext(request))


def privacy_terms(request):
    if django.utils.translation.get_language() == "es":
        return render_to_response('privacy_terms_es.html', {}, context_instance=RequestContext(request))
    if django.utils.translation.get_language() == "en":
        return render_to_response('privacy_terms_en.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response('privacy_terms_en.html', {}, context_instance=RequestContext(request))
