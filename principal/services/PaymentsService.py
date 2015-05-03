from principal.models import Payment, Traveller
from datetime import datetime


def save(payment):
    payment.save()


def create(id_traveller, amount):
    payment = Payment(traveller=Traveller.objects.get(id=id_traveller),
                      amount=amount,
                      date=datetime.now())
    return payment


def all_payments(id_traveller):
    payment = Payment.objects.all().filter(traveller=id_traveller).order_by('-date')
    return payment