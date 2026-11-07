GOAL:
merge_intervals() returns wrong results for touching and unsorted intervals

`django.utils.intervals.merge_intervals(intervals)` merges closed intervals given as (start, end) tuples.
Two problems:

1. Intervals that only touch must be merged, because the intervals are closed:
   merge_intervals([(1, 3), (3, 5)]) should return [(1, 5)], but it returns [(1, 3), (3, 5)].
2. The input may come in any order. merge_intervals([(6, 8), (1, 3), (2, 4)]) should return
   [(1, 4), (6, 8)] (sorted by start), but the current result is wrong.

The result must always be sorted by start, and the caller's list must not be modified.


POSITIONS:
- S1 (model qwen2.5-vl-72b@default, status open, revision 0)
  diff:
diff --git a/django/utils/intervals.py b/django/utils/intervals.py
index 4312fe6..a8ca975 100644
--- a/django/utils/intervals.py
+++ b/django/utils/intervals.py
@@ -1,8 +1,9 @@
 def merge_intervals(intervals):
     """Merge overlapping closed intervals given as (start, end) tuples."""
+    sorted_intervals = sorted(intervals)
     merged = []
-    for start, end in intervals:
-        if merged and start < merged[-1][1]:
+    for start, end in sorted_intervals:
+        if merged and start <= merged[-1][1]:
             merged[-1] = (merged[-1][0], max(merged[-1][1], end))
         else:
             merged.append((start, end))

  latest visible test result (tail):
test_disjoint (core_tests.test_intervals.IntervalTests) ... ok
test_empty (core_tests.test_intervals.IntervalTests) ... ok
test_overlapping_sorted (core_tests.test_intervals.IntervalTests) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK

OPEN OBJECTIONS / SUGGESTIONS:
(none)
DECISIONS:
(none)