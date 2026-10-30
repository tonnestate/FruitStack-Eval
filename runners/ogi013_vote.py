"""Objection ledger and release-vote grounding (Addenda 6 and 7). Everything here is decided by the host from the ledger and its own event log, never from a voter's claim.

Objection lifecycle (Addendum 7 B.1):
  OPEN               raised (team.objection)
  ADDRESSED_PENDING  a revision WITH changed code lists the id in responding_to (an unchanged-code revision leaves it OPEN and records CONTESTED_BY_AUTHOR)
  VERIFIED_RESOLVED  only by a re-examination after that revision, by a lineage other than the reviser, with a check executed after the revision (or by a specialist adjudication)
  WITHDRAWN          only inside a vote, with a stated reason AND a check by that voter executed after the objection was raised whose output the reason refers to
An 'APPROVE: EXCELLENT' is grounded iff: fresh own check after the candidate's latest change; stated checks; OWN_OBJECTIONS agrees with the ledger (NONE if the voter has no row,
else every id with a resolution and the ledger state VERIFIED_RESOLVED / valid WITHDRAWN). An UNGROUNDED_APPROVAL counts as REJECT."""
import re
import time

FIELD = re.compile(r"^[ \t]*OWN_OBJECTIONS:[ \t]*(.*?)(?=^[ \t]*[A-Z][A-Z_]{3,}:|\Z)", re.M | re.S)
OBJ_ID = re.compile(r"\bO\d+\b")
VERDICT_LINE = re.compile(r"^[ \t]*[-*]?[ \t]*(O\d+)[ \t]*[:\-]?[ \t]*(RESOLVED|STILL_OPEN)\b", re.M)
OPEN, PENDING, RESOLVED, WITHDRAWN = "OPEN", "ADDRESSED_PENDING", "VERIFIED_RESOLVED", "WITHDRAWN"


class Ledger:
    def __init__(self):
        self.objs, self.n = [], 0
        self.emit = lambda *a, **k: None
        self.on_change = lambda o: None          # called after every objection state change (the audit trail of the ledger)

    def _set(self, o, state, **info):
        o["state"], o["open"] = state, state in (OPEN, PENDING)
        o.update(info)
        self.on_change(o)

    def objection(self, target, lineage, text, kind="objection", grounded=True) -> str:
        self.n += 1
        oid = f"O{self.n}"
        self.objs.append({"id": oid, "target": target, "lineage": lineage, "text": text[:1500], "kind": kind, "grounded": grounded, "raised_ns": time.monotonic_ns(),
                          "state": OPEN, "open": True, "contested": 0, "decided_by": None, "revised_ns": None})
        self.on_change(self.objs[-1])
        self.emit("OBJECTION", id=oid, target=target, lineage=lineage, okind=kind, grounded=grounded)   # not kind=: Episode.event(kind, ...) takes that name
        return oid

    def revise(self, target, rev, changed_code, responding_to, reason="") -> None:
        for o in self.objs:
            if o["id"] in responding_to and o["target"] == target and o["state"] == OPEN:
                if changed_code:
                    self._set(o, PENDING, revised_ns=time.monotonic_ns(), revision=rev)
                else:
                    o["contested"] += 1                                     # CONTESTED_BY_AUTHOR: stays OPEN
                    o["author_reason"] = reason[:500]
                    self.on_change(o)
                self.emit("OBJECTION_REVISED", id=o["id"], rev=rev, state=o["state"], contested=o["contested"])

    def reexamine(self, target, text, examiner_lineage, excluded_lineages, checks, from_state=PENDING, decided_by="reexamination") -> list:
        """text: per id 'O3: RESOLVED' / 'O3: STILL_OPEN'. A verdict counts only from a lineage not in excluded_lineages (the reviser/author) and with a check executed after the revision."""
        if examiner_lineage in excluded_lineages:
            return []
        changed = []
        for oid, verdict in VERDICT_LINE.findall(text or ""):
            o = next((x for x in self.objs if x["id"] == oid and x["target"] == target and x["state"] == from_state), None)
            if not o or not any(t > (o["revised_ns"] or o["raised_ns"]) for t, _ in checks):
                continue
            if verdict == "RESOLVED":
                self._set(o, RESOLVED, decided_by=decided_by)
            else:
                self._set(o, OPEN, decided_by=None, contested=0)
            changed.append((oid, o["state"]))
            self.emit("OBJECTION_" + o["state"], id=oid, by=examiner_lineage, decided_by=decided_by)
        return changed

    def open_count(self, target: str) -> int:
        """Addendum 5/7: GROUNDED objections that are OPEN or ADDRESSED_PENDING; ungrounded ones are recorded but neither count nor block."""
        return sum(1 for o in self.objs if o["target"] == target and o["open"] and o["kind"] == "objection" and o["grounded"])


