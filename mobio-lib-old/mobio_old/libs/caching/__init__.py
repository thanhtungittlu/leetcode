#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: locnh
    Company: MobioVN
    Email: locnh@mobio.vn
    Date created: 04/10/2019
"""
import configparser
import json
import threading
import time
import weakref
from collections import OrderedDict
from functools import wraps

import redis
import logging

import sys

logger = logging.getLogger(__name__)


class StoreType:
    LOCAL = 1
    REDIS = 2


class RedisType:
    REPLICA = 1
    CLUSTER = 2


CACHE_MAX_SIZE_DEFAULT = 1024000
EXPIRATION_DEFAULT = 60 * 60
EXPIRATION_NEVER = -1


class LruCache:
    def __init__(self, max_size=CACHE_MAX_SIZE_DEFAULT,
                 expiration=EXPIRATION_DEFAULT,
                 store_type=StoreType.LOCAL,
                 config_file_name=None, redis_uri=None, cache_prefix=None,
                 redis_cluster_uri=None, redis_type=RedisType.REPLICA):
        self.max_size = max_size
        self.expiration = expiration
        self.store_type = store_type
        self.config_file_name = config_file_name
        self._accept_none = None
        self.cache_prefix = cache_prefix
        if self.store_type == StoreType.LOCAL:
            self.cache = LRUCacheDict(self.max_size, self.expiration)
        elif self.store_type == StoreType.REDIS:
            if self.config_file_name is None and not cache_prefix:
                raise ValueError('config_file_name must not be None if store_type is REDIS and cache_prefix is empty')
            self.cache = RedisCacheDict(self.config_file_name, self.max_size, self.expiration, redis_uri=redis_uri,
                                        cache_prefix=self.cache_prefix,
                                        redis_cluster_uri=redis_cluster_uri, redis_type=redis_type)
        else:
            raise NotImplementedError('store_type=%s' % self.store_type)

    def accept_none(self, accept_none):
        self._accept_none = accept_none

    def add(self, prefix_key=None, expiration=None):
        """
        # >>> @lru_cache_function(3, 1)
        # ... def f(x):
        # ...    print "Calling f(" + str(x) + ")"
        # ...    return x
        # >>> f(3)
        # Calling f(3)
        # 3
        # >>> f(3)
        # 3
        """

        def wrapper(func):
            return LRUCachedFunction(func, prefix_key, self.cache, expiration=expiration, accept_none=self._accept_none)

        return wrapper

    def add_for_class(self, prefix_key=None, expiration=None):
        """
        # >>> @lru_cache_function(3, 1)
        # ... def f(x):
        # ...    print "Calling f(" + str(x) + ")"
        # ...    return x
        # >>> f(3)
        # Calling f(3)
        # 3
        # >>> f(3)
        # 3
        """

        def wrapper(func):
            me = self

            @wraps(func)
            def wrapped(my_self, *args, **kwargs):
                if me.cache is None:
                    if me.store_type == StoreType.LOCAL:
                        me.cache = LRUCacheDict()
                    elif me.store_type == StoreType.REDIS:
                        if me.config_file_name is None:
                            raise ValueError('config_file_name must not be None if store_type is REDIS')
                        self.cache = RedisCacheDict(me.config_file_name, cache_prefix=me.cache_prefix)
                    else:
                        raise NotImplementedError('store_type=%s' % me.store_type)

                if isinstance(func, staticmethod):
                    func_name = func.__func__.__name__
                else:
                    func_name = func.__name__
                name = prefix_key if prefix_key else "%s.%s" % (type(my_self).__name__, func_name)

                key = name + "#" + repr((args, kwargs))

                try:
                    # print("cache key", key)
                    return me.cache[key]
                except KeyError:
                    try:
                        value = func(my_self, *args, **kwargs)
                    except TypeError as e:
                        if 'missing 1 required positional argument' in str(e):
                            raise KeyError('you must use add function')
                        else:
                            raise e
                    # me.cache[key] = value
                    me.cache.set_item(key, value, expiration, me._accept_none)
                    return value

            return wrapped

        return wrapper

    def delete_cache_by_key(self, key):
        if self.cache:
            return self.cache.delete_item(key)
        return -1

    def delete_cache_by_pattern(self, pattern):
        if self.cache and isinstance(self.cache, RedisCacheDict):
            return self.cache.delete_by_pattern(pattern)
        return -1

class LRUCachedFunction(object):
    """
    Một chức năng ghi nhớ, được hỗ trợ bởi một bộ nhớ cache LRU.

    """

    def __init__(self, a_function, prefix_key=None, cache=None, store_type=StoreType.LOCAL, config_file_name=None,
                 expiration=EXPIRATION_DEFAULT, accept_none=None, cache_prefix=None):
        self.expiration = expiration
        self._accept_none = accept_none
        if cache:
            self.cache = cache
        else:
            if store_type == StoreType.LOCAL:
                self.cache = LRUCacheDict()
            elif store_type == StoreType.REDIS:
                if config_file_name is None and not cache_prefix:
                    raise ValueError('config_file_name must not be None if store_type is REDIS')
                self.cache = RedisCacheDict(config_file_name, cache_prefix=cache_prefix)
            else:
                raise NotImplementedError('store_type=%s' % store_type)
        self.function = a_function
        if isinstance(self.function, staticmethod):
            self.__name__ = prefix_key if prefix_key else self.function.__func__.__name__
        else:
            self.__name__ = prefix_key if prefix_key else self.function.__name__

    def __call__(self, *args, **kwargs):
        # Về nguyên tắc một repr python (...) không nên trả về bất kỳ ký tự '#'.
        key = self.__name__ + "#" + repr((args, kwargs))

        try:
            # print("cache key", key)
            return self.cache[key]
        except KeyError:
            try:
                # khi chạy cython phải thực hiện call hàm static theo kiêu meta-class.
                # còn trên python gọi như bình thường
                if isinstance(self.function, staticmethod):
                    value = self.function.__func__(*args, **kwargs)
                else:
                    value = self.function(*args, **kwargs)
            except TypeError as e:
                if 'missing 1 required positional argument' in str(e):
                    raise KeyError('you must use add_for_class function')
                else:
                    raise e
            # self.cache[key] = value
            self.cache.set_item(key, value, self.expiration, self._accept_none)
            return value


def _lock_decorator(func):
    """
    If the LRUCacheDict is concurrent, then we should lock in order to avoid
    conflicts with threading, or the ThreadTrigger.
    """

    def withlock(self, *args, **kwargs):
        if self.concurrent:
            with self._rlock:
                return func(self, *args, **kwargs)
        else:
            return func(self, *args, **kwargs)

    # withlock.__name__ == func.__name__
    return withlock


class LRUCacheDict(object):
    """ A dictionary-like object, supporting LRU caching semantics.

    >>> d = LRUCacheDict(max_size=3, expiration=3)
    >>> d['foo'] = 'bar'
    >>> d['foo']
    'bar'
    >>> import time
    >>> time.sleep(4) # 4 seconds > 3 second cache expiry of d
    >>> d['foo']
    Traceback (most recent call last):
        ...
    KeyError: 'foo'
    >>> d['a'] = 'A'
    >>> d['b'] = 'B'
    >>> d['c'] = 'C'
    >>> d['d'] = 'D'
    >>> d['a'] # Should return value error, since we exceeded the max cache size
    Traceback (most recent call last):
        ...
    KeyError: 'a'

    By default, this cache will only expire items whenever you poke it - all methods on
    this class will result in a cleanup. If the thread_clear option is specified, a background
    thread will clean it up every thread_clear_min_check seconds.

    If this class must be used in a multithreaded environment, the option concurrent should be
    set to true. Note that the cache will always be concurrent if a background cleanup thread
    is used.
    """

    def __init__(self, max_size=CACHE_MAX_SIZE_DEFAULT, expiration=EXPIRATION_DEFAULT,
                 thread_clear=False,
                 concurrent=False):
        self.max_size = max_size
        self.expiration = expiration
        self.__values = {}
        self.__expire_times = OrderedDict()
        self.__access_times = OrderedDict()
        self.thread_clear = thread_clear
        self.concurrent = concurrent or thread_clear
        if self.concurrent:
            self._rlock = threading.RLock()
        if thread_clear:
            et = self.EmptyCacheThread(self)
            et.start()

    class EmptyCacheThread(threading.Thread):
        daemon = True

        def __init__(self, cache, peek_duration=60):
            # me = self
            #
            # def kill_self(o):
            #     me
            self.ref = weakref.ref(cache)
            self.peek_duration = peek_duration
            super(LRUCacheDict.EmptyCacheThread, self).__init__()

        def run(self):
            while self.ref():
                c = self.ref()
                if c:
                    next_expire = c.cleanup()
                    if next_expire is None:
                        time.sleep(self.peek_duration)
                    else:
                        time.sleep(next_expire + 1)
                        # c = None

    @_lock_decorator
    def size(self):
        return len(self.__values)

    @_lock_decorator
    def clear(self):
        """
        Clears the dict.

        >>> d = LRUCacheDict(max_size=3, expiration=1)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> d.clear()
        >>> d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        self.__values.clear()
        self.__expire_times.clear()
        self.__access_times.clear()

    def __contains__(self, key):
        return key in self.__values

    @_lock_decorator
    def has_key(self, key):
        """
        This method should almost NEVER be used. The reason is that between the time
        has_key is called, and the key is accessed, the key might vanish.

        You should ALWAYS use a try: ... except KeyError: ... block.

        >>> d = LRUCacheDict(max_size=3, expiration=1)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> import time
        >>> if d.has_key('foo'):
        ...    time.sleep(2) #Oops, the key 'foo' is gone!
        ...    d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        return key in self.__values

    @_lock_decorator
    def __setitem__(self, key, value):
        t = int(time.time())
        self.__delete__(key)
        self.__values[key] = value
        self.__access_times[key] = t
        self.__expire_times[key] = t + self.expiration
        self.cleanup()

    @_lock_decorator
    def set_item(self, key, value, expiration=None, accept_none=None):
        if not expiration:
            expiration = self.expiration
        if accept_none is not None:
            if not value and accept_none == False:
                print("value is None => ignore")
                return
        t = int(time.time())
        self.__delete__(key)
        self.__values[key] = value
        self.__access_times[key] = t
        self.__expire_times[key] = t + expiration
        self.cleanup()

    @_lock_decorator
    def __getitem__(self, key):
        t = int(time.time())
        del self.__access_times[key]
        self.__access_times[key] = t
        self.cleanup()
        return self.__values[key]

    @_lock_decorator
    def getitem(self, key):
        t = int(time.time())
        del self.__access_times[key]
        self.__access_times[key] = t
        self.cleanup()
        return self.__values.get(key)

    @_lock_decorator
    def __delete__(self, key):
        if key in self.__values:
            del self.__values[key]
            del self.__expire_times[key]
            del self.__access_times[key]

    @_lock_decorator
    def delete_item(self, *keys):
        for key in keys:
            if key in self.__values:
                del self.__values[key]
                del self.__expire_times[key]
                del self.__access_times[key]

    @_lock_decorator
    def cleanup(self):
        if self.expiration is None:
            return None
        t = int(time.time())
        # Delete expired
        next_expire = None
        keys = list(self.__expire_times.keys())
        for k in keys:
            value = self.__expire_times.get(k, None)
            if value and value < t:
                self.__delete__(k)
            else:
                next_expire = value
                break

        # If we have more than self.max_size items, delete the oldest
        while len(self.__values) > self.max_size:
            keys = list(self.__access_times.keys())
            for k in keys:
                self.__delete__(k)
                break
        if not (next_expire is None):
            return next_expire - t
        else:
            return None


class REDIS:
    HOST = 'host'
    PORT = 'port'
    EXPIRED_TIME_FOR_KEY = 'expired_time_for_key'
    CACHE_PREFIX = 'cache_prefix'


class RedisCacheDict:
    """ A dictionary-like object, supporting LRU caching semantics.
    #
    # >>> d = RedisCacheDict(max_size=3, expiration=3)
    # >>> d['foo'] = 'bar'
    # >>> d['foo']
    # 'bar'
    # >>> import time
    # >>> time.sleep(4) # 4 seconds > 3 second cache expiry of d
    # >>> d['foo']
    # Traceback (most recent call last):
    #     ...
    # KeyError: 'foo'
    # >>> d['a'] = 'A'
    # >>> d['b'] = 'B'
    # >>> d['c'] = 'C'
    # >>> d['d'] = 'D'
    # >>> d['a'] # Should return value error, since we exceeded the max cache size
    # Traceback (most recent call last):
        ...
    KeyError: 'a'

    By default, this cache will only expire items whenever you poke it - all methods on
    this class will result in a cleanup. If the thread_clear option is specified, a background
    thread will clean it up every thread_clear_min_check seconds.

    If this class must be used in a multithreaded environment, the option concurrent should be
    set to true. Note that the cache will always be concurrent if a background cleanup thread
    is used.
    """

    def __init__(self, config_file_name, max_size=CACHE_MAX_SIZE_DEFAULT, expiration=EXPIRATION_DEFAULT,
                 concurrent=False, redis_uri=None, cache_prefix=None,
                 redis_cluster_uri=None, redis_type=RedisType.REPLICA
                 ):
        self.max_size = max_size
        self.expiration = expiration

        config = None
        if config_file_name:
            config = configparser.ConfigParser()
            config.read(config_file_name, 'utf-8')

        if isinstance(redis_type, str):
            value_redis_type = int(redis_type)
        else:
            value_redis_type = redis_type

        if value_redis_type == RedisType.CLUSTER:
            if redis_cluster_uri:
                self._redis = redis.from_url(redis_uri)
            else:
                from redis.cluster import RedisCluster as Redis
                self._redis = Redis.from_url(redis_cluster_uri)
        else:
            self._redis = redis.from_url(redis_uri)
            # if not redis_uri:
            #     self.host = config.get(REDIS.__name__, REDIS.HOST)
            #     self.port = config.get(REDIS.__name__, REDIS.PORT)
            #     self._redis = redis.Redis(host=self.host, port=self.port, db=0)
            # else:
            #     self._redis = redis.from_url(redis_uri)

        if config:
            try:
                self.cache_prefix = config.get(REDIS.__name__, REDIS.CACHE_PREFIX)
            except Exception as e:
                print(e)
                if cache_prefix:
                    self.cache_prefix = cache_prefix
                else:
                    raise e

        elif cache_prefix:
            self.cache_prefix = cache_prefix
        else:
            raise ValueError('config_file_name or cache_prefix must not be None if store_type is REDIS')

        self.concurrent = concurrent
        if self.concurrent:
            self._rlock = threading.RLock()

        self.is_redis_ready = self.check_connection_available()

    def norm_key(self, key):
        return self.cache_prefix + "#" + key

    def check_connection_available(self):
        try:
            self._redis.ping()
            return True
        except redis.ConnectionError:
            print("check_connection_available: redis connection not available: host = %s, port = %s"
                  % (self.host, self.port))
            return False

    @_lock_decorator
    def size(self):
        return self._redis.dbsize()

    @_lock_decorator
    def clear(self):
        """
        Clears the dict. Không thực hiện do trong Redis có thể dùng chung nhiều dự án
        """
        pass

    def __contains__(self, key):
        return self._redis.exists(self.norm_key(key))

    @_lock_decorator
    def has_key(self, key):
        """
        This method should almost NEVER be used. The reason is that between the time
        has_key is called, and the key is accessed, the key might vanish.

        You should ALWAYS use a try: ... except KeyError: ... block.

        >>> d = LRUCacheDict(max_size=3, expiration=1)
        >>> d['foo'] = 'bar'
        >>> d['foo']
        'bar'
        >>> import time
        >>> if d.has_key('foo'):
        ...    time.sleep(2) #Oops, the key 'foo' is gone!
        ...    d['foo']
        Traceback (most recent call last):
        ...
        KeyError: 'foo'
        """
        return self._redis.exists(self.norm_key(key))

    @_lock_decorator
    def __setitem__(self, key, value, expiration=None, accept_none=None):
        if self.is_redis_ready:
            if accept_none is not None:
                if not value and not accept_none:
                    print("value is None => ignore")
                    return
            self._redis.set(key, value, self.expiration)
            self.cleanup()
        else:
            print("REDIS not ready for cache")

    @_lock_decorator
    def set_item(self, key, value, expiration=None, accept_none=None):
        if not expiration:
            expiration = self.expiration
        if self.is_redis_ready:
            if accept_none is not None:
                if not value and not accept_none:
                    print("value is None => ignore")
                    return

            _key = self.norm_key(key)
            if expiration == EXPIRATION_NEVER:
                try:
                    self._redis.set(_key, json.dumps(value), None)
                except:
                    pass
            else:
                try:
                    self._redis.set(_key, json.dumps(value), expiration)
                except:
                    pass
            self.cleanup()
        else:
            print("REDIS not ready for cache")

    @_lock_decorator
    def __getitem__(self, key):
        if self.is_redis_ready:
            value = self._redis.get(self.norm_key(key))
            if not value:
                raise KeyError
            if sys.version_info.major < 3:
                return json.loads(value.decode("utf-8"), encoding="utf-8")
            elif sys.version_info.major == 3:
                if sys.version_info.minor <= 8:
                    return json.loads(value.decode("utf-8"), encoding="utf-8")
                else:
                    return json.loads(value.decode("utf-8"))
            else:
                return json.loads(value.decode("utf-8"))
        raise KeyError

    @_lock_decorator
    def __delete__(self, key):
        self._redis.delete(self.norm_key(key))

    @_lock_decorator
    def delete_item(self, keys):
        if self.is_redis_ready:
            _keys = list(map(lambda x: self.norm_key(x), keys))
            for k in _keys:
                self._redis.delete(k)
            return True
        raise KeyError

    @_lock_decorator
    def delete_by_pattern(self, pattern):
        if self.is_redis_ready:
            keys = self._redis.keys(pattern)
            for k in keys:
                logger.debug("m_caching::delete_by_pattern: delete key: %s" % k)
                self._redis.delete(k)
            return True
        raise KeyError

    @_lock_decorator
    def cleanup(self):
        # keys = self._redis.keys()
        # a_range = self.size() - self.max_size
        # if a_range > 0:
        #     self._redis.delete(keys[0:a_range])
        pass


lru_local_cache = LruCache()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    __store_type = StoreType.REDIS
    __file_config = '/Volumes/ML_encrypt/Gitbucket/m-caching/tests/cache.conf'

    lru_cache = LruCache(store_type=__store_type, redis_uri="redis://redis-server:6379/0",cache_prefix="hihi",
                         config_file_name='/Volumes/ML_encrypt/Gitbucket/m-caching/tests/cache.conf')
    lru_cache.accept_none(False)

    class TestCache:
        # @staticmethod
        @lru_cache.add_for_class()
        def test(self, x):
            print("TestCache::test param %s" % x)
            return x + 1

        @staticmethod
        @lru_cache.add()
        def test_static(x):
            print("TestCache::test_static test param %s" % x)
            return x + 1


    @lru_cache.add()
    def some_expensive_method(x):
        print("Calling some_expensive_method(" + str(x) + ")")
        return x + 200


    @lru_cache.add()
    def obj_some_expensive_method(x):
        print("Calling some_expensive_method(" + str(x) + ")")
        return {"title": "data", "value": x}

    @lru_cache.add()
    def test_empty_string():
        print("test_empty_string()")
        return ""


    @lru_cache.add()
    def test_empty_array():
        print("test_empty_array()")
        return []


    @lru_cache.add()
    def test_zero_value():
        print("test_zero_value()")
        return 0

    # This will print "Calling f(3)", will return 3
    print('cache value', some_expensive_method(3))
    # This will not print anything, but will return 3 (unless 15 minutes
    # have passed between the first and second function call).
    print('get cache value', some_expensive_method(3))

    # cache new value
    print('cache new value', some_expensive_method(4))
    # get cache new value
    print('get cache new value', some_expensive_method(4))

    # get cache old value
    print('get cache old value', some_expensive_method(3))

    d = LRUCacheDict(max_size=3, expiration=3)
    d['foo'] = 'bar'
    print(d['foo'])  # prints "bar"

    # 4 seconds > 3 second cache expiry of d
    time.sleep(4)
    # KeyError
    try:
        print(d['foo'])
    except KeyError:
        print("not have foo")

    obj = obj_some_expensive_method(3)
    print(obj)

    obj['title'] = "new value"

    print(obj_some_expensive_method(3))
    print("test_empty_string: " + test_empty_string())
    print("test_empty_array: " + str(test_empty_array()))
    print("test_zero_value: " + str(test_zero_value()))

    tc = TestCache()
    tt = tc.test(1)
    tt += tc.test(2)
    tt += tc.test(2)
    tt += TestCache.test_static(2)
    tt += tc.test_static(2)

    print(tt)
    time.sleep(5)
    lru_cache.delete_cache_by_pattern("locnh*")