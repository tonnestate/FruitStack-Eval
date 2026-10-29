#!/usr/bin/env python3
"""Decision-level metrics for the COLLAB mechanism, computed MECHANICALLY from the run evidence and the official tau2 reference (evaluation_criteria.actions); no judgement call, no model.
A reviewed decision has a DRAFT action and a FINAL action (ORG_COLLAB event). Each is classified against the task's expected actions:
  MATCH_EXPECTED    tool call whose name equals an expected action and whose arguments contain that action's arguments
  WRONG_ARGS        same tool name as an expected action, other arguments
  UNEXPECTED_WRITE  a write tool that no expected action uses (tau2's DB check penalises it)
  UNEXPECTED_TRANSFER  transfer_to_human_agents when the reference does not expect one (it ends the episode)
  SAFE_NON_WRITE    a message or a read tool
Outcome of a review: PREVENTED_WRITE_ERROR (bad draft -> SAFE_NON_WRITE or MATCH_EXPECTED), ERROR_REPLACED_BY_DIFFERENT_ERROR (bad -> bad, other class), ERROR_NOT_FIXED (bad, unchanged),
CORRECT_BLOCKED (MATCH_EXPECTED -> anything else), VALIDATED_CORRECT (MATCH_EXPECTED unchanged), UNNECESSARY_CHANGE (SAFE/ MATCH -> other SAFE/MATCH differing), NO_CHANGE_SAFE.
AMENDMENT-1 (prospective, before any COLLAB-1 data): a deviation from the reference is NOT called a policy violation. The official grader of these tasks (reward_basis DB/COMMUNICATE) does not evaluate
the NL policy assertions, so policy compliance is reported as UNJUDGED unless `reward_info.nl_assertions` is present; what is measured instead is (a) `state_changing_deviations` - writes that were
EXECUTED SUCCESSFULLY (tool message without error) although the reference does not contain them, (b) `unnecessary_transfer` - an executed transfer the reference does not contain, and (c) objectives completed / abandoned
with a mechanical cause. Attempted (proposed by draft/final) and executed (official messages) actions are kept apart. The reference is read ONLY here, in the evaluator; no agent code imports this module.
usage: decision_metrics.py RUN_ARM_DIR TASKS_JSON TASK_ID     (RUN_ARM_DIR holds tasks/<id>/{official-result.json,fruitstack-events.jsonl})"""
import json
import sys
from pathlib import Path

WRITE_TOOLS = {"book_reservation", "cancel_reservation", "update_reservation_flights", "update_reservation_passengers", "update_reservation_baggages", "send_certificate",
               "cancel_pending_order", "exchange_delivered_order_items", "modify_pending_order_address", "modify_pending_order_items", "modify_pending_order_payment",
               "modify_user_address", "return_delivered_order_items"}
BAD = {"WRONG_ARGS", "UNEXPECTED_WRITE", "UNEXPECTED_TRANSFER"}


def _contains(actual, wanted) -> bool:
    if isinstance(wanted, dict):
        return isinstance(actual, dict) and all(k in actual and _contains(actual[k], v) for k, v in wanted.items())
    if isinstance(wanted, list):
        return isinstance(actual, list) and len(actual) == len(wanted) and all(_contains(a, w) for a, w in zip(actual, wanted))
    return actual == wanted


def classify(action: dict | None, expected: list[dict]) -> str:
    if not action or action.get("action") != "tool":
        return "SAFE_NON_WRITE"
    name, args = action.get("name"), action.get("arguments") or {}
    same = [e for e in expected if e.get("name") == name]
    if any(_contains(args, e.get("arguments") or {}) for e in same):
        return "MATCH_EXPECTED"
    if same:
        return "WRONG_ARGS"
    if name == "transfer_to_human_agents":
        return "UNEXPECTED_TRANSFER"
    return "UNEXPECTED_WRITE" if name in WRITE_TOOLS else "SAFE_NON_WRITE"


def outcome(draft_class: str, final_class: str, changed: bool) -> str:
    if draft_class in BAD:
        if not changed:
            return "ERROR_NOT_FIXED"
        return "ERROR_REPLACED_BY_DIFFERENT_ERROR" if final_class in BAD else "PREVENTED_WRITE_ERROR"
    if draft_class == "MATCH_EXPECTED":
        return "VALIDATED_CORRECT" if not changed or final_class == "MATCH_EXPECTED" else "CORRECT_BLOCKED"
    return "NO_CHANGE_SAFE" if not changed else "UNNECESSARY_CHANGE"


def _parse(text):
    try:
        obj = json.loads(text) if isinstance(text, str) else text
        return obj if isinstance(obj, dict) else None
    except ValueError:
        return None


STOP_TOKEN = "###STOP###"


