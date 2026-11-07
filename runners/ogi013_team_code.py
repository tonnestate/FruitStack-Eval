"""OGI-013 Experiment B (Addendum 3): a CherryMe-led coding team on one task.

CherryMe's run_rounds stays the organisation (n_solvers=2, DEFAULT_MAX_ROUNDS, specialist via `signature`); this module only supplies work(): real sticky coding sessions,
the shared team state (team_state.md, in every prompt), stall-triggered help, joint release and attribution snapshots.
Modes: team (T) | indep (N: independent sticky sessions, no exchange, release by rule 2) | solo (S: one sticky author session).
usage (host python via ogi013_host_bootstrap.py --runner): ogi013_team_code.py --base DIR --task-json agent_task.json --python PY --out OUT --mode team|indep|solo
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import subprocess
import tempfile
import threading
import traceback
from pathlib import Path
from types import SimpleNamespace

import ogi013_candidates as oc
import ogi013_conc as conc
import ogi013_code_task as ct
from ogi013_roster import InfraSupply, Roster
from ogi013_mango_ledger import InfraMangoFailed, MangoLedger
from ogi013_vote import OPEN, PENDING, Ledger, judge_vote, locked, tally as release_tally, vote_stop, next_no_shrink
from ogi013_coding_gate import CodingGate


def _is_stop(exc):
    from ogi013_tau2_agent import _is_stop as tau2_is_stop
    return tau2_is_stop(exc)

GROUNDS_RULE = ("After that first line give a GROUNDS section: every check you made and what each showed, including the test commands you ran and their results. "
                "A verdict without grounds is not accepted as an examination.\n")
TEAM_CRITIC_HEAD = ct.CRITIC_HEAD.replace("followed by the specific problems and the evidence you observed (test output, code facts).", "followed by the specific problems.\n" + GROUNDS_RULE)
HELP_HEAD = ("\nYou are instead a colleague asked for help by a teammate whose work has stalled (condition: {cond}); the repository is a copy of their workspace. Look at their current change, "
             "latest test output and recent actions, work out what is blocking them, and finish with a plain message: ISSUES: FOUND followed by concrete observations and suggestions "
             "(facts you verified, not a finished patch).\n<current_diff>\n{diff}\n</current_diff>\n"
             "<latest_test_output>\n{tests}\n</latest_test_output>\n<recent_actions>\n{recent}\n</recent_actions>\n")
VOTE_HEAD = ("\nYou are instead a member of the team that produced the candidate patch below (sha256 {sha}), casting your RELEASE VOTE. Your vote must cite this sha256. The repository is a copy of the candidate workspace: read, search and run tests; "
             "you cannot edit. Finish with a plain message whose FIRST line is exactly one of 'APPROVE: EXCELLENT', 'APPROVE: ACCEPTABLE' or 'REJECT'. Then state what you checked, which tests you ran "
             "and what they showed, and, in a line starting 'OWN_OBJECTIONS:', either NONE (if you raised no objection) or EVERY objection id you raised with how it was resolved (e.g. 'OWN_OBJECTIONS: O2 fixed in revision 1 (test X now passes); O5 WITHDRAWN'). The host compares this with the ledger. Vote EXCELLENT only if you would stand behind this patch resolving the "
             "issue completely without breaking existing behaviour.\n<candidate_diff>\n{diff}\n</candidate_diff>\n")
MAX_VOTE_CYCLES = 8              # = CherryMe DEFAULT_MAX_ROUNDS
RAN = re.compile(r"^Ran (\d+) tests?", re.M)
FAILCOUNT = re.compile(r"\((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?")


class Pos:
    def __init__(self, pid: str, ws: Path, gate: CodingGate):
        self.id, self.ws, self.gate = pid, ws, gate
        self.diff = ""
        self.model = None
        self.keys: set = set()
        self.status = "open"
        self.test_tail = ""
        self.last_run: tuple | None = None
        self.rev = 0
        self.slot = None              # roster slot (solver1 / solver2 / specialist)
        self.exams: list = []          # examinations since the last revision (newest last)
        self.snapshots: list = []


class TeamState(Ledger):
    """team_state.md: goal, per position diff + latest full visible test result + status, open objections, decisions. Never truncated by age. The objection ledger (lifecycle) is ogi013_vote.Ledger."""
    def __init__(self, goal: str, path: Path):
        super().__init__()
        self.goal, self.path, self.pos, self.decisions = goal, path, {}, []
        self.votes, self.release, self.mango, self._written = [], None, None, {}
        self.roster_changes_provider = lambda: []
        self.candidates_provider = lambda: []                  # set by the driver: the candidate ledger (without diffs) travels with the state
        self.consistency_guard = True
        self.diff_report = None
        self.howto, self.roster_line, self.driver_visible = "", "", {}       # R4 block, R8 roster line, driver-run visible result per position
        self.on_change = self._objection_changed
        self.independent = False        # Addendum 8: True from episode start until the SOLVE phase ends; a solver (or its helper) then sees only its own position

    # ---- MangoMe as the work ledger (AMENDMENT-MANGO-1 / C.3) -------------------------------------------------------------------------------------------------
    PERSISTED_OBJ_KEYS = ("id", "target", "lineage", "text", "kind", "grounded", "state", "open", "contested", "decided_by", "author_reason", "ground", "declined", "arbitrated", "exchanges", "replies", "needs_arbitration")

    def _objection_row(self, o) -> dict:
        return {k: o.get(k) for k in self.PERSISTED_OBJ_KEYS}

    def _objection_changed(self, o) -> None:
        if self.mango is not None:
            row = self._objection_row(o)
            self.mango.write("TEAM_OBJECTION", f"{o['id']}:{o['state']}:{o.get('contested', 0)}:{self.mango.seq}", row)
            self._written[("obj", o["id"])] = json.dumps(row, sort_keys=True)

    @locked
    def state_dict(self) -> dict:
        return {"goal": self.goal, "independent": self.independent, "version": self.version, "howto": self.howto, "roster": self.roster_line, "driver_visible": self.driver_visible,
                "candidates": self.candidates_provider(), "roster_changes": self.roster_changes_provider(), "pos": [{"id": p.id, "slot": getattr(p, "slot", None), "model": p.model, "status": p.status, "rev": p.rev, "diff": p.diff, "test_tail": p.test_tail,
                         "sha256": hashlib.sha256((p.diff or "").encode()).hexdigest()} for p in self.pos.values()],
                "objs": [self._objection_row(o) for o in self.objs], "n": self.n, "decisions": list(self.decisions), "votes": list(self.votes), "release": self.release}

    @locked
    def persist(self) -> None:
        """Granular records for every changed row, then the full structured state as the LAST checkpoint (work_context returns only the latest one)."""
        if self.mango is None:
            return
        m = self.mango
        if ("goal",) not in self._written:
            m.write("TEAM_GOAL", "goal", {"goal": self.goal})
            self._written[("goal",)] = "1"
        for p in self.pos.values():
            row = {"id": p.id, "model": p.model, "status": p.status, "rev": p.rev, "sha256": hashlib.sha256((p.diff or "").encode()).hexdigest(), "diff": p.diff}
            enc = json.dumps(row, sort_keys=True)
            if self._written.get(("pos", p.id)) != enc:
                m.write("TEAM_POSITION", f"{p.id}:{p.rev}:{row['sha256'][:12]}:{p.status}", row)
                self._written[("pos", p.id)] = enc
        for o in self.objs:
            enc = json.dumps(self._objection_row(o), sort_keys=True)
            if self._written.get(("obj", o["id"])) != enc:
                self._objection_changed(o)               # state changed outside a ledger method (e.g. an evidenced withdrawal inside a vote)
        for i, d in enumerate(self.decisions):
            if ("dec", i) not in self._written:
                m.write("TEAM_DECISION", str(i), {"i": i, "text": d})
                self._written[("dec", i)] = d
        for i, v in enumerate(self.votes):
            if ("vote", i) not in self._written:
                m.write("TEAM_VOTE", str(i), v)
                self._written[("vote", i)] = "1"
        if self.release is not None and ("release",) not in self._written:
            m.write("TEAM_RELEASE", "release", self.release)
            self._written[("release",)] = "1"
        full = self.state_dict()
        enc = json.dumps(full, sort_keys=True, default=str)
        if self._written.get(("full",)) != enc:
            m.write("TEAM_STATE_FULL", "full", full)
            self._written[("full",)] = enc

    @classmethod
    def from_payload(cls, d: dict, path: Path) -> "TeamState":
        t = cls(d["goal"], path)
        t.independent, t.n = d.get("independent", False), d.get("n", 0)
        t.version = d.get("version", 0)
        t.howto, t.roster_line, t.driver_visible = d.get("howto", ""), d.get("roster", ""), dict(d.get("driver_visible", {}))
        for p in d["pos"]:
            t.pos[p["id"]] = SimpleNamespace(id=p["id"], slot=p.get("slot"), model=p["model"], status=p["status"], rev=p["rev"], diff=p["diff"], test_tail=p["test_tail"])
        t.objs = [{**o, "raised_ns": 0, "revised_ns": None} for o in d["objs"]]
        t.decisions, t.votes, t.release = list(d["decisions"]), list(d["votes"]), d["release"]
        t.candidates = list(d.get("candidates", []))
        return t

    @classmethod
    def restore(cls, ledger: MangoLedger, path: Path) -> "TeamState":
        """Rebuild the team state from MangoMe's work_context alone (restart test, final order C.4 step 3)."""
        d = ledger.latest()
        if not d or "goal" not in d:
            raise InfraMangoFailed("RESTORE_NO_TEAM_STATE: the latest checkpoint of the work holds no TEAM_STATE_FULL")
        return cls.from_payload(d, path)

    @locked
    def prompt(self, view=None, flush=True, guard=True) -> str:
        """MangoMe as the live shared workspace: the text every agent step sees is RENDERED FROM A MANGOME READ (work_context -> TEAM_STATE_FULL), never from the in-memory state. The in-memory state is
        only a write buffer: it is flushed first (flush=True), then the host reads back, renders, and compares with the in-memory render; any difference, or a failed/stale read, ends the episode
        INFRA_MANGOME_FAILED with the diff recorded."""
        import difflib
        if self.mango is None:
            return self.text(view)
        if flush:
            self.persist()
        try:
            d = self.mango.latest_full()
        except InfraMangoFailed as exc:
            if "READ_NOT_TEAM_STATE" not in str(exc):
                raise
            self._written.pop(("full",), None)                    # a granular record was the latest checkpoint: write the full state again, then read
            self.persist()
            d = self.mango.latest_full()
        r = TeamState.from_payload(d, self.path)
        shown = r.render(view)
        if guard and self.consistency_guard:
            mine = self.render(view)
            if mine != shown:
                self.diff_report = "\n".join(list(difflib.unified_diff(mine.splitlines(), shown.splitlines(), "in-memory", "mangome", lineterm="", n=1))[:60])
                raise InfraMangoFailed("CONSISTENCY_GUARD: the render from MangoMe differs from the in-memory state")
        if view is None or not (self.independent and view is not None):
            self.path.write_text(r.render(None))
        return shown

    @locked
    def text(self, view=None) -> str:
        self.persist()
        s = self.render(view)
        if not (self.independent and view is not None):
            self.path.write_text(s)
        return s

    def render(self, view=None) -> str:
        """view: id of the solver position whose session (or helper) is being prompted. A solver that has not yet submitted its first position receives NO team state at all (not even after the reveal
        barrier opened for the others); during independent solving a solver that has submitted sees only its own position, objections and decisions."""
        vp = self.pos.get(view) if view is not None else None
        if vp is not None and not vp.diff and getattr(vp, "slot", None) in ("solver1", "solver2"):
            return ""
        solo = self.independent and view is not None
        out = [f"GOAL:\n{self.goal}\n", f"STATE VERSION: {self.version}\n"] + ([self.howto + "\n"] if self.howto else []) + ([f"ROSTER (pinned for the whole episode): {self.roster_line}\n"] if self.roster_line else []) + ["POSITIONS:"]
        for p in self.pos.values():
            if solo and p.id != view:
                out.append(f"- {p.id}: (withheld during independent solving)")
                continue
            out.append(f"- {p.id} (model {p.model}, status {p.status}, revision {p.rev})\n  diff:\n{p.diff or '  (no accepted diff yet)'}\n  latest visible test result (tail):\n{p.test_tail or '  (none)'}\n  driver-run visible check of the current candidate: {self.driver_visible.get(p.id, '(not run yet)')}")
        out.append("OPEN OBJECTIONS / SUGGESTIONS:")
        out += [f"- {o['id']} on {o['target']} from {o['lineage']} [{o['kind']}{'' if o['grounded'] else ', UNGROUNDED'}, {o['state']}]: {o['text']}"
                + "".join(f"\n    REPLY {r['step']} ({r['role']}, {r['action']}, evidence {r['evidence']}, sha256 {r['sha256'][:12]}): {r['text'][:200]}" for r in o.get("replies", []))
                for o in self.objs if o["open"] and (not solo or o["target"] == view)] or ["(none)"]
        out.append("DECISIONS:")
        out += [f"- {d}" for d in self.decisions if not solo or d.startswith(f"{view} ")] or ["(none)"]
        return "\n".join(out)


