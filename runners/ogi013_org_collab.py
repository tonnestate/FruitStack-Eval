"""OGI-013 collaboration step (exploratory development branch ogi013-collab-dev; opt-in OGI013_ORG_COLLAB=1, the frozen conditions never use it).

Integration defect it removes: on the RG/2 path the criticism was a claim-level FALSIFY question whose workers saw the claim text and the first customer request but NOT the policy, the conversation
or the tool results, the single revision that followed was accepted unexamined, unresolved objections were not kept, and nothing recorded which contribution materially improved the result.

Division of labour (no duplicate review): the RG/2 economy gate decides WHETHER cooperation is justified (purpose recorded); this module IS the cooperation and runs CherryMe's Brother Mode on the ACTUAL proposed
solution with the full task materials: the draft is the first independent solution -> a different lineage CHALLENGES it (concrete objections + a proposed answer) -> the author REVISES on valid criticism ->
a changed position is examined AGAIN -> if an objection stays unresolved a specialist of a further lineage adjudicates -> the host consolidates the best supported position and keeps the unresolved objections.
PlumMe chooses every model (the injected `work`); CherryMe owns the organisation (cherryme.brother). Nothing is truncated; nothing is capped except the loop guards of Brother Mode.

Attribution rules (read from the ledger, never from a model's claim):
  improved          - the final action differs from the draft because a criticism found issues and a revision / specialist changed the answer
  validated         - at least one reviewer examined the draft, found nothing wrong, and the action stayed unchanged: an independent quality check, NOT an improvement
  review_unavailable- no critique was delivered (supply failure): neither validated nor improved (a failed review is never counted as agreement)
  unresolved        - issues were found and no revision / specialist changed the action: the objection stays visible
Agreement is a reviewer's claim, never proof: every agreeing reviewer is recorded with the answer it examined and the grounds it stated; a bare verdict is `ungrounded_agreement` and does not count
as validation. A specialist that overrules the author's rejection is recorded in `overruled`, and the specialist's answer is examined once more by a lineage not yet involved (`final_reviewed`)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable

from cherryme.brother import _FOUND, _NONE, CHALLENGE, SPECIALIST, _add, _ok, run_rounds

MAX_ROUNDS = 2
GROUNDS = ("\nIn either case, after the first line, state the specific checks you made against the materials (policy clause, conversation fact, tool result) and what each showed. "
           "A bare verdict without these checks is not accepted as an assessment.")


TERMINATION = ("A colleague rejected the proposed action and the replacement below ENDS the interaction (it hands the customer over or stops the work). Rejecting one action is not ending the task: the customer's "
               "other requests may still be open, and the policy may allow declining only the part it forbids.\n"
               "TASK MATERIALS:\n{task}\n\nREJECTED ACTION:\n{rejected}\n\nPROPOSED TERMINATING REPLACEMENT:\n{replacement}\n\n"
               "Reply in exactly these four lines:\n"
               "OPEN_REQUESTS: <every request of the customer that is still unmet, separated by ' | ', or NONE>\n"
               "TERMINATION_REQUIRED_CLAUSE: <a verbatim quote from the policy or instructions in the materials that REQUIRES ending the interaction for ALL open requests, or NONE>\n"
               "ALTERNATIVE: <ONE valid JSON action in the task's output format that declines only what the policy forbids and continues with the open requests, or NONE>\n"
               "VERDICT: CONTINUE or TERMINATE")


def _field(text: str, name: str) -> str:
    m = re.search(rf"^\s*{name}\s*:\s*(.*)$", text or "", re.I | re.M)
    return m.group(1).strip() if m else ""


def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().strip("\"'").lower())


def termination_review(*, task_prompt: str, policy_text: str, rejected: str, replacement: str, work: Callable[..., dict], parse: Callable[[str], dict | None],
                       terminating: Callable[[dict], bool], used: tuple, continuity=None) -> dict:
    """Rejecting one action is not ending the task. When a rejection ended up as an action that terminates the interaction (a human transfer), a lineage not yet involved is asked which requests are still open,
    for the verbatim policy clause that REQUIRES ending, and for a continuing alternative. The decision is mechanical, never a reviewer's say-so: TERMINATE stands only if the quoted clause really occurs in the
    policy / instructions AND no continuing, non-terminating alternative was offered while requests remain open; otherwise the continuing alternative is adopted, or - with none - the rejected action is
    declined without ending (DECLINE_FALLBACK, the host's generic decline). A review that cannot be delivered leaves the replacement untouched (a required transfer is never blocked by an outage)."""
    c = work(TERMINATION.format(task=task_prompt, rejected=rejected, replacement=replacement), "termination", exclude=used)
    text = _ok(c)
    out = {"reviewed": text is not None, "model": c.get("model_key"), "lineage": c.get("independence_key")}
    if text is None:
        out.update({"outcome": "REVIEW_UNAVAILABLE", "failure": c.get("failure_class") or "NO_ADMISSIBLE_WORKER"})
        return out
    opens = [x.strip() for x in re.split(r"\s*\|\s*", _field(text, "OPEN_REQUESTS")) if x.strip() and x.strip().upper() != "NONE"]
    clause, alt_text, verdict = _field(text, "TERMINATION_REQUIRED_CLAUSE"), _field(text, "ALTERNATIVE"), _field(text, "VERDICT").upper()
    clause_ok = bool(clause) and clause.upper() != "NONE" and _squash(clause) in _squash(task_prompt + "\n" + policy_text)
    alternative = parse(alt_text) if alt_text and alt_text.upper() != "NONE" else None
    alternative = alternative if alternative is not None and not terminating(alternative) else None
    out.update({"open_requests": opens, "clause": clause[:300], "clause_verified": clause_ok, "verdict": verdict, "alternative": alt_text[:300] if alternative else None, "grounds": text[:500]})
    if continuity is not None:
        for o in opens:
            continuity.register_objective(o, source="termination_review")
        continuity.reject("action", rejected[:300], reason="rejected by independent review")
        if clause_ok:
            continuity.restrict(clause, source="policy")
    if verdict == "TERMINATE" and clause_ok and not (opens and alternative is not None):
        out["outcome"] = "TERMINATE_APPROVED"
    elif alternative is not None:
        out.update({"outcome": "CONTINUE_ADOPTED", "action": alternative, "text": alt_text})
    else:
        out["outcome"] = "DECLINE_FALLBACK"
    if continuity is not None:
        continuity.decide(f"{out['outcome']}: {replacement[:160]}", grounds=(clause if clause_ok else "no verified clause requires ending the interaction")[:300])
    return out


def _grounds(text: str | None) -> str:
    """What a reviewer stated after the verdict line: the grounds of an agreement (a FOUND critique is its own grounds)."""
    parts = (text or "").strip().split("\n", 1)
    return parts[1].strip()[:400] if len(parts) > 1 else ""


@dataclass
class Collab:
    final_text: str
    final_action: dict | None
    changed: bool
    improved: bool
    validated: bool
    review_unavailable: bool
    unresolved: list = field(default_factory=list)
    attribution: list = field(default_factory=list)
    calls: int = 0
    rounds: int = 0
    stop_reason: str = ""
    specialist_used: bool = False
    failures: list = field(default_factory=list)
    agreement: list = field(default_factory=list)           # reviewers that found nothing: who, which answer, on what stated grounds (their claim, not proof)
    ungrounded_agreement: bool = False                      # every agreeing reviewer gave a bare verdict
    overruled: list = field(default_factory=list)           # author positions rejected after criticism and overruled by the specialist alone
    final_reviewed: bool = False                            # an independent reviewer examined exactly the final answer and found nothing
    independent_review: bool = False                        # a critique was delivered by a KNOWN lineage different from the author's (an unknown lineage proves nothing)
    termination: dict | None = None                         # the review of a terminating replacement (termination_review), None when no rejection ended in a terminating action
    closing: dict | None = None                             # final admissible action selected by the same controller that governed the exchanges
    declined: bool = False                                  # the rejected action is declined WITHOUT ending: the host's generic decline replaces it
    trail: list = field(default_factory=list)               # every ledger row in order: the draft, each critique (with its text), each revision, the specialist - who, which lineage, what


def collaborate(*, task_prompt: str, seed: dict, work: Callable[..., dict], ledger, claim_id: str, parse: Callable[[str], dict | None],
                digest: Callable[[dict], str], max_rounds: int = MAX_ROUNDS, terminating: Callable[[dict], bool] | None = None, policy_text: str = "",
                continuity=None, control=None) -> Collab:
    def sig(text: str) -> str | None:
        action = parse(text) if text else None
        return digest(action) if action is not None else None

    def asked(prompt, stage, *a, **kw):
        return work(prompt + GROUNDS if stage == "challenge" else prompt, stage, *a, **kw)

    seed_sig = sig(seed["text"])
    res = run_rounds(task_prompt=task_prompt, brief="", work=asked, ledger=ledger, claim_id=claim_id, n_solvers=1, review_single=True, seed_solution=seed,
                     max_rounds=max_rounds, signature=sig, control=control, defer_close=control is not None)
    rows = list(res.rows)
    by_id = {r.id: r for r in rows}
    crits = [r for r in rows if r.kind == "CRITIQUE"]
    found = [r for r in crits if r.epistemic_status == "DISSENT"]

    # positions after the rounds: the latest parseable one (the revised author position; a specialist's position when disagreement forced one) is the candidate
    final_text, final_action = seed["text"], parse(seed["text"])
    for text in reversed(list(res.positions.values())):
        action = parse(text)
        if action is not None:
            final_text, final_action = text, action
            break

    # unresolved objection after the rounds -> ONE specialist of a further lineage adjudicates (justified by substantive disagreement; Brother Mode's own tie-break needs several authors)
    verified_objection_ids = {r.id for r in found if (r.detail.get("verification") == "independently_confirmed"
                                                       and r.detail.get("relevance_assessed") is True
                                                       and r.detail.get("independent_confirmation") is True)}
    unresolved_ids = set(verified_objection_ids)
    for rv in rows:
        if rv.kind == "REVISION":
            prev = by_id.get(rv.detail.get("revises"))
            if sig(rv.answer_text or "") != (sig(prev.answer_text or "") if prev else seed_sig):
                unresolved_ids -= set(rv.detail.get("responding_to", []))
    specialist_used = False
    overruled: list = []
    if unresolved_ids and sig(final_text) == seed_sig and res.stop_reason != "LOOP_GUARD_FAILURES":
        specialists = True
        if control is not None:
            author = next((r.worker for r in reversed(rows) if r.kind in ("SOLUTION", "REVISION")), seed.get("model_key")) or "author"
            critics = list(dict.fromkeys(r.worker for r in found if r.id in unresolved_ids and r.worker and r.worker != author))
            critic = critics[0] if critics else "independent_reviewer"
            specialists = control.decide({"point": "SPECIALIST_OR_FINISH", "options": [SPECIALIST, "FINISH"], "baseline": SPECIALIST,
                                          "models": [author, critic], "signatures": {author: seed_sig, critic: "dissent"}, "disagree": True,
                                          "author": author, "verifications": [r.detail for r in found if r.id in unresolved_ids]}) == SPECIALIST
        if specialists:
            dossier = f"- position of the author:\n{final_text}\n" + "\n".join(f"- criticism (DISSENT):\n{r.answer_text}" for r in found if r.id in unresolved_ids)
            used = tuple(k for k in {seed.get("independence_key"), *[r.identity.get("independence_key") for r in crits]} if k)
            res.calls += 1
            c = work(SPECIALIST.format(task=task_prompt, dossier=dossier), "specialist", exclude=used)
            text = _ok(c)
            if text is not None:
                row = _add(ledger, claim_id, "SOLUTION", c, text, "UNVERIFIED", "SPECIALIST_TIEBREAK", {"resolves": [seed.get("receipt_id")] + [r.id for r in found]})
                rows.append(row)
                by_id[row.id] = row
                specialist_used = True
                if parse(text) is not None:
                    final_text, final_action = text, parse(text)
                if sig(final_text) != seed_sig and parse(text) is not None:       # the specialist moved the answer: nobody has examined it yet -> one renewed review by a lineage not yet involved
                    last_rev = next((r for r in reversed(rows) if r.kind == "REVISION"), None)
                    overruled.append({"author": seed.get("model_key"), "author_position": seed_sig, "overruled_by": row.worker,
                                      "author_grounds": (last_rev.answer_text or "")[:400] if last_rev else ""})
                    res.calls += 1
                    c2 = asked(CHALLENGE.format(task=task_prompt, work=final_text), "challenge", exclude=used + ((row.identity.get("independence_key"),) if row.identity.get("independence_key") else ()))
                    t2 = _ok(c2)
                    if t2 is not None:
                        hit = bool(_FOUND.search(t2)) or (not _NONE.search(t2) and len(t2) > 40)
                        r2 = _add(ledger, claim_id, "CRITIQUE", c2, t2, "DISSENT" if hit else "UNVERIFIED", "CRITICISM_FOUND" if hit else "NO_ISSUES_FOUND",
                                  {"targets": row.id, "round": res.rounds + 1, "reexamines": "SPECIALIST"})
                        rows.append(r2)
                        by_id[r2.id] = r2
                        crits.append(r2)
                        if hit:
                            found.append(r2)
                    else:
                        res.failures.append({"stage": "specialist_review", "class": c2.get("failure_class") or "NO_ADMISSIBLE_WORKER", "model": c2.get("model_key")})
            else:
                res.failures.append({"stage": "specialist", "class": c.get("failure_class") or "NO_ADMISSIBLE_WORKER", "model": c.get("model_key")})

    termination, declined = None, False
    seed_action = parse(seed["text"])
    if terminating is not None and final_action is not None and terminating(final_action) and not (seed_action is not None and terminating(seed_action)):
        used_now = tuple(k for k in {seed.get("independence_key"), *[r.identity.get("independence_key") for r in rows if r.identity.get("independence_key")]} if k)
        res.calls += 1
        termination = termination_review(task_prompt=task_prompt, policy_text=policy_text, rejected=seed["text"], replacement=final_text, work=asked, parse=parse, terminating=terminating, used=used_now,
                                         continuity=continuity)
        if termination["outcome"] == "CONTINUE_ADOPTED":
            final_text, final_action = termination["text"], termination["action"]
        elif termination["outcome"] == "DECLINE_FALLBACK":
            final_action, declined = None, True
    changed = sig(final_text) != seed_sig
    material_critics: set = set()
    attribution = []
    for rv in rows:
        if rv.kind == "REVISION":
            prev = by_id.get(rv.detail.get("revises"))
            moved = sig(rv.answer_text or "") != (sig(prev.answer_text or "") if prev else seed_sig)
            if moved:
                material_critics.update(rid for rid in rv.detail.get("responding_to", []) if rid in verified_objection_ids)
            attribution.append({"role": "revision", "model": rv.worker, "lineage": rv.identity.get("independence_key"), "changed_action": moved})
        elif rv.kind == "SOLUTION" and rv.reason == "SPECIALIST_TIEBREAK":
            moved = sig(rv.answer_text or "") != seed_sig
            if moved and sig(rv.answer_text or "") == sig(final_text):
                material_critics.update(rid for rid in rv.detail.get("resolves", []) if rid in verified_objection_ids)
            attribution.append({"role": "specialist", "model": rv.worker, "lineage": rv.identity.get("independence_key"), "changed_action": moved, "grounds": (rv.answer_text or "")[:400]})
    final_sig = sig(final_text)
    agreement = []
    for c in crits:
        tgt = by_id.get(c.detail.get("targets"))
        examined = sig(tgt.answer_text or "") if tgt else None
        has_issues = c.epistemic_status == "DISSENT"
        entry = {"role": "critique", "model": c.worker, "lineage": c.identity.get("independence_key"), "found_issues": has_issues, "materially_improved": c.id in material_critics,
                 "examined": examined, "grounds": _grounds(c.answer_text) if not has_issues else "", "grounds_stated": bool(_grounds(c.answer_text)) if not has_issues else True}
        attribution.append(entry)
        if not has_issues:
            agreement.append({"model": c.worker, "lineage": entry["lineage"], "agreed_with": examined, "grounds": entry["grounds"], "grounds_stated": entry["grounds_stated"]})
    unresolved = [{"critic": c.worker, "objection": (c.answer_text or "")[:400]} for c in found if c.id not in material_critics]
    improved = changed and bool(material_critics)
    trail = [{"stage": r.kind, "reason": r.reason, "model": r.worker, "lineage": r.identity.get("independence_key"), "status": r.epistemic_status, "text": (r.answer_text or "")[:600]} for r in rows]
    if termination is not None:
        trail.append({"stage": "TERMINATION_REVIEW", "reason": termination["outcome"], "model": termination.get("model"), "lineage": termination.get("lineage"), "status": "UNVERIFIED",
                      "text": ("open: " + " | ".join(termination.get("open_requests", [])) + f"; clause verified: {termination.get('clause_verified')}; verdict: {termination.get('verdict')}")[:600]})
    if sig(final_text) != seed_sig and not material_critics and not (termination and termination.get("outcome") in ("TERMINATE_APPROVED", "CONTINUE_ADOPTED")):
        final_text, final_action = seed["text"], parse(seed["text"])
    closing = None
    if control is not None:
        final_model = next((r.worker for r in reversed(rows) if r.kind in ("SOLUTION", "REVISION") and sig(r.answer_text or "") == final_sig), seed.get("model_key")) or "final"
        if declined:
            final_action, final_text, final_sig = ({"action": "message", "content": "I cannot perform that action."}, "", None)
        signatures = {final_model: final_sig} if final_sig is not None else {}
        closing = control.close({"signatures": signatures, "models": list(signatures), "disagree": False,
                                 "first": {seed.get("model_key") or "seed": seed_sig} if not declined else {},
                                 "levels": {}, "stop_reason": res.stop_reason})
        if not declined:
            selected = closing.get("final_answer")
            if selected != final_sig or final_action is None:
                raise ValueError("controller closing did not select the executed admissible final candidate")
    author = seed.get("independence_key")
    independent_review = any(c.identity.get("independence_key") and c.identity.get("independence_key") != author for c in crits)
    grounded = any(a["grounds_stated"] for a in agreement)
    final_reviewed = any(a["agreed_with"] == final_sig and a["agreed_with"] is not None for a in agreement)
    return Collab(final_text=final_text, final_action=final_action, changed=changed, improved=improved, validated=bool(crits) and not found and not changed and grounded,
                  review_unavailable=not crits, unresolved=unresolved, termination=termination, declined=declined, attribution=attribution, calls=res.calls, rounds=res.rounds, stop_reason=res.stop_reason,
                  specialist_used=specialist_used, failures=res.failures, agreement=agreement,
                  ungrounded_agreement=bool(agreement) and not grounded, overruled=overruled, final_reviewed=final_reviewed, independent_review=independent_review, trail=trail, closing=closing)
