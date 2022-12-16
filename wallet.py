import logging
from decimal import Decimal
from enum import Enum

logger = logging.getLogger(__name__)


class Coin(Enum):
    USDT = 'USDT'
    BTC = 'BTC'


class Wallet:
    def __init__(self, usdt=0.0, btc=0.0):
        self.balance = {
            Coin.USDT: usdt,
            Coin.BTC: btc
        }

    def get(self, coin): return self.balance.get(coin, 0.0)
    def set(self, coin, value): self.balance[coin] = value

    def add(self, coin, value):
        if coin not in self.balance:
            self.balance[coin] = 0
        self.balance[coin] += value

    def subtract(self, coin, value):
        self.add(coin, -value)

    def __repr__(self):
        return f'({self.balance[Coin.USDT]} USDT - {self.balance[Coin.BTC]} BTC)'

    def update_balances(self, binance_manager):
        for coin in Coin:
            data = binance_manager.client.get_asset_balance(asset=coin.value)
            self.set(coin, Decimal(data['free']))
        # logger.info(f'Updated balances - {self}')
