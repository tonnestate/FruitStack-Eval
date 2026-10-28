#!/usr/bin/env python3
"""Demonstration report for ONE rg2 run directory. Read-only; no network, no provider calls.

Applies the criteria of evidence/ogi013-rg2-demo/PROTOCOL.md to the existing traces only.
Anything absent from the traces is reported as null, never inferred.

CLI: rg2_trace_report.py RUN_DIR [--out report.json]
  --out writes the JSON report there and the markdown next to it (same stem, .md).
  Without --out, the markdown is printed to stdout.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

DELIVERED_KINDS = {"PROPOSAL", "CANDIDATE", "VERIFIER"}
VERDICT_KEYS = ("worker_contribution", "independent_verification", "causal_effect_on_decision",
                "productive_recovery", "knowledge_reuse", "organisational_success")
KNOWLEDGE_MARKERS = ("ZERO_CALL", "VERIFIED_KNOWLEDGE", "UNVERIFIED_FOR_THIS_CLAIM")
NOT_ACCEPTED = "original draft accepted - not organisational success"


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                rows.append({"_unparsed": line[:200]})
    return rows


def _reward(path: Path):
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("reward_info", {}).get("reward")
    except (json.JSONDecodeError, AttributeError):
        return None


def _attempt_progress(attempt: dict) -> bool:
    # the outcome is recorded per QUESTION (cherry events: question_outcome PROGRESS / COUNTED_FAILURE); an attempt counts only if its provider delivered
    return attempt.get("outcome") == "PROGRESS" and attempt.get("provider_ok") is not False


def _recovery(routing_seq: list[tuple[str, dict]]) -> tuple[list[dict], bool | None]:
    """routing_seq: ordered (kind, obj) pairs for one claim; kind is 'attempt' or 'intervention'.
    A SWITCH_WORKER is followed by attempts on another worker; productive if one has outcome PROGRESS."""
    switches, productive = [], None
    for idx, (kind, obj) in enumerate(routing_seq):
        if kind != "intervention" or obj.get("action") != "SWITCH_WORKER":
            continue
        later = [o for k, o in routing_seq[idx + 1:] if k == "attempt" and o.get("agent_id") != obj.get("agent_id")]
        hit = any(_attempt_progress(a) for a in later)
        switches.append({"agent_id": obj.get("agent_id"), "reason": obj.get("reason"),
                         "followups_on_other_worker": len(later), "progress_followup": hit})
        productive = hit if productive is None else (productive or hit)
    return switches, productive


def build_report(run_dir: Path, state_dir: Path | None = None) -> dict:
    """state_dir: the engine workspace shared by an arm (OGI013_ORG_STATE_DIR/cherry). When given, only rows of claims decided in THIS run_dir are read from it
    (two tasks of one arm share the state); without it the per-task <task>/org/cherry directory is read (legacy layout)."""
    run_dir = Path(run_dir)
    tasks_dir = run_dir / "tasks"
    task_dirs = sorted(p for p in tasks_dir.iterdir() if p.is_dir()) if tasks_dir.is_dir() else []

    decisions, revisions, interventions, all_attempt_codes = [], [], [], Counter()
    contrib_rows, verifier_rows, rewards, tasks_out = [], [], [], []
    episode_revisions, accounting_reuse, marker_hits = [], [], 0
    per_claim_routing: dict[str, list[tuple[str, dict]]] = {}
    per_claim_accounting: dict[str, dict] = {}

    for tdir in task_dirs:
        task = tdir.name
        fs = read_jsonl(tdir / "fruitstack-events.jsonl")
        own_claims = {c for e in fs if e.get("event") == "ORG_DECISION"
                      for c in [e.get("claim"), *[a.get("claim") for a in (e.get("atoms") or [])]] if c}
        if state_dir is not None:
            cherry = [e for e in read_jsonl(Path(state_dir) / "events.jsonl") if e.get("claim_id") in own_claims]
            contribs = [c for c in read_jsonl(Path(state_dir) / "contributions.jsonl") if c.get("claim_id") in own_claims]
        else:
            cherry = read_jsonl(tdir / "org" / "cherry" / "events.jsonl")
            contribs = read_jsonl(tdir / "org" / "cherry" / "contributions.jsonl")
        reward = _reward(tdir / "official-result.json")
        rewards.append(reward)
        verifier_logs = [str(p.relative_to(run_dir)) for p in tdir.rglob("verifier.log")]
        exc_log = tdir / "org" / "investigator-exceptions.log"

        for e in fs:
            if e.get("event") == "ORG_DECISION":
                decisions.append({"task": task, **{k: e.get(k) for k in (
                    "claim", "action", "status", "triage", "workers", "rows", "provider_calls", "dissent_n")}})
            elif e.get("event") == "ORG_REVISION":
                revisions.append({"task": task, "claim": e.get("claim") or e.get("claim_id"),
                                  "action_changed": e.get("action_changed"),
                                  "draft_action": e.get("draft_action"), "final_action": e.get("final_action")})
            elif e.get("event") == "EPISODE_CLOSED" and "revisions" in (e.get("stats") or {}):
                episode_revisions.append(e["stats"]["revisions"])

        for e in fs + cherry:
            if any(m in json.dumps(e) for m in KNOWLEDGE_MARKERS):
                marker_hits += 1

        for e in cherry:
            routing = e.get("routing")
            claim = e.get("claim_id")
            if not isinstance(routing, dict) or not claim:
                continue
            seq = per_claim_routing.setdefault(claim, [])
            for a in routing.get("attempts") or []:
                seq.append(("attempt", {**a, "outcome": e.get("question_outcome")}))
                all_attempt_codes[a.get("error_code") or "NONE"] += 1
            for i in routing.get("interventions") or []:
                seq.append(("intervention", {**i, "claim": claim, "task": task}))
                interventions.append({**i, "claim": claim, "task": task})
            acct = (routing.get("ensemble") or {}).get("accounting")
            if isinstance(acct, dict):
                per_claim_accounting[claim] = acct

        for c in contribs:
            contrib_rows.append({"task": task, "claim": c.get("claim_id"), "kind": c.get("kind"),
                                 "epistemic_status": c.get("epistemic_status"),
                                 "verdict": c.get("verdict"), "disposition": c.get("disposition"),
                                 "refs": tuple(c.get("evidence_refs") or ()),
                                 "key": (c.get("identity") or {}).get("independence_key") or (c.get("identity") or {}).get("model_key") or c.get("worker")})
        tasks_out.append({"task": task, "official_reward": reward, "verifier_log": verifier_logs or "not present",
                          "investigator_exceptions_lines": (sum(1 for _ in exc_log.open(encoding="utf-8"))
                                                            if exc_log.is_file() else None)})

    recovery_claims = {}
    for claim, seq in per_claim_routing.items():
        sw, prod = _recovery(seq)
        if sw:
            recovery_claims[claim] = {"switches": sw, "productive": prod}

    # ---- verdict ----
    ev = {}
    delivered = [r for r in contrib_rows if r["kind"] in DELIVERED_KINDS]
    if not contrib_rows:
        wc = None
        ev["worker_contribution"] = "no contribution rows in trace"
    else:
        wc = bool(delivered)
        ev["worker_contribution"] = f"{len(delivered)} delivered of {len(contrib_rows)} rows; kinds={dict(Counter(r['kind'] for r in contrib_rows))}"

    # CherryMe's EvidenceVerifier records its judgments as VERIFIER contribution rows whose verdict is the raw relation (SUPPORTS / CONTRADICTS / NOT_ADDRESSED); a quorum
    # promotion (SUPPORTS -> Evidence PASS, CONTRADICTS -> Evidence CONTRADICT) is the row with epistemic_status VERIFIED and disposition ACCEPTED. Legacy labels PASS/CONTRADICT are accepted too.
    promoted_labels = {"SUPPORTS", "CONTRADICTS", "PASS", "CONTRADICT"}
    vrows = [r for r in contrib_rows if r["kind"] == "VERIFIER"]
    pv = [r for r in vrows if r["verdict"] in promoted_labels and r["epistemic_status"] == "VERIFIED" and r["disposition"] == "ACCEPTED"]
    legacy = [r for r in contrib_rows if r["kind"] != "VERIFIER" and r["verdict"] in ("PASS", "CONTRADICT")]
    pv += legacy
    if not pv:
        iv = None if not vrows else False
        ev["independent_verification"] = (f"no quorum-promoted PASS/CONTRADICT; {len(vrows)} verifier judgments (relations={dict(Counter(r['verdict'] for r in vrows))}); verifier.log "
                                          + ("present (not parsed)" if any(t["verifier_log"] != "not present" for t in tasks_out) else "not present"))
    else:
        by_source: dict[tuple, set] = {}
        for r in pv:
            by_source.setdefault((r["claim"], r["refs"]), set()).add(r["key"])
        iv = any(len(keys - {None}) >= 2 for keys in by_source.values())
        ev["independent_verification"] = f"{len(pv)} quorum-promoted rows; distinct independence keys per (claim, source)={ {str(s[0]) + '|' + ','.join(s[1]): len(k) for s, k in by_source.items()} }"

    if revisions:
        changed = [r for r in revisions if r["action_changed"] is True]
        cz = True if changed else (False if all(r["action_changed"] is False for r in revisions) else None)
        ev["causal_effect_on_decision"] = f"{len(changed)} of {len(revisions)} ORG_REVISION with action_changed=true"
    elif episode_revisions and all(x == 0 for x in episode_revisions):
        cz = False
        ev["causal_effect_on_decision"] = "no ORG_REVISION events; EPISODE_CLOSED stats.revisions=0"
    else:
        cz = None
        ev["causal_effect_on_decision"] = "no ORG_REVISION events and no revision count in traces"

    switched = {c: v for c, v in recovery_claims.items()}
    if not switched:
        pr = None
        ev["productive_recovery"] = "no SWITCH_WORKER intervention in traces"
    else:
        pr = any(v["productive"] for v in switched.values())
        ev["productive_recovery"] = (f"{sum(len(v['switches']) for v in switched.values())} SWITCH_WORKER; "
                                     f"progress follow-ups on other worker={sum(1 for v in switched.values() for s in v['switches'] if s['progress_followup'])}")

    accounting_reuse = [a.get("reused_without_inference") for a in per_claim_accounting.values()
                        if "reused_without_inference" in a]
    if marker_hits:
        kr = True
        ev["knowledge_reuse"] = f"{marker_hits} events carry ZERO_CALL/VERIFIED_KNOWLEDGE/UNVERIFIED_FOR_THIS_CLAIM"
    elif accounting_reuse and all(x == 0 for x in accounting_reuse):
        kr = False
        ev["knowledge_reuse"] = "no markers; ensemble accounting reused_without_inference=0"
    else:
        kr = None
        ev["knowledge_reuse"] = "no ZERO_CALL/VERIFIED_KNOWLEDGE/unverified-lead markers in traces"

    known = [r for r in rewards if r is not None]
    if not known:
        reward_ok = None
    elif any(r != 1.0 for r in known):
        reward_ok = False
    elif len(known) == len(rewards):
        reward_ok = True
    else:
        reward_ok = None
    ev["official_reward"] = f"rewards per task={rewards}"

    # Registered rule (evidence/ogi013-rg2-demo/PROTOCOL.md, criterion 3): organisational success needs a CAUSAL contribution: an ORG_REVISION with action_changed=true after worker/verified
    # dissent. Independent verification, worker contribution, recovery and the reward are reported as separate observations but can never establish success on their own; a draft accepted
    # unchanged is never organisational success, whatever the reward (measurement-implementation correction, ERRATUM-1).
    if wc is False or reward_ok is False or cz is False:
        org = False
    elif wc is True and cz is True and reward_ok is True:
        org = True
    else:
        org = None
    ev["organisational_success"] = ("worker_contribution AND causal_effect_on_decision (ORG_REVISION with action_changed=true) AND reward 1.0; independent verification is reported separately"
                                    f" -> wc={wc}, causal={cz}, verification={iv}, reward_1={reward_ok}")

    verdict = {"worker_contribution": wc, "independent_verification": iv, "causal_effect_on_decision": cz,
               "productive_recovery": pr, "knowledge_reuse": kr, "organisational_success": org}
    note = NOT_ACCEPTED if reward_ok is True and cz is not True else None

    decision_out = []
    for d in decisions:
        claim = d["claim"]
        revs = [r for r in revisions if r["claim"] == claim]
        acct = per_claim_accounting.get(claim, {})
        attempts = [o for k, o in per_claim_routing.get(claim, []) if k == "attempt"]
        decision_out.append({
            **d,
            "draft_action": d["action"],
            "final_action": revs[-1]["final_action"] if revs else None,
            "revision": ("action_changed=%s" % revs[-1]["action_changed"]) if revs else "no ORG_REVISION observed",
            "rows_by_kind": dict(Counter(r["kind"] for r in contrib_rows if r["claim"] == claim)),
            "rows_by_epistemic_status": dict(Counter(r["epistemic_status"] for r in contrib_rows if r["claim"] == claim)),
            "planned_responsibilities": acct.get("planned_responsibilities"),
            "activated_workers": acct.get("activated_workers"),
            "dispatches_by_responsibility": acct.get("dispatches_by_responsibility"),
            "attempt_error_codes": dict(Counter(a.get("error_code") or "NONE" for a in attempts)),
            "switch_workers": recovery_claims.get(claim, {}).get("switches", []),
        })

    return {
        "run_dir": str(run_dir),
        "tasks": tasks_out,
        "decisions": decision_out,
        "attempt_error_codes": dict(all_attempt_codes),
        "interventions": interventions,
        "knowledge_marker_events": marker_hits,
        "plumme_state_rows": {n: len(read_jsonl(run_dir / "fruitstack" / "plumme-state" / n))
                              for n in ("receipts.jsonl", "decisions.jsonl")},
        "verdict": verdict,
        "evidence": ev,
        "note": note,
    }


def render_markdown(rep: dict) -> str:
    out = [f"# rg2 trace report: {rep['run_dir']}", ""]
    for t in rep["tasks"]:
        out.append(f"- task {t['task']}: official reward={t['official_reward']}; verifier.log={t['verifier_log']}")
    out += ["", "## Decisions"]
    for d in rep["decisions"]:
        out.append(f"- {d['claim']}: draft={d['draft_action']} final={d['final_action']} ({d['revision']}); "
                   f"status={d['status']} triage={d['triage']} workers={d['workers']}")
        out.append(f"  rows={d['rows_by_kind']} epistemic={d['rows_by_epistemic_status']}")
        out.append(f"  responsibilities planned={d['planned_responsibilities']} activated={d['activated_workers']} "
                   f"dispatches={d['dispatches_by_responsibility']} attempt_errors={d['attempt_error_codes']}")
    if not rep["decisions"]:
        out.append("- none (no ORG_DECISION events)")
    out += ["", f"Attempt error codes (run): {rep['attempt_error_codes'] or 'none'}",
            f"Interventions: {[(i.get('action'), i.get('agent_id'), i.get('reason')) for i in rep['interventions']] or 'none'}",
            f"Knowledge-marker events: {rep['knowledge_marker_events']}",
            "", "## Verdict"]
    for k in VERDICT_KEYS:
        out.append(f"- {k}: {rep['verdict'][k]} -- {rep['evidence'].get(k, '')}")
    if rep["note"]:
        out += ["", f"NOTE: {rep['note']}"]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--state-dir", type=Path, default=None, help="engine workspace shared by the arm (<OGI013_ORG_STATE_DIR>/cherry)")
    args = ap.parse_args()
    rep = build_report(args.run_dir, args.state_dir)
    md = render_markdown(rep)
    if args.out:
        args.out.write_text(json.dumps(rep, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        args.out.with_suffix(".md").write_text(md, encoding="utf-8")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
