"""Cooperation trace from the ledger (descriptive only; parallel organisation order, section 3 addition). usage: ogi013_trace.py RUN_DIR   (run dir = <out>/run)
Reports observations; it never states that the team cooperates well / improves / is better."""
import collections
import json
import sys
from pathlib import Path


def overlap(a, b):
    return max(0.0, min(a["end"], b["end"]) - max(a["start"], b["start"]))


def trace(run: Path) -> str:
    ev = [json.loads(l) for l in (run / "fruitstack-events.jsonl").read_text().splitlines() if l.startswith("{")]
    rj = json.loads((run / "run.json").read_text())
    led = json.loads((run / "ledger.json").read_text()) if (run / "ledger.json").exists() else {"objections": []}
    tm = json.loads((run / "timing.json").read_text()) if (run / "timing.json").exists() else {}
    objs = [o for o in led["objections"] if o.get("kind") == "objection"]
    grounded = [o for o in objs if o.get("grounded")]
    ungrounded = [o for o in objs if not o.get("grounded")]
    prompted = {i for e in ev if e["event"] == "REVISION" for i in e.get("responding_to", [])}
    replies = [e for e in ev if e["event"] == "REPLY"]
    out = [f"# Cooperation trace (observations only) — {run.parent.name}", ""]
    out += ["## 1 Counts", f"- grounded objections: {len(grounded)}; ungrounded objections: {len(ungrounded)}; ungrounded that entered a revision prompt: {len(prompted & {o['id'] for o in ungrounded})}",
            f"- REPLY events with evidence: {sum(1 for e in replies if e.get('evidence') in ('command', 'quote'))} (all replies {len(replies)}; UNGROUNDED_REPLY {sum(1 for e in ev if e['event'] == 'UNGROUNDED_REPLY')})",
            f"- evidenced WITHDRAWN: {sum(1 for e in replies if e.get('action') == 'withdraw')}; unresolved objections sent to the specialist: {sum(len(e.get('objections', [])) for e in ev if e['event'] == 'SPECIALIST_ADJUDICATION')}", ""]
    out += ["## 2 Positions"]
    changed = False
    for pid in sorted({e["pos"] for e in ev if e["event"] in ("SNAPSHOT", "REVISION", "REVISION_REJECTED", "REVISION_SKIPPED") and e.get("pos")}):
        for e in ev:
            if e.get("pos") != pid:
                continue
            if e["event"] == "SNAPSHOT":
                out.append(f"- {pid} {e['label']}: snapshot sha256 {e['sha'][:12]}")
            elif e["event"] == "REVISION":
                cites = ", ".join(f"{i} ({next((o['ground']['kind'] for o in objs if o['id'] == i and o.get('ground')), '?')})" for i in e.get("responding_to", [])) or "none"
                out.append(f"- {pid} rev{e['rev']} proposed, changed_code={e['changed_code']}, cites: {cites}")
            elif e["event"] == "REVISION_REJECTED":
                out.append(f"- {pid} rev{e['rev']} REJECTED_REVISION: {e['reason']}")
            elif e["event"] == "REVISION_SKIPPED":
                out.append(f"- {pid} revision skipped: {e['reason']}")
        changed = changed or any(c["status"] == "ADOPTED" and c["label"] != "first" and c["pos"] == pid for c in rj.get("candidates", []))
    out += ["- no position was changed by a ledger event (no revision adopted)" if not changed else "- at least one revision was adopted (see candidates)", ""]
    out += ["## 3 Candidates", "| candidate | sha256 | host-run check | status | reason |", "|---|---|---|---|---|"]
    for c in rj.get("candidates", []):
        out.append(f"| {c['id']} | {c['sha256'][:12]} | {c.get('visible') or '-'} | {c['status']} | {c.get('reason') or ''} |")
    out += [f"- protected best at the end: sha256 {(rj['release'].get('candidate_sha256') or '')[:12]} (position {rj['release'].get('released')}), class {rj['release'].get('class')}", ""]
    out += ["## 4 Concurrency"]
    ss, cs = tm.get("solver_sessions", []), tm.get("critic_sessions", [])
    out.append(f"- solver sessions: {ss}; overlap {tm.get('solver_overlap_seconds', 0)} s")
    out.append(f"- critic sessions: {cs}; pairwise overlap {[round(overlap(x, y), 2) for i, x in enumerate(cs) for y in cs[i + 1:]]} s")
    ws = tm.get("wall_share", {})
    out.append(f"- wall-clock share: queue wait {ws.get('queue_wait', 0)}, provider latency (ok) {ws.get('ok', 0)}, retry (rate limit {ws.get('rate_limit', 0)}, unavailable {ws.get('provider_unavailable', 0)}, unusable {ws.get('unusable_output', 0)}, other {ws.get('other', 0)}, wait {ws.get('retry_wait', 0)}); max calls in flight observed {tm.get('max_calls_in_flight_observed')} (cap {tm.get('max_concurrent_calls')})")
    out += [""]
    out += ["## 5 One exchange"]
    ex = next((o for o in led["objections"] if o.get("replies")), None)
    if ex is None:
        out.append("no exchange occurred")
    else:
        out.append(f"- {ex['id']} ({ex['lineage']}): {ex['text'][:300]!r}")
        for r in ex["replies"][:2]:
            out.append(f"- reply {r['step']} ({r['role']}, {r['action']}, evidence {r['evidence']}, sha256 {r['sha256'][:12]}): {r['text'][:300]!r}")
        out.append(f"- final state: {ex['state']}")
    out += ["", "## 6 Roster"]
    out.append(f"- roles: {rj.get('roster', {}).get('roster')}; check: {rj.get('roster', {}).get('check')}")
    for e in ev:
        if e["event"] == "ROSTER_CHANGE":
            out.append(f"- ROSTER_CHANGE {e['role']}: {e.get('from_model')} reason class {e.get('reason_class')}: {e.get('reason', '')[:140]}")
    steps = [e for e in ev if e["event"] == "STEP"]
    pins = {v for v in (rj.get("roster", {}).get("roster") or {}).values()} | {e.get("from_model") for e in ev if e["event"] == "ROSTER_CHANGE"} | {e.get("model") for e in ev if e["event"] == "ROSTER_PIN"}
    out.append(f"- executed-model check from the receipts: {len(steps)} steps; prefer_met {dict(collections.Counter(e.get('prefer_met') for e in steps))}; steps by a model outside every pin: "
               f"{sum(1 for e in steps if e.get('model_key') not in pins)}")
    return "\n".join(out)


if __name__ == "__main__":
    print(trace(Path(sys.argv[1])))
