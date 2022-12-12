class BaseBot:
    def __init__(self, wallet, order_simulator):
        self.wallet = wallet
        self.order_simulator = order_simulator
        order_simulator.order_fulfilled_listeners.append(self.order_listener)

    def order_listener(self, order):
        print('ORDER FULFILLED - missing implementation -', order)
