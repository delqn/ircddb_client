import unittest
import urllib2

from StringIO import StringIO

from .pull import Pull
from .test_fixtures import (COMBINED_MESSAGES, COMBINED_MESSAGES2, PARSED_MESSAGES,
                            RAW_RESPONSE, RAW_RESPONSE2)


class HTTPHandlerFirstPage(urllib2.HTTPHandler):
    def _urllib2_response(self, req):
        expected_url = 'http://live2.ircddb.net:8080/jj3.yaws?p=0'
        if req.get_full_url() != expected_url:
            raise ValueError('Expected url to be "{}" got "{}"'.format(
                expected_url, req.get_full_url()))
        resp = urllib2.addinfourl(StringIO(RAW_RESPONSE), RAW_RESPONSE, req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp

    def http_open(self, req):
        return self._urllib2_response(req)


class HTTPHandlerSecondPage(urllib2.HTTPHandler):
    def _urllib2_response(self, req):
        expected_url = 'http://live2.ircddb.net:8080/jj3.yaws?p=322945'
        if req.get_full_url() != expected_url:
            raise ValueError('Expected url to be "{}" got "{}"'.format(
                expected_url, req.get_full_url()))
        resp = urllib2.addinfourl(StringIO(RAW_RESPONSE2), RAW_RESPONSE2, req.get_full_url())
        resp.code = 200
        resp.msg = "OK"
        return resp

    def http_open(self, req):
        return self._urllib2_response(req)


class PullAndParseTest(unittest.TestCase):
    def setUp(self):
        url_opener = urllib2.build_opener(HTTPHandlerFirstPage)
        urllib2.install_opener(url_opener)
        self._pull = Pull()

    def test_first_pull(self):
        parsed_messages = self._pull._pull_and_parse_messages()
        self.assertEqual(parsed_messages, PARSED_MESSAGES)


class FullPullTest(unittest.TestCase):
    def setUp(self):
        self._pull = Pull()

    def test_full_pull_paging(self):
        # first pull
        url_opener = urllib2.build_opener(HTTPHandlerFirstPage)
        urllib2.install_opener(url_opener)
        messages = self._pull.pull()
        self.assertEqual(messages, COMBINED_MESSAGES)

        # second pull
        url_opener = urllib2.build_opener(HTTPHandlerSecondPage)
        urllib2.install_opener(url_opener)
        messages = self._pull.pull()
        self.maxDiff = None
        self.assertEqual(messages, COMBINED_MESSAGES2)
