#!/usr/bin/env python
# encoding: utf-8
"""
test_kvmap.py

Created by Matt Nunogawa on 2010-10-08.
Copyright (c) 2010 Matt Nunogawa. All rights reserved.
"""

import unittest2
import hashlib
from kvmap.dict_kvmap import DictKVMap
from kvmap.redis_kvmap import RedisKVMap
from keyvalue.redis_keyvalue import RedisKeyValue

class test_kvmap(unittest2.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    
    def checkCreateNewStorageId(self, kvmap_class):
        """docstring for checkCreateNewStorageId"""
        rangemax = 10
        kvmap = kvmap_class("test_maptype_testCreateNewStorageId", kvmap_class.__name__)

        for i in range(1,rangemax):
            sid = kvmap_class.create_new_sid("test_maptype", "test_maptype:234_fake_sha_%s:sid" % str(i), kvmap.kvstore)
            self.assertEqual(str(i), str(sid), )
            get_sid = kvmap.kvstore.get("test_maptype:234_fake_sha_%s:sid" % str(i))
            self.assertEqual(str(sid), str(get_sid), kvmap_class.__name__)

        self.assertEqual('1', kvmap_class.create_new_sid("test_maptype_2", "test_maptype_2:laskdjflaksdjf_fake_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        self.assertEqual('1', kvmap_class.create_new_sid("test_maptype_3", "test_maptype_2:laskdjflaksdjf_fake_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        self.assertEqual('2', kvmap_class.create_new_sid("test_maptype_2", "test_maptype_2:089u3smnsdksh9_fake_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        
        self.assertEqual(str(rangemax), kvmap.create_new_sid("test_maptype", "test_maptype:234_fake_sha_%s:sid" % str(i+1), kvmap.kvstore), kvmap_class.__name__)
    
    def checkCreateDuplicateStorageId(self, kvmap_class):
        "This used to crash some poor implementations of create_new_sid()"
        kvmap = kvmap_class("test_maptype_checkCreateDuplicateStorageId", kvmap_class.__name__)
        self.assertEqual('1', kvmap_class.create_new_sid("test_maptype_dup", "test_maptype_dup:dupilcate_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        self.assertEqual('1', kvmap_class.create_new_sid("test_maptype_dup", "test_maptype_dup:dupilcate_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        self.assertEqual('1', kvmap_class.create_new_sid("test_maptype_dup", "test_maptype_dup:dupilcate_sha:sid", kvmap.kvstore), kvmap_class.__name__)
        
    
    def checkGettersAndSetters(self, kvmap_class):
        kvmap = kvmap_class("test_maptype_test%s" % kvmap_class.__name__, "test_uid")
        
        test_names = ("bob", "jim")
        for test_name in test_names:
            kvmap.name = test_name
            self.assertEqual(kvmap.name,test_name)        

    def testCreateNewStorageIdRedisCreateSid(self):
        RedisKeyValue().datastore.flushdb()
        self.checkCreateNewStorageId(RedisKVMap)
    def testCreateNewStorageIdRedisDups(self):
        RedisKeyValue().datastore.flushdb()
        self.checkCreateDuplicateStorageId(RedisKVMap)
    
    def testCreateNewStorageIdDict(self):
        self.checkCreateNewStorageId(DictKVMap)
        self.checkCreateDuplicateStorageId(DictKVMap)
        
    def testGettersSetterstKVMap(self):
        kvmap_classes = []
        kvmap_classes.append(DictKVMap)
        kvmap_classes.append(RedisKVMap)
        
        for kvmap_class in kvmap_classes:
            self.checkGettersAndSetters(kvmap_class)

    def testInternalAttributes(self):
        """docstring for testInternalAttributes"""
        maptype = "testInternalAttributes_maptype"
        uid = "dummy_object_uid"
        dummy_object_kvmap = RedisKVMap(maptype, uid)
        
        self.assertEqual(dummy_object_kvmap.uid, uid)
        synthentic_type_hash_sid_key = maptype + ":" + hashlib.sha1(uid).hexdigest() + ":sid"
        self.assertEqual(dummy_object_kvmap.sid, "1")
        self.assertEqual(dummy_object_kvmap.type_hash_sid_key, synthentic_type_hash_sid_key)
        
    
if __name__ == '__main__':
    unittest2.main()