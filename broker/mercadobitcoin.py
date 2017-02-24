from abstract import BrokerAbstract

import requests

class MercadobitcoinBroker(BrokerAbstract):
    DATA_ENDPOINT = "https://www.mercadobitcoin.net/api/ticker/"
    CODE = "MBC"

    def getPrice(self):
        r = requests.get(self.DATA_ENDPOINT)
        data = r.json()
        return data['ticker']['last']
