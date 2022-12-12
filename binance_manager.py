from decimal import Decimal
from django.conf import settings
from binance.client import Client
from binance.websockets import BinanceSocketManager
from order_trade import Trade


class BinanceManager:
    """
    Manages the Binance API and listens to trades. Has 3 types of listeners:
    - msg_listeners: for listening to raw messages from binance trades
    - trade_listeners: for Trade objects
    - second_listeners: for listening to trades grouped by second
    """
    def __init__(self, trade_listener=None, second_listener=None, msg_listener=None):
        self.socket_manager = None
        self.current_second = None
        self.current_second_trades = []
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)
        self.msg_listeners = [msg_listener] if msg_listener else []
        self.trade_listeners = [trade_listener] if trade_listener else []
        self.second_listeners = [second_listener] if second_listener else []

    def start(self):
        self.socket_manager = BinanceSocketManager(self.client)
        self.socket_manager.start_aggtrade_socket('BTCUSDT', self.process_message)
        self.socket_manager.start()
        print('Binance manager started...')

    def process_message(self, msg):
        ts = msg['E']
        price = Decimal(msg['p'])
        qty = Decimal(msg['q'])

        second = ts // 1000

        old_second = None
        old_second_trades = None

        if not self.current_second:
            self.current_second = second
        elif self.current_second != second:
            old_second = self.current_second
            old_second_trades = self.current_second_trades
            self.current_second_trades = []
            self.current_second = second

        trade = Trade(price, qty, ts)
        self.current_second_trades.append(trade)

        for listener in self.msg_listeners:
            listener(msg)
        for listener in self.trade_listeners:
            listener(trade)
        if old_second and old_second_trades:
            for listener in self.second_listeners:
                listener(old_second, old_second_trades)
