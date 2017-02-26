from abstract import BrokerAbstract
import time
import datetime
import hmac
import hashlib
import json

import requests

class FoxbitBroker(BrokerAbstract):
    DATA_ENDPOINT = "https://api.blinktrade.com/api/v1/BRL/%s"
    TRADE_ENDPOINT = "https://api.blinktrade.com/tapi/v1/message"
    CODE = "FB"
    price = None
    orderbook = None

    def getPrice(self):
        if self.price is None:
            r = requests.get(self.DATA_ENDPOINT % ("ticker"))
            data = r.json()
            self.price = data['last']
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
        payload = {
            "MsgType": "U2",
            "BalanceReqID": 1,
        }
        headers = self._getHeaders()
        r = requests.post(self.TRADE_ENDPOINT, data = json.dumps(payload), headers=headers)
        data = r.json()
        btc =  float(data['Responses'][0]["4"]['BTC'])
        reais =  float(data['Responses'][0]["4"]['BRL'])

        return {
            'btc': float(btc/100000000),
            'reais': float(reais/100000000),
            'total': float(btc/100000000)*self.getPrice() + float(reais/100000000)
        }

    def sell(self, qty, price):
        nonce = self._get_nonce()
        payload = {
            "MsgType": "D",
            "ClOrdID": nonce,
            "Symbol": "BTCBRL",
            "Side": "2",
            "OrdType": "2",
            "Price": int(price*100000000),
            "OrderQty": int(qty*100000000),
            "BrokerID": 4
        }
        headers = self._getHeaders()
        r = requests.post(self.TRADE_ENDPOINT, data = json.dumps(payload), headers=headers)
        data = r.json()

        return data['Status'] == 200

    def buy(self, qty, price):
        nonce = self._get_nonce()
        payload = {
            "MsgType": "D",
            "ClOrdID": nonce,
            "Symbol": "BTCBRL",
            "Side": "1",
            "OrdType": "2",
            "Price": int(price*100000000),
            "OrderQty": int(qty*100000000),
            "BrokerID": 4
        }
        headers = self._getHeaders()
        r = requests.post(self.TRADE_ENDPOINT, data = json.dumps(payload), headers=headers)
        data = r.json()

        return data['Status'] == 200



    def _get_nonce(self):
        dt = datetime.datetime.utcnow()
        nonce = str(int(
            (time.mktime(dt.utctimetuple()) + dt.microsecond / float(1000000)) *
            1000000
        ))
        return nonce

    def _get_signature(self, nonce):
        return hmac.new(
            bytearray(self.getSecret(), 'utf-8'), bytearray(nonce, 'utf-8'), digestmod=hashlib.sha256
        ).hexdigest()

    def _getHeaders(self):
        nonce = self._get_nonce()
        signature = self._get_signature(nonce)
        return {
            'Nonce': nonce,
            'APIKey': self.getKey(),
            'Signature': signature,
            'Content-Type': "application/json",
        }