def help_guard(ep, positions: dict, p, independent: bool, call):
    """Addendum 8 B.3: during independent solving a helper must come from neither solver's lineage; with none eligible, no help is given (HELP_UNAVAILABLE_INDEPENDENCE)."""
    excl = tuple(sorted({k for q in positions.values() for k in q.keys})) if independent else tuple(p.keys)
    try:
        return call(excl)
    except RuntimeError as exc:
        if independent and "NO_ELIGIBLE_NEURON" in str(exc):
            ep.event("HELP_UNAVAILABLE_INDEPENDENCE", pos=p.id, excluded=list(excl))
            return None
        raise


def solver_similarity(diffs: list):
    """Line-level Jaccard similarity of the solvers' first positions (changed lines only); None with fewer than two positions."""
    sets = [{l for l in d.splitlines() if l[:1] in "+-" and l[:3] not in ("+++", "---")} for d in diffs[:2]]
    if len(sets) < 2:
        return None
    union = sets[0] | sets[1]
    return round(len(sets[0] & sets[1]) / len(union), 3) if union else 1.0


def outcome(run_output: str):
    """(tests executed, failing+erroring) from a Django runner transcript; None when nothing ran."""
    m = RAN.findall(run_output or "")
    if not m:
        return None
    n = int(m[-1])
    bad = len(re.findall(r"\.\.\. (?:FAIL|ERROR)\s*$", run_output, re.M))
    return n, bad


