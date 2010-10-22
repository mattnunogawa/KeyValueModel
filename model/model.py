#!/usr/bin/env python
# encoding: utf-8
"""
model.py

Created by Matt Nunogawa on 2010-10-02.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

import datetime
from datastore.constants import REQUIRED, KVMAP_KEY, FIELDS_KEY, FIELD_OPTIONS_KEY

###############################################################################
class ModelObjectBaseClass(object):
    """docstring for ModelObjectBaseClass"""
    def __init__(self, name, kvmap):
        "Init"
        
        #make sure that kvmap is a kvmap object
        getattr(kvmap, "create_new_sid") # this will fail if kvmap doesn't quack like a kvmap
        getattr(kvmap, "__getattr__") # this will fail if kvmap doesn't quack like a kvmap
        getattr(kvmap, "__setattr__") # this will fail if kvmap doesn't quack like a kvmap
        
        super(ModelObjectBaseClass, self).__init__()

        self.__dict__[FIELDS_KEY] = {
        "ts_add":"datetime", 
        "ts_mod":"datetime",
        }
        
        self.__dict__[FIELD_OPTIONS_KEY] = {
        "ts_add":{REQUIRED:True, },
        "ts_mod":{REQUIRED:True, },
        }
        
        self.__dict__[KVMAP_KEY] = kvmap
        
        now = datetime.datetime.now()
        self.ts_add = now
        self.ts_mod = now
        
        self.name = name
        
    def validate(self):
        """
        Validate all fields
        returns a two item tuple, where the first is a pass/fail bool and the second is a list of dictionaries of problems
        """
        
        for attr_name, options in self.field_options.items():
            attr = self.__getattr__(attr_name)
            for option_name, option_value in options.items():
                if option_name == REQUIRED and option_value == True:
                    if attr == None:
                        return (False, [{"attr_name": attr_name, "option_name":option_name, "option_value":option_value}])
        
        return (True, None)
    
    def save(self):
        "validate and save object.  Returns true on success"
        if self.validate():
            return True
        return False

    def __getattr__(self, name):
        """docstring for __getattr__"""
        try:
            return self.__dict__[name]
        except KeyError:
            if name in self.__dict__[FIELDS_KEY].keys():
                return self.__dict__[KVMAP_KEY].__getattr__(name)
            elif name == 'sid':
                return self.__dict__[KVMAP_KEY].sid
            elif name == 'type_hash_sid_key':
                return self.__dict__[KVMAP_KEY].type_hash_sid_key
            else:
                raise KeyError

    def __setattr__(self, name, value):
        """docstring for __setattr__"""
        if name in self.__dict__[FIELDS_KEY].keys():
            self.__dict__[KVMAP_KEY].__setattr__(name, value)
        else:
            self.__dict__[name] = value