#!/usr/bin/env python
# encoding: utf-8
"""
kvmap_base.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.

Used to save arbitrary dict-of-dicts style data objects with kv attributes
to a pure keyvalue back-end storage (such as redis or riak).

Example: a user object with the following attributes:

maptype: user
username (also uid): mattn
realname: Matt Nunogawa
email: nobody@example.com

A traditional python dict of dicts would look like:

{mattn:{
maptype:"user",
username:"mattn",
realname:"Matt Nunogawa",
email:"nobody@example.com",
}}

using a kvmap, this would be implemented as such:

object = KVMapRedis("user", "mattn")
object.realname = "Matt Nunogawa"
object.email = "nobody@example.com"

## Acronyms

sid storage_id: integer identifying this map (ie, 23)
uid unique_identifier: arbitrary string serving as unique identifier for this
    map (ie, http://example.com for a feed data object or
    mattn for a user data object)

"""

from hashlib import sha1

MAPTYPE_KEY = "maptype"
SID_KEY = "sid"
UID_KEY = "uid"
KVSTORE_KEY = "kvstore"
TYPE_HASH_SID_KEY = "type_hash_sid_key"

###############################################################################
# KVMapBase
###############################################################################
class KVMapBase:
    """
    abstract base class for an object that implements a pseudo-map type data
    structure on top of a vanilla key-value store
    """

    ###########################################################################
    def __init__(self, maptype, uid, kvmap):
        """
        Get or create a kvmap of type maptype for the specified uid
        example:

        object = KVMapDict("user", "mattn")
        object.realname = "Matt Nunogawa"
        object.email = "nobody@example.com"

        """
        #subclasses should override to provide a valid kvmap

        self.__dict__[MAPTYPE_KEY] = maptype
        self.__dict__[UID_KEY] = uid
        self.__dict__[KVSTORE_KEY] = kvmap
        hexdigest = sha1(uid).hexdigest()
        type_hash_sid_key = "%s:%s:sid" % (maptype, hexdigest)
        self.__dict__[TYPE_HASH_SID_KEY] = type_hash_sid_key

        #first we check to see if the uid exists in the kvmap
        some_sid = kvmap.get(type_hash_sid_key)

        if some_sid == None:
            # make the key and store the unique identifier
            some_sid = self.create_new_sid(maptype, type_hash_sid_key, kvmap)

            self.__dict__[SID_KEY] = some_sid
            # save the ui to kvmap
            self.__setattr__(UID_KEY, uid)
        else:
            self.__dict__[SID_KEY] = some_sid


    ###########################################################################
    def __str__(self): # pragma: no cover
        "nothing fancy here, just for debug"
        return "<kvmap class: %s type:%s sid:%s uid:%s hash_key:%s>" % (
        self.__class__,
        self.maptype,
        self.sid,
        self.uid,
        self.type_hash_sid_key,)

    ###########################################################################
    def __repr__(self): # pragma: no cover
        "simple repr"
        return self.__str__()

    ###########################################################################
    def sid_attr_for_key(self, key):
        "sid_attr_keys = <type>:<sid>:<attr>"
        return "%s:%s:%s" % (
        self.__dict__[MAPTYPE_KEY],
        self.__dict__[SID_KEY],
        key)

    ###########################################################################
    def __getattr__(self, key):
        "getter"
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            return self.kvstore.get(self.sid_attr_for_key(key))

    ###########################################################################
    def __setattr__(self, key, value):
        "setter"
        set_return_val = self.kvstore.set(self.sid_attr_for_key(key), value)
        if set_return_val != None:
            # some kind of error
            print "__setattr__"
            print key
            print value
            print self.kvstore
            print self.sid_attr_for_key(key)
            print "set_return_val"
            print set_return_val
            raise Exception
        else:
            # we successfully added the object, now we can add the key to our
            # set of keys
            pass

    ###########################################################################
    @classmethod
    def create_new_sid(cls, maptype, type_hash_sid_key, 
                       kvmap): # pragma: no cover
        """
        get or create a store id for a specific key.

        Care should be taken that this method is safe for concurrent accesses
        based on the particular kv datastore being used.

        Should return an int.  Typically returns an incremented value, ie, the
        first sid created is 1, the second created is 2, etc.
        """
        #subclasses should override
        print("Should never get here")
        print(cls.__name__)
        print(maptype)
        print(type_hash_sid_key)
        print(kvmap)
        return None

