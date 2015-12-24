#!/usr/bin/env python

import time

from multiprocessing import Pool

from ircddbclient import Push, Pull

MIN_TIME_BETWEEN_IRCDDB_PULLS = 30


def push(message):
    print 'pushing {}'.format(message)
    Push(class_name='ParsedStream').push(message)

if __name__ == '__main__':
    puller = Pull()
    while True:
        start_time = time.time()
        pool = Pool(5)
        messages = puller.pull()
        pool.map(push, messages)

        # take it easy on the ircDDB system
        elapsed_time = time.time() - start_time
        if elapsed_time < MIN_TIME_BETWEEN_IRCDDB_PULLS:
            time.sleep(MIN_TIME_BETWEEN_IRCDDB_PULLS - elapsed_time)
