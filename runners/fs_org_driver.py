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

from ogi013_learning_hook import LearningHook, format_brief, placebo_brief
from ogi013_org_discoveries import VERIFIERS, Ledger


@dataclass
class Task:
    task_ref: str
    prompt: str
    signature: Callable[[str], str | None]          # final-answer extraction from a position text
    grade: Callable[[str | None], float]            # independent grader in [0, 1]; called only after the episode
    grader: str                                     # verifier kind of the grader (ogi013_org_discoveries.VERIFIERS)
    score: Callable[[str], float] | None = None     # VISIBLE checks only (e.g. visible-test pass count), the same for every arm; None -> plurality
    check: Callable[[str], str] | None = None       # VISIBLE checks EXECUTED on a candidate text -> report (never the hidden grader); used by run_team's executed critique


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


TEAM_COMPONENTS = frozenset({"appleme", "lsd", "research_tree", "memory", "plumme_selection", "executed_critique"})
STUDY_ARMS = {"T", "E_div", "R_mono", "S", "G_mas"} | {f"T-{c}" for c in TEAM_COMPONENTS}   # rows of these arms are analysable only with a passed row-level identity check


def metered(work, log: list, roles: dict | None = None):
    """Every call's identity and tokens as the worker reports them from its PlumMe receipt / lease facts (model_key, independence_key, receipt_id, input/output tokens).
    roles {stage: model_key}: a call of that stage is routed to its declared roster member (e.g. Brother Mode's specialist call, which itself only excludes the solvers)."""
    def w(prompt, stage, **kw):
        if roles and stage in roles and not kw.get("prefer"):
            kw["prefer"] = roles[stage]
        c = work(prompt, stage, **kw)
        log.append({"stage": stage, "ok": bool(c.get("success") and (c.get("output") or "").strip()), "model_key": c.get("model_key"),
                    "independence_key": c.get("independence_key"), "receipt_id": c.get("receipt_id"), "prefer": kw.get("prefer"),
                    "input_tokens": c.get("input_tokens"), "output_tokens": c.get("output_tokens")})
        return c
    return w


def tokens(receipts: list) -> dict:
    known = [r for r in receipts if r["input_tokens"] is not None or r["output_tokens"] is not None]
    return {"input": sum(r["input_tokens"] or 0 for r in known), "output": sum(r["output_tokens"] or 0 for r in known), "calls_without_tokens": len(receipts) - len(known)}


def identity_check(receipts: list, roster: dict, cycle: list | None = None, roles: dict | None = None) -> str | None:
    """Row-level S1 guard, enforced from the executed receipts (None = valid, else the INFRA_IDENTITY reason).
    roster: the arm's declared members {model_key: independence_key}, pinned at lock. The successful solve calls must realise EXACTLY the declared distinct lineages
    (a declared multi-model roster run on one lineage, e.g. Luna twice, is invalid); no successful call may come from outside the roster; with a `cycle` (E_div/R_mono)
    the i-th successful solve call must be the planned member's lineage.
    roles {stage: model_key}: every successful call of that stage must come from that declared member (ROLE_MISMATCH). The "specialist" role is the roster rule of the prereg
    (§6): the Brother Mode tie-break lineage is a declared member of the SAME roster in every arm, so it is optional for the solve calls (a row that never needs it, or a
    control that never calls it, stays valid) and the team never gets a model the controls do not have."""
    declared = set(roster.values())
    if None in declared or len(declared) != len(roster):
        return "DECLARED_ROSTER_NOT_DISTINCT"
    roles = roles or {}
    if any(m not in roster for m in roles.values()):
        return "ROLE_OUTSIDE_ROSTER"
    ok = [r for r in receipts if r["ok"]]
    if any(r["independence_key"] is None for r in ok):
        return "RECEIPT_WITHOUT_LINEAGE"
    if any(r["independence_key"] not in declared for r in ok):
        return "LINEAGE_OUTSIDE_ROSTER"
    if any(r["stage"] in roles and r["independence_key"] != roster[roles[r["stage"]]] for r in ok):
        return "ROLE_MISMATCH"
    solve = [r for r in receipts if r["stage"] == "solve"]
    if cycle is not None and any(r["ok"] and r["independence_key"] != roster[cycle[i % len(cycle)]] for i, r in enumerate(solve)):
        return "PLAN_MISMATCH"
    realised = {r["independence_key"] for r in solve if r["ok"]}
    required = declared - ({roster[roles["specialist"]]} if "specialist" in roles else set())
    if not required <= realised:                                     # realised is a subset of declared (LINEAGE_OUTSIDE_ROSTER above)
        return "SINGLE_LINEAGE_ROW" if len(realised) == 1 and len(required) > 1 else "ROSTER_NOT_REALISED"
    return None


