#!/usr/bin/env python
import django
django.setup()

import logging
from decimal import Decimal
from binance_manager import BinanceManager, place_order, get_order, get_active_orders, BTCUSDT
from order_manager import BinanceOrderManager
from order_simulator import BINANCE_FEE_MULTIPLIER
from wallet import Wallet, Coin
from marto_python.strings import to_decimal
from order_trade import Order

logger = logging.getLogger(__name__)

max_buy = None
min_sell = None
INCR = 0.01


BUY_ORDER_ID = "buy_order_id"
SELL_ORDER_ID = "sell_order_id"
binance = BinanceManager()
order_manager = BinanceOrderManager(binance, Wallet())
wallet = order_manager.wallet
wallet.update_balances(binance)


def place_buy(price):
    usdt_balance = to_decimal(wallet.get(Coin.USDT), 2)
    price = to_decimal(price, 2)
    qty = to_decimal(usdt_balance / price, 5)
    while qty * price > usdt_balance:
        qty -= Decimal('0.00001')
    new_order = Order(Order.BUY, price, qty, client_id=BUY_ORDER_ID)
    return place_order(binance, new_order)


def place_sell(price):
    new_order = Order(Order.SELL, price, wallet.get(Coin.BTC), client_id=SELL_ORDER_ID)
    return place_order(binance, new_order)


def get_last_price():
    last_trade = binance.client.get_recent_trades(symbol=BTCUSDT, limit=1)[0]
    return to_decimal(last_trade['price'], 2)


while True:
    buy_order = get_order(binance, client_id=BUY_ORDER_ID)
    sell_order = get_order(binance, client_id=SELL_ORDER_ID)
    wallet.update_balances(binance)
    last_price = get_last_price()
    logger.info(f'{last_price} - {wallet}')

    if buy_order.is_active() or sell_order.is_active():
        continue

    if wallet.get(Coin.USDT) > Decimal(1):
        buy_price = min(sell_order.price * Decimal(1 - INCR), last_price)
        if max_buy and buy_price > max_buy:
            buy_price = max_buy
            logger.info(f'Using max_buy - {max_buy}')
        max_buy = None
        place_buy(buy_price)
    elif wallet.get(Coin.BTC) > Decimal(0.00001):
        sell_price = max(buy_order.price * Decimal(1 + INCR), last_price)
        if min_sell and sell_price < min_sell:
            sell_price = min_sell
            logger.info(f'Using min_sell - {min_sell}')
        min_sell = None
        place_sell(sell_price)
    else:
        logger.error(f'Ni orders, ni balance - {wallet}')
