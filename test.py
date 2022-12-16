#!/usr/bin/env python
import django
django.setup()

import json
from decimal import Decimal
from binance_manager import BinanceManager, place_order, get_order, get_active_orders, BTCUSDT
from order_manager import BinanceOrderManager
from order_simulator import OrderSimulator, BINANCE_FEE_MULTIPLIER
from bots.buy_sell_bot import BuySellBot
from bots.ladder_bot import LadderBot
from second_processor import SecondAggregator
from wallet import Wallet, Coin
from marto_python.strings import to_decimal
from order_trade import Order

binance = BinanceManager()
order_manager = BinanceOrderManager(binance, Wallet())
wallet = order_manager.wallet
wallet.update_balances(binance)

# usdt_balance = wallet.get(Coin.USDT)
# price = Decimal(17389)
# order = Order(Order.BUY, price, (usdt_balance / price) * BINANCE_FEE_MULTIPLIER, client_id="buy_order_id")
# placed_order = place_order(binance, order)

placed_order = get_order(binance, client_id="buy_order_id")

if placed_order.status == 'FILLED':
    print('buy order filled - selling')
    price = placed_order.price * Decimal(1.003)
    btc_balance = wallet.get(Coin.BTC)
    order = Order(Order.SELL, price, btc_balance, client_id="sell_order_id")
    placed_order = place_order(binance, order, test=True)

# orders = get_active_orders(binance)
# for o in orders:
#     order = get_order(binance, binance_id=o.binance_id)
#     print(order)


# simulator = OrderSimulator(wallet)

# bot = LadderBot(wallet, simulator)
# second_aggregator = SecondAggregator(listener=bot.process_seconds)
# binance.trade_listeners.append(simulator.process_trade)
# binance.second_listeners.append(second_aggregator.add_second)

# bot = BuySellBot(wallet, simulator, Decimal(18000))
# binance.trade_listeners += [bot.process_trade, simulator.process_trade]
# binance.start()
