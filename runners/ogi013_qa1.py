"""OGI-013 QA-1 runner: arms T (team), E (equal effort, majority vote), S (best constituent), L (Luna alone), exactly as pre-registered (OGI013_QA1_PREREG.md).
Pure logic first (parsing, grading, E's k, specialist rule); the stack parts import lazily. Question texts are never written to any committed file; results hold ids, letters, hashes and grades."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter

ANSWER_RE = re.compile(r"ANSWER:\s*([A-J])\b")
LETTERS = "ABCDEFGHIJ"

QUESTION_PROMPT = ("Answer the following multiple-choice question. Think it through, then finish with exactly one line of the form 'ANSWER: <letter>' (a single capital letter naming one option).\n\n"
                   "Question: {question}\n\nOptions:\n{options}\n")


def render_options(options: list) -> str:
    return "\n".join(f"{LETTERS[i]}. {o}" for i, o in enumerate(options))


def question_prompt(q: dict) -> str:
    return QUESTION_PROMPT.format(question=q["question"], options=render_options(q["options"]))


def parse_letter(text: str | None, n_options: int) -> str | None:
    """Strict `ANSWER: <letter>`, the LAST occurrence; a letter outside the option range or no match is None (graded incorrect)."""
    m = ANSWER_RE.findall(text or "")
    if not m or LETTERS.index(m[-1]) >= n_options:
        return None
    return m[-1]


def grade(letter: str | None, key: str) -> bool:
    return letter is not None and letter == key


def majority(letters: list) -> str | None:
    """Majority vote over the letters of the drafts; ties go to the earliest draft; unparsable drafts do not vote."""
    votes = [l for l in letters if l]
    if not votes:
        return None
    counts = Counter(votes)
    top = max(counts.values())
    return next(l for l in votes if counts[l] == top)


def final_answer(position_letters: dict, specialist_letter: str | None, earliest: str | None = None) -> tuple:
    """T's final answer: the agreed final position; without agreement the specialist chooses among the EXISTING final positions. A specialist letter that is not one of them is rejected
    (the earliest position's letter stands). Returns (letter, how)."""
    existing = [l for l in position_letters.values() if l]
    if existing and len(set(existing)) == 1 and len(existing) == len(position_letters):
        return existing[0], "agreed"
    if specialist_letter is not None:
        if specialist_letter in existing:
            return specialist_letter, "specialist"
        return (earliest or (existing[0] if existing else None)), "specialist_new_letter_rejected"
    return (earliest or (existing[0] if existing else None)), "no_agreement_no_specialist"


def e_draft_count(t_record: dict) -> int:
    """E's k = the number of model calls T used on that question (CherryMe calls recorded by T)."""
    return int(t_record["calls"])


def sha(text: str) -> str:
    return hashlib.sha256((text or "").encode()).hexdigest()


def load_jsonl(path) -> list:
    return [json.loads(l) for l in open(path) if l.strip()]


# ======================================================================================================================================================================
# stack-facing part (imports lazily; needs the host bootstrap environment: ogi013_host_bootstrap.py --runner runners/ogi013_qa1.py ...)
# ======================================================================================================================================================================
import argparse  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402
import uuid  # noqa: E402
from concurrent.futures import ThreadPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402
from types import SimpleNamespace  # noqa: E402

CODEX_HOME = "/root/.plumme/codex-headless-home"
GLOBAL_CALL_CAP = 6
Q_PAR = 4
EPISODE_MAX_TOKENS = {"T": 400_000, "E": 400_000, "S": 60_000}
EPISODE_MAX_CALLS = 300


class Infra(Exception):
    """An infrastructure failure of one arm attempt (INFRA_MANGOME_FAILED / INFRA_SUPPLY / INFRA_BUDGET_EXHAUSTED / crash): one rerun, then incorrect."""

    def __init__(self, kind: str, detail: str = ""):
        super().__init__(f"{kind}: {detail}")
        self.kind = kind


class Context:
    """Process-wide handles shared by all questions. Every (question, arm) gets its OWN MangoMe workspace/project, WorkIdentity and EXECUTE turn (PeachMe aborts a step with CANONICAL_CONTEXT_CHANGED when
    another work is admitted in the same project meanwhile) and its own memory key in the fixed OrangeMe project PeachMe is bound to. OrangeMe's ledger is a git repository: adapter calls are serialised."""

    def __init__(self, out: Path, s_model: str | None, call_cap: int):
        import ogi013_conc as conc
        from ogi013_tau2_agent import Stack
        from peachme.fruitstack import OrangeMemoryAdapter
        self.out, self.s_model = out, s_model
        self.stack = Stack.get(out / "fruitstack")
        self.env_lock = threading.RLock()
        self.gate = conc.CallGate(call_cap)
        self.results_lock = threading.Lock()
        self.actor = os.environ.get("ORANGEME_AGENT_ID", "claude-code-ogi")
        self.orange_lock = threading.RLock()
        for name in ("load", "store"):
            if not getattr(getattr(OrangeMemoryAdapter, name), "_qa1_locked", False):
                orig = getattr(OrangeMemoryAdapter, name)

                def locked(self_, *a, _orig=orig, **k):
                    with ORANGE_LOCK:
                        return _orig(self_, *a, **k)
                locked._qa1_locked = True
                setattr(OrangeMemoryAdapter, name, locked)
        from orangeme.runtime import OrangeRuntime
        with ORANGE_LOCK:
            self.orange = OrangeRuntime()          # PeachMe's memory adapter is bound to the OrangeMe project "FruitStack OGI Evaluation" (Stack.__init__); episode memory keys live in that ledger
        (out / "events").mkdir(parents=True, exist_ok=True)

    def episode(self, arm: str, qid: str, tag: str = ""):
        """One MangoMe WorkIdentity + EXECUTE turn per (question, arm), admitted by the host before the episode starts."""
        import ogi013_conc as conc
        from mangome.runtime import get_service
        from ogi013_tau2_agent import Episode
        text = f"QA-1 {arm} question {qid} {uuid.uuid4().hex[:8]}"
        mem = f"memory/qa1-{uuid.uuid4().hex[:10]}"
        with self.env_lock:
            m = get_service()
            e = m.enter_work(workspace_id=f"/ogi013/qa1/{uuid.uuid4().hex[:10]}", workspace_title="OGI-013 QA-1", actor_id=self.actor, request_text=text)
            work, project = e["work_identity"]["entity_id"], e["project"]["project_key"]
            turn = m.bind_work_turn(work_ref=work, request_text=text, mode="EXECUTE", actor_id=self.actor, authorized_by=self.actor)["turn"]["entity_id"]
            with ORANGE_LOCK:
                led = self.orange.project_ledger("FruitStack OGI Evaluation")
                led.put(mem, {"verified_findings": []}, expected_revision=0)
            os.environ.update({"OGI013_WORK_REF": work, "OGI013_PROJECT_REF": project, "OGI013_TURN_ID": turn, "OGI013_ACTOR_ID": self.actor, "OGI013_MEMORY_REF": mem})
            ep = Episode(self.stack, f"qa1-{arm}", qid, "qa1", self.out / "events" / f"{qid}_{arm}{tag}.jsonl")
        cap = EPISODE_MAX_TOKENS.get(arm, 100_000)
        self.stack.fs.governance.configure(ep.sid, ep.store_revision(self.stack), max_calls=EPISODE_MAX_CALLS, max_tokens=cap, max_cost_usd=0.0)
        ep.timing, ep.call_gate = conc.TimingRecorder(), self.gate
        ep.budget_profile = "qa"
        ep.token_cap, ep.gov_cfg = cap, dict(max_calls=EPISODE_MAX_CALLS, max_tokens=cap, max_cost_usd=0.0)
        return ep


ORANGE_LOCK = threading.RLock()


def check_budget(ep) -> None:
    reason = ep._flags().get("budget_exhausted")
    if reason:
        raise Infra("INFRA_BUDGET_EXHAUSTED", reason)


def pinned_step(ep, roster, role: str, prompt: str, tag: str, exclude=(), prefer=None) -> dict:
    """One call for a roster role: the pinned model is requested strictly (no silent handover); two consecutive failed steps replace it (ROSTER_CHANGE with reason class); the executed model is
    compared with the pin (a mismatch is a ROSTER_CHANGE, never silent). NO_ELIGIBLE_NEURON after the supply wait ends the attempt as INFRA_SUPPLY."""
    from ogi013_roster import FAILED_STEPS_BEFORE_CHANGE, STICKY_ALL, reason_class
    from peachme import PeachError
    pinned = roster.pinned(role) if roster is not None else None
    want = pinned or prefer
    for waited in range(11):
        try:
            d = ep.step(prompt, tag, exclude=tuple(x for x in exclude if x), prefer=want, sticky_attempts=STICKY_ALL if want else 1)
            break
        except RuntimeError as exc:
            if "NO_ELIGIBLE_NEURON" not in str(exc):
                raise
            if waited >= 10:
                raise Infra("INFRA_SUPPLY", f"no eligible model for {role}") from exc
            time.sleep(60)
        except PeachError as exc:
            if str(exc).startswith("BUDGET_EPISODE_EXHAUSTED"):
                raise Infra("INFRA_BUDGET_EXHAUSTED", str(exc)) from exc
            raise
    check_budget(ep)
    if roster is None:
        return d
    fails = roster.__dict__.setdefault("_fails", {})
    if d["success"]:
        fails[role] = 0
        roster.note_model(d["model_key"])
        if roster.pinned(role) is None:
            roster.pin(role, d["model_key"], d.get("independence_key"))
        elif d["model_key"] != roster.pinned(role):
            roster.change(role, f"executed by {d['model_key']} instead of the pinned {roster.pinned(role)}", "handover")
            roster.pin(role, d["model_key"], d.get("independence_key"))
    else:
        fails[role] = fails.get(role, 0) + 1
        if pinned and fails[role] >= FAILED_STEPS_BEFORE_CHANGE:
            roster.change(role, f"{fails[role]} consecutive failed steps on {pinned}: {d.get('failure_class')}", reason_class(d.get("failure_class")))
            fails[role] = 0
    return d


def strict_step(ep, prompt: str, model: str, tries: int = 6, pause: float = 30.0) -> dict:
    """A call to ONE named model (E's roster models, S's fixed model): strict preference, no handover; free-tier routes flap, so the same model is asked again after a pause. Only persistent
    failure is an infrastructure failure of the arm."""
    from ogi013_roster import STICKY_ALL
    d = {"success": False, "failure_class": "NOT_TRIED"}
    for i in range(tries):
        try:
            d = ep.step(prompt, "author", prefer=model, sticky_attempts=STICKY_ALL)
        except RuntimeError as exc:
            if "NO_ELIGIBLE_NEURON" not in str(exc):
                raise
            d = {"success": False, "failure_class": "NO_ELIGIBLE_NEURON"}
        check_budget(ep)
        if d["success"]:
            return d
        time.sleep(pause)
    return d


# ---- arm S ---------------------------------------------------------------------------------------------------------------------------------------------------
def run_S(ctx: Context, q: dict) -> dict:
    ep = ctx.episode("S", q["id"])
    t0 = time.monotonic()
    d = strict_step(ep, question_prompt(q), ctx.s_model)           # the fixed best constituent: strict, no handover
    if not d["success"]:
        raise Infra("INFRA_STEP_FAILED", str(d.get("failure_class")))
    letter = parse_letter(d["output"], len(q["options"]))
    return {"letter": letter, "output_sha256": sha(d["output"]), "model": d["model_key"], "calls": 1, "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"], "seconds": round(time.monotonic() - t0, 1),
            "mango_writes": 0, "mango_reads": 0}


