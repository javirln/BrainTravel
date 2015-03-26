from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED

from BrainTravel import settings
from principal.forms import FormPaypalOwn


def test_paypal_view(request):
    
    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "10000000.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id10",
        "notify_url": "http://564027ec.ngrok.com" + reverse('paypal-ipn'),
        "return_url": "http://564027ec.ngrok.com",
        "cancel_return": "https://www.example.com/your-cancel-location/",
    }

    # Create the instance.
    form = FormPaypalOwn(initial=paypal_dict, button_type="buy")
    context = {"form": form}
    return render_to_response("payment.html", context)




