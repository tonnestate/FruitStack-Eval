GOAL:
LRUCache evicts recently used keys and misbehaves for capacity 0 and updates

`django.utils.lru.LRUCache` is meant to be a least-recently-used cache, but:

1. get() of an existing key must mark it as most recently used. With capacity 2:
   put("a"), put("b"), get("a"), put("c") must evict "b", not "a". Today "a" is evicted.
2. put() of an existing key updates the value and also marks the key as most recently used.
   With capacity 2: put("a",1), put("b",2), put("a",3), put("c",4) must keep "a" (value 3) and evict "b".
3. A cache with capacity 0 stores nothing: after put("a", 1), len(cache) == 0 and get("a") is None.
   A negative capacity must raise ValueError in the constructor.


POSITIONS:
- S1 (model qwen2.5-vl-72b@default, status open, revision 0)
  diff:
diff --git a/django/utils/lru.py b/django/utils/lru.py
index 5dd51cf..5315758 100644
--- a/django/utils/lru.py
+++ b/django/utils/lru.py
@@ -5,13 +5,22 @@ class LRUCache:
     """A least-recently-used cache holding at most `capacity` entries."""
 
     def __init__(self, capacity):
+        if capacity < 0:
+            raise ValueError("Capacity must be non-negative")
         self.capacity = capacity
         self._data = OrderedDict()
 
     def get(self, key, default=None):
-        return self._data.get(key, default)
+        if key in self._data:
+            self._data.move_to_end(key)
+            return self._data[key]
+        return default
 
     def put(self, key, value):
+        if self.capacity == 0:
+            return
+        if key in self._data:
+            self._data.move_to_end(key)
         self._data[key] = value
         if len(self._data) > self.capacity:
             self._data.popitem(last=False)

  latest visible test result (tail):
tests (unittest.loader._FailedTest) ... ERROR

======================================================================
ERROR: tests (unittest.loader._FailedTest)
----------------------------------------------------------------------
ImportError: Failed to import test module: tests
Traceback (most recent call last):
  File "/root/.local/share/uv/python/cpython-3.8-linux-x86_64-gnu/lib/python3.8/unittest/loader.py", line 154, in loadTestsFromName
    module = __import__(module_name)
ModuleNotFoundError: No module named 'core_tests.tests'


----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (errors=1)

- S2 (model north-mini-code@default, status open, revision 0)
  diff:
  (no accepted diff yet)
  latest visible test result (tail):
  (none)
- S3 (model north-mini-code@default, status open, revision 0)
  diff:
  (no accepted diff yet)
  latest visible test result (tail):
  (none)
OPEN OBJECTIONS / SUGGESTIONS:
- O1 on S3 from north [suggestion, UNGROUNDED, OPEN]: ISSUES: FOUND
The current implementation of LRUCache does not handle the specified requirements correctly:
1. The `get()` method does not mark the accessed key as most recently used.
2. The `put()` method does not update the value and mark the key as most recently used when updating an existing key.
3. The cache does not properly handle a capacity of 0, storing items despite the zero capacity.
4. There is no validation for negative capacity values in the constructor.
The existing tests do not cover these issues, which need to be addressed.
- O2 on S3 from qwen3.5 [suggestion, UNGROUNDED, OPEN]: ISSUES: FOUND
The current implementation of LRUCache has several issues based on the requirements and the recent actions taken:
1. The `get()` method does not mark the accessed key as most recently used. This needs to be fixed by moving the accessed key to the end of the ordered dictionary.
2. The `put()` method does not update the value and mark the key as most recently used when updating an existing key. This should be handled similarly to the `get()` method.
3. The cache does not properly handle a capacity of 0, storing items despite the zero capacity. This behavior needs to be corrected so that no items are stored when the capacity is 0.
4. The constructor now correctly raises a ValueError for negative capacity values, but this change alone does not address all the issues mentioned. Further changes are required to meet the specified requirements.
DECISIONS:
- S1 produced its first gate-accepted diff (29ed13ea46)