# ---- arm L ---------------------------------------------------------------------------------------------------------------------------------------------------
def run_L(ctx: Context, q: dict) -> dict:
    t0 = time.monotonic()
    prompt = question_prompt(q) + "\nAnswer directly from your own knowledge and reasoning. Do not run commands or read files."
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only", "-m", "gpt-6-luna", "-c", 'approval_policy="never"', "-C", tmp, "--json", "-"], input=prompt,
                           capture_output=True, text=True, env={**os.environ, "CODEX_HOME": CODEX_HOME}, timeout=900)
    events = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    msgs = [e["item"]["text"] for e in events if e.get("type") == "item.completed" and e["item"].get("type") == "agent_message"]
    if r.returncode != 0 or not msgs:
        raise Infra("INFRA_LUNA_FAILED", (r.stderr or "")[-200:])
    tok = sum((e.get("usage", {}).get("input_tokens", 0) + e.get("usage", {}).get("output_tokens", 0)) for e in events if e.get("type") == "turn.completed")
    return {"letter": parse_letter(msgs[-1], len(q["options"])), "output_sha256": sha(msgs[-1]), "model": "gpt-6-luna", "calls": 1, "tokens": tok, "seconds": round(time.monotonic() - t0, 1), "mango_writes": 0, "mango_reads": 0}


