#!/usr/bin/env python
import django
django.setup()

from decimal import Decimal
from binance_manager import BinanceManager
from order_simulator import OrderSimulator
from bots.buy_sell_bot import BuySellBot
from bots.ladder_bot import LadderBot
from second_processor import SecondAggregator
from wallet import Wallet, Coin

binance = BinanceManager()
wallet = Wallet(usdt=Decimal(1000), btc=Decimal(0.0))
simulator = OrderSimulator(wallet)

# bot = LadderBot(wallet, simulator)
# second_aggregator = SecondAggregator(listener=bot.process_seconds)
# binance.trade_listeners.append(simulator.process_trade)
# binance.second_listeners.append(second_aggregator.add_second)

bot = BuySellBot(wallet, simulator, Decimal(18000))
binance.trade_listeners += [bot.process_trade, simulator.process_trade]
binance.start()
