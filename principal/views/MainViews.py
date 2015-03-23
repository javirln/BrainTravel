from django.shortcuts import render_to_response
from django.template.context import RequestContext
from principal.utils import BrainTravelUtils as btutils

def home(request):
    btutils.save_info(request, "Welcome to BrainTravel.")
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
