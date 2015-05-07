# -*- coding: latin-1 -*-

from principal.models import CoinHistory


def list_coin_history_traveller(id_traveller):
    coin_history = CoinHistory.objects.all().filter(traveller=id_traveller).order_by('-date')
    return coin_history


def check_coins_available(traveller, coins_spent):
    coins_available = traveller.coins
    return not coins_available < coins_spent


def check_coins(days):
    if days <= 3:
        coins = 20
    elif 3 < days <= 7:
        coins = 40
    else:
        coins = 80
    return coins