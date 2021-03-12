#!/usr/bin/env python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trading.settings")
# import django
# django.setup()
# from django.conf import settings

from binance_manager import BinanceManager
from order_simulator import OrderSimulator
from second_processor import SecondProcessor
from trading_bot import TradingBot
from wallet import Wallet

wallet = Wallet(usdt=0, btc=1.0)
simulator = OrderSimulator(wallet)
bot = TradingBot(wallet, simulator)
second_agregator = SecondProcessor(trades_listener=bot.process_second_trades)
binance_manager = BinanceManager(trade_listener=simulator.process_trade, second_listener=second_agregator.add_second_trades)
binance_manager.start()

