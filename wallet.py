from enum import Enum


class Coin(Enum):
    USDT = 'USDT'
    BTC = 'BTC'


BINANCE_FEE = 0.001
BINANCE_FEE_MULTIPLIER = 1 - BINANCE_FEE


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

    def substract(self, coin, value):
        self.add(coin, -value)

    def __repr__(self):
        return f'({self.balance[Coin.USDT]} USDT - {self.balance[Coin.BTC]} BTC)'