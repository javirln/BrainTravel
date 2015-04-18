# -*- coding: latin-1 -*-

from principal.models import CoinHistory, Traveller


def list_coin_history_traveller(id_traveller):
    coin_history = CoinHistory.objects.all().filter(traveller=id_traveller)
    return coin_history


def increase_coins(id_traveller, coin_number):
    traveller = Traveller.objects.all().filter(traveller=id_traveller)
    traveller.coins(traveller+coin_number)
    traveller.save()