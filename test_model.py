#!/usr/bin/env python
# encoding: utf-8
"""
test_model.py

Created by Matt Nunogawa on 2010-10-02.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

import unittest2
from datastore import model
from datastore.constants import REQUIRED
from kvmap.dict_kvmap import DictKVMap

TEST_USERNAME = "TEST_KEY_Q9ScKfgtNhsOdQkZeCBFDhH5WZWUGYkD"

class TestObject(model.ModelObjectBaseClass):
    def __init__(self, username, kvmap=None):
        kvmap = DictKVMap("test_object_maptype", "test_object_uid")
        super(TestObject, self).__init__(username, kvmap)
        custom_fields = {
        "username":"string", 
        "password":"string",
        "email":"string",
        }

        custom_field_options = {
        "username":{REQUIRED:True, },
        "password":{REQUIRED:True, },
        }

        self.fields.update(custom_fields)
        self.field_options.update(custom_field_options)

        self.username = username


class test_model(unittest2.TestCase):
    def setUp(self):
        "setUp is run before every test"
        self.modelObject = TestObject(TEST_USERNAME)

    def tearDown(self):
        "setUp is run before every test"
        self.modelObject = None

    def testKeyError(self):
        "If an attribute is not defined in the self.modelObject.fields dictionary, it should raise KeyError"
        self.assertRaises(KeyError, self.modelObject.__getattr__, "bogusAttribute")

    def testInit(self):        
        self.assertIsNotNone(self.modelObject.ts_add)
        self.assertIsNotNone(self.modelObject.ts_mod)
        self.assertIsNotNone(self.modelObject.username)
        self.assertIsNone(self.modelObject.password)
        self.assertIsNone(self.modelObject.email)

    def testValidateTrueRequiredFields(self):
        self.modelObject.password = 'pass'
        self.assertIsNotNone(self.modelObject.password)
        (validate_result, ignore) = self.modelObject.validate()
        self.assertTrue(validate_result)

    def testValidateTrueOptionalFields(self):
        self.modelObject.email = 'a@b.c'
        self.assertIsNotNone(self.modelObject.email)
        (validate_result, ignore) = self.modelObject.validate()
        self.assertFalse(validate_result)

    def testValidateFalse(self):
        "test our model validate function"
        (validate_result, ignore) = self.modelObject.validate()
        self.assertFalse(validate_result)
        self.modelObject.email = 'a@b.c'
        (validate_result, ignore) = self.modelObject.validate()
        self.assertFalse(validate_result)
    
    
if __name__ == '__main__':  # pragma: no cover
    unittest2.main()