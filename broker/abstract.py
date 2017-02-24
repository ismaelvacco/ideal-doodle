
class BrokerAbstract(object):
    def getPrice(self):
        raise Exception("implement the method")

    def getBook(self):
        raise Exception("implement the method")

    def sell(self, qty, price):
        raise Exception("implement the method")

    def buy(self, qty, price):
        raise Exception("implement the method")
