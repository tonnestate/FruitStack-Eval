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


def summarize(official: dict, events: list[dict], expected: list[dict]) -> dict:
    executed = [{"name": tc["name"], "arguments": tc.get("arguments") or {}} for m in official.get("messages", []) if m.get("role") == "assistant" for tc in (m.get("tool_calls") or [])]
    classes = [classify({"action": "tool", **t}, expected) for t in executed]
    reviews = []
    for e in events:
        if e.get("event") != "ORG_COLLAB":
            continue
        texts = [t.get("text") for t in e.get("trail") or [] if t.get("stage") in ("SOLUTION", "REVISION", "SPECIALIST")]      # `draft` / `final` in the event are ids; the texts are in the trail
        d, f = _parse(texts[0] if texts else None), _parse(texts[-1] if texts else None)
        dc, fc = classify(d, expected), classify(f, expected)
        reviews.append({"purpose": e.get("purpose"), "action": e.get("action"), "draft_class": dc, "final_class": fc, "changed": bool(e.get("changed")), "outcome": outcome(dc, fc, bool(e.get("changed"))),
                        "independent_review": e.get("independent_review"), "final_reviewed": e.get("final_reviewed"), "calls": e.get("calls")})
    expected_names = [e["name"] for e in expected]
    done = [n for n in expected_names if any(x["name"] == n and c == "MATCH_EXPECTED" for x, c in zip(executed, classes))]
    return {"reward": (official.get("reward_info") or {}).get("reward"), "termination": official.get("termination_reason"), "executed_actions": [{"name": x["name"], "class": c} for x, c in zip(executed, classes)],
            "unexpected_writes_executed": sum(1 for c in classes if c == "UNEXPECTED_WRITE"), "unexpected_transfer_executed": sum(1 for c in classes if c == "UNEXPECTED_TRANSFER"),
            "expected_actions": expected_names, "expected_actions_completed": done, "reviews": reviews}


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
