import mercadobitcoin
import foxbit

def getBrokers():
    return [
        mercadobitcoin.MercadobitcoinBroker(),
        foxbit.FoxbitBroker(),
    ]