# ---- arm E ---------------------------------------------------------------------------------------------------------------------------------------------------
def run_E(ctx: Context, q: dict, t_rec: dict) -> dict:
    """The same roster models, round-robin, k independent drafts (k = T's call count), majority vote; no critique, no exchange."""
    ep = ctx.episode("E", q["id"])
    t0 = time.monotonic()
    models = [m for m in t_rec["roster_models"] if m]
    k = e_draft_count(t_rec)
    if not models or k < 1:
        raise Infra("INFRA_NO_ROSTER", "T recorded no roster / calls")
    prompt = question_prompt(q)

    def draft(i):
        return strict_step(ep.fork(), prompt, models[i % len(models)])

    with ThreadPoolExecutor(max_workers=4) as pool:
        ds = list(pool.map(draft, range(k)))
    check_budget(ep)
    letters = [parse_letter(d["output"], len(q["options"])) if d["success"] else None for d in ds]
    if all(not d["success"] for d in ds):
        raise Infra("INFRA_STEP_FAILED", "all E drafts failed")
    return {"letter": majority(letters), "draft_letters": letters, "k": k, "draft_failures": sum(1 for d in ds if not d["success"]), "calls": k, "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"],
            "seconds": round(time.monotonic() - t0, 1), "mango_writes": 0, "mango_reads": 0}