def _identity(arm: str, receipts: list, roster: dict | None, cycle=None, roles=None) -> dict:
    if roster is None:
        if arm in STUDY_ARMS:
            raise ValueError(f"arm {arm} needs its declared roster for the row-level identity check")
        return {"identity_valid": None, "exclusion": None}
    why = identity_check(receipts, roster, cycle, roles)
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


def run_episode(task: Task, *, work, hook: LearningHook, arm: str, n_solvers: int = 2, max_rounds: int = 3, control=None, roster: dict | None = None,
                specialist: str | None = None, brief: str | None = None) -> dict:
    """specialist: the roster member Brother Mode's tie-break is routed to (prereg §6). brief: a fixed brief instead of the hook's retrieval (EVAL-002 sham arm; nothing is
    retrieved or applied then)."""
    from cherryme.brother import run_rounds
    from cherryme.contributions import ContributionLedger
    t0 = time.monotonic()
    brief, used = (brief, []) if brief is not None else hook.brief(task.task_ref, task.prompt)
    roles = {"specialist": specialist} if specialist else None
    cl, receipts = ContributionLedger(), []
    res = run_rounds(task_prompt=task.prompt, brief=brief, work=metered(work, receipts, roles), ledger=cl, claim_id=f"{hook.run_id}:{task.task_ref}", n_solvers=n_solvers,
                     max_rounds=max_rounds, signature=task.signature, control=control)
    answer, how = final_answer(res, task.signature, task.task_ref, task.score)
    first = next(iter(res.positions.values()), None)
    try:                                                   # capture never changes the answer; failures are reported
        captured, cap_err = capture_brother(hook, task.task_ref, cl.rows, task.signature), None
    except Exception as exc:  # noqa: BLE001
        captured, cap_err = [], f"{type(exc).__name__}: {str(exc)[:120]}"
    return {"task": task.task_ref, "arm": arm, "run": hook.run_id, "answer": answer, "how": how,
            "primary_retained": task.signature(first) if first else None, "stop": res.stop_reason, "calls": res.calls, "rounds": res.rounds,
            "failures": len(res.failures), "seconds": round(time.monotonic() - t0, 3), "retrieved": used, "brief_chars": len(brief), "captured": captured, "capture_error": cap_err,
            "brief_errors": list(hook.errors), "lineages": sorted({_lineage(r) for r in cl.rows if r.kind == "SOLUTION" and _lineage(r)}),
            "row_kinds": dict(Counter(r.kind for r in cl.rows)), "members": member_answers(cl.rows, task.signature), "receipts": receipts, "tokens": tokens(receipts),
            "specialist_used": res.specialist_used, **_identity(arm, receipts, roster, roles=roles)}


_RESEARCH_ADVICE = {"SEEK_INDEPENDENT_EVIDENCE", "ADVERSARIAL_REVIEW", "OPEN_ALTERNATIVE_BRANCH"}


def _fixed_roster(w, roster: dict, cycle: list, roles: dict | None):
    """plumme_selection OFF: every call without a prefer is pinned to a roster member by a fixed rule (per stage kind a round-robin over `cycle`, skipping excluded lineages)."""
    seen: Counter = Counter()

    def p(prompt, stage, **kw):
        if not kw.get("prefer") and stage not in (roles or {}):
            kind, ex = stage.split(":")[0], set(kw.get("exclude") or ())
            rot = cycle[seen[kind] % len(cycle):] + cycle[:seen[kind] % len(cycle)]
            seen[kind] += 1
            kw["prefer"] = next((m for m in rot if roster[m] not in ex), rot[0])
        return w(prompt, stage, **kw)
    return p


