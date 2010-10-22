#!/usr/bin/env python
# encoding: utf-8
"""
dict_keyvalue.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.


In-memory kv store.  Designed to be used for testing.
"""

from keyvalue.keyvalue_base import KeyValueBaseClass

###############################################################################
class DictionaryKeyValue(KeyValueBaseClass):
    "In-memory kv store.  Designed to be used for testing."
    
    ###########################################################################
    def exists(self, key):
        "returns True if the key exists, False otherwise"
        return key in self.__dict__

    ###########################################################################
    def get(self, key):
        "Returns the value for the given key, or None if the key doesn't exist"
        value_to_return = None
        
        try:
            value_to_return = self.__dict__[key]
        except(KeyError):
            pass
        
        return value_to_return
    
    ###########################################################################
    def set(self, key, value):
        """
        Sets the value for the given key.
        
        Returns None on success or some kind of error string or object if there
        was some kind of error.
        """
        self.__dict__[key] = value
        return None
