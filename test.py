#!/usr/bin/env python
from binance_manager import BinanceManager
from order_simulator import OrderSimulator
from second_processor import SecondAggregator
from trading_bot import TradingBot
from wallet import Wallet

wallet = Wallet(usdt=0, btc=1.0)
simulator = OrderSimulator(wallet)
bot = TradingBot(wallet, simulator)
second_aggregator = SecondAggregator(listener=bot.process_seconds)

binance = BinanceManager(trade_listener=simulator.process_trade, second_listener=second_aggregator.add_second)
binance.start()
