import time

TTL = 300  # seconds
GC_INTERVAL = 300  # seconds


class Cache(object):

    # we need a cache since messages arrive in 2 parts:
    # on PTT-on and PTT-off.  We combine these into one.
    _cache = {}
    _last_time_gc_ran = time.time()

    def __init__(self, ttl=None, gc_interval=None):
        self._ttl = ttl if ttl is not None else TTL
        self._gc_interval = gc_interval if gc_interval is not None else GC_INTERVAL

    def _collect_garbage(self):
        if time.time() <= self._last_time_gc_ran + self._gc_interval:
            return
        expired_keys = [
            key for key, (_, ts) in self._cache.iteritems()
            if time.time() - ts > self._ttl]
        for expired_key in expired_keys:
            del self._cache[expired_key]
        self._last_time_gc_ran = time.time()

    def push(self, key, stuff):
        self._cache[key] = (stuff, time.time())
        self._collect_garbage()

    def pop(self, key):
        stuff, _ = self._cache.pop(key, [None, None])
        return stuff
