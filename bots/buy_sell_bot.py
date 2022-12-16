import logging

from decimal import Decimal
from bots.base_bot import BaseBot
from order_trade import Order
from wallet import Coin

logger = logging.getLogger(__name__)


class BuySellBot(BaseBot):
    def __init__(self, wallet, order_manager, buy_at):
        super().__init__(wallet, order_manager)
        self.buy_at = buy_at
        self.sell_at = None

    def process_trade(self, trade):
        if self.order_manager.orders:
            return
        wallet = self.order_manager.wallet
        USDT_balance = wallet.get(Coin.USDT)
        BTC_balance = wallet.get(Coin.BTC)

        if USDT_balance > 0 and self.buy_at:
            price = min(self.buy_at, trade.price)
            qty = USDT_balance / price
            self.buy_at = None
            self.sell_at = price * Decimal(1.01)
            self.order_manager.place(Order(Order.BUY, price, qty))
        elif BTC_balance > 0 and self.sell_at:
            price = max(self.sell_at, trade.price)
            qty = BTC_balance
            self.buy_at = price * Decimal(0.99)
            self.sell_at = None
            self.order_manager.place(Order(Order.SELL, price, qty))
        else:
            logger.error(f'No order and nothing to do! - '
                         f'{USDT_balance} USDT - {BTC_balance} BTC - '
                         f'{self.buy_at} - {self.sell_at}')
