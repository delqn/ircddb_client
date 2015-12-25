#!/usr/bin/env python

import argparse
import time

from multiprocessing import Pool

from ircddbclient import Push, Pull

MIN_TIME_BETWEEN_IRCDDB_PULLS = 30


def push(message):
    print 'pushing {}'.format(message)
    Push(class_name='ParsedStream').push(message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--multiprocessing', type=bool, default=False,
                        help='Enable multiprocessing. Disabled by default.')
    args = parser.parse_args()
    puller = Pull()
    while True:
        start_time = time.time()
        messages = puller.pull()
        if args.multiprocessing:
            pool = Pool(5)
            pool.map(push, messages)
        else:
            for msg in messages:
                push(msg)

        # take it easy on the ircDDB system
        elapsed_time = time.time() - start_time
        if elapsed_time < MIN_TIME_BETWEEN_IRCDDB_PULLS:
            time.sleep(MIN_TIME_BETWEEN_IRCDDB_PULLS - elapsed_time)
