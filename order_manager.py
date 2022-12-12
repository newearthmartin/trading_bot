import logging

logger = logging.getLogger(__name__)


class OrderManagerBase:
    def __init__(self, wallet):
        self.orders = []
        self.wallet = wallet
        self.order_fulfilled_listeners = []

    def place(self, order):
        logger.info(f'placed {order}')
        self.orders.append(order)

    def order_fulfilled(self, order, price, value):
        order.fulfilled = True
        order.price_fulfilled = price
        order.value_fulfilled = value
        self.orders.remove(order)
        logger.info(f'order fulfilled - {order.action()} @ {order.price_fulfilled} - {self.wallet}')
        for listener in self.order_fulfilled_listeners:
            listener(order)
