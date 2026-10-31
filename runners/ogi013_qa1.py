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


class Outage:
    """Systemic-outage rule (deviation D4): infrastructure failures of one arm are held back until a success of that arm shows they were isolated. After OUTAGE_STREAK
    consecutive failures in an arm the held rows are discarded (not written), the process stops taking new work and exits with RESTART_CODE; a supervisor starts it fresh
    and every discarded (question, arm) is tried once more (`retried`). A failure of an already retried pair is final."""
    OUTAGE_STREAK = 5
    RESTART_CODE = 75

    def __init__(self, retried=()):
        self.retried = {tuple(x) for x in retried}
        self.held: dict[str, list] = {}
        self.tripped = False
        self.lock = threading.Lock()

    def offer(self, row: dict) -> tuple[list, list]:
        """Return (rows to write now, qids/arms discarded for a retry)."""
        arm, key = row["arm"], (row["qid"], row["arm"])
        with self.lock:
            if row["status"] == "OK":
                out = self.held.pop(arm, []) + [row]
                return out, []
            if key in self.retried:
                return self.held.pop(arm, []) + [row], []
            held = self.held.setdefault(arm, [])
            held.append(row)
            if len(held) >= self.OUTAGE_STREAK:
                self.tripped = True
                gone = [(r["qid"], r["arm"]) for r in held]
                self.held[arm] = []
                return [], gone
            return [], []

    def flush(self) -> list:
        with self.lock:
            rows = [r for h in self.held.values() for r in h]
            self.held = {}
            return rows


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
        retried_path = out / "retried.jsonl"
        self.outage = Outage([(r[0], r[1]) for r in (json.loads(l) for l in retried_path.read_text().splitlines())] if retried_path.exists() else [])
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
    import ogi013_argument as ag
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
    pos_lin: dict = {}                                                   # position id -> lineage of its author (receipts); pos_first: its first letter
    pos_first: dict = {}
    spec_lin: list = []
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
                        pos_lin[pid], pos_first[pid] = d.get("independence_key"), parse_letter(d["output"], n_opt)
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
                d = pinned_step(child, roster, "critic", view_prompt(prompt + extra + ag.CRITIC_INSTRUCTIONS, None), "critic", exclude=tuple(exclude) + roster.lineages("critic"))
                if d["success"] and tgt is not None:
                    text = d["output"]
                    with plock:
                        for o in answered:
                            m = re.search(rf"^\s*{o['id']}\s*:\s*(WITHDRAW|MAINTAIN)\b(.*?)(?=^\s*O\d+\s*:|\Z)", text, re.I | re.M | re.S)
                            if m:
                                team.reply(o["id"], "critic", m.group(1).lower(), m.group(2).strip() or text, ag.ledger_ground(ag.classify_argument(text, task)))
                        if re.match(r"\s*ISSUES:\s*FOUND", text, re.I) or (not re.match(r"\s*ISSUES:\s*NONE", text, re.I) and len(text) > 40):
                            counters["objections"] += 1
                            ground = ag.ledger_ground(ag.classify_argument(text, task))
                            counters["grounded_objections"] += int(oc.is_grounded(ground))
                            oid = team.objection(tgt.id, d.get("independence_key"), text, grounded=oc.is_grounded(ground), ground=ground)
                            obj_ids_for.setdefault(tgt.id, []).append(oid)
                return d
            if stage == "revise":
                pos = by_model.get(prefer) or next(iter(team.pos.values()))
                d = pinned_step(child, roster, pos.slot, view_prompt(prompt + ag.REPLY_INSTRUCTIONS, None), "author", exclude=exclude)
                if d["success"]:
                    with plock:
                        old, new = parse_letter(pos.diff, n_opt), parse_letter(d["output"], n_opt)
                        for oid in obj_ids_for.pop(pos.id, []):
                            if new == old:                                      # the author keeps its answer: a reply (needs evidence: a quote of the question; else UNGROUNDED_REPLY)
                                team.reply(oid, "author", "evidence", d["output"], ag.ledger_ground(ag.classify_argument(d["output"], task)))
                            else:
                                team.reply(oid, "author", "concede", d["output"])
                        if new != old:
                            counters["answer_changes"] += 1
                        pos.diff, pos.rev, pos.status = d["output"], pos.rev + 1, "revised"
                        team.decisions.append(f"{pos.id} revised (letter {old} -> {new})")
                return d
            if stage == "specialist":
                d = pinned_step(child, roster, "specialist", view_prompt(prompt, None), "critic", exclude=tuple(exclude) + roster.lineages("specialist"))
                if d.get("success"):
                    spec_lin.append(d.get("independence_key"))
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
    if len(firsts) < 2:                                                  # amendment QA-1b/2: a T row is OK only if two positions (distinct lineages, enforced by the roster) were submitted
        raise Infra("INFRA_TEAM_INCOMPLETE", f"{len(firsts)} independent position(s) submitted; stop={res.stop_reason}")
    position_letters = {k: parse_letter(v, n_opt) for k, v in res.positions.items() if not k.endswith("#sp")}
    spec_rows = [r for r in ledger.rows if r.kind == "SOLUTION" and r.reason == "SPECIALIST_TIEBREAK"]
    spec_letter = parse_letter(spec_rows[-1].answer_text, n_opt) if spec_rows else None
    earliest = firsts[0] if firsts else None
    letter, how = final_answer(position_letters, spec_letter, earliest=earliest)
    team.decisions.append(f"final answer {letter} ({how})")
    team.release = {"class": "QA1_FINAL", "letter": letter, "how": how}
    team.persist()
    replies = sum(len(o.get("replies", [])) for o in team.objs)
    indep = [o for o in team.objs if o.get("lineage") and o["lineage"] != pos_lin.get(o["target"])]          # a critique from the lineage of the position it judges does not count
    evidenced_replies = sum(1 for o in indep for r in o.get("replies", []) if r.get("evidence") in ("command", "quote"))
    level = lambda k: {"quote": "formal", "command": "verified"}.get(k)         # noqa: E731 - ledger kind -> evidence level
    formal_replies = sum(1 for o in indep for r in o.get("replies", []) if level(r.get("evidence")) == "formal")
    verified_replies = sum(1 for o in indep for r in o.get("replies", []) if level(r.get("evidence")) == "verified")
    formal_objections = sum(1 for o in indep if (o.get("ground") or {}).get("level") == "formal")
    verified_objections = sum(1 for o in indep if (o.get("ground") or {}).get("level") == "verified")
    critics = {o["lineage"] for o in team.objs if o.get("lineage")}
    independence_ok = not any(l in set(pos_lin.values()) | critics for l in spec_lin)                                   # a specialist of the same lineage as a position it judges does not count
    (ctx.out / "exchange").mkdir(exist_ok=True)                           # the full exchange for the report (model text; kept out of results.jsonl)
    (ctx.out / "exchange" / f"{q['id']}.json").write_text(json.dumps({
        "first_answers": [{"slot": r.slot if hasattr(r, "slot") else None, "text": r.answer_text} for r in ledger.rows if r.kind == "SOLUTION" and r.reason == "INDEPENDENT_SOLUTION"],
        "objections": team.objs, "decisions": team.decisions, "final": {"letter": letter, "how": how}}, default=str))
    return {"letter": letter, "how": how, "first_letters": {f"S{i + 1}": l for i, l in enumerate(firsts)}, "final_positions": position_letters, "specialist_letter": spec_letter, "calls": res.calls,
            "rounds": res.rounds, "stop": res.stop_reason, "late": res.late, "roster_models": [roster.pinned(r) for r in ("solver1", "solver2", "critic", "specialist")], "roster": roster.summary(),
            "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"], "seconds": round(time.monotonic() - t0, 1), "mango_writes": team.mango.writes, "mango_reads": team.mango.reads,
            "objections": counters["objections"], "grounded_objections": counters["grounded_objections"], "replies": replies, "evidenced_replies": evidenced_replies, "formal_objections": formal_objections, "verified_objections": verified_objections, "formal_replies": formal_replies, "verified_replies": verified_replies, "independent_grounded_objections": sum(1 for o in indep if o.get("grounded")), "independence_ok": independence_ok,
            "lineages": {"positions": pos_lin, "critics": sorted({o["lineage"] for o in team.objs if o.get("lineage")}), "specialist": spec_lin}, "first_by_pos": pos_first,
            "objection_target_first": [pos_first.get(o["target"]) for o in indep], "answer_changes": counters["answer_changes"],
            "evidenced_withdrawn": sum(1 for o in team.objs if o.get("decided_by") == "withdrawn_with_evidence"), "work_ref": ep.work, "timing": ep.timing.report()}


