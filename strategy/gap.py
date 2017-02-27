import broker


class GapStrategy(object):
    QTY_TEST = 0.04
    TRY_SELL_STATE = 'try_sell_state'
    TRY_BUY_STATE = 'try_buy_state'
    NEW_ORDER_BUY = 'new_order_buy'
    state = NEW_ORDER_BUY
    def execute(self):
        for b in broker.getBrokers():
            gap = b.getGap()
            max_profit = gap*100/b.getPriceSellNow(self.QTY_TEST)
            if max_profit > 0.6 and self.state == self.NEW_ORDER_BUY:
                buy_price = b.getPriceSellNow(self.QTY_TEST)+0.0001
                if b.buy(self.QTY_TEST, buy_price):
                    self.state = self.TRY_BUY_STATE
