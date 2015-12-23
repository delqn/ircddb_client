#!/usr/bin/env python

import json
import httplib
import urllib

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('service.conf')
APP_ID = config.get('parse', 'app-id')
KEY = config.get('parse', 'key')


class PushMessage(object):
    HOST = 'api.parse.com'
    PORT = 443
    URL = '/1/classes/{}'
    data = {}
    headers = {}
    class_name = None

    def __init__(self, class_name, data):
        self.class_name = class_name
        self.data = data
        self.headers = {
            "X-Parse-Application-Id": APP_ID,
            "X-Parse-REST-API-Key": KEY,
            "Content-Type": "application/json"}

    def _get_record(self):
        key = self.data.get('key')
        if not key:
            return {}
        connection = httplib.HTTPSConnection(self.HOST, self.PORT)
        connection.connect()
        params = urllib.urlencode({'where': json.dumps({'key': key})})
        url = self.URL.format(self.class_name) + '?{}'.format(params)
        connection.request('GET', url=url, headers=self.headers)
        response = {}
        try:
            response = json.loads(connection.getresponse().read())
        except ValueError as e:
            print e
        if 'error' in response:
            raise ValueError('[Parse Error] ' + response['error'])
        results = response['results']
        return results[0] if results else {}

    def __call__(self):
        objectId = self._get_record().get('objectId')
        if objectId:
            method = 'PUT'
            url = self.URL.format(self.class_name) + '/{}'.format(objectId)
        else:
            method = 'POST'
            url = self.URL.format(self.class_name)
        connection = httplib.HTTPSConnection(self.HOST, self.PORT)
        connection.connect()
        connection.request(method, url, json.dumps(self.data), self.headers)
        response = {}
        try:
            response = json.loads(connection.getresponse().read())
        except ValueError as e:
            print e
        if 'error' in response:
            raise ValueError('[Parse Error] ' + response['error'])
        return response
