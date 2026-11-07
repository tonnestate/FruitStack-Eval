"""PARALLEL ORGANISATION ORDER P4/P5: the cap on simultaneous provider calls and the timing instrumentation. Engineering only: no hypothesis, no metric.
CallGate: at most MAX_CONCURRENT_CALLS provider calls in flight per episode; queue wait is recorded.
TimingRecorder: per call queue wait, provider latency, retry wait, outcome class; shares of WALL time per category from merged wall-clock intervals (overlapping calls count once), not from sums."""
from __future__ import annotations

import threading
import time
from contextlib import contextmanager

MAX_CONCURRENT_CALLS = 2
CATEGORIES = ("ok", "rate_limit", "provider_unavailable", "unusable_output", "other", "queue_wait", "retry_wait")


def outcome_class(code) -> str:
    c = (code or "").upper()
    if not c:
        return "ok"
    if "RATE_LIMIT" in c:
        return "rate_limit"
    if "UNAVAILABLE" in c:
        return "provider_unavailable"
    if "UNUSABLE" in c:
        return "unusable_output"
    return "other"


def merged_length(intervals) -> float:
    total, end = 0.0, None
    for a, b in sorted(intervals):
        if end is None or a > end:
            total += b - a
            end = b
        elif b > end:
            total += b - end
            end = b
    return total


class TimingRecorder:
    def __init__(self, clock=time.monotonic):
        self.clock, self.t0, self.lock = clock, clock(), threading.Lock()
        self.intervals: dict = {c: [] for c in CATEGORIES}
        self.calls: list = []

    def add(self, category: str, start: float, end: float, **extra) -> None:
        with self.lock:
            self.intervals[category].append((start, end))
            self.calls.append({"category": category, "start": round(start - self.t0, 3), "end": round(end - self.t0, 3), **extra})

    def report(self, wall: float | None = None) -> dict:
        with self.lock:
            wall = wall if wall is not None else self.clock() - self.t0
            sums = {c: round(sum(b - a for a, b in v), 3) for c, v in self.intervals.items()}
            wall_s = {c: round(merged_length(v), 3) for c, v in self.intervals.items()}
            busy = merged_length([i for v in self.intervals.values() for i in v])
            return {"wall_seconds": round(wall, 3), "sum_seconds": sums, "wall_clock_seconds": wall_s,
                    "wall_share": {c: round(s / wall, 4) if wall else 0.0 for c, s in wall_s.items()}, "any_activity_share": round(busy / wall, 4) if wall else 0.0,
                    "calls": len(self.calls), "max_concurrent_calls": MAX_CONCURRENT_CALLS}


class CallGate:
    def __init__(self, cap: int = MAX_CONCURRENT_CALLS, recorder: TimingRecorder | None = None):
        self.cap, self.sem, self.rec = cap, threading.BoundedSemaphore(cap), recorder
        self.lock, self.in_flight, self.max_seen = threading.Lock(), 0, 0

    @contextmanager
    def slot(self):
        t = (self.rec.clock if self.rec else time.monotonic)()
        self.sem.acquire()
        t2 = (self.rec.clock if self.rec else time.monotonic)()
        if self.rec and t2 > t:
            self.rec.add("queue_wait", t, t2)
        with self.lock:
            self.in_flight += 1
            self.max_seen = max(self.max_seen, self.in_flight)
        try:
            yield
        finally:
            with self.lock:
                self.in_flight -= 1
            self.sem.release()
