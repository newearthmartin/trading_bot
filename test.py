#!/usr/bin/env python
import django
django.setup()

import json
from decimal import Decimal
from binance_manager import BinanceManager, get_active_orders, BTCUSDT
from order_simulator import OrderSimulator
from bots.buy_sell_bot import BuySellBot
from bots.ladder_bot import LadderBot
from second_processor import SecondAggregator
from wallet import Wallet, Coin
from order_trade import Order

binance = BinanceManager()
# wallet = Wallet()
# wallet.update_balances(binance)
# print(wallet)

orders = [Order.from_binance(o).binance_id for o in get_active_orders(binance)]

for order_id in orders:
    order = binance.client.get_order(symbol=BTCUSDT, orderId=order_id)
    order = Order.from_binance(order)
    print(order)


# simulator = OrderSimulator(wallet)

# bot = LadderBot(wallet, simulator)
# second_aggregator = SecondAggregator(listener=bot.process_seconds)
# binance.trade_listeners.append(simulator.process_trade)
# binance.second_listeners.append(second_aggregator.add_second)

# bot = BuySellBot(wallet, simulator, Decimal(18000))
# binance.trade_listeners += [bot.process_trade, simulator.process_trade]
# binance.start()
