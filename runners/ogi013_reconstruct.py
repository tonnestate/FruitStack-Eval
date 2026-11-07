"""OFFLINE reconstruction of archived OGI-013 collaboration episodes (no provider call, no write to any source).

Sources (read-only): per-episode exchange files + result rows of
  S1      research/OGI013-QA1/runs/s1/run1/out            (16 T episodes; 12 were Luna-only duplication, see S1_RECLASSIFICATION.json)
  QA2D-v2 research/OGI013-QA1/runs/qa2d_v2/out/run        (T arm, genuine Luna+nemotron duo)
  HOSTCHECK research/OGI013-QA1/runs/qa1b/hostcheck1/run  (engineering host check, NOT study data; QID 8512)
usage: ogi013_reconstruct.py --runs /root/fruits/research/OGI013-QA1/runs --out evidence/ogi013-reconstruction

Evidence levels used in the output (never merged):
  model_asserted   an objection/answer text produced by a model (never proof by itself)
  executed         a sandbox/format check ran (ground.argument.executed true)
  dataset_key      the benchmark answer key of the question (external ground truth for the final letter)
Counterfactual (what a different controller would have chosen) is NOT computed here; see S1_COUNTERFACTUAL.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

LETTER = re.compile(r"ANSWER:\s*\(?([A-J])\b")


def letter(text) -> str | None:
    m = LETTER.findall(text or "")
    return m[-1] if m else None


def rows(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip().startswith("{")]   # logs may carry non-JSON lines


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def objection_view(o: dict) -> dict:
    g = o.get("ground") or {}
    return {"id": o.get("id"), "target": o.get("target"), "raised_by_lineage": o.get("lineage"), "state": o.get("state"),
            "decided_by": o.get("decided_by"), "ground_level": g.get("level"), "executed": (g.get("argument") or {}).get("executed"),
            "proposed_letter": letter(o.get("text")), "replies": [{"action": r.get("action"), "evidence": r.get("evidence"),
                                                                   "letter": letter(r.get("text"))} for r in o.get("replies", [])],
            "evidence_level": "executed" if (g.get("argument") or {}).get("executed") else "model_asserted"}


def classify(first: dict[str, str | None], final: str | None, key: str, primary: str) -> str:
    """Observed effect of the whole episode on the PRIMARY (designated first) answer; ground truth = dataset key."""
    p, fin = first.get(primary), final
    if fin is None:
        return "NO_FINAL"
    if primary is None:                                   # role order unknown: only the claim that holds for every ordering
        if fin == key:
            return "IMPROVED_OVER_BOTH_FIRST_ANSWERS" if key not in first.values() else "RIGHT_ANSWER_PRESENT_FROM_START"
        return "FINAL_WRONG"
    if p == fin:
        return "UNCHANGED_RIGHT" if fin == key else "UNCHANGED_WRONG"
    if p == key:
        return "DEGRADED"                       # primary was right, final is not the primary's answer and is wrong
    return "IMPROVED" if fin == key else "CHANGED_STILL_WRONG"


def episode(source: str, qid: str, ex: dict, row: dict, extra: dict) -> dict:
    fa = ex["first_answers"]
    if isinstance(fa, dict):
        first = {k: letter(v) for k, v in fa.items()}
        primary = "luna"
    else:                                                  # list = arrival order, NOT role order; roles come from the result row when recorded
        arr = [letter(a.get("text")) for a in fa]
        pos = row.get("first_by_pos") or {}
        if pos.get("S1"):
            first, primary = {"S1": pos["S1"]}, "S1"
            rest = list(arr)
            if pos["S1"] in rest:
                rest.remove(pos["S1"])
            first.update({"S2" if pos.get("S2") else "extra_sample": (pos.get("S2") or (rest[0] if rest else None))})
        else:
            first, primary = {f"arrival{i + 1}": v for i, v in enumerate(arr)}, None   # role order not recorded (host check)
    key, fin = row.get("key"), (ex.get("final") or {}).get("letter") or row.get("letter")
    objs = [objection_view(o) for o in ex.get("objections", [])]
    members_right = sorted(k for k, v in first.items() if v == key)
    return {"source": source, "qid": qid, "key": key, "first_letters": first, "primary": primary,
            "objections": objs, "final_letter": fin, "controller_path": (ex.get("final") or {}).get("how") or row.get("stop"),
            "final_correct": fin == key, "effect_on_primary": classify(first, fin, key, primary),
            "a_member_first_answer_was_right": members_right,
            "correct_answer_available_but_not_selected": bool(members_right) and fin != key,
            "n_objections": len(objs), "n_executed_objections": sum(1 for o in objs if o["executed"]),
            "verified_discovery_stored": False, "discovery_reused": False, **extra}


def build(runs: Path, reclass: dict) -> list[dict]:
    out = []
    s1 = runs / "s1/run1/out"
    s1rows = {r["qid"]: r for r in rows(s1 / "results.jsonl") if r["arm"] == "T"}
    rc = {r["qid"]: r for r in reclass["rows"]}
    for qid, row in s1rows.items():
        f = s1 / "exchange" / f"{qid}.json"
        if f.exists():
            ex = json.loads(f.read_text())
            out.append(episode("S1", qid, ex, row, {"cooperation": rc[qid]["cooperation"], "valid_duo": rc[qid]["valid_duo"],
                                                   "evidence_file": f"exchange/{qid}.json"}))
    q2 = runs / "qa2d_v2/out/run"
    for row in rows(q2 / "results.jsonl"):
        if row["arm"] != "T" or row["status"] != "OK":
            continue
        f = q2 / "exchange" / f"{row['qid']}.json"
        if f.exists():
            out.append(episode("QA2D-v2", row["qid"], json.loads(f.read_text()), row,
                               {"cooperation": "LUNA_NEMOTRON_DUO", "valid_duo": True, "evidence_file": f"exchange/{row['qid']}.json"}))
    hc = runs / "qa1b/hostcheck1/run"
    hrow = next(r for r in rows(runs / "qa1b/hostcheck1.log") if r.get("qid") == "8512" and r.get("arm") == "T")
    out.append(episode("HOSTCHECK(engineering,not study data)", "8512", json.loads((hc / "exchange/8512.json").read_text()), hrow,
                       {"cooperation": "LUNA_NEMOTRON_DUO", "valid_duo": True, "evidence_file": "exchange/8512.json"}))
    return out


def summary(eps: list[dict]) -> dict:
    s: dict = {}
    for e in eps:
        grp = s.setdefault(e["source"] + ("/valid_duo" if e["valid_duo"] else "/not_a_duo"), {})
        grp[e["effect_on_primary"]] = grp.get(e["effect_on_primary"], 0) + 1
        grp["n"] = grp.get("n", 0) + 1
        grp["objection_episodes"] = grp.get("objection_episodes", 0) + (1 if e["n_objections"] else 0)
        grp["unselected_correct_available"] = grp.get("unselected_correct_available", 0) + (1 if e["correct_answer_available_but_not_selected"] else 0)
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--reclass", default="evidence/ogi013-small-proof/s1_results/S1_RECLASSIFICATION.json")
    a = ap.parse_args()
    runs, out = Path(a.runs), Path(a.out)
    eps = build(runs, json.loads(Path(a.reclass).read_text()))
    (out / "sources").mkdir(parents=True, exist_ok=True)
    manifest = {}
    for e in eps:                                         # preserve the raw per-episode exchange next to the analysis, with hashes
        base = {"S1": "s1/run1/out", "QA2D-v2": "qa2d_v2/out/run"}.get(e["source"], "qa1b/hostcheck1/run")
        src = runs / base / e["evidence_file"]
        dst = out / "sources" / f"{e['source'].split('(')[0]}_{e['qid']}.json"
        shutil.copyfile(src, dst)
        manifest[dst.name] = {"origin": f"{base}/{e['evidence_file']}", "sha256": sha(src)}
    (out / "EPISODES.json").write_text(json.dumps({"episodes": eps, "summary": summary(eps), "manifest": manifest}, indent=1, sort_keys=True))
    print(json.dumps(summary(eps), indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
