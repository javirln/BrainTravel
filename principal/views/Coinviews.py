# -*- coding: iso-8859-1 -*-
import ast

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.utils.translation import ugettext as _

from BrainTravel import settings
from principal.forms import FormPaypalOwn
from principal.services import CoinService, UserService, PaymentsService, CoinHistoryService
from django.views.decorators.csrf import csrf_exempt
from principal.utils import BrainTravelUtils


@csrf_exempt
@login_required()
def list_coin_traveller(request):
    
    #Si la peticion es post, viene de PayPal
    if request.method == "POST":
        BrainTravelUtils.save_info(request, _("Thanks for your bought!. It's possible that coins revenue take for a minutes. Please, be patient :)"))
    
    
    try:
        list_coin_history = CoinService.list_coin_history_traveller(request.user.id)
        paginator = Paginator(list_coin_history, 10)
        page = request.GET.get('page')
        try:
            list_coin_history = paginator.page(page)
        except PageNotAnInteger:
            list_coin_history = paginator.page(1)
        except EmptyPage:
            list_coin_history = paginator.page(paginator.num_pages)
    except:
        return render_to_response('error.html', context_instance=RequestContext(request))
        
    
    return render_to_response('list_coin_history.html', {'list_coin_history': list_coin_history}, context_instance=RequestContext(request))

@permission_required('principal.traveller')
def buy_coins(request):
    try:
        # Paquete 1
        track_data1 = {'user_id': request.user.id, 'package_number': '1'}
        paypal_dict_1 = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "4.50",
            "item_name": _("40 Coins"),
            "notify_url": "http://54.69.54.93" + reverse('paypal-ipn'),
            "return_url": "http://54.69.54.93/coin/list/",
            "cancel_return": "http://54.69.54.93/payment_cancel",
            "currency_code": "EUR",
            "custom": track_data1,
        }

        # Paquete 2
        track_data2 = {'user_id': request.user.id, 'package_number': '2'}
        paypal_dict_2 = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "7.00",
            "item_name": _("60 Coins"),
            "notify_url": "http://54.69.54.93" + reverse('paypal-ipn'),
            "return_url": "http://54.69.54.93/coin/list/",
            "cancel_return": "http://54.69.54.93/coin/payment_cancel",
            "currency_code": "EUR",
            "custom": track_data2,
        }

        # Paquete 3
        track_data3 = {'user_id': request.user.id, 'package_number': '3'}
        paypal_dict_3 = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": "10.00",
            "item_name": _("100 Coins"),
            "notify_url": "http://54.69.54.93" + reverse('paypal-ipn'),
            "return_url": "http://54.69.54.93/coin/list/",
            "cancel_return": "http://54.69.54.93/payment_cancel",
            "currency_code": "EUR",
            "custom": track_data3,
        }

        form1 = FormPaypalOwn(initial=paypal_dict_1)
        form2 = FormPaypalOwn(initial=paypal_dict_2)
        form3 = FormPaypalOwn(initial=paypal_dict_3)

        data = {"form1": form1, "form2": form2, "form3": form3}
        return render_to_response('buy_coins.html', data, context_instance=RequestContext(request))

    except:
        return render_to_response('error.html', context_instance=RequestContext(request))


#----------- SEÑALES DE VUELTA DE PAYPAL--------------------
def receive_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        custom_data = ast.literal_eval(ipn_obj.custom)

        #Dictionary where relations package_number and coins
        dict_coins = {'1': '40', '2':'60', '3':'100'}

        try:
            coins_amount = dict_coins[custom_data['package_number']]
            user = UserService.add_coins(coins_amount, custom_data['user_id'])
            UserService.save(user)

            payment = PaymentsService.create(user.id, ipn_obj.mc_gross)
            PaymentsService.save(payment)

            coin_history = CoinHistoryService.create(amount_coins=coins_amount, concept=ipn_obj.item_name, traveller=user, payment=payment)
            
            CoinHistoryService.save(coin_history)

        except Exception as e:
            print(e)


def error(sender, **kwargs):
    print("Algo ha pasado")

valid_ipn_received.connect(receive_payment)
invalid_ipn_received.connect(error)




