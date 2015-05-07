# -*- coding: iso-8859-1 -*-


from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
