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
- S1 (model nemotron-3.5-lightning@default, status open, revision 0)
  diff:
  (no accepted diff yet)
  latest visible test result (tail):
  (none)
OPEN OBJECTIONS / SUGGESTIONS:
(none)
DECISIONS:
(none)