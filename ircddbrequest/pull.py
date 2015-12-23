import urllib2

URL = "http://live2.ircddb.net:8080/jj3.yaws?p={}"


class PullMessages(object):
    _page = 0

    def __init__(self, start_page=0):
        self._page = start_page

    def _should_ignore(self, message):
        # this would be a duplicate message
        if message.startswith('{}:'.format(self._page)):
            return True

        # irregular messages
        if len(message) < 74 or message[21] == '*':
            return True

        return False

    def pull(self):
        try:
            response = urllib2.urlopen(URL.format(self._page))
            messages = response.read().strip().split('\n')
            return [message for message in messages if not self._should_ignore(message)]
        except urllib2.URLError as e:
            print e
            return []
