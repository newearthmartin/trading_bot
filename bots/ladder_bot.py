from decimal import Decimal
from wallet import Coin
from order_simulator import BINANCE_FEE
from order_trade import Order
from bots.base_bot import BaseBot

LAST_N = 3
SELL_THEN_BUY = 'SELL_THEN_BUY'
JUST_DO_IT = 'JUST_DO_IT'

DIGITS = Decimal(10) ** -3


class LadderBot(BaseBot):
    """
    Trading bot that works by listening to trades aggregated on seconds
    """
    def process_seconds(self, trades):
        last_price = trades[-1]
        price_decimal = Decimal(last_price).quantize(DIGITS)
        if len(trades) < LAST_N:
            print(price_decimal)
            return

        all_up_down, up_down = LadderBot.is_ladder(trades[-LAST_N:])

        all_up_down_msg = ' '
        if all_up_down:
            all_up_down_msg = '↑' if up_down else '↓'
        print(price_decimal, all_up_down_msg)

        if all_up_down:
            BTC_balance = self.wallet.get(Coin.BTC)
            if not up_down and BTC_balance > 0:
                fee_multiplier = 1 - BINANCE_FEE * 2
                order = Order(Order.SELL, last_price * fee_multiplier, BTC_balance, order_type=SELL_THEN_BUY)
                self.order_simulator.place(order)

    @staticmethod
    def is_ladder(last_trades):
        p0 = None
        up_down = None
        for p in last_trades:
            if p0 and p0 != p:
                new_up_down = p0 < p
                if up_down is None:
                    up_down = new_up_down
                elif up_down != new_up_down:
                    return False, None
            p0 = p
        return up_down is not None, up_down

    def order_listener(self, order):
        if order.order_type == SELL_THEN_BUY:
            fee_multiplier = 1 - BINANCE_FEE * 2 - 0.002
            price = order.price_fulfilled * fee_multiplier
            qty = self.wallet.get(Coin.USDT) / price
            order = Order(Order.BUY, price, qty, order_type=JUST_DO_IT)
            self.order_simulator.place(order)
