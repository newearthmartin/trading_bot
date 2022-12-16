from decimal import Decimal


class Order:
    BUY = 'BUY'
    SELL = 'SELL'

    def __init__(self, side, price, qty, order_type=None,client_id=None, binance_id=None, status=None):
        self.client_id = client_id
        self.binance_id = binance_id
        self.side = side
        self.price = price
        self.qty = qty
        self.fulfilled = False
        self.order_type = order_type
        self.status = status

    def is_active(self):
        return self.status in ['NEW', 'PARTIALLY_FILLED']

    def __repr__(self):
        order_str = f'{self.side} {self.qty} @ {self.price}'
        if self.order_type:
            order_str += f' - {self.order_type}'
        if self.status:
            order_str += f' - {self.status}'
        if self.binance_id:
            order_str = f'binance {self.binance_id} - {order_str}'
        if self.client_id:
            order_str = f'client {self.client_id} - {order_str}'
        return f'({order_str})'

    @staticmethod
    def from_binance(o):
        assert(o['side'] in [Order.BUY, Order.SELL])
        return Order(o['side'], Decimal(o['price']), Decimal(o['origQty']),
                     binance_id=o['orderId'], client_id=o['clientOrderId'], status=o['status'])


class Trade:
    def __init__(self, price, qty, ts):
        self.price = price
        self.qty = qty
        self.ts = ts

    def __repr__(self):
        return f'({self.price}, {self.qty}, {self.ts})'
