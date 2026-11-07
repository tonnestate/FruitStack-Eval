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


STUDY_ARMS = {"T", "E_div", "R_mono", "S"}          # rows of these arms are analysable only with a passed row-level identity check


def metered(work, log: list):
    """Every call's identity and tokens as the worker reports them from its PlumMe receipt / lease facts (model_key, independence_key, receipt_id, input/output tokens)."""
    def w(prompt, stage, **kw):
        c = work(prompt, stage, **kw)
        log.append({"stage": stage, "ok": bool(c.get("success") and (c.get("output") or "").strip()), "model_key": c.get("model_key"),
                    "independence_key": c.get("independence_key"), "receipt_id": c.get("receipt_id"), "prefer": kw.get("prefer"),
                    "input_tokens": c.get("input_tokens"), "output_tokens": c.get("output_tokens")})
        return c
    return w


def tokens(receipts: list) -> dict:
    known = [r for r in receipts if r["input_tokens"] is not None or r["output_tokens"] is not None]
    return {"input": sum(r["input_tokens"] or 0 for r in known), "output": sum(r["output_tokens"] or 0 for r in known), "calls_without_tokens": len(receipts) - len(known)}


def identity_check(receipts: list, roster: dict, cycle: list | None = None) -> str | None:
    """Row-level S1 guard, enforced from the executed receipts (None = valid, else the INFRA_IDENTITY reason).
    roster: the arm's declared members {model_key: independence_key}, pinned at lock. The successful solve calls must realise EXACTLY the declared distinct lineages
    (a declared multi-model roster run on one lineage, e.g. Luna twice, is invalid); no successful call may come from outside the roster; with a `cycle` (E_div/R_mono)
    the i-th successful solve call must be the planned member's lineage."""
    declared = set(roster.values())
    if None in declared or len(declared) != len(roster):
        return "DECLARED_ROSTER_NOT_DISTINCT"
    ok = [r for r in receipts if r["ok"]]
    if any(r["independence_key"] is None for r in ok):
        return "RECEIPT_WITHOUT_LINEAGE"
    if any(r["independence_key"] not in declared for r in ok):
        return "LINEAGE_OUTSIDE_ROSTER"
    solve = [r for r in receipts if r["stage"] == "solve"]
    if cycle is not None and any(r["ok"] and r["independence_key"] != roster[cycle[i % len(cycle)]] for i, r in enumerate(solve)):
        return "PLAN_MISMATCH"
    realised = {r["independence_key"] for r in solve if r["ok"]}
    if realised != declared:
        return "SINGLE_LINEAGE_ROW" if len(realised) == 1 and len(declared) > 1 else "ROSTER_NOT_REALISED"
    return None


def _identity(arm: str, receipts: list, roster: dict | None, cycle=None) -> dict:
    if roster is None:
        if arm in STUDY_ARMS:
            raise ValueError(f"arm {arm} needs its declared roster for the row-level identity check")
        return {"identity_valid": None, "exclusion": None}
    why = identity_check(receipts, roster, cycle)
    return {"identity_valid": why is None, "exclusion": None if why is None else f"INFRA_IDENTITY:{why}"}


def split_valid(rows: list) -> tuple[list, list]:
    """Analysis entry: rows with a failed identity check are excluded (kept with their reason); unchecked rows of study arms never count."""
    valid = [r for r in rows if r.get("identity_valid") is True]
    return valid, [r for r in rows if r not in valid]


def member_answers(rows, signature) -> list[dict]:
    """Each blind solver's FIRST answer and the final answer of the same position (following its REVISION chain). Specialist tie-break rows are not members' first answers."""
    nxt = {(r.detail or {}).get("revises"): r for r in rows if r.kind == "REVISION"}
    out = []
    for s in (r for r in rows if r.kind == "SOLUTION" and r.reason == "INDEPENDENT_SOLUTION"):
        last = s
        while last.id in nxt:
            last = nxt[last.id]
        out.append({"lineage": _lineage(s), "first": signature(s.answer_text), "final": signature(last.answer_text)})
    return out