# ---- orchestration -------------------------------------------------------------------------------------------------------------------------------------------
def plum_state(ctx, model: str) -> dict:
    """Availability of one cognitive model as PlumMe reports it: per offer the health state, retry window, circuit/credential/pool facts (cooldown with expiry vs exhausted)."""
    sch = ctx.stack.svc.scheduler
    offers = []
    for o in sch.store.market.offers.values():
        if o.model_key != model:
            continue
        f = sch.route_state(o)
        av = sch.availability(o)
        offers.append({"offer": o.offer_id, "health": getattr(o.health, "value", str(o.health)), "circuit_open": f["circuit_open"], "credential_available": f["credential_available"],
                       "pool_state": f["pool_state"], "pool_blocked_until": f["pool_blocked_until"], "retry_after_s": av.get("retry_after_seconds"), "quota_exhausted": av["quota_exhausted"]})
    return {"model": model, "offers": offers}


def chain_stages(row: dict) -> dict:
    """Cooperation chain (a)-(e) from one T row: two independent first answers, an objection with evidence from a lineage other than the position's own, a reply with evidence,
    a documented position change or an evidenced withdrawal, a final answer (a specialist of a judged lineage voids the chain). Returns the stages reached and where it stopped."""
    st = {"a": len(row.get("first_letters") or {}) >= 2, "b": (row.get("independent_grounded_objections") or 0) >= 1, "c": (row.get("evidenced_replies") or 0) >= 1,
          "d": (row.get("answer_changes") or 0) >= 1 or (row.get("evidenced_withdrawn") or 0) >= 1, "e": row.get("letter") is not None and row.get("independence_ok", True)}
    reached = ""
    for k in "abcde":
        if not st[k]:
            break
        reached += k
    return {**st, "reached": reached or "-", "complete": reached == "abcde"}