def _executed_critique(w, check, ev):
    """executed_critique ON: before a Brother Mode challenge the host EXECUTES the task's visible checks on the challenged solution and hands the report to the critic; the
    call is then marked verification="verified" (CherryMe's 'executed' critique level, see critique_ground). OFF: the critic sees no execution, the critique stays asserted."""
    def c(prompt, stage, **kw):
        if stage != "challenge":
            return w(prompt, stage, **kw)
        target = prompt.split("--- colleague solution ---\n", 1)[-1].split("\n--- end ---", 1)[0]    # cherryme.brother.CHALLENGE markers
        report = check(target)
        ev("EXECUTED_CRITIQUE", chars=len(report))
        return {**w(f"{prompt}\n\nThe host EXECUTED the task's visible checks on this colleague solution:\n{report}\n", stage, **kw), "verification": "verified"}
    return c


def run_team(task: Task, *, work, hook: LearningHook, roster: dict, components=TEAM_COMPONENTS, cycle: list | None = None, n_solvers: int = 2, max_rounds: int = 3,
             advice_rounds: int = 1, specialist: str | None = None, arm: str | None = None) -> dict:
    """T, the full FruitStack team, through CherryMe's research path in the order of peachme.research.run_research (Research Tree -> memory brief -> LSD Room ->
    Brother Mode on the root -> AppleMe diagnosis -> apply_advice -> prioritized re-investigation -> finalize). The study's `work` stays the worker (receipts, tokens, identity
    guard on EVERY call incl. LSD; the tree and AppleMe make no model calls). run_research itself is not called: its WorkerPool is bound to a PeachMe runtime and its results
    carry no token counts (gap, see PR). `components` switches (TEAM_COMPONENTS); an ablation removes exactly one and is recorded in the row (arm "T-<component>"):
      research_tree     off: Brother Mode runs on the task directly (no tree); AppleMe then advises Brother Mode through CherryMe's AdvisoryControl, LSD hypotheses have no consumer
      appleme           off: no diagnosis, no advice (the tree funds nothing beyond the root)
      lsd               off: no LSD Room calls
      memory            off: no LearningHook brief, no capture
      plumme_selection  off: fixed roster rule (_fixed_roster) instead of PlumMe's AUTO pick
      executed_critique off: critics get no executed visible-check report (also a no-op when the task has no `check`, recorded as NO_VISIBLE_CHECK)
    Final answer: select_answer over the final positions of every Brother Mode investigation."""
    from cherryme.appleme_bridge import AdvisoryControl, doctor_advice, research_tree_events
    from cherryme.brother import run_rounds
    from cherryme.contributions import ContributionLedger
    from cherryme.lsd_room import run_lsd_room
    from cherryme.research_tree import ResearchTree
    comps = frozenset(components)
    if comps - TEAM_COMPONENTS:
        raise ValueError(f"unknown components {sorted(comps - TEAM_COMPONENTS)}")
    off = sorted(TEAM_COMPONENTS - comps)
    if arm is None:
        if len(off) > 1:
            raise ValueError("a study ablation turns exactly one component off; name the arm explicitly otherwise")
        arm = f"T-{off[0]}" if off else "T"
    t0, events, receipts = time.monotonic(), [], []
    ev = lambda kind, **kw: events.append({"type": kind, **kw})          # noqa: E731
    roles = {"specialist": specialist} if specialist else None
    w = metered(work, receipts, roles)
    if "plumme_selection" not in comps:
        w = _fixed_roster(w, roster, cycle or list(roster), roles)
    ev("SELECTION", mode="plumme" if "plumme_selection" in comps else "fixed_roster")
    critique = "ON" if "executed_critique" in comps and task.check else "NO_VISIBLE_CHECK" if "executed_critique" in comps else "OFF"
    if critique == "ON":
        w = _executed_critique(w, task.check, ev)
    brief, used = hook.brief(task.task_ref, task.prompt) if "memory" in comps else ("", [])
    if "memory" in comps:
        ev("MEMORY_BRIEF", retrieved=list(used), chars=len(brief))
    cl, tree = ContributionLedger(), None
    if "research_tree" in comps:
        tree = ResearchTree.start(task.prompt, researcher="fs_org_driver.run_team")
        ev("RESEARCH_STARTED", root=tree.root)
    hyps = run_lsd_room(task.prompt, w, tree=tree, node=tree.root if tree else None, context=brief) if "lsd" in comps else []
    if "lsd" in comps:
        ev("LSD_ROOM", hypotheses=len(hyps))
    kw = dict(n_solvers=n_solvers, signature=task.signature, max_rounds=max_rounds, brief=brief, ledger=cl)
    control = AdvisoryControl(cl, signature=task.signature) if tree is None and "appleme" in comps else None
    if tree is not None:
        results = [tree.investigate(tree.root, w, **kw)]
    else:
        results = [run_rounds(task_prompt=task.prompt, work=w, claim_id=f"{hook.run_id}:{task.task_ref}", control=control, **kw)]
    ev("BROTHER_MODE", stop=results[0].stop_reason, calls=results[0].calls, rounds=results[0].rounds, failures=len(results[0].failures))
    if control is not None:
        ev("COGNITIVE_DIAGNOSIS", source="AdvisoryControl", decisions=[r["because"] for r in control.records])
    if tree is not None and "appleme" in comps:
        advice = doctor_advice(research_tree_events(tree))
        ev("COGNITIVE_DIAGNOSIS", source="research_tree", status=advice["status"], advisory=advice["advisory"], findings=[f.get("code") for f in advice.get("findings", [])])
        for _round in range(advice_rounds):
            ev("ADVICE_APPLIED", actions=[a.get("action") for a in tree.apply_advice(advice)])
            if not set(advice["advisory"]) & _RESEARCH_ADVICE:
                break
            results += [tree.investigate(node, w, **kw) for node in tree.prioritize(1, advice=advice)]
            advice = doctor_advice(research_tree_events(tree))
            ev("COGNITIVE_DIAGNOSIS", source="research_tree", status=advice["status"], advisory=advice["advisory"], findings=[f.get("code") for f in advice.get("findings", [])])
    if tree is not None:
        final = tree.finalize(reason="fs_org_driver.run_team")
        ev("RESEARCH_FINALIZED", node=final.get("node"), status=final.get("status"), provisional=final.get("provisional"))
    answer, how = select_answer(task.task_ref, [t for r in results for t in r.positions.values()], task.signature, task.score)
    captured, cap_err = [], None
    if "memory" in comps:
        try:                                                   # capture never changes the answer; failures are reported
            captured = capture_brother(hook, task.task_ref, cl.rows, task.signature)
        except Exception as exc:  # noqa: BLE001
            cap_err = f"{type(exc).__name__}: {str(exc)[:120]}"
    return {"task": task.task_ref, "arm": arm, "run": hook.run_id, "components": sorted(comps), "ablated": off[0] if len(off) == 1 else off or None,
            "executed_critique": critique, "answer": answer, "how": how, "calls": len(receipts), "failures": sum(not r["ok"] for r in receipts),
            "investigations": len(results), "hypotheses": len(hyps), "seconds": round(time.monotonic() - t0, 3), "retrieved": list(used), "brief_chars": len(brief),
            "captured": captured, "capture_error": cap_err, "events": events, "stages": dict(Counter(r["stage"].split(":")[0] for r in receipts)),
            "lineages": sorted({_lineage(r) for r in cl.rows if r.kind == "SOLUTION" and _lineage(r)}), "row_kinds": dict(Counter(r.kind for r in cl.rows)),
            "members": member_answers(cl.rows, task.signature), "receipts": receipts, "tokens": tokens(receipts),
            "specialist_used": any(r.specialist_used for r in results), **_identity(arm, receipts, roster, roles=roles)}


