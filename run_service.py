#!/usr/bin/env python

import time

from ircddbclient import Push, Pull

MIN_TIME_BETWEEN_IRCDDB_PULLS = 30

if __name__ == '__main__':
    puller = Pull()
    pusher = Push(class_name='ParsedStream')

    while True:
        start_time = time.time()
        for message in puller.pull():
            print message
            pusher.push(message)

        # take it easy on the ircDDB system
        elapsed_time = time.time() - start_time
        if elapsed_time < MIN_TIME_BETWEEN_IRCDDB_PULLS:
            time.sleep(MIN_TIME_BETWEEN_IRCDDB_PULLS - elapsed_time)
