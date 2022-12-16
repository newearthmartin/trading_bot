import logging
from decimal import Decimal
from django.conf import settings
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from order_trade import Trade, Order
from marto_python.exceptions import log_exceptions
from marto_python.strings import to_decimal

logger = logging.getLogger(__name__)


BTCUSDT = 'BTCUSDT'


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
        logger.info('Setting up Binance client')
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)
        self.msg_listeners = [msg_listener] if msg_listener else []
        self.trade_listeners = [trade_listener] if trade_listener else []
        self.second_listeners = [second_listener] if second_listener else []

    def start(self):
        self.socket_manager = BinanceSocketManager(self.client)
        self.socket_manager.start_aggtrade_socket(BTCUSDT, self.process_message)
        self.socket_manager.start()
        logger.info('Binance manager started...')

    @log_exceptions(lggr=logger)
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


def get_active_orders(binance):
    orders = binance.client.get_all_orders(symbol=BTCUSDT, limit=10)
    orders = [Order.from_binance(o) for o in orders]
    orders = [o for o in orders if o.is_active()]
    return orders


def get_order(binance, binance_id=None, client_id=None):
    kwargs = {'symbol': BTCUSDT}
    if binance_id:
        kwargs['orderId'] = binance_id
    elif client_id:
        kwargs['origClientOrderId'] = client_id
    order = binance.client.get_order(**kwargs)
    return Order.from_binance(order)


def place_order(binance, order, test=False):
    assert(order.client_id is not None)
    assert(order.binance_id is None)
    assert(order.status is None)

    price = str(to_decimal(order.price, 2))
    qty = str(to_decimal(order.qty, 5))

    logger.info(f'placing order - ({order.client_id} - {order.side} - {qty} @ {price})')
    create_fn = binance.client.create_order if not test else binance.client.create_test_order
    create_fn(
        symbol=BTCUSDT, side=order.side, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC,
        newClientOrderId=order.client_id, quantity=qty, price=price)

    placed_order = get_order(binance, client_id=order.client_id)
    logger.info(f'placed order - {placed_order}')
    return placed_order
