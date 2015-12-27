import mock
import socket
import unittest

from .push import Push


RAW_RESPONSE = "blah"


class PushTest(unittest.TestCase):
    def setUp(self):
        self._push = Push(class_name='ParsedStream')
        self._push._request = mock.Mock()

    def test_push(self):
        self._push.push(data={'a': 1})
        self._push._request.assert_called_once_with('POST', '/1/classes/ParsedStream', {'a': 1})

    def test_push_with_socket_error_on_get_existing_record(self):
        self._push._get_existing_record = mock.Mock()
        self._push._get_existing_record.side_effect = socket.gaierror
        self._push.push(data={'a': 1})
        self.assertFalse(self._push._request.called)
        self.assertEqual(self._push._get_existing_record.call_count, 3)
