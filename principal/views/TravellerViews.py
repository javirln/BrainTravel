from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template.context import RequestContext

from principal.services import TravellerService
from principal.models import Traveller
from principal.forms import TravellerEditProfileForm, TravellerEditPasswordForm


# author: Juane
@login_required()
@permission_required('principal.traveller')
def profile_details(request, traveller_id):
    try:
        traveller = TravellerService.find_one(traveller_id)
        return render_to_response('profile_details.html', {'traveller': traveller}, context_instance=RequestContext(request))
    except AssertionError:
        render_to_response('error.html')


# author: Juane
@login_required()
@permission_required('principal.traveller')
def profile_edit(request):
    try:
        traveller = Traveller.objects.get(id=request.user.id)
        if request.POST:
            form = TravellerEditProfileForm(request.POST, request.FILES)
            if form.is_valid():
                traveller = TravellerService.construct_profile(request.user.id, form)
                TravellerService.save(traveller)
                return HttpResponseRedirect('/profile/'+str(traveller.id))
        else:
            data = {'first_name': traveller.first_name, 'last_name': traveller.last_name, 'genre': traveller.genre,
                    'id': traveller.id, 'photo': traveller.photo}
            form = TravellerEditProfileForm(initial=data)
        return render_to_response('profile_edit.html', {"form": form, "photo_profile": traveller.photo}, context_instance=RequestContext(request))
    except AssertionError:
        return render_to_response('error.html')


# author: Juane
@login_required()
@permission_required('principal.traveller')
def profile_edit_password(request):
    try:
        if request.POST:
            form = TravellerEditPasswordForm(request.POST)
            if form.is_valid():
                traveller = TravellerService.construct_password(request.user.id, form)
                TravellerService.save(traveller)
                return HttpResponseRedirect('/profile/'+str(traveller.id))
        else:
            traveller = TravellerService.find_one(request.user.id)
            data = {'id': traveller.id}
            form = TravellerEditPasswordForm(initial=data)
        return render_to_response('profile_edit_password.html', {"form": form}, context_instance=RequestContext(request))
    except AssertionError:
        return render_to_response('error.html')