def grade_after(row: dict, task: Task) -> dict:
    """AFTER the episode only (no grading result ever enters a live context): reward of the selected answer, and the collaboration-effect metrics (prereg DRAFT §5):
      correct := grade == 1.0
      episode class  CORRECTED  no member's first answer correct, final correct      (wrong -> right)
                     DAMAGED    >=1 member's first answer correct, final wrong       (right -> wrong; for E_div/R_mono: a correct draft was not selected)
                     HELD       >=1 first correct, final correct;   UNSOLVED  no first correct, final wrong
      member counts  corrected_members: first wrong, that member's final position right; damaged_members: first right, final position wrong (0 for controls)."""
    ok = lambda a: task.grade(a) == 1.0          # noqa: E731
    members = row.get("members") or []
    any_first, final = any(ok(m["first"]) for m in members), ok(row["answer"])
    row["reward"] = task.grade(row["answer"])
    row["effect"] = {"class": ("HELD" if final else "DAMAGED") if any_first else ("CORRECTED" if final else "UNSOLVED"),
                     "corrected_members": sum(not ok(m["first"]) and ok(m["final"]) for m in members),
                     "damaged_members": sum(ok(m["first"]) and not ok(m["final"]) for m in members),
                     "first_correct": sum(ok(m["first"]) for m in members), "members": len(members)}
    return row


def run_episode(task: Task, *, work, hook: LearningHook, arm: str, n_solvers: int = 2, max_rounds: int = 3, control=None, roster: dict | None = None) -> dict:
    from cherryme.brother import run_rounds
    from cherryme.contributions import ContributionLedger
    t0 = time.monotonic()
    brief, used = hook.brief(task.task_ref, task.prompt)
    cl, receipts = ContributionLedger(), []
    res = run_rounds(task_prompt=task.prompt, brief=brief, work=metered(work, receipts), ledger=cl, claim_id=f"{hook.run_id}:{task.task_ref}", n_solvers=n_solvers,
                     max_rounds=max_rounds, signature=task.signature, control=control)
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
            "row_kinds": dict(Counter(r.kind for r in cl.rows)), "members": member_answers(cl.rows, task.signature), "receipts": receipts, "tokens": tokens(receipts), **_identity(arm, receipts, roster)}


def run_samples(task: Task, *, work, arm: str, roster: dict, cycle: list, k: int, token_budget: int | None = None, max_calls: int | None = None) -> dict:
    """Non-collaborative controls with T's selector: independent drafts from the SAME solve prompt T's solvers get (no brief, no critique, exchange or revision),
    then select_answer. One runner, three arms:
      E_div  (diversity-only, primary contrast to T): roster = T's roster, cycle = list(roster)  -> round-robin over the same models
      R_mono (same-model repeated sampling):          roster = {pin: lineage}, cycle = [pin]      -> one model, same budget
      S      (single member):                          roster = {m: lineage},   cycle = [m], k = 1
    Budget: with token_budget (T's receipted input+output tokens on this task) drafts are drawn until it is reached; when a receipt carries no token count the call
    count k (T's receipted calls) decides. max_calls (default 3k) caps either rule. Never tuned on outcomes: k and token_budget come from T's receipts."""
    from cherryme.brother import SOLVE
    t0, receipts, texts = time.monotonic(), [], []
    w, prompt, cap = metered(work, receipts), SOLVE.format(task=task.prompt, brief=""), max_calls or 3 * max(1, k)

    def more() -> bool:
        if len(receipts) >= cap:
            return False
        t = tokens(receipts)
        if token_budget is None or t["calls_without_tokens"]:
            return len(receipts) < k
        return t["input"] + t["output"] < token_budget
    while more():
        c = w(prompt, "solve", prefer=cycle[len(receipts) % len(cycle)])
        if receipts[-1]["ok"]:
            texts.append(c["output"])
    answer, how = select_answer(task.task_ref, texts, task.signature, task.score)
    return {"task": task.task_ref, "arm": arm, "answer": answer, "how": how, "calls": len(receipts), "failures": sum(not r["ok"] for r in receipts),
            "seconds": round(time.monotonic() - t0, 3), "drafts": len(texts), "members": [{"lineage": r["independence_key"], "first": task.signature(t), "final": task.signature(t)}
                                                                            for r, t in zip([r for r in receipts if r["ok"]], texts)], "receipts": receipts, "tokens": tokens(receipts),
            **_identity(arm, receipts, roster, cycle)}


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
    grade_after(ctl, task), grade_after(app, task)
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
