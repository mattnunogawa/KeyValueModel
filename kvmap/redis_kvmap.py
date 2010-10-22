#!/usr/bin/env python
# encoding: utf-8
"""
redis_kvmap.py

Created by Matt Nunogawa on 2010-10-13.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

from kvmap.kvmap_base import KVMapBase
from keyvalue.redis_keyvalue import RedisKeyValue

###############################################################################
class RedisKVMap(KVMapBase):
    """docstring for RedisKVMap"""
    def __init__(self, maptype, uid, **kwargs):
        """docstring for __init__"""
        kvstore = RedisKeyValue(**kwargs)
        KVMapBase.__init__(self, maptype, uid, kvstore)

    ###########################################################################
    @classmethod
    def create_new_sid(cls, maptype, type_hash_sid_key, kvstore):
        """
        get or create a store id for a specific key

        see "A digression. How to get unique identifiers for strings" at the below link for more info
        http://code.google.com/p/redis/wiki/IntroductionToRedisDataTypes
        """
        
        if kvstore.exists(type_hash_sid_key):
            return kvstore.get(type_hash_sid_key)

        # this global key is where we store the next counter to use...
        sid_counter_key = "global:next.%s.sid" % maptype
        
        #since the key doesn't exist, we have to make it.
        next_sid = str(kvstore.incr(sid_counter_key))
        
        did_succeed = kvstore.setnx(type_hash_sid_key, next_sid)
        
        if did_succeed == True:
            # successfully make a new sid, return it.
            return next_sid
        else:
            # some time between when we did incr(sid_counter_key) 
            # and setnx, somebody else used our sid!
            # since our sid is already being used, we have to try again.
            return cls.create_new_sid(maptype, type_hash_sid_key, kvstore)