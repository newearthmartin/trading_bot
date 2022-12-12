from bots.base_bot import BaseBot
from wallet import Coin


class BuySellBot(BaseBot):
    def __init__(self, wallet, order_simulator, buy_at):
        super().__init__(wallet, order_simulator)
        self.orders = []
        self.buy_at = buy_at

    def process_trade(self, trade):
        if not self.orders:
            print(trade)
            return
        USDT_balance = self.wallet.get(Coin.USDT)
        BTC_balance = self.wallet.get(Coin.BTC)

        print('PROCESS TRADE', trade, self.wallet.get(Coin.USDT), 'USDT -', self.wallet.get(Coin.BTC), 'BTC')
