#!/usr/bin/env python
from binance_manager import BinanceManager
from order_simulator import OrderSimulator
from bots.buy_sell_bot import BuySellBot
from bots.ladder_bot import LadderBot
from second_processor import SecondAggregator
from wallet import Wallet

wallet = Wallet(usdt=1000, btc=0.0)
simulator = OrderSimulator(wallet)

bot = LadderBot(wallet, simulator)
second_aggregator = SecondAggregator(listener=bot.process_seconds)
binance = BinanceManager(trade_listener=simulator.process_trade, second_listener=second_aggregator.add_second)

# bot = BuySellBot(wallet, simulator, 17000)
# binance = BinanceManager()
# binance.trade_listeners += [bot.process_trade, simulator.process_trade]

binance.start()