def funcs_of(diff: str) -> frozenset:
    """(file, enclosing function from the hunk header) for every hunk of a diff."""
    out, cur = set(), None
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
        elif line.startswith("@@") and cur:
            out.add((cur, line.split("@@")[-1].strip()))
    return frozenset(out)


def infra_failed_exit(ep, out: Path, exc: BaseException, t0: float, extra: dict | None = None) -> int:
    """C.2 / confirmation order: a failed MangoMe write ends the episode INFRA_MANGOME_FAILED, an unfillable roster INFRA_SUPPLY: infrastructure, never a result, never silently continued."""
    status = "INFRA_SUPPLY" if isinstance(exc, InfraSupply) else "INFRA_MANGOME_FAILED"
    ep.event(status, error=str(exc)[:400])
    ep.close(status)
    (out / "run.json").write_text(json.dumps({"status": status, "error": str(exc)[:400], "work_ref": ep.work, "turn_id": ep.turn_id, "project_ref": ep.project,
                                               "seconds": round(time.monotonic() - t0, 1), **(extra or {})}, indent=1))
    print(json.dumps({"status": status}))
    return 3


def main(argv=None) -> int:
    from ogi013_tau2_agent import Episode, Stack
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--task-json", type=Path, required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mode", choices=["team", "indep", "solo", "naive"], required=True)
    ap.add_argument("--n-critiques", type=int, default=0, help="naive (arm N): critique calls, measured from the T episode")
    ap.add_argument("--n-revisions", type=int, default=0, help="naive (arm N): revise calls, measured from the T episode")
    ap.add_argument("--n-sessions", type=int, default=2, help="indep: number of independent sessions")
    ap.add_argument("--max-calls", type=int, default=int(os.environ.get("OGI013_EP_MAX_CALLS", 1500)))
    ap.add_argument("--max-tokens", type=int, default=int(os.environ.get("OGI013_EP_MAX_TOKENS", 3000000)))
    ap.add_argument("--max-concurrent-calls", type=int, default=conc.MAX_CONCURRENT_CALLS, help="cap on simultaneous provider calls per episode (P4)")
    ap.add_argument("--solver-wait", type=float, default=600.0, help="SOLVER_WAIT: seconds after the first submitted position before the reveal barrier opens (P1)")
    ap.add_argument("--sequential-rounds", action="store_true", help="debug: run the CherryMe rounds without concurrency")
    ap.add_argument("--wall-seconds", type=int, default=int(os.environ.get("OGI013_EP_WALL", 14400)))
    a = ap.parse_args(argv)
    task = json.loads(a.task_json.read_text())
    issue = task["problem_statement"]
    a.out.mkdir(parents=True, exist_ok=True)
    stack = Stack.get(a.out / "fruitstack")
    import ogi013_host_composer
    stack.fs.attach_host_effects(**ogi013_host_composer.host_effects())
    effects = stack.fs.effects
    ep = Episode(stack, a.mode, task["instance_id"], "django", a.out / "fruitstack-events.jsonl")
    stack.fs.governance.configure(ep.sid, ep.store_revision(stack), max_calls=a.max_calls, max_tokens=a.max_tokens, max_cost_usd=0.0)
    t0 = time.monotonic()
    ctx = ct.Ctx(ep, effects, None, t0 + a.wall_seconds, a.out)
    timing = conc.TimingRecorder()
    ep.timing, ep.call_gate = timing, conc.CallGate(a.max_concurrent_calls, timing)
    ep.token_cap, ep.gov_cfg = a.max_tokens, dict(max_calls=a.max_calls, max_tokens=a.max_tokens, max_cost_usd=0.0)
    plock = threading.RLock()                 # the episode lock: shared-state mutation and adoption decisions are serialised
    slot_taken: set = set()
    solver_sessions: list = []
    critic_sessions: list = []
    team = TeamState(issue, a.out / "team_state.md")
    team.emit = ep.event
    team.mango = MangoLedger(stack.fs.mango, ep.work, ep.actor, ep.turn_id, ep.sid)      # MangoMe is the work ledger of the episode; a failed write ends it INFRA_MANGOME_FAILED
    infra: list = []

    def infra_extra() -> dict:
        return {"mango_writes": team.mango.writes, "mango_reads": team.mango.reads, "consistency_guard_diff": team.diff_report}
    labels_base = oc.visible_labels(a.base)
    labels_fallback: list = []                # tasks whose suite is large: the labels of the first candidate's own relevant run
    team.howto = oc.howto_block(a.python, labels_base or ["<dotted.test.module>"])         # R4

    def candidate_checker(diff, repros):
        """R1: the HOST runs the visible tests (and the recorded reproductions of grounded objections) on the candidate tree. Hidden tests are never consulted."""
        with tempfile.TemporaryDirectory() as tmp:
            tree = oc.tree_with_diff(a.base, diff, Path(tmp) / "tree")
            labels = labels_base or labels_fallback
            res = oc.run_visible(a.python, tree, labels) if labels else {"passed": 0, "failed": 0, "executed": 0, "tail": ""}
            rp = {}
            for oid, rep in repros.items():
                if rep["tool"] == "run_python":
                    rp[oid] = ct.Sandbox(tree, a.python).run_python(rep["args"].get("code", ""), rep["args"].get("label", "")).startswith("exit=0")
                else:
                    r2 = oc.run_visible(a.python, tree, rep["args"].get("modules", []))
                    rp[oid] = r2["executed"] > 0 and r2["failed"] == 0
            return {**res, "repro": rp}

    cled = oc.CandidateLedger(candidate_checker, on_write=team.mango.write)
    team.candidates_provider = lambda: [{k: v for k, v in c.items() if k != "diff"} for c in cled.cands]
    team.roster_changes_provider = lambda: list(roster.changes)

    def roster_emit(kind, **kw):
        ep.event(kind, **kw)
        team.roster_line = ", ".join(f"{r}={v['model_key']}" for r, v in sorted(roster.pins.items()))
    roster = Roster(emit=roster_emit, write=team.mango.write)
    team.independent = a.mode == "team"
    author_head = ct.SYSTEM.format(issue=issue) + ct.AUTHOR_NOTE
    tools_rw = {"list_dir", "read_file", "search", "edit_file", "run_tests", "run_python"}
    tools_ro = {"list_dir", "read_file", "search", "run_tests", "run_python"}
    holders: dict[str, str] = {}              # role-holder model key -> lineage (solvers, specialist, challengers, helpers)
    positions: dict[str, Pos] = {}
    by_text: dict[str, Pos] = {}
    by_model: dict[str, Pos] = {}
    snaps = a.out / "snapshots"
    snaps.mkdir(exist_ok=True)

    def new_pos(prefix: str, pid: str | None = None) -> Pos:
        with plock:
            pid = pid if pid and pid not in positions else f"{prefix}{len(positions) + 1}"
            ws = a.out / "ws" / pid
            shutil.copytree(a.base, ws)
            p = Pos(pid, ws, CodingGate(ws, task["base_commit"], a.out / "gate" / pid))
            positions[pid] = team.pos[pid] = p
            ep.event("POSITION_OPENED", pos=pid)
            return p

    def claim_slot() -> str:
        """A solve call claims a solver slot atomically (concurrent solvers): the first slot nobody holds, else a slot whose position produced no accepted diff."""
        with plock:
            for slot in ("solver1", "solver2"):
                if slot not in slot_taken:
                    slot_taken.add(slot)
                    return slot
            for slot in ("solver1", "solver2"):
                if not any(q.diff for q in positions.values() if q.slot == slot):
                    return slot
            return "solver1"

    def freeze_locked(p: Pos, dec, label: str) -> None:
        with plock:
            freeze(p, dec, label)

    def freeze(p: Pos, dec, label: str) -> None:
        p.gate.snapshot(f"P{p.rev}", dec)
        p.changed_ns = time.monotonic_ns()
        ep.event("SNAPSHOT", pos=p.id, label=label, sha=dec.diff_sha256, author_lineages=sorted(p.keys))
        (snaps / f"{p.id}_{label}.diff").write_text(dec.diff)
        p.snapshots.append({"label": label, "sha256": dec.diff_sha256, "file": f"{p.id}_{label}.diff"})
        p.diff, p.status = dec.diff, p.status if label != "first" else "open"
        p.last_run = p.session_sb.last_run
        p.test_tail = (p.last_run[2][-3000:] if p.last_run else "")
        team.mango.write("TEAM_SNAPSHOT", f"{p.id}:{label}", {"pos": p.id, "label": label, "rev": p.rev, "sha256": dec.diff_sha256, "files": list(dec.changed_source_files)})
        by_text[dec.diff] = p
        if not labels_base and not labels_fallback and p.last_run:
            labels_fallback.extend(x for x in p.last_run[0][2:] if re.fullmatch(r"[\w.]+", x) and not x.isdigit())
        if a.mode != "naive":                                      # arm N has no ledger, no driver-run checks, no rollback
            cand = cled.add(p.id, label, dec.diff)                 # R1: immutable candidate with sha256 and the driver-run visible check
            team.driver_visible[p.id] = f"{cand['visible'].get('passed')} passed, {cand['visible'].get('failed')} failed (sha256 {cand['sha256'][:12]})"

    def restore_workspace(p: Pos, diff: str) -> None:
        """Roll the position's workspace back to a candidate (the incumbent / protected best): base tree plus that candidate's diff, under django/ only."""
        subprocess.run(["git", "checkout", "-q", task["base_commit"], "--", "django"], cwd=p.ws, check=True)
        subprocess.run(["git", "clean", "-fdq", "--", "django"], cwd=p.ws, check=True)
        if diff.strip():
            subprocess.run(["git", "apply", "--whitespace=nowarn", "-"], cwd=p.ws, input=diff, text=True, check=True)
        p.diff = diff
        by_text[diff] = p

    def result(out, st):
        if isinstance(out, str) and out.startswith("STOP:"):
            return {"success": False, "output": None, "model_key": st and st["model_key"], "independence_key": st and st["independence_key"], "receipt_id": st and st["receipt_id"], "failure_class": out}
        return {"success": True, "output": out, "model_key": st["model_key"], "independence_key": st["independence_key"], "receipt_id": st["receipt_id"]}

    helper_lineages: set = set()

    def helper_for(p: Pos):
        def helper(cond, diff, tests, recent):
            copy = a.out / "help" / f"{p.id}_{cond}_{time.time_ns()}"
            shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            saved = ctx.last_session

            def call(excl):
                return ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + HELP_HEAD.format(cond=cond, diff=diff[:6000], tests=tests, recent=recent), ct.Sandbox(copy, a.python, readonly=True),
                                     tools_ro, exclude=excl, gated=False, team=team, view=p.id, wait_supply=not team.independent, roster=roster, role_key="critic")
            got = help_guard(ep, positions, p, team.independent, call)
            hgs = ctx.last_session
            ctx.last_session = saved
            if got is None:
                return None, None
            out, st = got
            if isinstance(out, str) and out.startswith("STOP:"):
                return None, None
            hoid = team.objection(p.id, st["independence_key"], out, kind="suggestion", grounded=ct.grounded_text(out, hgs))
            holders[st["model_key"]] = st["independence_key"]
            if team.independent:
                helper_lineages.add(st["independence_key"])
            ep.event("HELP_ANSWER", pos=p.id, rev=p.rev, author_lineages=sorted(p.keys), condition=cond, model=st["model_key"], lineage=st["independence_key"], objection_ids=[hoid], text=out[:300])
            return out, st["model_key"]
        return helper

    def session(p: Pos, head: str, turns=None, exclude=()):
        p.session_sb = ct.Sandbox(p.ws, a.python)
        out, st = ct.agent_loop(ctx, "author", head, p.session_sb, tools_rw | {"decline"}, gated=True, gate=p.gate, team=team if a.mode == "team" else None,
                                helper=helper_for(p) if a.mode == "team" else None, limit=turns, exclude=tuple(exclude), view=p.id, roster=roster, role_key=p.slot)
        if st:
            p.model = p.model or st["model_key"]
            p.keys.add(st["independence_key"])
            by_model[st["model_key"]] = p
            holders[st["model_key"]] = st["independence_key"]
        return out, st

    def work(prompt: str, stage: str, prefer=None, exclude=()):
        try:
            if stage != "solve":
                team.independent = False                                  # the SOLVE phase is over: full shared state for every role
            if stage == "solve":
                slot = claim_slot() if a.mode == "team" else ("solver1" if a.mode == "solo" else f"solver{len(positions) + 1}")
                p = new_pos("S", {"solver1": "S1", "solver2": "S2"}.get(slot))
                p.slot = slot
                # independent lineages: never a lineage that already holds a position, nor one that helped during independent solving (Addendum 8 B.3)
                excl = tuple(exclude) + tuple(sorted({k for q in positions.values() for k in q.keys} | helper_lineages)) if a.mode == "team" else ()
                t_s = time.monotonic()
                out, st = session(p, author_head, exclude=excl)
                solver_sessions.append((p.id, t_s, time.monotonic()))
                if not isinstance(out, str):
                    p.rev = 0
                    freeze_locked(p, out, "first")
                    team.decisions.append(f"{p.id} produced its first gate-accepted diff ({out.diff_sha256[:10]})")
                    out = out.diff
                    if team.independent and sum(1 for q in positions.values() if q.diff) >= 2:
                        team.independent = False                          # both solvers delivered their first positions
                        ep.event("INDEPENDENT_PHASE_END", positions=[q.id for q in positions.values() if q.diff])
                return result(out, st)
            if stage == "challenge":
                tgt = next((p for t, p in by_text.items() if t and t in prompt), None)
                copy = a.out / "challenge" / f"{tgt.id}_r{tgt.rev}_{len(tgt.exams)}_{time.time_ns()}"
                shutil.copytree(tgt.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                pending = [o for o in team.objs if o["target"] == tgt.id and o["state"] == PENDING]
                if pending:                                           # Addendum 7: re-examination of addressed objections, preferably by the raiser
                    prompt += ("\nThe author claims these earlier objections are now addressed. After running a check yourself, write one line per id exactly 'O<n>: RESOLVED' or 'O<n>: STILL_OPEN':\n"
                               + "\n".join(f"{o['id']}: {o['text'][:400]}" for o in pending))
                    raiser = {v: k for k, v in holders.items()}.get(pending[0]["lineage"])
                    prefer = prefer or raiser
                answered = [o for o in team.objs if o["target"] == tgt.id and o["state"] == OPEN and o["exchanges"] == 1]
                if answered:                                          # exchange 2: the critic responds ONCE to the author's evidence
                    prompt += ("\nThe author answered these objections with evidence. Respond once to each, on its own line: 'O<n>: WITHDRAW' plus your evidence (a reproduction you ran, or a quote of the task text) if you now agree, "
                               "or 'O<n>: MAINTAIN' plus NEW evidence if you do not:\n" + "\n".join(f"{o['id']}: {o['replies'][-1]['text'][:400]}" for o in answered))
                t_c = time.monotonic()
                out, st = ct.agent_loop(ctx, "critic", TEAM_CRITIC_HEAD.format(issue=issue) + "\n" + prompt, ct.Sandbox(copy, a.python, readonly=True), tools_ro, prefer=prefer, exclude=tuple(exclude) + tuple(tgt.keys), gated=False, team=team, roster=roster, role_key="critic")
                gs = ctx.last_session
                critic_sessions.append((tgt.id, t_c, time.monotonic()))
                if isinstance(out, str) and not out.startswith("STOP:"):
                    found = bool(re.match(r"\s*ISSUES:\s*FOUND", out, re.I))
                    exam = {"verdict": "FOUND" if found else "NONE", "lineage": st["independence_key"], "model": st["model_key"], "test_runs": ctx.last_session["test_runs"], "grounded": False, "text": out}
                    ground = oc.classify_objection(out, issue, gs["check_log"]) if found else {"kind": "suggestion"}           # R2: only a failing command output or a verbatim task-text quote grounds an objection
                    exam["grounded"] = oc.is_grounded(ground)
                    tgt.exams.append(exam)
                    holders[st["model_key"]] = st["independence_key"]
                    changes = team.reexamine(tgt.id, out, st["independence_key"], tuple(tgt.keys), gs["checks"]) if pending else []
                    for o in answered:                                # the critic's single response in the exchange (a reply without evidence is logged UNGROUNDED_REPLY and changes nothing)
                        m = re.search(rf"^\s*{o['id']}\s*:\s*(WITHDRAW|MAINTAIN)\b(.*?)(?=^\s*O\d+\s*:|\Z)", out, re.I | re.M | re.S)
                        if m:
                            team.reply(o["id"], "critic", m.group(1).lower(), m.group(2).strip() or out, oc.classify_objection(m.group(2) + "\n" + out, issue, gs["check_log"]))
                    oids = []
                    if found and not any(state == OPEN for _, state in changes):
                        oids.append(team.objection(tgt.id, exam["lineage"], out, grounded=exam["grounded"], ground=ground))
                        if ground.get("kind") == "command":
                            cled.add_repro(oids[-1], ground["repro"])
                    ep.event("CHALLENGE", pos=tgt.id, rev=tgt.rev, author_lineages=sorted(tgt.keys), verdict=exam["verdict"], lineage=exam["lineage"], model=exam["model"], test_runs=exam["test_runs"], grounded=exam["grounded"],
                             objection_ids=oids, reexamined=changes)
                    if found:
                        tgt.status = "challenged"
                    elif exam["grounded"]:
                        tgt.status = "validated"
                        team.decisions.append(f"{tgt.id} examined by {exam['lineage']}: ISSUES: NONE with grounds")
                return result(out, st)
            if stage == "revise":
                p = by_model.get((prefer or "").split("#")[0]) or by_model.get(prefer or "")
                before = p.diff
                openo = [o for o in team.objs if o["state"] == OPEN and o["target"] == p.id and o["kind"] == "objection"]
                grounded = [o for o in openo if o["grounded"] and not o["declined"]]
                suggestions = [o for o in openo if not o["grounded"]]
                if not grounded:                                       # R2: an ungrounded objection never forces a revision
                    ep.event("REVISION_SKIPPED", pos=p.id, reason="NO_GROUNDED_OBJECTION", suggestions=[o["id"] for o in suggestions])
                    return {"success": True, "output": p.diff, "model_key": p.model, "independence_key": next(iter(sorted(p.keys)), None), "receipt_id": None}
                crit = "GROUNDED OBJECTIONS (address each, or decline it with the decline tool {\"id\": \"O3\", \"reason\": \"one line\"}):\n" + "\n".join(
                    f"{o['id']}: {o['text'][:900]}" + (f"\n  reproduction the host will re-run: {json.dumps(o['ground'].get('repro'))}" if (o.get("ground") or {}).get("kind") == "command" else "") for o in grounded)
                if suggestions:
                    crit += "\nSUGGESTIONS (optional, may be wrong, ignore freely):\n" + "\n".join(f"{o['id']}: {o['text'][:300]}" for o in suggestions)
                rev_head = (author_head + "\nThe task text above is authoritative and wins over any opinion of a model, including a reviewer's. Change the code only to satisfy the task text and the grounded objections.\n" + crit +
                            "\nYour final answer is the repository state: change the files if an objection is right, re-run the relevant tests, then submit.")
                out, st = session(p, rev_head)
                if not isinstance(out, str):
                    with plock:                               # adoption decisions are serialised: exactly one incumbent per position at any time
                        p.rev += 1
                        label = f"rev{p.rev}"
                        declined = [o["id"] for o in grounded if o["declined"]]
                        claimed = [o["id"] for o in grounded if not o["declined"]]
                        ep.event("REVISION", pos=p.id, rev=p.rev, responding_to=claimed, declined=declined, changed_code=out.diff != before, reviser_lineage=st["independence_key"], snapshot=f"{p.id}_{label}")
                        p.exams = []
                        p.gate.snapshot(f"P{p.rev}", out)
                        p.changed_ns = time.monotonic_ns()
                        if out.diff == before:
                            team.revise(p.id, p.rev, False, claimed, reason="revision submitted with unchanged code")
                            team.decisions.append(f"{p.id} revision {p.rev}: unchanged code")
                        else:
                            dec = cled.consider_revision(p.id, label, out.diff, claimed)
                            if dec["adopted"]:
                                (snaps / f"{p.id}_{label}.diff").write_text(out.diff)
                                p.snapshots.append({"label": label, "sha256": out.diff_sha256, "file": f"{p.id}_{label}.diff"})
                                p.diff, p.status = out.diff, "revised"
                                p.last_run = p.session_sb.last_run
                                p.test_tail = (p.last_run[2][-3000:] if p.last_run else "")
                                by_text[out.diff] = p
                                c = dec["cand"]
                                team.driver_visible[p.id] = f"{c['visible'].get('passed')} passed, {c['visible'].get('failed')} failed (sha256 {c['sha256'][:12]})"
                                team.mango.write("TEAM_SNAPSHOT", f"{p.id}:{label}", {"pos": p.id, "label": label, "rev": p.rev, "sha256": out.diff_sha256, "files": list(out.changed_source_files)})
                                team.revise(p.id, p.rev, True, claimed)
                                team.decisions.append(f"{p.id} revision {p.rev} ADOPTED (driver-run visible score not lower; claimed reproductions pass)")
                            else:
                                (snaps / f"{p.id}_{label}_REJECTED.diff").write_text(out.diff)
                                restore_workspace(p, cled.incumbent(p.id)["diff"])
                                ep.event("REVISION_REJECTED", pos=p.id, rev=p.rev, reason=dec["reason"], sha=out.diff_sha256, incumbent=cled.incumbent(p.id)["id"])
                                team.revise(p.id, p.rev, False, claimed, reason=f"REVISION_REJECTED:{dec['reason']}")
                                team.decisions.append(f"{p.id} revision {p.rev} REJECTED_REVISION ({dec['reason']}); incumbent {cled.incumbent(p.id)['id']} stays")
                    arbitrate(p)
                    out = p.diff
                return result(out, st)
            if stage == "specialist":
                p = new_pos("SP")
                p.slot = "specialist"
                ep.event("SPECIALIST", pos=p.id, lineage=None)
                out, st = session(p, author_head + "\n" + prompt + "\nYour final answer is the repository state: produce your own change, test it, then submit.", exclude=tuple(roster.lineages("specialist")))
                if not isinstance(out, str):
                    freeze_locked(p, out, "first")
                    team.decisions.append(f"specialist {p.id} produced a gate-accepted diff")
                    out = out.diff
                return result(out, st)
            return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
        except Exception as exc:  # noqa: BLE001
            if _is_stop(exc):
                raise
            ep.event("WORK_ERROR", stage=stage, error=f"{type(exc).__name__}: {str(exc)[:300]}", trace=traceback.format_exc()[-1500:])
            return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "failure_class": (str(exc) or type(exc).__name__)[:80]}

    def arbitrate(p: Pos) -> None:
        """R2: if the author declined a grounded objection (or contested it twice), ONE independent specialist (not the author, not the raiser's lineage) gets the task text plus both claims, must run a
        reproduction, and decides. At most one arbitration per objection; the task text wins over any model opinion."""
        cont = [o for o in team.objs if o["target"] == p.id and o["state"] == OPEN and o["kind"] == "objection" and o["grounded"] and not o["arbitrated"] and (o["needs_arbitration"] or o["contested"] >= 2)]
        if not cont:
            return
        copy = a.out / "adjudicate" / f"{p.id}_r{p.rev}_{time.time_ns()}"
        shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        head = (ct.CRITIC_HEAD.format(issue=issue) + "\nYou are the SPECIALIST arbitrating a disagreement between a reviewer and the author. The task text above is authoritative and wins over any model's opinion. Run your own reproduction, then reply "
                "with one line per id exactly 'O<n>: RESOLVED' (the author is right) or 'O<n>: STILL_OPEN' (the objection stands), then your grounds.\n<candidate_diff>\n" + p.diff + "\n</candidate_diff>\n"
                + "\n".join(f"{o['id']} (reviewer): {o['text'][:600]}\nAUTHOR'S REASON: {o.get('author_reason', '')}" for o in cont))
        saved = ctx.last_session
        out, st = ct.agent_loop(ctx, "critic", head, ct.Sandbox(copy, a.python, readonly=True), tools_ro, exclude=tuple(p.keys) + tuple(o["lineage"] for o in cont) + tuple(roster.lineages("specialist")), gated=False, team=team,
                                roster=roster, role_key="specialist")
        gs = ctx.last_session
        ctx.last_session = saved
        for o in cont:
            o["arbitrated"] = True                              # at most one arbitration per objection
        if isinstance(out, str) and not out.startswith("STOP:"):
            holders[st["model_key"]] = st["independence_key"]
            ch = team.reexamine(p.id, out, st["independence_key"], tuple(p.keys), gs["checks"], from_state=OPEN, decided_by="specialist")
            for o in cont:
                if o["state"] == OPEN:
                    o["declined"] = False                       # the objection stands: the author must address it
            ep.event("SPECIALIST_ADJUDICATION", pos=p.id, lineage=st["independence_key"], objections=[o["id"] for o in cont], decided=ch)

    def select_roster() -> None:
        """P1: the roster is fixed FIRST: the two solver lineages are chosen sequentially through PlumMe AUTO exclusion (one tiny ping per solver), before any real call."""
        used: list = []
        for role in ("solver1", "solver2"):
            d = {"success": False}
            for attempt in range(3):
                try:
                    d = ep.step("Reply with the single word READY.", "author", exclude=tuple(used), prefer=None, sticky_attempts=1)
                except RuntimeError as exc:
                    if "NO_ELIGIBLE_NEURON" not in str(exc):
                        raise
                    d = {"success": False}
                if d["success"]:
                    break
                time.sleep(ct.SUPPLY_WAIT_SECONDS)
            if not d["success"]:
                raise InfraSupply(f"roster: the eligible pool cannot fill {role}")
            roster.pin(role, d["model_key"], d.get("independence_key"))
            roster.note_model(d["model_key"])
            holders[d["model_key"]] = d.get("independence_key")
            used.append(d.get("independence_key"))

    def work_threaded(prompt, stage, **kw):
        """Every concurrent worker runs on its own forked PeachMe session (same work/turn, shared log/stats/gate)."""
        child = ep.fork()
        ctx.bind_thread_ep(child)
        try:
            return work(prompt, stage, **kw)
        finally:
            ctx.unbind_thread_ep()

    def signature(text: str):
        """Positions disagree when their visible-test outcome vectors differ, or, both passing, when their diffs change different functions."""
        p = by_text.get(text)
        if p is None:
            return hashlib.sha256(text.encode()).hexdigest()[:12]
        o = outcome(p.last_run[2]) if p.last_run else None
        if o is None or o[1]:
            return f"tests:{o}"
        return "tests:pass:" + ";".join(sorted(f"{f}|{h}" for f, h in funcs_of(text)))

    status, res = "NO_PATCH", None
    ep.event("EPISODE_OPENED", work=ep.work, mode=a.mode, max_tokens=a.max_tokens, max_calls=a.max_calls)
    try:
        if a.mode == "team":
            from cherryme.brother import run_rounds
            from cherryme.contributions import ContributionLedger
            select_roster()
            res = run_rounds(task_prompt=f"Task: resolve this issue in the repository.\n{issue}\n", brief="", work=work if a.sequential_rounds else work_threaded, ledger=ContributionLedger(), claim_id=ep.claim.id,
                             signature=signature, parallel=not a.sequential_rounds, solver_wait=a.solver_wait, max_workers=a.max_concurrent_calls)
            ep.event("TEAM_ROUNDS", stop=res.stop_reason, calls=res.calls, rounds=res.rounds, issues_found=res.issues_found, revised=res.revised, specialist=res.specialist_used, failures=res.failures)
        elif a.mode == "indep":
            for i in range(a.n_sessions):
                work("", "solve")
        elif a.mode == "naive":
            # R6 arm N: naive chain. Same eligible supply and pinned author, same number of critique and revise calls as T, same caps; plain "pass the patch, revise on any critique, last patch wins":
            # no ledger, no grounding rule, no rollback, no arbitration, no vote.
            p = new_pos("S")
            p.slot = "solver1"
            out, st = session(p, author_head)
            if not isinstance(out, str):
                freeze_locked(p, out, "first")
                for i in range(a.n_critiques):
                    copy = a.out / "naive_critic" / f"{i}_{time.time_ns()}"
                    shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                    crit, cst = ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + "\n<proposed_change>\n" + p.diff + "\n</proposed_change>\n", ct.Sandbox(copy, a.python, readonly=True), tools_ro,
                                              exclude=tuple(p.keys), gated=False, roster=roster, role_key="critic")
                    ep.event("NAIVE_CRITIQUE", i=i, verdict=(crit if isinstance(crit, str) else "")[:60])
                    if i >= a.n_revisions or not isinstance(crit, str) or crit.startswith("STOP:"):
                        continue
                    out, st = session(p, author_head + "\nA colleague reviewed your change. Critique:\n" + crit[:3000] + "\nRevise the code if you think the critique is right, re-run the relevant tests, then submit.")
                    if not isinstance(out, str):
                        p.rev += 1
                        p.gate.snapshot(f"P{p.rev}", out)
                        (snaps / f"{p.id}_rev{p.rev}.diff").write_text(out.diff)
                        p.snapshots.append({"label": f"rev{p.rev}", "sha256": out.diff_sha256, "file": f"{p.id}_rev{p.rev}.diff"})
                        p.diff = out.diff                                  # last patch wins
                        ep.event("NAIVE_REVISION", rev=p.rev, sha=out.diff_sha256)
        else:
            p = new_pos("S")
            out, st = session(p, author_head)
            if not isinstance(out, str):
                freeze_locked(p, out, "first")
    except (InfraMangoFailed, InfraSupply) as exc:
        infra.append(exc)
    except BaseException as exc:  # noqa: BLE001 - a stop is recorded; accepted positions stay, nothing is synthesised
        ep.event("RUN_STOPPED", exception=type(exc).__name__, error=str(exc)[:400], budget_stop=_is_stop(exc))

    # joint release (B.4): unanimous grounded APPROVE: EXCELLENT; hidden tests never consulted
    def protected_best():
        """R1: the best of EVERY adopted candidate (driver-run score; ties -> earliest); the position's workspace is rolled back to it if it is not the current incumbent."""
        c = cled.best()
        if c is None:
            return None
        p = positions[c["pos"]]
        if p.diff != c["diff"]:
            restore_workspace(p, c["diff"])
        return p

    def vote(p: Pos, model: str, lineage):
        copy = a.out / "vote" / f"{p.id}_r{p.rev}_{len(votes_log)}_{time.time_ns()}"
        shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        saved = ctx.last_session
        csha = oc.sha256(p.diff)
        role = next((r for r, v in roster.pins.items() if v["model_key"] == model), None)
        out, st = ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + VOTE_HEAD.format(diff=p.diff, sha=csha), ct.Sandbox(copy, a.python, readonly=True), tools_ro, prefer=model, exclude=tuple(p.keys), gated=False, team=team,
                                roster=roster, role_key=role)
        gs = ctx.last_session
        runs = gs["test_runs"] + gs["py_runs"]
        ctx.last_session = saved
        if isinstance(out, str) and out.startswith("STOP:"):
            return {"voter": model, "lineage": lineage, "verdict": "NO_VOTE", "counts": "REJECT", "text": out}
        j = judge_vote(out, lineage, team.objs, p.id, gs["checks"], getattr(p, "changed_ns", 0), ct.grounded_text(out, gs), returned_lineage=st["independence_key"], author_lineages=tuple(p.keys), candidate_sha=csha)
        return {"check_log": gs["check_log"], "voter": model, "lineage": st["independence_key"], "withdrawals": j["withdrawals"], "verdict": j["verdict"], "counts": j["counts"], "text": out, "test_runs": runs, "grounded": ct.grounded_text(out, gs), "reason": j["reason"], "rev": p.rev, "author_lineages": sorted(p.keys)}

    votes_log: list = []
    cls, chosen, guard, open_at_stop, withdrawals = "NO_PATCH", None, None, [], 0

    if a.mode == "team" and cled.best() is not None:
        from cherryme.brother import CHALLENGE, REVISE
        prompt0 = f"Task: resolve this issue in the repository.\n{issue}\n"
        cycle, no_shrink, prev_open, prev_score, fails = 0, 0, None, (-1, 0), 0
        try:
            while True:
                chosen = protected_best()
                votes_now, seen_models = [], set()
                for role, pin in list(roster.pins.items()):             # R8: the voters are the pinned roster members
                    model, lineage = pin["model_key"], pin["lineage"]
                    if lineage in chosen.keys or model in seen_models:   # Addendum 6 section 4: nobody votes on a position from the author's own lineage; the author's endorsement is its submission
                        continue
                    seen_models.add(model)
                    v = vote(chosen, model, lineage)
                    votes_log.append({"cycle": cycle, "pos": chosen.id, **{k: v[k] for k in v if k != "text"}})
                    team.votes.append(votes_log[-1])
                    team.persist()
                    voids = []
                    if v["counts"] != "EXCELLENT" and v["verdict"] != "NO_VOTE":
                        vground = oc.classify_objection(v["text"], issue, v.get("check_log", [])) if v["verdict"] != "UNGROUNDED_APPROVAL" else {"kind": "suggestion"}
                        voids.append(team.objection(chosen.id, v["lineage"], f"[{v['verdict']}] {v['text']}", grounded=oc.is_grounded(vground), ground=vground))
                        if vground.get("kind") == "command":
                            cled.add_repro(voids[-1], vground["repro"])
                    ep.event("RELEASE_VOTE", objection_ids=voids, withdrawals=v.get("withdrawals", 0), cycle=cycle, pos=chosen.id, voter=v["voter"], lineage=v["lineage"], verdict=v["verdict"], test_runs=v.get("test_runs"), reason=v.get("reason"), rev=v.get("rev"), author_lineages=v.get("author_lineages"))
                    votes_now.append(v)
                    (a.out / "votes").mkdir(exist_ok=True)
                    (a.out / "votes" / f"c{cycle}_{chosen.id}_{len(votes_log)}.txt").write_text(v["text"] or "")
                if release_tally(votes_now) == "RELEASED_UNANIMOUS_EXCELLENT":
                    cls, withdrawals = "RELEASED_UNANIMOUS_EXCELLENT", sum(v.get("withdrawals", 0) for v in votes_now)
                    break
                fails = fails + 1 if not any(v["verdict"] != "NO_VOTE" for v in votes_now) else 0
                open_now, score = team.open_count(chosen.id), cled.score(chosen.diff)         # Addendum 5: GROUNDED open objections shrink, or the best position's visible result improves
                no_shrink = next_no_shrink(no_shrink, prev_open, open_now, prev_score, score)
                prev_open, prev_score = open_now, score
                cycle += 1
                guard = vote_stop(no_shrink, cycle, fails, MAX_VOTE_CYCLES)
                if guard:
                    break
                arbitrate(chosen)
                crit = "\n---\n".join(o["text"] for o in team.objs if o["state"] == OPEN and o["target"] == chosen.id)
                r = work(REVISE.format(task=prompt0, own=chosen.diff, critique=crit), "revise", prefer=chosen.model)
                if r["success"]:
                    work(CHALLENGE.format(task=prompt0, work=chosen.diff), "challenge", exclude=tuple(chosen.keys))
        except (InfraMangoFailed, InfraSupply) as exc:
            infra.append(exc)
        except BaseException as exc:  # noqa: BLE001
            guard = f"STOP:{type(exc).__name__}"
            ep.event("LOOP_GUARD", guard="EPISODE_CIRCUIT_BREAKER", exception=type(exc).__name__, error=str(exc)[:300], budget_stop=_is_stop(exc))
        if cls != "RELEASED_UNANIMOUS_EXCELLENT":
            chosen, cls = protected_best(), oc.release_class(False)
            open_at_stop = [o for o in team.objs if o["open"]]
            ep.event("LOOP_GUARD", guard=guard, open_objections=[o["id"] for o in open_at_stop])
    elif a.mode == "naive":
        chosen, cls = (next((q for q in positions.values() if q.diff), None)), "NAIVE_LAST_PATCH"
    elif cled.best() is not None:
        chosen, cls = protected_best(), "CANDIDATE_UNVALIDATED"      # indep / solo: the protected best by the driver-run visible score
    firsts = [positions[k].snapshots[0] for k in positions if positions[k].snapshots and not k.startswith("SP")]
    sim = solver_similarity([(snaps / f["file"]).read_text() for f in firsts]) if a.mode == "team" else None
    ep.event("SOLVER_SIMILARITY", jaccard=sim, positions=[f["file"] for f in firsts[:2]])
    team.text()
    if ep._flags().get("budget_exhausted"):
        cls = "INFRA_BUDGET_EXHAUSTED"                         # the episode's own token budget ended it at the first refusal; the reason is in run.json
    elif chosen is None and oc.infra_author_failed(ep.stats, len(cled.cands)):
        cls = "INFRA_AUTHOR_FAILED"                           # R5: the author's supply failed; infrastructure, never NO_PATCH
    ep.event("ROSTER_CHECK", **roster.check())
    final = chosen.diff if chosen else ""
    if chosen:
        (snaps / "RELEASED.diff").write_text(final)
    if infra:                                  # C.2: infrastructure, never a result; nothing is released
        return infra_failed_exit(ep, a.out, infra[0], t0, infra_extra())
    release = {"solver_similarity": sim, "guard": guard, "votes": votes_log, "class": cls, "withdrawals": withdrawals, "released": chosen.id if chosen else None, "sha256": hashlib.sha256(final.encode()).hexdigest() if final else None,
               "candidate_sha256": hashlib.sha256(final.encode()).hexdigest() if final else None}
    ep.event("RELEASE", **release)
    team.release = release
    try:
        team.persist()
    except InfraMangoFailed as exc:
        return infra_failed_exit(ep, a.out, exc, t0, infra_extra())
    status = cls
    ep.close(status)
    (a.out / "final.diff").write_text(final)
    summary = {"status": status, "work_ref": ep.work, "turn_id": ep.turn_id, "project_ref": ep.project, "mango_writes": team.mango.writes, "mango_reads": team.mango.reads, "consistency_guard_diff": team.diff_report, "budget_exhausted_reason": ep._flags().get("budget_exhausted"), "release": release, "roster": roster.summary(),
               "candidates": [{k: v for k, v in c.items() if k != "diff"} for c in cled.cands], "seconds": round(time.monotonic() - t0, 1), "stats": ep.stats,
               "positions": {p.id: {"model": p.model, "keys": sorted(k for k in p.keys if k), "status": p.status, "revisions": p.rev, "snapshots": p.snapshots,
                                    "exams": [{k: v for k, v in e.items() if k != "text"} for e in p.exams]} for p in positions.values()},
               "rounds": {"stop": res.stop_reason, "calls": res.calls, "specialist": res.specialist_used} if res else None}
    tr = timing.report()
    tr["max_concurrent_calls"] = a.max_concurrent_calls
    overlap = 0.0
    if len(solver_sessions) >= 2:
        s0, s1 = sorted(solver_sessions, key=lambda x: x[1])[:2]
        overlap = max(0.0, min(s0[2], s1[2]) - max(s0[1], s1[1]))
    tr["solver_sessions"] = [{"pos": pid, "start": round(b - timing.t0, 2), "end": round(e - timing.t0, 2)} for pid, b, e in solver_sessions]
    tr["solver_overlap_seconds"] = round(overlap, 2)
    tr["max_calls_in_flight_observed"] = ep.call_gate.max_seen
    tr["critic_sessions"] = [{"pos": pid, "start": round(b - timing.t0, 2), "end": round(e - timing.t0, 2)} for pid, b, e in critic_sessions]
    (a.out / "ledger.json").write_text(json.dumps({"objections": [{k: v for k, v in o.items() if k not in ("raised_ns", "revised_ns")} for o in team.objs], "decisions": team.decisions, "version": team.version}, indent=1, default=str))
    (a.out / "timing.json").write_text(json.dumps(tr, indent=1))
    summary["timing"] = {"max_concurrent_calls": a.max_concurrent_calls, "max_calls_in_flight_observed": ep.call_gate.max_seen, "solver_overlap_seconds": tr["solver_overlap_seconds"], "wall_share": tr["wall_share"]}
    (a.out / "run.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({k: summary[k] for k in ("status", "release", "seconds")}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
