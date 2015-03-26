from principal.models import CoinHistory


def save(coin_history):
    coin_history.save()


def create(amount_coins, concept, traveller, payment):
    
    
    coin_history = CoinHistory(amount = amount_coins,
                               date = payment.date,
                               concept = concept,
                               traveller = traveller)
    return coin_history