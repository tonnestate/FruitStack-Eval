"""Release-vote grounding (Addendum 6 section 1): decided by the host from the objection ledger and its own event log, never from the voter's claim.
An 'APPROVE: EXCELLENT' is grounded iff (1) the voter ran run_tests/run_python on the candidate AFTER the candidate's latest change, (2) the vote states what was checked
and the result, (3) its OWN_OBJECTIONS field agrees with the ledger. An UNGROUNDED_APPROVAL counts as REJECT."""
import re

FIELD = re.compile(r"^[ \t]*OWN_OBJECTIONS:[ \t]*(.*?)(?=^[ \t]*[A-Z][A-Z_]{3,}:|\Z)", re.M | re.S)
OBJ_ID = re.compile(r"\bO\d+\b")


def judge_vote(text: str, lineage, objs: list, target: str, check_ns: list, change_ns: int, checks_stated: bool) -> dict:
    """objs: ledger rows {id, target, lineage, kind, open, answered_by, withdrawn}. Returns {verdict, counts, reason}."""
    lines = (text or "").strip().splitlines()
    first = lines[0].strip().upper() if lines else ""
    verdict = "EXCELLENT" if first.startswith("APPROVE: EXCELLENT") else "ACCEPTABLE" if first.startswith("APPROVE: ACCEPTABLE") else "REJECT"
    if verdict == "REJECT":
        return {"verdict": "REJECT", "counts": "REJECT", "reason": "voted REJECT"}

    def bad(why):
        return {"verdict": "UNGROUNDED_APPROVAL", "counts": "REJECT", "reason": why, "claimed": verdict}
    if not any(t > change_ns for t in check_ns):
        return bad("no run_tests/run_python by the voter after the candidate's latest change")
    if not checks_stated:
        return bad("the vote does not name what was checked and what it showed")
    m = FIELD.search(text)
    if not m:
        return bad("OWN_OBJECTIONS field missing")
    field = m.group(1).strip()
    mine = [o for o in objs if o["lineage"] == lineage and o["target"] == target and o["kind"] == "objection"]
    says_none = field.upper().startswith("NONE")
    if not mine:
        return {"verdict": verdict, "counts": verdict, "reason": "ok"} if says_none else bad("OWN_OBJECTIONS must read NONE: the ledger has no objection by this voter")
    if says_none:
        return bad("voter wrote NONE although the ledger has objections by it")
    listed = set(OBJ_ID.findall(field))
    missing = [o["id"] for o in mine if o["id"] not in listed]
    if missing:
        return bad(f"ledger objections not listed: {missing}")
    for o in mine:
        res = re.search(rf"\b{o['id']}\b[ \t:,-]*(.*)", field)
        resolution = (res.group(1) if res else "").strip()
        if len(resolution) < 3:
            return bad(f"{o['id']} has no stated resolution")
        if re.search(r"\bWITHDRAWN\b", resolution, re.I) and not o.get("answered_by"):
            o["withdrawn"] = True                                      # an explicit act of this voter, recorded in the ledger
        if not (o.get("answered_by") or o.get("withdrawn")):
            return bad(f"{o['id']} is still open in the ledger")
    return {"verdict": verdict, "counts": verdict, "reason": "ok"}


def tally(votes: list) -> str:
    return "RELEASED_UNANIMOUS_EXCELLENT" if votes and all(v["counts"] == "EXCELLENT" for v in votes) else "RETURN_TO_AUTHOR"
