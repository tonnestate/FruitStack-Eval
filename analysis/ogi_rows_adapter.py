"""Adapter: result rows of runners/fs_org_driver.py (FruitStack-Eval PR #16) -> ogi_analyze input rows.

Driver row fields used (after grade_after): task, arm in {T,E_div,R_mono,S,G_mas}, reward (1.0 = correct),
effect{class,first_correct,members}, tokens{input,output,calls_without_tokens}, calls, receipts[],
identity_valid (True/False/None), exclusion ("INFRA_IDENTITY:<why>" or None), lineages.
The driver rows carry no task family: pass `family` (or the row's own "family" key wins).
Excluded rows stay in the output with valid=False and `exclusion` (the reason), so ogi_analyze.split_valid
reports them by reason. Use roles=ogi_analyze.STUDY_ROLES with analyze().
"""
from __future__ import annotations

import json

STUDY_ARMS = {"T", "E_div", "R_mono", "S", "G_mas"}


def _arm(r: dict) -> str:
    if r["arm"] != "S":
        return r["arm"]
    keys = [c.get("model_key") for c in r.get("receipts", []) if c.get("ok") and c.get("model_key")]
    return f"S_{keys[0]}" if keys else "S_unknown"  # single member = the model its one solve call ran on


def adapt_row(r: dict, family: str | None = None) -> dict:
    tok = r.get("tokens") or {}
    eff = r.get("effect") or {}
    out = {"task_id": r["task"], "family": r.get("family", family), "arm": _arm(r),
           "tokens_in": tok.get("input", 0), "tokens_out": tok.get("output", 0),
           "tokens_incomplete": bool(tok.get("calls_without_tokens")),
           "calls": r.get("calls", len(r.get("receipts", []))),
           "lineages": r.get("lineages") or sorted({c["independence_key"] for c in r.get("receipts", []) if c.get("ok") and c.get("independence_key")}),
           "correct": r.get("reward") == 1.0, "member_first_correct": None, "valid": True, "exclusion": None}
    if eff.get("members"):  # harm() needs only whether any first answer was right
        fc = eff["first_correct"]
        out["member_first_correct"] = [True] * fc + [False] * (eff["members"] - fc)
    if r["arm"] not in STUDY_ARMS:
        out["valid"], out["exclusion"] = False, f"NOT_STUDY_ARM:{r['arm']}"
    elif r.get("identity_valid") is not True:
        out["valid"] = False
        out["exclusion"] = r.get("exclusion") or "IDENTITY_UNCHECKED"
    elif r.get("reward") is None:
        out["valid"], out["exclusion"] = False, "NOT_GRADED"
    return out


def adapt_rows(rows: list[dict], family: str | None = None) -> list[dict]:
    return [adapt_row(r, family) for r in rows]


def load_driver_rows(path: str, family: str | None = None) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return adapt_rows([json.loads(line) for line in f if line.strip()], family)
