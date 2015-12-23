#!/usr/bin/env python

import datetime
import re
import time
import threading

from ircddbclient import PushMessage, PullMessages

CACHE_TTL = 300  # seconds
SLEEP_SECONDS = 20


def cleanup(string):
    x = re.sub(r'[_]+', ' ', string) if string else string
    return None if x == ' ' else x


def when(string):
    dt = dict(
        year=int(string[:4]),
        month=int(string[4:6]),
        day=int(string[6:8]),
        hour=int(string[8:10]),
        minute=int(string[10:12]),
        second=int(string[12:14]))
    return {
        "__type": "Date",
        "iso": datetime.datetime(**dt).isoformat(),
        }

PIECES = (
    ('rowID', r'^(\d*):', int),
    ('when', r':(\d{14})', when),
    ('myCall', r'^\d*:\d{14}(.{8})', cleanup),
    ('rpt1', r'^\d*:.{22}(.{8})', cleanup),
    ('qsoStarted', r'^\d*:.{30}(\d)', lambda x: x == '0'),
    ('rpt2', r'^\d*:.{31}(.{8})', cleanup),
    ('urCall', r'^\d*:.{39}(.{8})', cleanup),
    ('flags', r'^\d*:.{47}(.{6})', cleanup),
    ('myRadio', r'^\d*:.{53}(.{4})', cleanup),
    ('dest', r'^\d*:.{59}(.{8})', cleanup),
    ('txStats', r'^\d*:.{67}(.{20})', cleanup),
    ('key', r'^\d*:\d{14}(.{33})', lambda x: x[:16] + '1' + x[17:]),
)

cache = {}


def extract(msg):
    _data = {}
    for k, regex, transform in PIECES:
        matches = re.findall(regex, msg)
        value = matches[0] if len(matches) else None
        _data[k] = transform(value) if transform else value
    return _data


def expire_cache():
    keys_to_delete = [k for k, _, _, ts in cache.iteritems() if time.time() - ts > CACHE_TTL]
    for k in keys_to_delete:
        del cache[k]


def push_message(msg):
    PushMessage(class_name='Stream', data={'Message': msg})()


def push_parsed_message(data_):
    PushMessage(class_name='ParsedStream', data=data_)()


if __name__ == '__main__':
    puller = PullMessages()

    while True:
        for message in puller.pull():
            print message

            threading.Thread(target=push_message, args=(message,)).start()

            data = extract(message)
            page = data.pop('rowID')
            key = data.get('key')

            if data.pop('qsoStarted'):
                cache[key] = (data['txStats'], data['dest'], time.time())
            else:
                info, dest, _ = cache.pop(key, [None, None, None])
                data['info'] = info
                data['dest'] = dest
                # threading.Thread(
                #    target=push_parsed_message, args=(data,)).start()
                push_parsed_message(data)

        expire_cache()
        time.sleep(SLEEP_SECONDS)
