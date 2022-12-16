#!/usr/bin/env python
import django
django.setup()
from django.conf import settings

import os
import json

from binance_manager import BinanceManager


class SaveMsgs:
    """
    Msg listener that will dump messages to a file msgs.txt
    """
    def __init__(self):
        self.msg_count = 0
        out_path = os.path.join(settings.BASE_DIR, 'msgs.txt')
        print(f'Writing msgs to {out_path}')
        self.out_file = open(out_path, 'a')

    def listener(self, msg):
        self.out_file.write(json.dumps(msg) + '\n')
        self.out_file.flush()
        self.msg_count += 1
        if self.msg_count % 100 == 0:
            print(f'saved {self.msg_count} msgs')


if __name__ == "__main__":
    save_msgs = SaveMsgs()
    binance_manager = BinanceManager(msg_listener=save_msgs.listener)
    binance_manager.start()
