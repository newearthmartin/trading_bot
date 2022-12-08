from wallet import BTC, USDT, BINANCE_FEE_MULTIPLIER


class OrderSimulator:
    def __init__(self, wallet):
        self.orders = []
        self.wallet = wallet
        self.order_fulfilled_listeners = []

    def place(self, order):
        print(f'placing {order} - {order.order_type}')
        self.orders.append(order)

    def process_trade(self, trade):
        for order in self.orders.copy():
            assert(not order.fulfilled)
            trade_value = trade.price * order.qty
            if order.buy_not_sell and trade.price <= order.price:
                if self.wallet.get(USDT) >= trade_value:
                    self.wallet.substract(USDT, trade_value)
                    self.wallet.add(BTC, order.qty * BINANCE_FEE_MULTIPLIER)
                    order.fulfilled = True
            elif not order.buy_not_sell and trade.price >= order.price:
                if self.wallet.get(BTC) >= order.qty:
                    self.wallet.add(USDT, trade_value * BINANCE_FEE_MULTIPLIER)
                    self.wallet.substract(BTC, order.qty)
                    order.fulfilled = True

            if order.fulfilled:
                order.price_fulfilled = trade.price
                order.value_fulfilled = trade_value
                self.orders.remove(order)
                print(f'order fulfilled - {order.action()} @ {order.price_fulfilled} - {self.wallet}')
                for listener in self.order_fulfilled_listeners:
                    listener(order)
