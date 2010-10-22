#!/usr/bin/env python
# encoding: utf-8
"""
TestKeyValue.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

import unittest2
from keyvalue.dict_keyvalue import DictionaryKeyValue
from keyvalue.redis_keyvalue import RedisKeyValue

class TestKeyValue(unittest2.TestCase):
    def setUp(self):
        RedisKeyValue().datastore.flushdb()
    def tearDown(self):
        RedisKeyValue().datastore.flushdb()

    def check_exists(self, kvmap):
        CHECK_EXISTS_KEY = 'check_exists_key'
        self.assertFalse(kvmap.exists(CHECK_EXISTS_KEY))
        kvmap.set(CHECK_EXISTS_KEY, 'bogus')
        self.assertTrue(kvmap.exists(CHECK_EXISTS_KEY))
    
    def check_get(self, kvmap):
        self.assertIsNone(kvmap.get('one'))
    
    def check_set(self, kvmap):
        kvmap.set('two_key', 'two_value')
        self.assertEquals(kvmap.get('two_key'), 'two_value')
        kvmap.set('three', "3")
        self.assertEquals(kvmap.get('three'), "3")
        set_return_val = kvmap.set('three', "3")
        self.assertIsNone(set_return_val)
        

    def testExistsKeyValue(self):
        kvmaps = (DictionaryKeyValue(), RedisKeyValue(), )
        for keyvalue_store in kvmaps:
            self.check_exists(keyvalue_store)
    
    def testGetKeyValue(self):
        kvmaps = (DictionaryKeyValue(), RedisKeyValue(), )
        for keyvalue_store in kvmaps:
            self.check_get(keyvalue_store)

    def testSetKeyValue(self):
        kvmaps = (DictionaryKeyValue(), RedisKeyValue(), )
        for keyvalue_store in kvmaps:
            self.assertIsNone(self.check_set(keyvalue_store))

    def testRedisIncr(self):
        kvmap = RedisKeyValue()
        TEST_INCR_KEY = 'test_incr_key'
        kvmap.set(TEST_INCR_KEY, 3)
        returned_val = kvmap.incr(TEST_INCR_KEY)
        self.assertEqual(returned_val, 4)
        self.assertEqual(kvmap.get(TEST_INCR_KEY), '4')

        returned_val = kvmap.incr(TEST_INCR_KEY, 5)
        self.assertEqual(returned_val, 9)
        self.assertEqual(kvmap.get(TEST_INCR_KEY), '9')
        
    
if __name__ == '__main__':
    unittest2.main()