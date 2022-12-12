import logging
from wallet import Coin, BINANCE_FEE_MULTIPLIER
from order_manager import OrderManagerBase

logger = logging.getLogger(__name__)


class OrderSimulator(OrderManagerBase):
    """
    Simulates orders to test a trading strategy without actually making the trades on Binance
    """
    def process_trade(self, trade):
        for order in self.orders.copy():
            assert(not order.fulfilled)
            trade_value = trade.price * order.qty

            fulfilled = False
            if order.buy_not_sell and trade.price <= order.price:
                if self.wallet.get(Coin.USDT) >= trade_value:
                    self.wallet.substract(Coin.USDT, trade_value)
                    self.wallet.add(Coin.BTC, order.qty * BINANCE_FEE_MULTIPLIER)
                    fulfilled = True
            elif not order.buy_not_sell and trade.price >= order.price:
                if self.wallet.get(Coin.BTC) >= order.qty:
                    self.wallet.add(Coin.USDT, trade_value * BINANCE_FEE_MULTIPLIER)
                    self.wallet.substract(Coin.BTC, order.qty)
                    fulfilled = True

            if fulfilled:
                self.order_fulfilled(order, trade.price, trade_value)