# ---- arm T ---------------------------------------------------------------------------------------------------------------------------------------------------
def run_T(ctx: Context, q: dict) -> dict:
    from cherryme.brother import run_rounds
    from cherryme.contributions import ContributionLedger
    import ogi013_candidates as oc
    from ogi013_mango_ledger import InfraMangoFailed, MangoLedger
    from ogi013_roster import InfraSupply, Roster
    from ogi013_team_code import TeamState
    ep = ctx.episode("T", q["id"])
    t0 = time.monotonic()
    n_opt = len(q["options"])
    task = question_prompt(q)
    team = TeamState(task, ctx.out / "events" / f"{q['id']}_T_team_state.md")
    team.mango = MangoLedger(ctx.stack.fs.mango, ep.work, ep.actor, ep.turn_id, ep.sid)
    roster = Roster(emit=ep.event, write=team.mango.write)
    team.roster_changes_provider = lambda: list(roster.changes)
    team.independent = True
    plock = threading.RLock()
    slots_taken: set = set()
    by_model: dict = {}
    obj_ids_for: dict = {}
    counters = Counter()

    def ping(role, exclude, prefer=None):
        d = {"success": False}
        for _ in range(6):
            try:
                d = ep.step("Reply with the single word READY.", "author", exclude=tuple(x for x in exclude if x), prefer=prefer, sticky_attempts=99 if prefer else 1)
            except RuntimeError as exc:
                if "NO_ELIGIBLE_NEURON" not in str(exc):
                    raise
                d = {"success": False}
            if d["success"]:
                break
            time.sleep(30)
        if not d["success"]:
            raise Infra("INFRA_SUPPLY", f"roster: cannot fill {role}")
        roster.pin(role, d["model_key"], d.get("independence_key"))
        return d

    def claim_slot() -> str:
        with plock:
            for s in ("solver1", "solver2"):
                if s not in slots_taken:
                    slots_taken.add(s)
                    return s
            return "solver1"

    def view_prompt(base: str, view):
        ts = team.prompt(view)                                            # MangoMe is the live workspace: the state comes from a work_context read
        return base + (f"\n<team_state>\n{ts}\n</team_state>\n" if ts else "")

    def work(prompt, stage, prefer=None, exclude=()):
        child = ep.fork()
        if stage != "solve":
            team.independent = False                                          # the reveal barrier is open: full shared state for the roles that have submitted (a late solver stays blind)
        try:
            if stage == "solve":
                slot = claim_slot()
                pid = {"solver1": "S1", "solver2": "S2"}[slot]
                with plock:
                    pos = SimpleNamespace(id=pid, slot=slot, model=roster.pinned(slot), status="open", rev=0, diff="", test_tail="")
                    team.pos[pid] = pos
                d = pinned_step(child, roster, slot, view_prompt(prompt, pid), "author", exclude=exclude)
                if d["success"]:
                    with plock:
                        pos.model, pos.diff, pos.status = d["model_key"], d["output"], "submitted"
                        by_model[d["model_key"]] = pos
                        team.decisions.append(f"{pid} submitted its first answer")
                return d
            if stage == "challenge":
                tgt = next((p for p in team.pos.values() if p.diff and p.diff in prompt), None)
                answered = [o for o in team.objs if tgt and o["target"] == tgt.id and o["state"] == "OPEN" and o["exchanges"] == 1]
                extra = ""
                if answered:
                    extra = ("\nThe author answered these objections. Respond once to each, on its own line: 'O<n>: WITHDRAW' plus your evidence if you now agree, or 'O<n>: MAINTAIN' plus new evidence if not:\n"
                             + "\n".join(f"{o['id']}: {o['replies'][-1]['text'][:300]}" for o in answered))
                d = pinned_step(child, roster, "critic", view_prompt(prompt + extra, None), "critic", exclude=tuple(exclude) + roster.lineages("critic"))
                if d["success"] and tgt is not None:
                    text = d["output"]
                    with plock:
                        for o in answered:
                            m = re.search(rf"^\s*{o['id']}\s*:\s*(WITHDRAW|MAINTAIN)\b(.*?)(?=^\s*O\d+\s*:|\Z)", text, re.I | re.M | re.S)
                            if m:
                                team.reply(o["id"], "critic", m.group(1).lower(), m.group(2).strip() or text, oc.classify_objection(text, task, []))
                        if re.match(r"\s*ISSUES:\s*FOUND", text, re.I) or (not re.match(r"\s*ISSUES:\s*NONE", text, re.I) and len(text) > 40):
                            counters["objections"] += 1
                            ground = oc.classify_objection(text, task, [])
                            counters["grounded_objections"] += int(oc.is_grounded(ground))
                            oid = team.objection(tgt.id, d.get("independence_key"), text, grounded=oc.is_grounded(ground), ground=ground)
                            obj_ids_for.setdefault(tgt.id, []).append(oid)
                return d
            if stage == "revise":
                pos = by_model.get(prefer) or next(iter(team.pos.values()))
                d = pinned_step(child, roster, pos.slot, view_prompt(prompt, None), "author", exclude=exclude)
                if d["success"]:
                    with plock:
                        old, new = parse_letter(pos.diff, n_opt), parse_letter(d["output"], n_opt)
                        for oid in obj_ids_for.pop(pos.id, []):
                            if new == old:                                      # the author keeps its answer: a reply (needs evidence: a quote of the question; else UNGROUNDED_REPLY)
                                team.reply(oid, "author", "evidence", d["output"], oc.classify_objection(d["output"], task, []))
                            else:
                                team.reply(oid, "author", "concede", d["output"])
                        if new != old:
                            counters["answer_changes"] += 1
                        pos.diff, pos.rev, pos.status = d["output"], pos.rev + 1, "revised"
                        team.decisions.append(f"{pos.id} revised (letter {old} -> {new})")
                return d
            if stage == "specialist":
                d = pinned_step(child, roster, "specialist", view_prompt(prompt, None), "critic", exclude=tuple(exclude) + roster.lineages("specialist"))
                return d
            return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
        except (Infra, InfraMangoFailed, InfraSupply):
            raise
        except Exception as exc:  # noqa: BLE001 - one failing worker never stops another
            return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "failure_class": f"{type(exc).__name__}: {str(exc)[:80]}"}

    def work_wrapped(prompt, stage, **kw):
        out = work(prompt, stage, **kw)
        return {**out, "model_key": out.get("model_key"), "independence_key": out.get("independence_key"), "receipt_id": out.get("receipt_id")}

    # roster FIRST (P1): solver1 is the fixed best constituent (S), solver2 a distinct lineage
    d1 = ping("solver1", (), prefer=ctx.s_model)
    ping("solver2", (d1.get("independence_key"),))
    ledger = ContributionLedger()
    try:
        res = run_rounds(task_prompt=task, brief="", work=work_wrapped, ledger=ledger, claim_id=ep.claim.id, signature=lambda text: parse_letter(text, n_opt) or "?", parallel=True, solver_wait=600,
                         max_workers=2)
        team.persist()
    except InfraMangoFailed as exc:
        raise Infra("INFRA_MANGOME_FAILED", f"{exc} | diff: {team.diff_report}") from exc
    except InfraSupply as exc:
        raise Infra("INFRA_SUPPLY", str(exc)) from exc
    check_budget(ep)
    firsts = [parse_letter(r.answer_text, n_opt) for r in ledger.rows if r.kind == "SOLUTION" and r.reason == "INDEPENDENT_SOLUTION"]
    position_letters = {k: parse_letter(v, n_opt) for k, v in res.positions.items() if not k.endswith("#sp")}
    spec_rows = [r for r in ledger.rows if r.kind == "SOLUTION" and r.reason == "SPECIALIST_TIEBREAK"]
    spec_letter = parse_letter(spec_rows[-1].answer_text, n_opt) if spec_rows else None
    earliest = firsts[0] if firsts else None
    letter, how = final_answer(position_letters, spec_letter, earliest=earliest)
    team.decisions.append(f"final answer {letter} ({how})")
    team.release = {"class": "QA1_FINAL", "letter": letter, "how": how}
    team.persist()
    replies = sum(len(o.get("replies", [])) for o in team.objs)
    return {"letter": letter, "how": how, "first_letters": {f"S{i + 1}": l for i, l in enumerate(firsts)}, "final_positions": position_letters, "specialist_letter": spec_letter, "calls": res.calls,
            "rounds": res.rounds, "stop": res.stop_reason, "late": res.late, "roster_models": [roster.pinned(r) for r in ("solver1", "solver2", "critic", "specialist")], "roster": roster.summary(),
            "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"], "seconds": round(time.monotonic() - t0, 1), "mango_writes": team.mango.writes, "mango_reads": team.mango.reads,
            "objections": counters["objections"], "grounded_objections": counters["grounded_objections"], "replies": replies, "answer_changes": counters["answer_changes"],
            "evidenced_withdrawn": sum(1 for o in team.objs if o.get("decided_by") == "withdrawn_with_evidence"), "work_ref": ep.work, "timing": ep.timing.report()}


