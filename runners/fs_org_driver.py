"""Non-frozen FruitStack organizational-learning driver (NOT a frozen OGI arm; S1/QA-1/QA-2D drivers are untouched).

One episode = one CherryMe Brother Mode collaboration (cherryme.brother.run_rounds) on an arbitrary task, with the opt-in LearningHook:
  applied arm: verified, applicable discoveries from OTHER runs are shown as the `brief` (retrieval + application recorded);
  control arm: same task, same workers, no brief (apply=False) -> nothing retrieved, nothing applied.
After both arms the task's INDEPENDENT grader (a test run, an official grader, a dataset key: never a model) scores each final answer outside any live context, and
the applied arm's discoveries receive an OUTCOME against the control. Discoveries made in an episode are captured as ASSERTED (a critique that changed an answer);
only independent verification (verifier kinds of the ledger) can make them reusable. Optional mirrors: OrangeMe projection (cross-session) and MangoMe (ledger mirror).
Every arm writes an instrumentation row (calls, failures, seconds, retrieved ids, answer, reward) for later, separately preregistered comparisons. No result here is evidence
of organizational gain by itself.
"""
from __future__ import annotations

import hashlib
import time
from collections import Counter
from dataclasses import dataclass
from typing import Callable

from ogi013_learning_hook import LearningHook
from ogi013_org_discoveries import VERIFIERS, Ledger


@dataclass
class Task:
    task_ref: str
    prompt: str
    signature: Callable[[str], str | None]          # final-answer extraction from a position text
    grade: Callable[[str | None], float]            # independent grader in [0, 1]; called only after the episode
    grader: str                                     # verifier kind of the grader (ogi013_org_discoveries.VERIFIERS)
    score: Callable[[str], float] | None = None     # VISIBLE checks only (e.g. visible-test pass count), the same for every arm; None -> plurality


def _lineage(row) -> str | None:
    return (getattr(row, "identity", None) or {}).get("independence_key")


def critique_ground(detail: dict | None) -> dict:
    """Brother Mode critique host facts -> objection ground in the LearningHook vocabulary. CherryMe's own mapping (appleme_bridge.critique_level) decides the level;
    `verification == "verified"` means the critic's check was EXECUTED (ogi013 level `reproduced`). Only an executed check sets argument.executed, so a model-asserted or
    merely 'independent' critique stays ASSERTED (EVAL-002 defect: the ground used to carry the level only, and LearningHook never verified anything)."""
    from cherryme.appleme_bridge import critique_level
    d = detail or {}
    executed = d.get("verification") == "verified"
    level = {"executed": "reproduced"}.get(critique_level(d), critique_level(d))
    if level == "none":
        level = d.get("verification") or "model_asserted"
    return {"level": level, "argument": {"executed": executed, "source": "cherryme.brother critique verification"}}


def capture_brother(hook: LearningHook, task_ref: str, rows, signature) -> list[str]:
    """A CRITIQUE from a DIFFERENT lineage that a later REVISION answered with a changed answer is a candidate discovery (ASSERTED; VERIFIED only when the critique was backed
    by an executed check, see critique_ground). Same-lineage critique is ignored."""
    by_id = {r.id: r for r in rows}
    objections = []
    for rev in (r for r in rows if r.kind == "REVISION"):
        before = by_id.get((rev.detail or {}).get("revises"))
        for cid in (rev.detail or {}).get("responding_to", []):
            crit = by_id.get(cid)
            if crit is None or before is None or _lineage(crit) is None or _lineage(crit) == _lineage(before):
                continue
            if signature(rev.answer_text) != signature(before.answer_text):
                objections.append({"id": crit.id, "state": "ACCEPTED", "lineage": _lineage(crit), "target": before.id, "text": crit.answer_text or "",
                                   "ground": critique_ground(crit.detail)})
    if not objections:
        return []
    ids = {r.worker: {"model": r.worker, "lineage": _lineage(r), "receipt": r.receipt} for r in rows if r.kind == "SOLUTION"}
    return hook.capture(task_ref, objections=objections, final_letter=None, first_letter=None, how="brother_mode", identities=ids)


