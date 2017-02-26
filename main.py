import broker
import time

from broker.common import getLogging

BTC_TRANSACTION = 0.1

log = getLogging()

brokers_compare = []
def can_compare(brokerA, brokerB):
    if brokerA.CODE == brokerB.CODE:
        return False
    keyA = "%s-%s" % (brokerA.CODE, brokerB.CODE)
    keyB = "%s-%s" % (brokerB.CODE, brokerA.CODE)
    if keyA in brokers_compare or keyB in brokers_compare:
        return False
    brokers_compare.append(keyA)
    brokers_compare.append(keyB)
    return  True

def get_broker_by_code(code):
    for b in broker.getBrokers():
        if b.CODE == code:
            return b

def execute_arbitragem(compare, qty):
    sell_broker = get_broker_by_code(compare["sell"])
    buy_broker = get_broker_by_code(compare["buy"])

    response_sell = sell_broker.sell(qty, int(compare["sell_per"]))
    log.info("Efetuada venda em %s de %sBTC por R$%s" % (sell_broker.CODE, qty, compare["sell_per"]))
    response_buy = buy_broker.buy(qty, int(compare["buy_per"]))
    log.info("Efetuada compra em %s de %sBTC por R$%s" % (buy_broker.CODE, qty, compare["buy_per"]))

    return response_sell and response_buy

if __name__ == "__main__":
    QTY_TEST = 0.009
    while True:
        brokers_compare = []
        for b in broker.getBrokers():
            b.initialize()
            b.getSummarize()
            for c in broker.getBrokers():
                c.initialize()
                if can_compare(b, c):
                    comp = c.compare(b, QTY_TEST)
                    if not comp:
                        log.info("operacao inviavel de lucro")
                        continue
                    log.info("comprando em %(buy)s, por R$%(buy_per)s e vendendo em %(sell)s, por R$%(sell_per)s obtera um lucro bruto de %(real_delta_perc)s" % comp)
                    if (comp["real_delta"]*100 >0.9) or (comp['buy'] == "MCB" and comp["real_delta"]*100 >0.7):
                        execute_arbitragem(comp, QTY_TEST)
                    else:
                        log.info("aguardando oportunidade melhor" % comp)

        time.sleep(30)


    # b = broker.foxbit.FoxbitBroker()
    # print b.buy(0.0009,3670)
