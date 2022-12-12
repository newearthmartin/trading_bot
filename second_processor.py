from decimal import Decimal

MAX_SECONDS = 60 * 60 * 24


class SecondAggregator:
    """
    Holds a list of the last MAX_SECONDS trades
    """
    def __init__(self, listener=None):
        self.last_second_trades = []
        self.listener = listener

    def add_second(self, ts, trades):
        if not trades:
            return

        avg_price = Decimal(0.0)
        for trade in trades:
            avg_price += trade.price
        avg_price /= len(trades)

        self.last_second_trades.append(avg_price)
        if len(self.last_second_trades) > MAX_SECONDS:
            self.last_second_trades = self.last_second_trades[MAX_SECONDS // 2:]

        if self.listener:
            self.listener(self.last_second_trades)