# ---- orchestration -------------------------------------------------------------------------------------------------------------------------------------------
def attempt(fn, *a):
    """One arm attempt; infrastructure failures (and crashes) are classified, never raised."""
    try:
        return {"status": "OK", **fn(*a)}
    except Infra as e:
        return {"status": e.kind, "detail": str(e)[:300]}
    except Exception as e:  # noqa: BLE001
        return {"status": "INFRA_CRASH", "detail": f"{type(e).__name__}: {str(e)[:300]}"}


def finish(q: dict, arm: str, res: dict, rerun: bool) -> dict:
    ok = res["status"] == "OK"
    row = {"qid": q["id"], "arm": arm, "key": q["key"], "letter": res.get("letter"), "correct": bool(ok and grade(res.get("letter"), q["key"])), "status": "OK" if ok else "INFRA_FAILED",
           "infra_detail": None if ok else f"{res['status']}: {res.get('detail', '')}", "rerun": rerun}
    row.update({k: v for k, v in res.items() if k not in ("status", "letter", "detail", "timing", "roster", "draft_letters") or k in ("roster",)})
    return row


def run_arm(fn, q, arm, *args) -> dict:
    res = attempt(fn, *args)
    rerun = False
    if res["status"] != "OK":                                            # one rerun on infrastructure failure only
        rerun = True
        res = attempt(fn, *args)
    return finish(q, arm, res, rerun)


