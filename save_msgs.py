#!/usr/bin/env python
from binance_manager import BinanceManager, SaveMsgs

save_msgs = SaveMsgs()
binance_manager = BinanceManager(msg_listener=save_msgs.listener)
binance_manager.start()
