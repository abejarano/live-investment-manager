from decimal import Decimal

from django.http import HttpResponse
from django.views.generic import TemplateView

from apps.crypto.models import Crypto
from binance.spot import Spot as BinanceClient


class Price(TemplateView):


    def get(self, request, *args, **kwargs):
        cryptos = Crypto.objects.filter(status=True, integration_binance=True)
        binance = BinanceClient()
        for crypto in cryptos:
            response = binance.ticker_24hr(crypto.name + "USDT")
            crypto.price = Decimal(response['lastPrice'])
            crypto.price_change = Decimal(response['priceChangePercent'])
            crypto.save()

        return HttpResponse('Hello world')
