# -*- coding: latin-1 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from principal.services import CoinService


@login_required()
def list_coin_traveller(request):
    if request.method == 'GET':
        try:
            # is_traveller = True
            # try:
            #     admin = request.user.administrator
            #     is_traveller = False
            #
            # except Exception:
            #     is_traveller = True

            list_coin_history = CoinService.list_coin_history_traveller(request.user.id)
            return render_to_response('list_coin_history.html',
                                      {'list_coin_history': list_coin_history},
                                      context_instance=RequestContext(request))

            # return render_to_response('list_coin_history.html',
            #                           {'list_coin_history': list_coin_history, 'is_traveller': is_traveller},
            #                           context_instance=RequestContext(request))
        except Exception as e:
            return HttpResponse(e)