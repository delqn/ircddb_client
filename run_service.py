#!/usr/bin/env python

import time

from ircddbclient import Parser, PushMessage, PullMessages

SLEEP_SECONDS = 20


def push_message(msg):
    PushMessage(class_name='Stream', data={'Message': msg})()


def push_parsed_message(data_):
    PushMessage(class_name='ParsedStream', data=data_)()

if __name__ == '__main__':
    puller = PullMessages()
    parser = Parser()
    while True:
        for message in puller.pull():
            print message
            # threading.Thread(target=push_message, args=(message,)).start()
            push_parsed_message(message)
        time.sleep(SLEEP_SECONDS)
