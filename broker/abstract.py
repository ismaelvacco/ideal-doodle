from common import getLogging
import ConfigParser

log = getLogging()
config = ConfigParser.ConfigParser()
config.read("etc/credentials.ini")

class BrokerAbstract(object):
    def getPrice(self):
        raise Exception("implement the method")

    def getBook(self):
        raise Exception("implement the method")

    def sell(self, qty, price):
        raise Exception("implement the method")

    def buy(self, qty, price):
        raise Exception("implement the method")

    def getBalance(self):
        raise Exception("implement the method")

    def compare(self, broker, qty):
#        delta = abs(self.getPrice() - broker.getPrice())/min([self.getPrice(),broker.getPrice()])
        if self.getPriceBuyNow(qty) < broker.getPriceSellNow(qty):
            priceBuy = self.getPriceBuyNow(qty)
            priceSell = broker.getPriceSellNow(qty)
            buy = self.CODE
            sell = broker.CODE
        elif broker.getPriceBuyNow(qty) < self.getPriceSellNow(qty):
            priceBuy = broker.getPriceBuyNow(qty)
            priceSell = self.getPriceSellNow(qty)
            buy = broker.CODE
            sell = self.CODE
        else:
            log.info("BROKER A - PRECO DE COMPRA: %s" % self.getPriceBuyNow(qty))
            log.info("BROKER B - PRECO DE VENDA: %s" % broker.getPriceSellNow(qty))
            log.info("BROKER B - PRECO DE COMPRA: %s" % broker.getPriceBuyNow(qty))
            log.info("BROKER A - PRECO DE VENDA: %s" % self.getPriceSellNow(qty))
            return False

        real_delta = (priceSell - priceBuy)/priceBuy

        return {
#            'delta': delta,
            'real_delta': real_delta,
#            'delta_perc': "%.2f%%" % (delta*100),
            'real_delta_perc': "%.2f%%" % (real_delta*100),
            "buy": buy,
            "sell": sell,
            'buy_per': priceBuy,
            'sell_per': priceSell,
        }

    def getPriceBuyNow(self, qty):
        orderbook = self.getBook()
        price = 0
        for order in orderbook['sell']:
            price = order[0]
            qty = qty-order[1]
            if qty <= 0:
                break
        return price

    def getPriceSellNow(self, qty):
        orderbook = self.getBook()
        price = 0
        for order in orderbook['buy']:
            price = order[0]
            qty = qty-order[1]
            if qty <= 0:
                break
        return price

    def initialize(self):
        self.price = None
        self.orderbook = None

    def getSecret(self):
        return config.get(self.CODE,'secret')

    def getKey(self):
        return config.get(self.CODE,'key')

    def getSummarize(self):
        balance = self.getBalance()
        btc_qty = balance['total'] - balance['reais']
        log.info("%s --- BTC: R$%.2f (%.2f%%) - Reais: R$%.2f (%.2f%%) - Total: R$%.2f" % (self.CODE, btc_qty, 100*(btc_qty/balance['total']), balance['reais'], 100*(balance['reais']/balance['total']), balance['total']))


    def getGap(self, qty = 0.1):
        return self.getPriceBuyNow(qty) - self.getPriceSellNow(qty)