def run_samples(task: Task, *, work, arm: str, roster: dict, cycle: list, k: int, token_budget: int | None = None, max_calls: int | None = None,
                specialist: str | None = None) -> dict:
    """Non-collaborative controls with T's selector: independent drafts from the SAME solve prompt T's solvers get (no brief, no critique, exchange or revision),
    then select_answer. One runner, three arms:
      E_div  (diversity-only, primary contrast to T): roster = T's roster, cycle = list(roster)  -> round-robin over the same models
      R_mono (same-model repeated sampling):          roster = {pin: lineage}, cycle = [pin]      -> one model, same budget
      S      (single member):                          roster = {m: lineage},   cycle = [m], k = 1
    Budget: with token_budget (T's receipted input+output tokens on this task) drafts are drawn until it is reached; when a receipt carries no token count the call
    count k (T's receipted calls) decides. max_calls (default 3k) caps either rule. Never tuned on outcomes: k and token_budget come from T's receipts.
    specialist: T's declared specialist member when the roster carries one (optional lineage, see identity_check)."""
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
            **_identity(arm, receipts, roster, cycle, {"specialist": specialist} if specialist else None)}


LEAD = ("{task}\n\nYou lead a team of {n} workers who will each solve this task independently and in parallel. Write a short brief for them: how to decompose the task, "
        "what to check with the available tools, and the exact final-answer format. Do not solve the task yourself.")
