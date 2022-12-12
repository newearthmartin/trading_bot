class Order:
    def __init__(self, buy_not_sell, price, qty, order_type=None):
        self.buy_not_sell = buy_not_sell
        self.price = price
        self.qty = qty
        self.fulfilled = False
        self.order_type = type

    def action(self):
        return 'BUY' if self.buy_not_sell else 'SELL'

    def __repr__(self):
        return f'({self.action()} {self.qty} @ {self.price})'


class Trade:
    def __init__(self, price, qty, ts):
        self.price = price
        self.qty = qty
        self.ts = ts

    def __repr__(self):
        return f'({self.price}, {self.qty}, {self.ts})'
