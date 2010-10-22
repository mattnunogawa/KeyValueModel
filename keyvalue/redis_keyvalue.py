#!/usr/bin/env python
# encoding: utf-8
"""
redis_keyvalue.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

from redis import Redis

###############################################################################
class RedisKeyValue:
    "RedisKeyValue"
    
    ###########################################################################
    def __init__(self, **kwargs):
        """ Constructor """
        self.datastore = Redis(**kwargs)
    
    ###########################################################################
    def exists(self, key):
        "returns True if the key exists, False otherwise"
        return self.datastore.exists(key)    

    ###########################################################################
    def get(self, key):
        "Returns the value for the given key, or None if the key doesn't exist"
        return self.datastore.get(key)
    
    ###########################################################################
    def set(self, key, value):
        """
        Sets the value for the given key.
        
        we need to invert the return value however. 
        kvmap will return None on sucess and some kind of error message on 
        failure.
        """
        if self.datastore.set(key, value):
            return None
        else:
            return "set failure"

    ###########################################################################
    def setnx(self, key, value):
        """
        Sets the value for the given key.
        
        Integer reply, specifically:

        1 if the key was set
        0 if the key was not set
        """
        return self.datastore.setnx(key, value)
    
    ###########################################################################
    def incr(self, key, inc_value=1):
        "if the key is an integer, increment by inc_value"
        if inc_value == 1:
            return self.datastore.incr(key)
        else:
            return self.datastore.incr(key, inc_value)
