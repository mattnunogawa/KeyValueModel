#!/usr/bin/env python
# encoding: utf-8
"""
keyvalue_base.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

###############################################################################
class KeyValueBaseClass: #pragma no cover
    """
    Abstract superclass to interface to any kv backend (redis, riak, etc...)
    """
    ###########################################################################
    def __init__(self):
        """ Constructor """
        # subclasses should override
        pass

    ###########################################################################
    def exists(self, key):
        "returns True if the key exists, False otherwise"
        pass
    
    ###########################################################################
    def get(self, key):
        "Returns the value for the given key, or None if the key doesn't exist"
        # subclasses should override
        print self
        print key
        return None
        
    ###########################################################################
    def set(self, key, value):
        "Sets the value for the given key."
        print self
        print key
        print value
        # subclasses should override
        return "Attempting to use abstract base class"
    

    ###########################################################################
    def incr(self, key, inc_value=1):
        "if the key is an integer, increment by inc_value"
        pass
