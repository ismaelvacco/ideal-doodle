from abstract import BrokerAbstract

import requests

class FoxbitBroker(BrokerAbstract):
    DATA_ENDPOINT = "https://api.blinktrade.com/api/v1/BRL/ticker"
    CODE = "FB"

    def getPrice(self):
        r = requests.get(self.DATA_ENDPOINT)
        data = r.json()
        return data['last']
