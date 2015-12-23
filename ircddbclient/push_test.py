import mock
import unittest

from .push import Push


RAW_RESPONSE = "blah"


class PushTest(unittest.TestCase):
    def setUp(self):
        self._push = Push(class_name='ParsedStream')
        self._push._request = mock.Mock()

    def test_push_pop(self):
        self._push.push(data={'a': 1})
        self._push._request.assert_called_once_with(
            'POST', '/1/classes/ParsedStream', '{"a": 1}')
