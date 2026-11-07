"""SINGLE-E baseline helpers: pure functions, no I/O (pre-registered in evidence/ogi013-c3-prereg/PROTOCOL.md).

SINGLE-E = equal-effort single model: k independent drafts from the same supply, majority canonical action. No cooperation."""
import json
from typing import Mapping


def canonical_action(action: dict) -> str:
    if action["action"] == "message":
        body = {"action": "message", "content": " ".join(str(action["content"]).split())}
    else:
        body = {"action": "tool", "name": action["name"], "arguments": action.get("arguments", {})}
    return json.dumps(body, sort_keys=True, ensure_ascii=False)


def majority_action(actions: list) -> tuple:
    """Majority canonical action over drafts (None = unparseable, ignored). Ties -> earliest draft among the tied.
    Returns (winning action dict or None, {counts, winner_index, ties}); winner_index indexes the input list."""
    first, counts = {}, {}
    for i, a in enumerate(actions):
        if a is None:
            continue
        key = canonical_action(a)
        first.setdefault(key, i)
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return None, {"counts": {}, "winner_index": None, "ties": False}
    top = max(counts.values())
    tied = [key for key, c in counts.items() if c == top]
    winner_index = min(first[key] for key in tied)
    return actions[winner_index], {"counts": counts, "winner_index": winner_index, "ties": len(tied) > 1}


def read_k(env: Mapping[str, str]) -> int:
    try:
        k = int(env.get("OGI013_SINGLE_E_K"))
    except (TypeError, ValueError):
        raise RuntimeError("SINGLE_E_K_REQUIRED") from None
    if k < 1:
        raise RuntimeError("SINGLE_E_K_REQUIRED")
    return k
