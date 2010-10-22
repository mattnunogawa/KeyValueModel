#!/usr/bin/env python
# encoding: utf-8
"""
redis_hashlayer_keyvalue.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.

Based on blog entry:
http://antirez.com/post/redis-weekly-update-7.html

"""

from keyvalue.redis_keyvalue import RedisKeyValue
import hashlib

def get_hash_name(key):
    "get_hash_name"
    return hashlib.sha1(key).hexdigest()[:4]

###############################################################################
class RedisHashLayerKeyValue(RedisKeyValue):
    """docstring for RedisHashLayerKeyValue"""
    def __init__(self, **kwargs):
        "__init__, just passing along kwargs"
        RedisKeyValue.__init__(**kwargs)

    def exists(self, key):
        "exists"
        return self.datastore.hexists(get_hash_name(key), key)

    def get(self, key):
        "Returns the value for the given key, or None if the key doesn't exist"
        return self.datastore.hget(get_hash_name(key), key)

    def set(self, key, value):
        "Sets the value for the given key."
        self.datastore.hset(get_hash_name(key), key, value)