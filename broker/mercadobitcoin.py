from abstract import BrokerAbstract

import requests
import urllib
import time
import datetime
import hmac
import hashlib
import json

class MercadobitcoinBroker(BrokerAbstract):
    DATA_ENDPOINT = "https://www.mercadobitcoin.net/api/%s/"
    TRADE_ENDPOINT = "https://www.mercadobitcoin.net/tapi/v3/"
    CODE = "MBC"
    price = None
    orderbook = None

    REQUEST_PATH = "/tapi/v3/"
    def getPrice(self):
        if self.price is None:
            r = requests.get(self.DATA_ENDPOINT % ('ticker'))
            data = r.json()
            self.price = data['ticker']['last']
        return self.price


    def getBook(self):
        if self.orderbook is None:
            r = requests.get(self.DATA_ENDPOINT % ('orderbook'))
            data = r.json()
            self.orderbook = data
        return {
            'sell': self.orderbook['asks'][0:10],
            'buy': self.orderbook['bids'][0:10],
        }

    def getBalance(self):
        nonce = self._get_nonce()
        payload = {
            "tapi_method": "get_account_info",
            "tapi_nonce": nonce,
        }
        headers = self._getHeaders(payload)
        r = requests.post(self.TRADE_ENDPOINT, data = payload, headers=headers)
        data = r.json()
        # data = r.json()

        btc = float(data['response_data']['balance']['btc']['total'])
        reais = float(data['response_data']['balance']['brl']['total'])

        return {
            'btc': btc,
            'reais': reais,
            'total': btc*self.getPrice() + reais
        }

    def sell(self, qty, price):
        nonce = self._get_nonce()
        payload = {
            'tapi_method': 'place_sell_order',
            'tapi_nonce': nonce,
            'coin_pair': 'BRLBTC',
            'quantity': str(qty),
            'limit_price': str(price)
        }
        headers = self._getHeaders(payload)
        r = requests.post(self.TRADE_ENDPOINT, data = payload, headers=headers)
        data = r.json()

        return data['status_code'] == 100

    def buy(self, qty, price):
        nonce = self._get_nonce()
        payload = {
            'tapi_method': 'place_buy_order',
            'tapi_nonce': nonce,
            'coin_pair': 'BRLBTC',
            'quantity': str(qty),
            'limit_price': str(price)
        }
        headers = self._getHeaders(payload)
        r = requests.post(self.TRADE_ENDPOINT, data = payload, headers=headers)
        data = r.json()

        print data

        return data['status_code'] == 100


    def _get_nonce(self):
        dt = datetime.datetime.utcnow()
        nonce = str(int(
            (time.mktime(dt.utctimetuple()) + dt.microsecond / float(1000000)) *
            1000000
        ))
        return nonce

    def _get_signature(self, payload):
        params = urllib.urlencode(payload)
        message = "%s?%s" % (self.REQUEST_PATH, params)
        H = hmac.new(self.getSecret(), digestmod=hashlib.sha512)
        H.update(message)
        return H.hexdigest()

    def _getHeaders(self, payload):
        signature = self._get_signature(payload)
        return {
            'TAPI-ID': self.getKey(),
            'TAPI-MAC': signature,
            'Content-Type': "application/x-www-form-urlencoded",
        }
