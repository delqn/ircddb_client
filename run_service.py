#!/usr/bin/env python

import time

from ircddbclient import Parser, PushMessage, PullMessages

SLEEP_SECONDS = 20

if __name__ == '__main__':
    puller = PullMessages()
    parser = Parser()
    while True:
        for message in puller.pull():
            print message
            PushMessage(class_name='ParsedStream', data=message)()
        time.sleep(SLEEP_SECONDS)
