from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template.context import RequestContext

from principal.services import TravellerService
from principal.models import Traveller
from principal.forms import TravellerEditProfileForm, TravellerEditPasswordForm


# author: Juane
@login_required()
def profile_details(request, traveller_id):
    traveller = TravellerService.find_one(traveller_id)
    return render_to_response('profile_details.html', {'traveller': traveller}, context_instance=RequestContext(request))


# author: Juane
@login_required()
def profile_edit(request):
    if request.user.is_authenticated():
        if request.POST:
            form = TravellerEditProfileForm(request.POST, request.FILES)
            if form.is_valid():
                traveller = Traveller.objects.get(id=form.cleaned_data['id'])
                traveller.first_name = form.cleaned_data['first_name']
                traveller.last_name = form.cleaned_data['last_name']
                traveller.genre = form.cleaned_data['genre']
                traveller.photo = form.cleaned_data['photo']
                TravellerService.save(traveller)
                return HttpResponseRedirect('/profile/'+traveller.id)
        else:
            traveller = Traveller.objects.get(id=request.user.id)
            data = {'first_name': traveller.first_name, 'last_name': traveller.last_name, 'genre': traveller.genre,
                    'id': traveller.id, 'photo': traveller.photo}
            form = TravellerEditProfileForm(initial=data)
        return render_to_response('profile_edit.html', {"form": form}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))


# author: Juane
@login_required()
def profile_edit_password(request):
    if request.user.is_authenticated():
        if request.POST:
            form = TravellerEditPasswordForm(request.POST)
            if form.is_valid():
                traveller = Traveller.objects.get(id=form.cleaned_data['id'])
                traveller.set_password(form.cleaned_data['password'])
                TravellerService.save(traveller)
                return HttpResponseRedirect('/profile/'+traveller.id)
        else:
            traveller = Traveller.objects.get(id=request.user.id)
            data = {'id': traveller.id}
            form = TravellerEditPasswordForm(initial=data)
        return render_to_response('profile_edit_password.html', {"form": form}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', context_instance=RequestContext(request))
