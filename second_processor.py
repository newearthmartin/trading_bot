MAX_SECONDS = 60 * 60 * 24


class SecondProcessor:
    def __init__(self, trades_listener=None):
        self.last_second_trades = []
        self.trades_listener = trades_listener

    def add_second_trades(self, ts, trades):
        if not trades:
            return

        avg_price = 0.0
        for trade in trades:
            avg_price += trade.price
        avg_price /= len(trades)

        self.last_second_trades.append(avg_price)
        if len(self.last_second_trades) > MAX_SECONDS:
            self.last_second_trades = self.last_second_trades[MAX_SECONDS // 2:]

        if self.trades_listener:
            self.trades_listener(self.last_second_trades)
