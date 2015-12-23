import time
import urllib2

from .parser import Parser

CACHE_TTL = 300  # seconds
CACHE_GC_EVERY_SECONDS = 300  # how often should we run this
EXTERNAL_KEYS = ['when', 'myCall', 'rpt1', 'rpt2', 'urCall', 'flags', 'myRadio', 'dest',
                 'txStats', 'key']
URL = "http://live2.ircddb.net:8080/jj3.yaws?p={}"


# we need a cache since messages arrive in 2 parts:
# on PTT-on and PTT-off.  We combine these into one.
cache = {}


class PullMessages(object):
    _next_page = 0
    _cache_gc_ran = time.time()

    def __init__(self, start_next_page=0):
        self._next_page = start_next_page
        self._parser = Parser()

    def _gc_cache(self):
        if time.time() <= self._cache_gc_ran + CACHE_GC_EVERY_SECONDS:
            return
        keys_to_delete = [k for k, (_, _, ts) in cache.iteritems() if time.time() - ts > CACHE_TTL]
        for k in keys_to_delete:
            del cache[k]
        self._cache_gc_ran = time.time()

    def _should_ignore(self, message):
        # this would be a duplicate message
        if message.startswith('{}:'.format(self._next_page)):
            return True

        # irregular messages
        if len(message) < 74 or message[21] == '*':
            return True

        return False

    def _pull_and_parse_messages(self):
        try:
            response = urllib2.urlopen(URL.format(self._next_page))
            raw_messages = response.read().strip().split('\n')
            parsed_messages = []
            for raw_message in raw_messages:
                if not self._should_ignore(raw_message):
                    print raw_message
                    parsed_messages.append(self._parser.parse(raw_message))
            self._next_page = parsed_messages[-1]['rowID']
            return parsed_messages
        except urllib2.URLError as e:
            print e
            return []

    def pull(self):
        complete_messages = []
        for message in self._pull_and_parse_messages():

            key = message.get('key')
            message_is_incomplete = message.get('qsoStarted')

            if message_is_incomplete:
                cache[key] = (message['txStats'], message['dest'], time.time())
            else:
                info, dest, _ = cache.pop(key, [None, None, None])
                message['info'] = info
                message['dest'] = dest
                # threading.Thread(
                #    target=push_parsed_message, args=(message,)).start()
                filtered_message = {k: v for k, v in message.iteritems() if k in EXTERNAL_KEYS}
                complete_messages.append(filtered_message)

        return complete_messages
