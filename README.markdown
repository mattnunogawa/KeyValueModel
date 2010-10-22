KeyValueModel

This is an early attempt at creating a robust model layer (as in model-view-controller) on top of the popular key-value stores (more popularly know as NoSQL databases).

The initial implementation supports Redis, but we plan to add Riak and MongoDB as some point as well.  

Three main components so far:

- keyvalue: an simple api on top of a key value store.  Currently no more that a get/set/exists? layer over the native APIs.
- kvmap: a generic api for creating "maps" on top of a simple kv store.  
- model: a more robust model.  By subclassing the ModelObjectBaseClass, you can add attributes to model objects which are automatically persisted to the kvstore.


Limitations:

- Lots!  Consider this a 0.0.1 release.  
- We are using redis' type:HASH:attribute nomenclature for now, but Riak and MongoDB have better support for JSON as values, that that approach may not scale.  Also redis' new hashmaps may change that approach as well.
- Lots of keys.  Give that kv stores don't usually have things like indices or what not, we have to make them manually and store them next to our data.  This means to store a single data object takes many keys, especially if you need advanced indexing/ordering.
- Missing functionality/DB support

Benefits:

- Fast:  when configured with the right options, kvstores are almost always fast!  you can write to them fast and read from them fast.  (usually searching them is slow, but we have ideas to get around that)
- Flexible:  Key value stores main benefit is flexibility.  By baking in the ability to add an attribute at any time and update gracefully if the attribute isn't found, the kvstore eliminates the need for hard schema and expensive database migrations.