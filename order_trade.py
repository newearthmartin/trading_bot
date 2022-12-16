from decimal import Decimal

class Order:
    def __init__(self, buy_not_sell, price, qty, order_type=None, binance_id=None, status=None):
        self.binance_id = binance_id
        self.buy_not_sell = buy_not_sell
        self.price = price
        self.qty = qty
        self.fulfilled = False
        self.order_type = order_type
        self.status = status

    def action(self):
        return 'BUY' if self.buy_not_sell else 'SELL'

    def __repr__(self):
        order_str = f'{self.action()} {self.qty} @ {self.price}'
        if self.order_type:
            order_str += f' - {self.order_type}'
        if self.status:
            order_str += f' - {self.status}'
        if self.binance_id:
            order_str = f'id {self.binance_id}: {order_str}'
        return f'({order_str})'

    @staticmethod
    def from_binance(o):
        side = o['side']
        if side == 'BUY':
            buy_not_sell = True
        elif side == 'SELL':
            buy_not_sell = False
        else:
            raise Exception(f'expected BUY or SELL - {side}')

        return Order(buy_not_sell, Decimal(o['price']), Decimal(o['origQty']),
                     binance_id=o['orderId'], status=o['status'])


class Trade:
    def __init__(self, price, qty, ts):
        self.price = price
        self.qty = qty
        self.ts = ts

    def __repr__(self):
        return f'({self.price}, {self.qty}, {self.ts})'
