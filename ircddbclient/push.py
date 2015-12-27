#!/usr/bin/env python

import httplib
import json
import socket
import sys
import time
import urllib

import ConfigParser

config = ConfigParser.ConfigParser()
config.read('service.conf')
APP_ID = config.get('parse', 'app-id')
KEY = config.get('parse', 'key')


class Push(object):
    HOST = 'api.parse.com'
    PORT = 443
    URL = '/1/classes/{}'
    data = {}
    headers = {}
    class_name = None

    def __init__(self, class_name):
        self.class_name = class_name
        self.headers = {
            "X-Parse-Application-Id": APP_ID,
            "X-Parse-REST-API-Key": KEY,
            "Content-Type": "application/json"}

    def _get_existing_record(self, data):
        key = data.get('key')
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
        results = response.get('results')
        return results[0] if results else {}

    def _request(self, method, url, data):
        connection = httplib.HTTPSConnection(self.HOST, self.PORT)
        connection.connect()
        connection.request(method, url, json.dumps(data), self.headers)
        response = connection.getresponse().read()
        try:
            json_response = json.loads(response)
        except ValueError as e:
            # keep going - this happens with Parse once in a while
            json_response = {}
            print 'Parse did not respond with valid JSON: {}'.format(e)
        if 'error' in json_response:
            raise ValueError('[Parse Error] ' + response['error'])
        return json_response

    def push(self, data):
        """Push a new record into the remote DB/Parse.
        Args:
            data (dict)
        Returns:
            json with the Parse response
        """
        for _ in range(3):
            sleep_time = 0
            get_existing_record_err = False
            try:
                objectId = self._get_existing_record(data).get('objectId')
                break
            except socket.error as e:
                get_existing_record_err = True
                sys.stdout.write(
                    '[Push] Error get_existing_record: {}\n'.format(e.message))
                sleep_time += 1
                time.sleep(sleep_time)
        if get_existing_record_err:
            # If we have not been able to obtain an existing record due to an error
            # skip pushing this event.
            sys.stdout.write('[Parse] could not get existing object due to socket errors. '
                             'Skipping this record.\n')
            return {}
        if objectId:
            method = 'PUT'
            url = self.URL.format(self.class_name) + '/{}'.format(objectId)
        else:
            method = 'POST'
            url = self.URL.format(self.class_name)
        return self._request(method, url, data)