def process_question(ctx: Context, q: dict, arms: set, done: set, sink) -> None:
    pool = ThreadPoolExecutor(max_workers=2)
    futs = {}
    if "S" in arms and (q["id"], "S") not in done:
        futs["S"] = pool.submit(run_arm, run_S, q, "S", ctx, q)
    if "L" in arms and (q["id"], "L") not in done:
        futs["L"] = pool.submit(run_arm, run_L, q, "L", ctx, q)
    t_row = None
    if "T" in arms and (q["id"], "T") not in done:
        t_row = run_arm(run_T, q, "T", ctx, q)
        sink(t_row)
    if "E" in arms and (q["id"], "E") not in done:
        if t_row is None:
            t_row = next((r for r in load_jsonl(ctx.out / "results.jsonl") if r["qid"] == q["id"] and r["arm"] == "T"), None)
        if t_row and t_row.get("status") == "OK":
            sink(run_arm(run_E, q, "E", ctx, q, t_row))
        else:
            sink({"qid": q["id"], "arm": "E", "key": q["key"], "letter": None, "correct": False, "status": "INFRA_FAILED", "infra_detail": "T failed: E has no k", "rerun": False})
    for arm, f in futs.items():
        sink(f.result())
    pool.shutdown()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--arms", default="T,E,S,L")
    ap.add_argument("--s-model", default=None)
    ap.add_argument("--select-s", action="store_true", help="print the model PlumMe AUTO ranks first for the solve role and exit")
    ap.add_argument("--q-par", type=int, default=Q_PAR)
    ap.add_argument("--call-cap", type=int, default=GLOBAL_CALL_CAP)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, a.s_model, a.call_cap)
    if a.select_s:
        # lock-time selection: the model PlumMe AUTO ranks first for the solve role among models that pass an availability probe of 10 consecutive calls (a free route that cannot serve a 198-question run
        # would turn the S arm and T's solver 1 into infrastructure failures); a failing model's lineage is excluded and AUTO is asked again
        ep = ctx.episode("S", "select")
        excluded, log = [], []
        for _ in range(8):
            d = {"success": False}
            for _t in range(10):
                d = ep.step("Reply with the single word READY.", "author", exclude=tuple(excluded), sticky_attempts=1)
                if d["success"]:
                    break
                time.sleep(20)
            if not d["success"]:
                break
            model, lin = d["model_key"], d.get("independence_key")
            ok = 0
            for _p in range(10):
                r = ep.step("Reply with the single word READY.", "author", prefer=model, sticky_attempts=99)
                ok += int(r["success"] and r.get("model_key") == model)
            log.append({"model": model, "lineage": lin, "probe_ok": ok})
            if ok == 10:
                print(json.dumps({"s_model": model, "independence_key": lin, "probe": log, "success": True}))
                return 0
            excluded.append(lin)
        print(json.dumps({"s_model": None, "probe": log, "success": False}))
        return 2
    if not a.s_model:
        raise SystemExit("--s-model is required (selected and recorded at lock time)")
    qs = load_jsonl(a.data)[: a.limit or None]
    res_path = a.out / "results.jsonl"
    done = {(r["qid"], r["arm"]) for r in (load_jsonl(res_path) if res_path.exists() else [])}
    arms = set(a.arms.split(","))

    def sink(row):
        with ctx.results_lock:
            with res_path.open("a") as fh:
                fh.write(json.dumps(row) + "\n")
        print(json.dumps({k: row.get(k) for k in ("qid", "arm", "letter", "correct", "status", "calls", "tokens", "seconds")}), flush=True)
    with ThreadPoolExecutor(max_workers=a.q_par) as pool:
        list(pool.map(lambda q: process_question(ctx, q, arms, done, sink), qs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
