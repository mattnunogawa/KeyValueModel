#!/usr/bin/env python
# encoding: utf-8
"""
users.py

Created by Matt Nunogawa on 2010-09-30.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

from datastore.model import ModelObjectBaseClass
from datastore.constants import REQUIRED, KVMAP_KEY
from kvmap.redis_kvmap import RedisKVMap


HOST = 'localhost'
PORT = 6379
DB = 1

MAPTYPE = "user"

###############################################################################
class UserObject(ModelObjectBaseClass):
    """docstring for UserObject"""
    def __init__(self, username, kvmap=None, host=HOST, port=PORT, db=DB):
        
        #add this user to our datastore
        if kvmap == None: # pragma: no cover
            self.__dict__[KVMAP_KEY] = RedisKVMap(MAPTYPE, username, host=host, port=port, db=db)
        else:
            self.__dict__[KVMAP_KEY] = kvmap
    
        super(UserObject, self).__init__(username, self.__dict__[KVMAP_KEY])
        
    
        user_fields = {
        "username":"string", 
        "password":"string",
        "realname":"string",
        "email":"string",
        }
        
        user_field_options = {
        "username":{REQUIRED:True, },
        "password":{REQUIRED:True, },
        }
        
        self.fields.update(user_fields)
        self.field_options.update(user_field_options)
        
        self.username = username
