#!/usr/bin/env python

import time

from ircddbclient import Push, Pull

SLEEP_SECONDS = 20

if __name__ == '__main__':
    puller = Pull()
    pusher = Push(class_name='ParsedStream')
    while True:
        for message in puller.pull():
            print message
            pusher.push(data=message)
        time.sleep(SLEEP_SECONDS)
