import unittest

from .cache import Cache


class CacheTest(unittest.TestCase):
    def setUp(self):
        self._cache = Cache()

    def test_push_pop(self):
        KEY = 'a'
        self._cache.push(KEY, ('a', 'b'))
        stuff = self._cache.pop(KEY)
        self.assertEqual(stuff, ('a', 'b'))


class CacheGCTest(unittest.TestCase):
    def setUp(self):
        self._cache = Cache(ttl=0, gc_interval=0)

    def test_collect_garbage(self):
        KEY = 'a'
        self._cache.push(KEY, ('a', 'b'))
        stuff = self._cache.pop(KEY)
        self.assertIsNone(stuff)