SYNTHESIZE = ("{task}\n\nYour workers solved this task independently (UNVERIFIED):\n{drafts}\n\n"
              "Synthesize their work into one final solution and give your final answer in exactly the format the task asks for.")


def run_multi(task: Task, *, work, roster: dict, cycle: list, k: int, lead: str | None = None, token_budget: int | None = None, max_calls: int | None = None,
              specialist: str | None = None, arm: str = "G_mas") -> dict:
    """G_mas, the generic multi-agent control (Anthropic orchestrator-worker pattern): the lead writes a brief, workers solve independently from T's solve prompt (the brief
    in its `{brief}` slot; no worker sees another's work), the lead synthesizes; select_answer over the workers' drafts plus the synthesis. No critique, no revision, no
    specialist, no memory, no AppleMe / Research Tree / LSD room. Same roster, work() interface, identity guard and token budget rule as run_samples; one call is reserved
    for the synthesis (token rule: a worker is drawn only while spent + 2 x mean call <= budget; call rule: lead + workers + synthesis = k)."""
    from cherryme.brother import SOLVE
    lead = lead or cycle[0]
    t0, receipts, texts = time.monotonic(), [], []
    w, cap = metered(work, receipts), max_calls or 3 * max(1, k)
    c = w(LEAD.format(task=task.prompt, n=len(cycle)), "lead", prefer=lead)
    brief = f"Brief from the team lead:\n{c['output'].strip()}\n\n" if receipts[-1]["ok"] else ""
    prompt = SOLVE.format(task=task.prompt, brief=brief)

    def more() -> bool:
        n = len(receipts)
        if n + 1 >= cap:
            return False
        t = tokens(receipts)
        if token_budget is None or t["calls_without_tokens"]:
            return n + 1 < k
        spent = t["input"] + t["output"]
        return spent + 2 * spent / n <= token_budget
    i = 0
    while more():                    # ponytail: workers are drawn one after another (each independent of the others); concurrent dispatch is wall-clock only
        c = w(prompt, "solve", prefer=cycle[i % len(cycle)])
        i += 1
        if receipts[-1]["ok"]:
            texts.append(c["output"])
    synth = None
    if texts:
        drafts = "\n".join(f"--- worker {j + 1} ---\n{t}\n--- end ---" for j, t in enumerate(texts))
        c = w(SYNTHESIZE.format(task=task.prompt, drafts=drafts), "synthesize", prefer=lead)
        synth = c["output"] if receipts[-1]["ok"] else None
    answer, how = select_answer(task.task_ref, texts + ([synth] if synth else []), task.signature, task.score)
    roles = {"lead": lead, "synthesize": lead, **({"specialist": specialist} if specialist else {})}
    return {"task": task.task_ref, "arm": arm, "answer": answer, "how": how, "synthesis": task.signature(synth) if synth else None, "calls": len(receipts),
            "failures": sum(not r["ok"] for r in receipts), "seconds": round(time.monotonic() - t0, 3), "drafts": len(texts),
            "stages": dict(Counter(r["stage"] for r in receipts)),
            "members": [{"lineage": r["independence_key"], "first": task.signature(t), "final": task.signature(t)}
                        for r, t in zip([r for r in receipts if r["stage"] == "solve" and r["ok"]], texts)],
            "receipts": receipts, "tokens": tokens(receipts), **_identity(arm, receipts, roster, cycle, roles)}


