"""CHAIN.md + lineage-diversity check (Addendum 6 sections 3 and 4) from a team run's event log (the ledger) and grades.json (hidden tests, outside every agent loop).
usage: ogi013_chain.py RUN_DIR [RUN_DIR ...] > CHAIN.md"""
import collections
import json
import sys
from pathlib import Path


def load(run: Path):
    return [json.loads(l) for l in (run / "fruitstack-events.jsonl").read_text().splitlines() if l.startswith("{")], json.loads((run / "grades.json").read_text())


def sessions_of(ev):
    stack, out = [], {}
    for i, e in enumerate(ev):
        if e["event"] == "SESSION_START":
            stack.append({"tokens": 0, "calls": 0})
        elif e["event"] == "STEP" and stack:
            stack[-1]["tokens"] += (e.get("tokens_in") or 0) + (e.get("tokens_out") or 0)
            stack[-1]["calls"] += 1
        elif e["event"] == "SESSION_END" and stack:
            out[i] = stack.pop()
    return out


def last_session_before(i, sess):
    k = max((j for j in sess if j < i), default=None)
    return sess.get(k, {"tokens": 0, "calls": 0})


def chain(run: Path):
    ev, grades = load(run)
    sess = sessions_of(ev)
    snaps = [(e["pos"], e["label"]) for e in ev if e["event"] == "SNAPSHOT"]
    g = lambda pos, label: grades.get(f"{pos}_{label}.diff")
    prev_label = {}
    for (pos, label) in snaps:
        prev_label.setdefault((pos, label), None)
    order = collections.defaultdict(list)
    for pos, label in snaps:
        order[pos].append(label)
    objs = {e["id"]: (i, e) for i, e in enumerate(ev) if e["event"] == "OBJECTION"}
    revs = [(i, e) for i, e in enumerate(ev) if e["event"] == "REVISION"]
    rows = []
    for i, e in enumerate(ev):
        kind = {"CHALLENGE": "challenge", "HELP_ANSWER": "help", "SPECIALIST": "specialist"}.get(e["event"])
        if e["event"] == "RELEASE_VOTE" and e.get("verdict") not in ("EXCELLENT",):
            kind = "vote_rejection"
        if not kind or (kind == "challenge" and e.get("verdict") != "FOUND"):
            continue
        ids = e.get("objection_ids") or []                       # linked by id only (Addendum 7 B.3)
        oid = next((k for k in ids if k in objs), None)
        c1 = bool(oid and objs[oid][1]["grounded"]) if kind != "specialist" else None
        rev = next(((j, r) for j, r in revs if oid and j > i and oid in r["responding_to"]), None)
        c2 = bool(rev and rev[1]["changed_code"])
        c3 = bool(rev and any(x["event"] in ("CHALLENGE", "RELEASE_VOTE") and x.get("pos") == rev[1]["pos"] and x.get("rev") == rev[1]["rev"] and x.get("lineage") != rev[1]["reviser_lineage"]
                               and (x.get("test_runs") or 0) >= 1 for x in ev[rev[0]:]))
        c4 = harm = None
        if rev:
            pos, n = rev[1]["pos"], rev[1]["rev"]
            labels = order[pos]
            after, before = g(pos, f"rev{n}"), g(pos, labels[labels.index(f"rev{n}") - 1]) if f"rev{n}" in labels and labels.index(f"rev{n}") > 0 else None
            if after and before:
                c4 = after["f2p_passed"] > before["f2p_passed"] and after["p2p_passed"] >= before["p2p_passed"]
                harm = after["f2p_passed"] < before["f2p_passed"] or after["p2p_passed"] < before["p2p_passed"]
        s1 = last_session_before(i, sess)
        s2 = last_session_before(rev[0], sess) if rev else {"tokens": 0, "calls": 0}
        status = "COMPLETE" if (c1 and c2 and c3 and c4) else "HARMFUL" if harm else "PARTIAL"
        rows.append({"kind": kind, "pos": e.get("pos"), "objection": oid, "C1": c1, "C2": c2, "C3": c3, "C4": c4, "status": status, "tokens": s1["tokens"] + s2["tokens"], "calls": s1["calls"] + s2["calls"]})
    # section 4 diversity
    firsts = {e["pos"]: set(e.get("author_lineages") or []) for e in ev if e["event"] == "SNAPSHOT" and e["label"] == "first"}
    contrib = [e for e in ev if e["event"] in ("CHALLENGE", "RELEASE_VOTE", "HELP_ANSWER")]
    own = [e for e in contrib if e.get("lineage") in (e.get("author_lineages") or [])]
    cnt = collections.Counter(e.get("lineage") for e in contrib)
    top = max(cnt.values()) / len(contrib) if contrib else 1.0
    sl = list(firsts.values())
    diverse = {"solver_lineages": {k: sorted(v) for k, v in firsts.items()}, "solvers_distinct": len(sl) >= 2 and all(not (a & b) for n, a in enumerate(sl) for b in sl[n + 1:]),
               "own_lineage_contributions": len(own), "top_lineage_share": round(top, 3), "contributions_by_lineage": dict(cnt)}
    diverse["G_dev_lineage_ok"] = diverse["solvers_distinct"] and not own and top <= 0.5
    return rows, diverse


if __name__ == "__main__":
    print("# CHAIN\n\nC1 grounded objection; C2 later revision lists the id in responding_to and changes code; C3 re-examined by a different lineage with a fresh check; C4 hidden F2P up and P2P not worse.\n")
    for r in sys.argv[1:]:
        rows, d = chain(Path(r))
        done = sum(x["status"] == "COMPLETE" for x in rows)
        print(f"## {Path(r).name}\n\ncomplete {done}, partial {sum(x['status'] == 'PARTIAL' for x in rows)}, harmful {sum(x['status'] == 'HARMFUL' for x in rows)}; tokens per complete chain: {round(sum(x['tokens'] for x in rows) / done) if done else 'n/a'}\n")
        print("| intervention | pos | objection | C1 | C2 | C3 | C4 | status | tokens | calls |\n|---|---|---|---|---|---|---|---|---|---|")
        for x in rows:
            print(f"| {x['kind']} | {x['pos']} | {x['objection']} | {x['C1']} | {x['C2']} | {x['C3']} | {x['C4']} | {x['status']} | {x['tokens']} | {x['calls']} |")
        rj = Path(r) / "run.json"
        sim = json.loads(rj.read_text()).get("release", {}).get("solver_similarity") if rj.exists() else None
        print(f"\nSolver similarity (line-level Jaccard of the two first positions): {sim}")
        print(f"\nLineage diversity: {json.dumps(d)}\n")