def chain_class(row: dict) -> str:
    """After checking the key: HARMFUL (a first answer right, final wrong) > IMPROVING (a first answer wrong, final right) > PROTECTIVE (an objection against a right first answer, final right) > NEUTRAL."""
    key, final = row.get("key"), row.get("letter")
    firsts = [l for l in (row.get("first_by_pos") or {}).values() if l]
    if any(l == key for l in firsts) and final != key:
        return "HARMFUL"
    if final == key and any(l != key for l in firsts):
        return "IMPROVING"
    if final == key and any(l == key for l in (row.get("objection_target_first") or [])):
        return "PROTECTIVE"
    return "NEUTRAL"


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
    if ctx.outage.tripped:                                               # systemic outage: take no new work, the supervisor restarts the process
        return
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
    elif "E" in arms:
        t_row = next((r for r in load_jsonl(ctx.out / "results.jsonl") if r["qid"] == q["id"] and r["arm"] == "T"), None)
    # E starts only after T has a valid result; a T failure is retried by the outage/restart rule and never marks E as failed here (final T failures get their E row in `close_out`)
    if "E" in arms and (q["id"], "E") not in done and t_row and t_row.get("status") == "OK":
        sink(run_arm(run_E, q, "E", ctx, q, t_row))
    for arm, f in futs.items():
        sink(f.result())
    pool.shutdown()


def close_out(ctx: Context, arms: set, res_path: Path) -> None:
    """Final T failures (after the retry) leave E without a k: record E as failed because of T, once, at the end."""
    if "E" not in arms:
        return
    rows = load_jsonl(res_path) if res_path.exists() else []
    have = {(r["qid"], r["arm"]) for r in rows}
    for r in rows:
        if r["arm"] == "T" and r["status"] != "OK" and (r["qid"], "E") not in have:
            with res_path.open("a") as fh:
                fh.write(json.dumps({"qid": r["qid"], "arm": "E", "key": r["key"], "letter": None, "correct": False, "status": "INFRA_FAILED", "infra_detail": "T failed after retry: E has no k", "rerun": False}) + "\n")