def _h(*parts) -> str:
    return hashlib.sha256("\0".join(map(str, parts)).encode()).hexdigest()


def task_order(task_refs: list[str], seed) -> list[str]:
    """EVAL-002 task order: a permutation fixed by the seed (deterministic per seed, recorded with the run)."""
    return sorted(task_refs, key=lambda t: _h(seed, "task", t))


def sham_brief(ledger: Ledger, task: Task, run: str, length: int, seed, n_items: int = 3) -> dict:
    """EVAL-002 sham arm: ogi013_learning_hook.placebo_brief (INDEPENDENTLY_CHECKED, never-contradicted, leak-checked discoveries of unrelated tasks, same
    formatter, item count and length as the memory brief). -> {"text", "ids", "items", "chars", ...}. Read-only."""
    return placebo_brief(ledger, task.task_ref, run, task.prompt, length=length, n_items=n_items, seed=seed)


def run_pair(task: Task, *, work, ledger: Ledger, tag: str, projection=None, results=None, sham: bool = False, seed=None, roster: dict | None = None,
             specialist: str | None = None) -> dict:
    """EVAL-002 arms on one task: control (no brief), applied (verified, retrieved discoveries) and, with sham=True, sham (a brief of the same form and length from
    non-retrievable discoveries, sham_brief). Arm order: control, applied, sham without a seed; with a seed a permutation fixed by sha256(seed, task, arm), recorded.
    Independent grading afterwards; outcome recorded for every discovery applied in the applied arm (against the control)."""
    if task.grader not in VERIFIERS:
        raise ValueError(f"the grader must be independent of the models: one of {sorted(VERIFIERS)}")
    arms = ["control", "applied"] + (["sham"] if sham else [])
    if seed is not None:
        arms.sort(key=lambda a: _h(seed, task.task_ref, a))
    prompts: dict[str, list] = {a: [] for a in arms}
    hooks = {a: LearningHook(ledger, run_id=f"{tag}:{a}", apply=a == "applied") for a in arms}
    hook = hooks["applied"]
    real = ledger.retrievable(task.task_ref, hook.run_id, task.prompt)[: hook.max_items]
    placebo = sham_brief(ledger, task, hook.run_id, len(format_brief(real)), seed, n_items=len(real)) if sham else None
    fixed = {"sham": placebo["text"]} if sham else {}

    def recording(arm):
        def w(prompt, stage, **kw):
            prompts[arm].append((stage, prompt))
            return work(prompt, stage, **kw)
        return w
    rows = {a: run_episode(task, work=recording(a), hook=hooks[a], arm=a, brief=fixed.get(a), roster=roster, specialist=specialist) for a in arms}
    for a in arms:                                         # presentation parity, recorded in every row
        rows[a]["brief_items"] = placebo["items"] if a == "sham" else len(rows[a]["retrieved"])
    if sham:
        rows["sham"]["sham_brief"] = {k: v for k, v in placebo.items() if k != "text"}
    ctl, app = rows["control"], rows["applied"]
    for row in rows.values():
        grade_after(row, task)
    if app["retrieved"]:
        hook.outcomes(task.task_ref, reward=app["reward"], control_reward=ctl["reward"], control_run=ctl["run"], grader=task.grader)
    out = {"task": task.task_ref, **rows, "order": arms, "seed": seed, "prompts": prompts}
    if projection is not None:
        out["projected"] = projection.publish(ledger)
    if results is not None:
        import json
        from pathlib import Path
        with Path(results).open("a", encoding="utf-8") as f:
            for a in arms:
                f.write(json.dumps({**rows[a], "grader": task.grader, "order": arms, "seed": seed}, sort_keys=True) + "\n")
    return out


def run_transfer(tasks: list[Task], *, seed, tag: str, **kw) -> dict:
    """EVAL-002 transfer set: run_pair per task in task_order(seed) (memory content can depend on earlier tasks, so the order is randomized and recorded)."""
    by_ref = {t.task_ref: t for t in tasks}
    order = task_order(list(by_ref), seed)
    return {"seed": seed, "order": order, "pairs": [run_pair(by_ref[r], seed=seed, tag=f"{tag}/{r}", **kw) for r in order]}