def _refers(reason: str, outputs: list) -> bool:
    toks = {t for t in re.findall(r"[A-Za-z_][\w.]{5,}", reason) if t.upper() != "WITHDRAWN"}
    return any(t in out for t in toks for out in outputs)


def judge_vote(text: str, lineage, objs: list, target: str, checks: list, change_ns: int, checks_stated: bool, returned_lineage=None, author_lineages=()) -> dict:
    """checks: the voter's own (ns, output) of run_tests/run_python. Returns {verdict, counts, reason, withdrawals}."""
    if returned_lineage is not None and returned_lineage in author_lineages:
        return {"verdict": "NO_VOTE", "counts": "REJECT", "reason": "VOTER_LINEAGE_FALLBACK", "withdrawals": 0}
    lines = (text or "").strip().splitlines()
    first = lines[0].strip().upper() if lines else ""
    verdict = "EXCELLENT" if first.startswith("APPROVE: EXCELLENT") else "ACCEPTABLE" if first.startswith("APPROVE: ACCEPTABLE") else "REJECT"
    if verdict == "REJECT":
        return {"verdict": "REJECT", "counts": "REJECT", "reason": "voted REJECT", "withdrawals": 0}

    def bad(why):
        return {"verdict": "UNGROUNDED_APPROVAL", "counts": "REJECT", "reason": why, "claimed": verdict, "withdrawals": 0}
    if not any(t > change_ns for t, _ in checks):
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
        return {"verdict": verdict, "counts": verdict, "reason": "ok", "withdrawals": 0} if says_none else bad("OWN_OBJECTIONS must read NONE: the ledger has no objection by this voter")
    if says_none:
        return bad("voter wrote NONE although the ledger has objections by it")
    listed = set(OBJ_ID.findall(field))
    missing = [o["id"] for o in mine if o["id"] not in listed]
    if missing:
        return bad(f"ledger objections not listed: {missing}")
    withdraw = []
    for o in mine:
        res = re.search(rf"\b{o['id']}\b[ \t:,-]*(.*)", field)
        resolution = (res.group(1) if res else "").strip()
        if len(resolution) < 3:
            return bad(f"{o['id']} has no stated resolution")
        if o["state"] in (RESOLVED, WITHDRAWN):
            continue
        if o["state"] == OPEN and re.search(r"\bWITHDRAWN\b", resolution, re.I) or o["state"] == PENDING and re.search(r"\bWITHDRAWN\b", resolution, re.I):
            reason = re.sub(r"(?i)\bWITHDRAWN\b", "", resolution).strip()
            outs = [out for t, out in checks if t > o["raised_ns"]]
            if len(reason) < 20 or not outs or not _refers(reason, outs):
                return bad(f"{o['id']}: withdrawal needs a reason referring to the output of a check executed after the objection was raised")
            withdraw.append(o)
            continue
        return bad(f"{o['id']} is {o['state']} in the ledger (only VERIFIED_RESOLVED or an evidenced withdrawal closes an objection)")
    for o in withdraw:                                                  # applied only when the whole vote is grounded
        o["state"], o["open"], o["decided_by"] = WITHDRAWN, False, "withdrawn_in_vote"
    return {"verdict": verdict, "counts": verdict, "reason": "ok", "withdrawals": len(withdraw)}


def tally(votes: list) -> str:
    return "RELEASED_UNANIMOUS_EXCELLENT" if votes and all(v["counts"] == "EXCELLENT" for v in votes) else "RETURN_TO_AUTHOR"


def next_no_shrink(no_shrink: int, prev_open, open_now: int, prev_score, score) -> int:
    """Addendum 5/7: a vote cycle is progress only if GROUNDED open (OPEN/ADDRESSED_PENDING) objections shrank, or the best visible result improved."""
    return 0 if prev_open is None or open_now < prev_open or score > prev_score else no_shrink + 1


def vote_stop(no_shrink: int, cycle: int, fails: int, max_cycles: int):
    return "VOTE_NO_SHRINK_3" if no_shrink >= 3 else "VOTE_CYCLES_8" if cycle >= max_cycles else "VOTE_FAILURES_3" if fails >= 3 else None
