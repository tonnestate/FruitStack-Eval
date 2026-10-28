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
  unresolved        - issues were found and no revision / specialist changed the action: the objection stays visible"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from cherryme.brother import SPECIALIST, _add, _ok, run_rounds

MAX_ROUNDS = 2


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


def collaborate(*, task_prompt: str, seed: dict, work: Callable[..., dict], ledger, claim_id: str, parse: Callable[[str], dict | None],
                digest: Callable[[dict], str], max_rounds: int = MAX_ROUNDS) -> Collab:
    def sig(text: str) -> str | None:
        action = parse(text) if text else None
        return digest(action) if action is not None else None

    seed_sig = sig(seed["text"])
    res = run_rounds(task_prompt=task_prompt, brief="", work=work, ledger=ledger, claim_id=claim_id, n_solvers=1, review_single=True, seed_solution=seed,
                     max_rounds=max_rounds, signature=sig)
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
    unresolved_ids = {r.id for r in found}
    for rv in rows:
        if rv.kind == "REVISION":
            prev = by_id.get(rv.detail.get("revises"))
            if sig(rv.answer_text or "") != (sig(prev.answer_text or "") if prev else seed_sig):
                unresolved_ids -= set(rv.detail.get("responding_to", []))
    specialist_used = False
    if unresolved_ids and sig(final_text) == seed_sig and res.stop_reason != "LOOP_GUARD_FAILURES":
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
        else:
            res.failures.append({"stage": "specialist", "class": c.get("failure_class") or "NO_ADMISSIBLE_WORKER", "model": c.get("model_key")})

    changed = sig(final_text) != seed_sig
    material_critics: set = set()
    attribution = []
    for rv in rows:
        if rv.kind == "REVISION":
            prev = by_id.get(rv.detail.get("revises"))
            moved = sig(rv.answer_text or "") != (sig(prev.answer_text or "") if prev else seed_sig)
            if moved:
                material_critics.update(rv.detail.get("responding_to", []))
            attribution.append({"role": "revision", "model": rv.worker, "lineage": rv.identity.get("independence_key"), "changed_action": moved})
        elif rv.kind == "SOLUTION" and rv.reason == "SPECIALIST_TIEBREAK":
            moved = sig(rv.answer_text or "") != seed_sig
            if moved and sig(rv.answer_text or "") == sig(final_text):
                material_critics.update(rv.detail.get("resolves", []))
            attribution.append({"role": "specialist", "model": rv.worker, "lineage": rv.identity.get("independence_key"), "changed_action": moved})
    for c in crits:
        attribution.append({"role": "critique", "model": c.worker, "lineage": c.identity.get("independence_key"), "found_issues": c.epistemic_status == "DISSENT",
                            "materially_improved": c.id in material_critics})
    unresolved = [{"critic": c.worker, "objection": (c.answer_text or "")[:400]} for c in found if c.id not in material_critics]
    improved = changed and bool(material_critics)
    return Collab(final_text=final_text, final_action=final_action, changed=changed, improved=improved, validated=bool(crits) and not found and not changed,
                  review_unavailable=not crits, unresolved=unresolved, attribution=attribution, calls=res.calls, rounds=res.rounds, stop_reason=res.stop_reason,
                  specialist_used=specialist_used, failures=res.failures)
