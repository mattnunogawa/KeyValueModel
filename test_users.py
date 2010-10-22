#!/usr/bin/env python
# encoding: utf-8
"""
test_users.py

Created by Matt Nunogawa on 2010-10-14.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

import unittest2
from datastore.users import UserObject
from keyvalue.dict_keyvalue import DictionaryKeyValue

TEST_USERNAME = "TEST_USERNAME_ASJVSK23wkjhs98hlhr23r4t"

TEST_DB = 0

class test_users(unittest2.TestCase):
    def setUp(self):
        "setUp is run before every test"
        self.modelObject = UserObject(TEST_USERNAME, db=TEST_DB)

    def tearDown(self):
        "setUp is run before every test"
        self.modelObject = None

    def testKeyError(self):
        "If an attribute is not defined in the self.modelObject.fields dictionary, it should raise KeyError"
        self.assertRaises(KeyError, self.modelObject.__getattr__, "bogusAttribute")
    
    def testLoadUser(self):
        """docstring for testCreateUser"""
        otherUserObject = UserObject(TEST_USERNAME, db=TEST_DB)
        self.assertEquals(otherUserObject.username, self.modelObject.username)
        self.assertEquals(otherUserObject.sid, self.modelObject.sid)
        self.assertEquals(otherUserObject.type_hash_sid_key, self.modelObject.type_hash_sid_key)
    
    def testUserValidation(self):
        """docstring for testUserValidation"""
        pass
if __name__ == '__main__':
    unittest2.main()