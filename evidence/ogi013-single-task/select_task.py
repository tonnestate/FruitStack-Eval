#!/usr/bin/env python3
"""OGI-013 SINGLE-TASK selection (frozen BEFORE any model ran on it). Source: SWE-bench Lite (princeton-nlp/SWE-bench_Lite, test split, 300 instances; executable FAIL_TO_PASS / PASS_TO_PASS tests).
Pool rule (metadata only; no model output, no result of any kind is read): pure-Python repositories installable without compiled extensions (django, sympy, pytest, requests, flask); SWE-bench
Lite contains only single-file gold patches, so "reasoning across several components" is operationalised as a gold patch with >= 3 hunks and >= 40 changed lines, and >= 2 FAIL_TO_PASS tests. Selection: the smallest sha256("OGI013-SINGLE-TASK-1|" + instance_id)."""
import hashlib, json, re
t = json.load(open("swe_bench_lite.json"))
REPOS = {"django/django", "sympy/sympy", "pytest-dev/pytest", "psf/requests", "pallets/flask"}
def src_files(p): return [f for f in re.findall(r"^diff --git a/(\S+)", p, re.M) if "/tests/" not in f and not f.startswith("tests/") and "test_" not in f.rsplit("/", 1)[-1]]
def hunks(p): return len(re.findall(r"^@@ ", p, re.M))
def changed(p): return sum(1 for l in p.splitlines() if l[:1] in "+-" and l[:3] not in ("+++", "---"))
pool = [x for x in t if x["repo"] in REPOS and hunks(x["patch"]) >= 3 and changed(x["patch"]) >= 40 and len(json.loads(x["FAIL_TO_PASS"])) >= 2]
pool.sort(key=lambda x: hashlib.sha256(("OGI013-SINGLE-TASK-1|" + x["instance_id"]).encode()).hexdigest())
print(len(pool), "in pool")
for x in pool[:5]:
    print(x["instance_id"], x["repo"], hunks(x["patch"]), changed(x["patch"]), len(json.loads(x["FAIL_TO_PASS"])), len(json.loads(x["PASS_TO_PASS"])))
sel = pool[0]
json.dump(sel, open("task.json", "w"), indent=1)
print("SELECTED", sel["instance_id"])
