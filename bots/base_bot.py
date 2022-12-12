class BaseBot:
    def __init__(self, wallet, order_manager):
        self.wallet = wallet
        self.order_manager = order_manager
        self.order_manager.order_fulfilled_listeners.append(self.order_listener)

    def order_listener(self, order):
        pass
