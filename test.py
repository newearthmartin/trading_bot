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
# order_manager = BinanceOrderManager(binance, Wallet())
# wallet = order_manager.wallet
# wallet.update_balances(binance)

# simulator = OrderSimulator(wallet)

# bot = LadderBot(wallet, simulator)
# second_aggregator = SecondAggregator(listener=bot.process_seconds)
# binance.trade_listeners.append(simulator.process_trade)
# binance.second_listeners.append(second_aggregator.add_second)

# bot = BuySellBot(wallet, simulator, Decimal(18000))
# binance.trade_listeners += [bot.process_trade, simulator.process_trade]
# binance.start()

last_trade = binance.client.get_recent_trades(symbol=BTCUSDT, limit=1)[0]
last_price = to_decimal(last_trade['price'], 2)
