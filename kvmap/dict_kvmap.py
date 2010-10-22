#!/usr/bin/env python
# encoding: utf-8
"""
dict_kvmap.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

from kvmap.kvmap_base import KVMapBase
from keyvalue.dict_keyvalue import DictionaryKeyValue

###############################################################################
class DictKVMap(KVMapBase):
    """docstring for DictKVMap"""
    def __init__(self, maptype, uid):
        """docstring for __init__
        
        maptype is the type of map
        uid is a unique identifier
        
        """
        
        kvstore = DictionaryKeyValue()
        KVMapBase.__init__(self, maptype, uid, kvstore)

    ###########################################################################
    @classmethod
    def create_new_sid(cls, maptype, type_hash_sid_key, kvstore):
        """docstring for create_new_sid
        This class is meant primarily for testing
        This method is likely NOT concurrent or persitant
        """
        
        if kvstore.exists(type_hash_sid_key):
            return kvstore.get(type_hash_sid_key)
        
        # this global key is where we store the next counter to use...
        sid_counter_key = "global:next.%s.sid" % maptype 
        
        if kvstore.exists(sid_counter_key):
            next_sid = str(int(kvstore.get(sid_counter_key)) + 1)
        else:
            next_sid = '1'

        kvstore.set(sid_counter_key, next_sid)
        
        #since the key doesn't exist, we have to make it.
        kvstore.set(type_hash_sid_key, next_sid)
        
        return next_sid