def note_restart(ctx: Context, arm: str, pairs: list) -> None:
    """Log one systemic-outage restart (deviation D4) and remember the discarded pairs so that each is retried once after the restart."""
    with ctx.results_lock:
        with (ctx.out / "retried.jsonl").open("a") as fh:
            for qid, a_ in pairs:
                fh.write(json.dumps([qid, a_]) + "\n")
        with (ctx.out / "restarts.jsonl").open("a") as fh:
            fh.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "arm": arm, "discarded": pairs}) + "\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--arms", default="T,E,S,L")
    ap.add_argument("--s-model", default=None)
    ap.add_argument("--diagnose-pin", default=None, help="diagnostic: try to lease the pinned model once and print the exception")
    ap.add_argument("--probe-calls", type=int, default=10, help="--select-s: availability probe calls per candidate (QA-1b: 30)")
    ap.add_argument("--probe-interval", type=float, default=0.0, help="--select-s: seconds between probe calls (QA-1b: 60, i.e. 30 calls over 30 minutes)")
    ap.add_argument("--run-cap", type=int, default=0, help="QA-1b: ONE run-level PlumMe RunBudget (provider requests incl. failover/continuation/rotation; cost 0) bound for the whole run")
    ap.add_argument("--capacity", type=float, default=0.0, help="QA-1b: capacity measurement: up to 8 eligible models of distinct lineages, each called at its own pace for this many minutes (in parallel)")
    ap.add_argument("--supply-check", action="store_true", help="QA-1b: T roster supply check (2 solvers of distinct lineages, critic, specialist; 5 of 5 probes each) and exit")
    ap.add_argument("--chain-hunt", type=int, default=0, help="QA-1b: run arm T alone, question by question, until the first complete cooperation chain (a-e) or this many questions")
    ap.add_argument("--select-s", action="store_true", help="print the model PlumMe AUTO ranks first for the solve role and exit")
    ap.add_argument("--q-par", type=int, default=Q_PAR)
    ap.add_argument("--call-cap", type=int, default=GLOBAL_CALL_CAP)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, a.s_model, a.call_cap)
    run_budget = None
    if a.run_cap:
        from plumme.budget import RunBudget
        run_budget = RunBudget(max_provider_calls=a.run_cap, max_cost_usd=0.0)
        ctx.stack.svc.set_run_budget(run_budget)
    if a.diagnose_pin:
        import asyncio
        from plumme.models import BudgetEnvelope, CognitiveOwner, NeuronRequest, SelectionMode
        req = NeuronRequest(consumer="peachme", objective="diag", role_id="REASONING", cognitive_owner=CognitiveOwner.CONSUMER, selection_mode=SelectionMode.PINNED_MODEL, pinned_model_key=a.diagnose_pin,
                            required_skill_ids=[], budget=BudgetEnvelope(max_concurrency=1, max_cost_usd=0.0), metadata={"exclude_small_models": True})
        try:
            lease = asyncio.run(ctx.stack.svc.acquire_neuron(req))
            print(json.dumps({"pinned": a.diagnose_pin, "ok": True, "route": getattr(lease.route, "model", None)}))
        except Exception as exc:  # noqa: BLE001
            print(json.dumps({"pinned": a.diagnose_pin, "ok": False, "error": f"{type(exc).__name__}: {str(exc)[:600]}"}))
        return 0
    if a.capacity:
        # Capacity measurement under the call caps (lead, 2026-10-31): per model at most 5 calls, one every 6 minutes; at most 40 calls in all. Single attempt per call (no step retries).
        # EXHAUSTED (Retry-After > 10 min, or a message naming quota/credit/daily/monthly/exhausted) and UNAVAILABLE (two cooldown refusals in a row) are final for this run: no further call.
        ep0 = ctx.episode("T", "capacity")
        found, lins, cnt = [], [], {"n": 0}
        for _ in range(8):                                                 # discovery: AUTO picks eligible models of distinct lineages (small-model exclusion is applied by the heart); this IS call 1 of each
            d = ep0.step("Reply with the single word READY.", "author", exclude=tuple(lins), sticky_attempts=1)
            cnt["n"] += 1
            if not d["success"]:
                break
            found.append((d["model_key"], d.get("independence_key")))
            lins.append(d.get("independence_key"))
        table = {m: {"lineage": l, "calls": 1, "successes": 1, "state": "OK", "refusals": []} for m, l in found}
        tlock, t_start = threading.Lock(), time.monotonic()
        TERMINAL = {"QUOTA_EXHAUSTED", "AUTH_EXPIRED", "UNAVAILABLE"}      # PlumMe offer health that needs new information (never requalified in-process): exhaustion, not a cooldown

        def measure(m):
            ep, t = ep0.fork(), table[m]
            for k in range(1, 5):
                time.sleep(max(0.0, t_start + k * 360 - time.monotonic()))
                with tlock:
                    if cnt["n"] >= 40:
                        return
                    cnt["n"] += 1
                    t["calls"] += 1
                try:
                    r = ep.step("Reply with the single word READY.", "author", prefer=m, sticky_attempts=99)
                    err = None
                except Exception as exc:  # noqa: BLE001
                    r, err = {"success": False}, f"{type(exc).__name__}: {str(exc)[:200]}"
                if r.get("success") and r.get("model_key") == m:
                    t["successes"] += 1
                    continue
                st = plum_state(ctx, m)                                      # availability comes from PlumMe (offer / pool / credential state), not from message text
                t["refusals"].append({"error": err or str(r.get("failure_class"))[:120], "plumme": st})
                if st["offers"] and all(o["health"] in TERMINAL or o["pool_state"] == "EXHAUSTED" for o in st["offers"]):
                    t["state"] = "EXHAUSTED"
                    return
        with ThreadPoolExecutor(max_workers=max(1, len(found))) as tp:
            list(tp.map(measure, [m for m, _ in found]))
        qual = {m: t for m, t in table.items() if t["successes"] >= 3}
        print(json.dumps({"capacity": table, "calls_total": cnt["n"], "qualifying": sorted(qual), "distinct_qualifying_lineages": len({t["lineage"] for t in qual.values()}),
                          "roster_possible": len({t["lineage"] for t in qual.values()}) >= 4}), flush=True)
        return 0
    if a.supply_check:
        ep = ctx.episode("T", "supply")
        picked, rows, lins = {}, [], []
        for role in ("solver1", "solver2", "critic", "specialist"):
            d = ep.step("Reply with the single word READY.", "author", exclude=tuple(lins if role != "solver1" else ()), sticky_attempts=1)
            if not d["success"]:
                rows.append({"role": role, "model": None, "ok": 0})
                continue
            m = d["model_key"]
            picked[role] = m
            if role in ("solver1", "solver2"):
                lins.append(d.get("independence_key"))
            ok = 0
            for _p in range(5):
                r = ep.step("Reply with the single word READY.", "author", prefer=m, sticky_attempts=99)
                ok += int(r["success"] and r.get("model_key") == m)
                time.sleep(a.probe_interval)
            rows.append({"role": role, "model": m, "lineage": d.get("independence_key"), "ok_of_5": ok})
        distinct = len({r.get("lineage") for r in rows[:2]}) == 2
        print(json.dumps({"supply": rows, "solver_lineages_distinct": distinct, "pass": distinct and all(r.get("ok_of_5") == 5 for r in rows)}))
        return 0
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
            for _p in range(a.probe_calls):
                r = ep.step("Reply with the single word READY.", "author", prefer=model, sticky_attempts=99)
                ok += int(r["success"] and r.get("model_key") == model)
                time.sleep(a.probe_interval)
            log.append({"model": model, "lineage": lin, "probe_ok": ok})
            if ok == a.probe_calls:
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
    if a.chain_hunt:
        for i, q in enumerate(qs[: a.chain_hunt], 1):
            row = attempt(run_T, ctx, q)
            full = finish(q, "T", row, False)
            ch = chain_stages(full)
            with res_path.open("a") as fh:
                fh.write(json.dumps({**full, "chain": ch, "chain_class": chain_class(full) if ch["complete"] else None}) + "\n")
            print(json.dumps({"hunt": i, "qid": q["id"], "category": q.get("category"), "status": full["status"], "detail": (full.get("infra_detail") or "")[:160], "chain": ch, "class": chain_class(full) if ch["complete"] else None,
                              "stop": full.get("stop"), "correct": full.get("correct"), "work_ref": full.get("work_ref"),
                              "run_budget_used": run_budget.provider_attempt_count if run_budget else None}), flush=True)
            if ch["complete"]:
                return 0
            if run_budget is not None and run_budget.provider_attempt_count >= run_budget.max_provider_calls:
                print(json.dumps({"hunt": "RUN_CAP_REACHED", "used": run_budget.provider_attempt_count}), flush=True)
                return 4
        return 3

    def write(rows):
        with ctx.results_lock:
            with res_path.open("a") as fh:
                for row in rows:
                    fh.write(json.dumps(row) + "\n")
        for row in rows:
            print(json.dumps({k: row.get(k) for k in ("qid", "arm", "letter", "correct", "status", "calls", "tokens", "seconds")}), flush=True)

    def sink(row):
        rows, gone = ctx.outage.offer(row)
        write(rows)
        if gone:
            note_restart(ctx, row["arm"], gone)
    with ThreadPoolExecutor(max_workers=a.q_par) as pool:
        list(pool.map(lambda q: process_question(ctx, q, arms, done, sink), qs))
    if ctx.outage.tripped:                                                # in-flight failures of the same outage are retried too
        note_restart(ctx, "*", [(r["qid"], r["arm"]) for r in ctx.outage.flush()])
        return Outage.RESTART_CODE
    write(ctx.outage.flush())
    close_out(ctx, arms, res_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
