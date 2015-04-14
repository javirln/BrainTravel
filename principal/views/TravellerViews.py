from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template.context import RequestContext

from principal.services import TravellerService, TripService, PaymentsService, CoinService
from principal.models import Traveller
from principal.forms import TravellerEditProfileForm, TravellerEditPasswordForm
from principal.utils import BrainTravelUtils
from django.http import HttpResponse


# author: Juane
@login_required()
@permission_required('principal.traveller')
def profile_details(request, traveller_id):
    try:
        traveller = TravellerService.find_one(traveller_id)
        if traveller.id == request.user.id:
            trips = TripService.list_my_trip(traveller.id)
            payments = PaymentsService.all_payments(traveller.id)
        else:
            trips = TripService.list_trip_approved(traveller.id)
            payments = []
        return render_to_response('profile_details.html', {'traveller': traveller, 'trips': len(trips), 'payments': len(payments)}, context_instance=RequestContext(request))
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
                BrainTravelUtils.save_success(request, "Profile successfully updated")
                return HttpResponseRedirect('/profile/'+str(traveller.id))
            else:
                message = ""
                for error in form.errors:
                    for me in form.errors[error]:
                        message = message + me
                BrainTravelUtils.save_error(request, message)
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
                BrainTravelUtils.save_success(request, "Password successfully updated")
                return HttpResponseRedirect('/profile/'+str(traveller.id))
            else:
                message = ""
                for error in form.errors:
                    for me in form.errors[error]:
                        message = message + me
                BrainTravelUtils.save_error(request, message)
        else:
            traveller = TravellerService.find_one(request.user.id)
            data = {'id': traveller.id}
            form = TravellerEditPasswordForm(initial=data)
        return render_to_response('profile_edit_password.html', {"form": form}, context_instance=RequestContext(request))
    except AssertionError:
        return render_to_response('error.html')

@login_required()
@permission_required('principal.traveller')
def all_payments(request):
    if request.method == 'GET' or request.method == 'POST':
        try:
            list_payments = PaymentsService.all_payments(request.user.id)
            return render_to_response('my_payments.html',
                                      {'list_payments': list_payments},
                                      context_instance=RequestContext(request))
        except Exception as e:
            return HttpResponse(e)