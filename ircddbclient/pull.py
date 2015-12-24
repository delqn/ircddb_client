import urllib2

from .cache import Cache
from .parser import Parser

EXTERNAL_KEYS = ['when', 'myCall', 'rpt1', 'rpt2', 'urCall', 'flags', 'myRadio', 'dest',
                 'txStats', 'info', 'key']
URL = "http://live2.ircddb.net:8080/jj3.yaws?p={}"


class Pull(object):
    _next_page = 0

    def __init__(self, start_next_page=0):
        self._cache = Cache()
        self._next_page = start_next_page
        self._parser = Parser()

    def _should_ignore_message(self, message):
        # this would be a duplicate message
        if message.startswith('{}:'.format(self._next_page)):
            return True

        # irregular messages (missing myCall)
        if len(message) < 74 or message[21] == '*':
            return True

        return False

    def _pull_and_parse_messages(self):
        try:
            response = urllib2.urlopen(URL.format(self._next_page))
            raw_messages = response.read().strip().split('\n')
            parsed_messages = []
            for raw_message in raw_messages:
                if not self._should_ignore_message(raw_message):
                    parsed_messages.append(self._parser.parse(raw_message))
            if parsed_messages:
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
                self._cache.push(key, (message['txStats'], message['dest']))
            else:
                cached_data = self._cache.pop(key)
                message['info'], message['dest'] = cached_data if cached_data else (None, None)
                filtered_message = {k: v for k, v in message.iteritems() if k in EXTERNAL_KEYS}
                complete_messages.append(filtered_message)
        return complete_messages