def _executed(official: dict) -> list[dict]:
    """Every tool call of the agent with the result of ITS execution: ok = the paired tool message exists and carries no error."""
    results = {m.get("id"): m for m in official.get("messages", []) if m.get("role") == "tool"}
    out = []
    for m in official.get("messages", []):
        if m.get("role") != "assistant":
            continue
        for tc in m.get("tool_calls") or []:
            r = results.get(tc.get("id"))
            out.append({"name": tc["name"], "arguments": tc.get("arguments") or {}, "ok": None if r is None else not bool(r.get("error"))})
    return out


def _abandon_cause(official: dict, remaining: list[str], deviations: list[str] | None = None) -> str:
    if not remaining:
        return "NONE"
    if deviations:
        return "WRONG_ACTION_EXECUTED"                                                             # the objective was lost to an executed state-changing deviation, not to a pending action
    msgs = official.get("messages", [])
    last_user = next((m for m in reversed(msgs) if m.get("role") == "user"), None)
    if last_user and "###TRANSFER###" in (last_user.get("content") or ""):
        return "TRANSFER"
    last_agent = next((m for m in reversed(msgs) if m.get("role") == "assistant"), None)
    if last_user and STOP_TOKEN in (last_user.get("content") or "") and not (last_agent or {}).get("tool_calls") and msgs and msgs[-1].get("role") == "user":
        return "PREMATURE_STOP_PENDING"
    return "OTHER_TERMINATION"


def summarize(official: dict, events: list[dict], expected: list[dict]) -> dict:
    executed = _executed(official)
    for x in executed:
        x["class"] = classify({"action": "tool", "name": x["name"], "arguments": x["arguments"]}, expected)
    reviews = []
    for e in events:
        if e.get("event") != "ORG_COLLAB":
            continue
        texts = [t.get("text") for t in e.get("trail") or [] if t.get("stage") in ("SOLUTION", "REVISION", "SPECIALIST")]      # `draft` / `final` in the event are ids; the texts are in the trail
        d, f = _parse(texts[0] if texts else None), _parse(texts[-1] if texts else None)
        if "final_text" in e:                                                                       # the action the host actually adopted (a termination review may replace the last revision)
            f = {"action": "message"} if e.get("declined") else (_parse(e["final_text"]) if e.get("final_text") else f)
        dc, fc = classify(d, expected), classify(f, expected)
        final_executed = bool(f and f.get("action") == "tool" and any(x["name"] == f.get("name") and x["ok"] for x in executed))
        reviews.append({"purpose": e.get("purpose"), "action": e.get("action"), "draft_class": dc, "final_class": fc, "changed": bool(e.get("changed")), "outcome": outcome(dc, fc, bool(e.get("changed"))),
                        "final_executed_ok": final_executed or not (f and f.get("action") == "tool"), "independent_review": e.get("independent_review"), "final_reviewed": e.get("final_reviewed"), "calls": e.get("calls")})
    expected_writes = [e["name"] for e in expected if e["name"] in WRITE_TOOLS]                    # objectives are the state-changing outcomes; lookups and searches are means, not objectives
    completed = [n for n in expected_writes if any(x["name"] == n and x["class"] == "MATCH_EXPECTED" and x["ok"] for x in executed)]
    remaining = [n for n in expected_writes if n not in completed]
    ri = official.get("reward_info") or {}
    deviations = [x["name"] for x in executed if x["class"] in ("UNEXPECTED_WRITE", "WRONG_ARGS") and x["ok"]]
    return {"reward": ri.get("reward"), "termination": official.get("termination_reason"), "db_match": (ri.get("db_check") or {}).get("db_match"),
            "policy_evidence": "NOT_EVALUATED_BY_OFFICIAL_GRADER" if ri.get("nl_assertions") is None else ri["nl_assertions"],
            "executed_actions": [{"name": x["name"], "class": x["class"], "ok": x["ok"]} for x in executed],
            "state_changing_deviations": deviations, "failed_write_attempts": [x["name"] for x in executed if x["class"] in ("UNEXPECTED_WRITE", "WRONG_ARGS") and x["ok"] is False],
            "unnecessary_transfer": any(x["class"] == "UNEXPECTED_TRANSFER" for x in executed), "expected_actions": [e["name"] for e in expected], "expected_writes": expected_writes, "expected_actions_completed": completed,
            "objectives_abandoned": remaining, "abandon_cause": _abandon_cause(official, remaining, deviations), "reviews": reviews}


def main(argv) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    arm, tasks, tid = Path(argv[1]), Path(argv[2]), argv[3]
    expected = next((t.get("evaluation_criteria") or {}).get("actions") or [] for t in json.loads(tasks.read_text()) if str(t["id"]) == tid)
    d = arm / "tasks" / tid
    events = [json.loads(x) for x in (d / "fruitstack-events.jsonl").read_text().splitlines() if x.strip()]
    print(json.dumps(summarize(json.loads((d / "official-result.json").read_text()), events, expected), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