def select_answer(task_ref: str, texts: list[str], signature, score: Callable[[str], float] | None = None) -> tuple[str | None, str]:
    """THE answer selector of every study arm (T, E_div, R_mono): one rule, applied to the arm's final candidate set.
    1. score (the task's VISIBLE checks, e.g. visible-test pass count; never the hidden grader) when the task has one: highest score;
    2. among those, plurality of the parsed answers (unparseable candidates only count when nothing parses);
    3. remaining tie: smallest sha256(task_ref, answer). Order-, model- and position-independent, so neither the first solver nor registration order can win a tie."""
    cands = [(signature(t), t) for t in texts]
    parsed = [c for c in cands if c[0] is not None]
    if not parsed:
        return None, "NO_PARSEABLE_CANDIDATE"
    if len({s for s, _ in cands}) == 1:
        return cands[0][0], "CONSENSUS"
    if score is not None:
        best = max(score(t) for _, t in parsed)
        parsed = [c for c in parsed if score(c[1]) == best]
    counts = Counter(s for s, _ in parsed)
    top = max(counts.values())
    tied = [s for s, n in counts.items() if n == top]
    if len(tied) == 1:
        return tied[0], "SELECTED"
    return min(tied, key=lambda s: hashlib.sha256(f"{task_ref}\0{s}".encode()).hexdigest()), "SELECTED_HASH_TIE"


def final_answer(res, signature, task_ref: str = "", score=None) -> tuple[str | None, str]:
    """T's final answer = select_answer over the final positions (the same selector as the controls). The old rule (first solver's position retained on disagreement)
    is reported as `primary_retained` for continuity only; it never decides."""
    return select_answer(task_ref, list(res.positions.values()), signature, score)


def run_episode(task: Task, *, work, hook: LearningHook, arm: str, n_solvers: int = 2, max_rounds: int = 3, control=None) -> dict:
    from cherryme.brother import run_rounds
    from cherryme.contributions import ContributionLedger
    t0 = time.monotonic()
    brief, used = hook.brief(task.task_ref, task.prompt)
    cl = ContributionLedger()
    res = run_rounds(task_prompt=task.prompt, brief=brief, work=work, ledger=cl, claim_id=f"{hook.run_id}:{task.task_ref}", n_solvers=n_solvers, max_rounds=max_rounds,
                     signature=task.signature, control=control)
    answer, how = final_answer(res, task.signature, task.task_ref, task.score)
    first = next(iter(res.positions.values()), None)
    try:                                                   # capture never changes the answer; failures are reported
        captured, cap_err = capture_brother(hook, task.task_ref, cl.rows, task.signature), None
    except Exception as exc:  # noqa: BLE001
        captured, cap_err = [], f"{type(exc).__name__}: {str(exc)[:120]}"
    return {"task": task.task_ref, "arm": arm, "run": hook.run_id, "answer": answer, "how": how,
            "primary_retained": task.signature(first) if first else None, "stop": res.stop_reason, "calls": res.calls, "rounds": res.rounds,
            "failures": len(res.failures), "seconds": round(time.monotonic() - t0, 3), "retrieved": used, "captured": captured, "capture_error": cap_err,
            "brief_errors": list(hook.errors), "lineages": sorted({_lineage(r) for r in cl.rows if r.kind == "SOLUTION" and _lineage(r)}),
            "row_kinds": dict(Counter(r.kind for r in cl.rows))}


def run_pair(task: Task, *, work, ledger: Ledger, tag: str, projection=None, results=None) -> dict:
    """Control first, then applied, on the same task; independent grading afterwards; outcome recorded for every discovery applied in the applied arm."""
    if task.grader not in VERIFIERS:
        raise ValueError(f"the grader must be independent of the models: one of {sorted(VERIFIERS)}")
    prompts: dict[str, list] = {"control": [], "applied": []}

    def recording(arm):
        def w(prompt, stage, **kw):
            prompts[arm].append((stage, prompt))
            return work(prompt, stage, **kw)
        return w
    ctl = run_episode(task, work=recording("control"), hook=LearningHook(ledger, run_id=f"{tag}:control", apply=False), arm="control")
    hook = LearningHook(ledger, run_id=f"{tag}:applied", apply=True)
    app = run_episode(task, work=recording("applied"), hook=hook, arm="applied")
    ctl["reward"], app["reward"] = task.grade(ctl["answer"]), task.grade(app["answer"])
    if app["retrieved"]:
        hook.outcomes(task.task_ref, reward=app["reward"], control_reward=ctl["reward"], control_run=ctl["run"], grader=task.grader)
    out = {"task": task.task_ref, "control": ctl, "applied": app, "prompts": prompts}
    if projection is not None:
        out["projected"] = projection.publish(ledger)
    if results is not None:
        import json
        from pathlib import Path
        with Path(results).open("a", encoding="utf-8") as f:
            for row in (ctl, app):
                f.write(json.dumps({**row, "grader": task.grader}, sort_keys=True) + "\n")
    return out
