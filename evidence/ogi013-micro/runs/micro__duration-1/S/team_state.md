GOAL:
parse_duration() silently accepts invalid input and rejects upper-case units

`django.utils.durations.parse_duration(text)` converts strings such as "1h30m" or "45s" into seconds.

Expected behaviour:
- Units are case-insensitive: parse_duration("2H5M") == 7500.
- The whole string must consist of <number><unit> parts with units h, m, s, each unit at most once,
  in the order h, m, s. Anything else must raise ValueError, e.g. "", "10", "5x", "1h 30m", "30m1h", "1h1h".

Currently "5x" returns 0, "" returns 0 and "2H5M" returns 0 instead of raising or parsing.


POSITIONS:
- S1 (model qwen3.5-9b@default, status open, revision 0)
  diff:
  (no accepted diff yet)
  latest visible test result (tail):
  (none)
OPEN OBJECTIONS / SUGGESTIONS:
(none)
DECISIONS:
(none)