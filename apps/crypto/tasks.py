from decimal import Decimal

from celery import shared_task

from apps.crypto.models import Crypto
from binance.spot import Spot as BinanceClient


@shared_task(name='prices')
def handle_price():
    cryptos = Crypto.objects.filter(status=True)

    binance = BinanceClient()

    for crypto in cryptos:
        response = binance.ticker_price(crypto.name + "USDT")
        crypto.price = Decimal(response['price'])
        crypto.save()
