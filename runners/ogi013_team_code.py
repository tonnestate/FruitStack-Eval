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
from pathlib import Path

import ogi013_code_task as ct
from ogi013_vote import judge_vote, tally as release_tally
from ogi013_coding_gate import CodingGate
from ogi013_tau2_agent import Episode, Stack, _is_stop

GROUNDS_RULE = ("After that first line give a GROUNDS section: every check you made and what each showed, including the test commands you ran and their results. "
                "A verdict without grounds is not accepted as an examination.\n")
TEAM_CRITIC_HEAD = ct.CRITIC_HEAD.replace("followed by the specific problems and the evidence you observed (test output, code facts).", "followed by the specific problems.\n" + GROUNDS_RULE)
HELP_HEAD = ("\nYou are instead a colleague asked for help by a teammate whose work has stalled (condition: {cond}); the repository is a copy of their workspace. Look at their current change, "
             "latest test output and recent actions, work out what is blocking them, and finish with a plain message: ISSUES: FOUND followed by concrete observations and suggestions "
             "(facts you verified, not a finished patch).\n<current_diff>\n{diff}\n</current_diff>\n"
             "<latest_test_output>\n{tests}\n</latest_test_output>\n<recent_actions>\n{recent}\n</recent_actions>\n")
VOTE_HEAD = ("\nYou are instead a member of the team that produced the candidate patch below, casting your RELEASE VOTE. The repository is a copy of the candidate workspace: read, search and run tests; "
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
        self.exams: list = []          # examinations since the last revision (newest last)
        self.snapshots: list = []


class TeamState:
    """team_state.md: goal, per position diff + latest full visible test result + status, open objections, decisions. Never truncated by age."""
    def __init__(self, goal: str, path: Path):
        self.goal, self.path, self.pos, self.objs, self.decisions, self.n = goal, path, {}, [], [], 0
        self.emit = lambda *a, **k: None           # set to Episode.event: every ledger row is also an event (Addendum 6: the audit trail)

    def objection(self, target: str, lineage, text: str, kind="objection", grounded=True) -> None:
        self.n += 1
        self.objs.append({"id": f"O{self.n}", "target": target, "lineage": lineage, "text": text[:1500], "kind": kind, "open": True, "grounded": grounded, "answered_by": None, "withdrawn": False})
        self.emit("OBJECTION", id=f"O{self.n}", target=target, lineage=lineage, kind=kind, grounded=grounded)

    def close_objections(self, target: str, reason: str) -> None:
        for o in self.objs:
            if o["target"] == target and o["open"]:
                o["open"], o["answered_by"] = False, reason
                self.decisions.append(f"{o['id']} on {target} superseded: {reason}")

    def open_count(self, target: str) -> int:
        """Addendum 5: only GROUNDED open objections count; ungrounded ones are recorded and shown but neither count nor block."""
        return sum(1 for o in self.objs if o["target"] == target and o["open"] and o["kind"] == "objection" and o["grounded"])

    def text(self) -> str:
        out = [f"GOAL:\n{self.goal}\n", "POSITIONS:"]
        for p in self.pos.values():
            out.append(f"- {p.id} (model {p.model}, status {p.status}, revision {p.rev})\n  diff:\n{p.diff or '  (no accepted diff yet)'}\n  latest visible test result (tail):\n{p.test_tail or '  (none)'}")
        out.append("OPEN OBJECTIONS / SUGGESTIONS:")
        out += [f"- {o['id']} on {o['target']} from {o['lineage']} [{o['kind']}{'' if o['grounded'] else ', UNGROUNDED'}]: {o['text']}" for o in self.objs if o["open"]] or ["(none)"]
        out.append("DECISIONS:")
        out += [f"- {d}" for d in self.decisions] or ["(none)"]
        s = "\n".join(out)
        self.path.write_text(s)
        return s


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


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--task-json", type=Path, required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--mode", choices=["team", "indep", "solo"], required=True)
    ap.add_argument("--n-sessions", type=int, default=2, help="indep: number of independent sessions")
    ap.add_argument("--max-calls", type=int, default=int(os.environ.get("OGI013_EP_MAX_CALLS", 1500)))
    ap.add_argument("--max-tokens", type=int, default=int(os.environ.get("OGI013_EP_MAX_TOKENS", 3000000)))
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
    team = TeamState(issue, a.out / "team_state.md")
    team.emit = ep.event
    author_head = ct.SYSTEM.format(issue=issue) + ct.AUTHOR_NOTE
    tools_rw = {"list_dir", "read_file", "search", "edit_file", "run_tests", "run_python"}
    tools_ro = {"list_dir", "read_file", "search", "run_tests", "run_python"}
    holders: dict[str, str] = {}              # role-holder model key -> lineage (solvers, specialist, challengers, helpers)
    positions: dict[str, Pos] = {}
    by_text: dict[str, Pos] = {}
    by_model: dict[str, Pos] = {}
    snaps = a.out / "snapshots"
    snaps.mkdir(exist_ok=True)

    def new_pos(prefix: str) -> Pos:
        pid = f"{prefix}{len(positions) + 1}"
        ws = a.out / "ws" / pid
        shutil.copytree(a.base, ws)
        p = Pos(pid, ws, CodingGate(ws, task["base_commit"], a.out / "gate" / pid))
        positions[pid] = team.pos[pid] = p
        ep.event("POSITION_OPENED", pos=pid)
        return p

    def freeze(p: Pos, dec, label: str) -> None:
        p.gate.snapshot(f"P{p.rev}", dec)
        p.changed_ns = time.monotonic_ns()
        ep.event("SNAPSHOT", pos=p.id, label=label, sha=dec.diff_sha256, author_lineages=sorted(p.keys))
        (snaps / f"{p.id}_{label}.diff").write_text(dec.diff)
        p.snapshots.append({"label": label, "sha256": dec.diff_sha256, "file": f"{p.id}_{label}.diff"})
        p.diff, p.status = dec.diff, p.status if label != "first" else "open"
        p.last_run = p.session_sb.last_run
        p.test_tail = (p.last_run[2][-3000:] if p.last_run else "")
        by_text[dec.diff] = p

    def result(out, st):
        if isinstance(out, str) and out.startswith("STOP:"):
            return {"success": False, "output": None, "model_key": st and st["model_key"], "independence_key": st and st["independence_key"], "receipt_id": st and st["receipt_id"], "failure_class": out}
        return {"success": True, "output": out, "model_key": st["model_key"], "independence_key": st["independence_key"], "receipt_id": st["receipt_id"]}

    def helper_for(p: Pos):
        def helper(cond, diff, tests, recent):
            copy = a.out / "help" / f"{p.id}_{cond}_{int(time.time())}"
            shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            saved = ctx.last_session
            out, st = ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + HELP_HEAD.format(cond=cond, diff=diff[:6000], tests=tests, recent=recent), ct.Sandbox(copy, a.python, readonly=True),
                                    tools_ro, exclude=tuple(p.keys), gated=False, team=team)
            hgs = ctx.last_session
            ctx.last_session = saved
            if isinstance(out, str) and out.startswith("STOP:"):
                return None, None
            team.objection(p.id, st["independence_key"], out, kind="suggestion", grounded=ct.grounded_text(out, hgs))
            holders[st["model_key"]] = st["independence_key"]
            ep.event("HELP_ANSWER", pos=p.id, rev=p.rev, author_lineages=sorted(p.keys), condition=cond, model=st["model_key"], lineage=st["independence_key"], text=out[:300])
            return out, st["model_key"]
        return helper

    def session(p: Pos, head: str, turns=None):
        p.session_sb = ct.Sandbox(p.ws, a.python)
        out, st = ct.agent_loop(ctx, "author", head, p.session_sb, tools_rw, gated=True, gate=p.gate, team=team if a.mode == "team" else None,
                                helper=helper_for(p) if a.mode == "team" else None, limit=turns)
        if st:
            p.model = p.model or st["model_key"]
            p.keys.add(st["independence_key"])
            by_model[st["model_key"]] = p
            holders[st["model_key"]] = st["independence_key"]
        return out, st

    def work(prompt: str, stage: str, prefer=None, exclude=()):
        try:
            if stage == "solve":
                p = new_pos("S")
                out, st = session(p, author_head)
                if not isinstance(out, str):
                    p.rev = 0
                    freeze(p, out, "first")
                    team.decisions.append(f"{p.id} produced its first gate-accepted diff ({out.diff_sha256[:10]})")
                    out = out.diff
                return result(out, st)
            if stage == "challenge":
                tgt = next((p for t, p in by_text.items() if t and t in prompt), None)
                copy = a.out / "challenge" / f"{tgt.id}_r{tgt.rev}_{len(tgt.exams)}"
                shutil.copytree(tgt.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                out, st = ct.agent_loop(ctx, "critic", TEAM_CRITIC_HEAD.format(issue=issue) + "\n" + prompt, ct.Sandbox(copy, a.python, readonly=True), tools_ro, exclude=tuple(exclude) + tuple(tgt.keys), gated=False, team=team)
                gs = ctx.last_session
                if isinstance(out, str) and not out.startswith("STOP:"):
                    found = bool(re.match(r"\s*ISSUES:\s*FOUND", out, re.I))
                    exam = {"verdict": "FOUND" if found else "NONE", "lineage": st["independence_key"], "model": st["model_key"], "test_runs": ctx.last_session["test_runs"], "grounded": ct.grounded_text(out, gs) and len(out) > 80, "text": out}
                    tgt.exams.append(exam)
                    holders[st["model_key"]] = st["independence_key"]
                    ep.event("CHALLENGE", pos=tgt.id, rev=tgt.rev, author_lineages=sorted(tgt.keys), verdict=exam["verdict"], lineage=exam["lineage"], model=exam["model"], test_runs=exam["test_runs"], grounded=exam["grounded"])
                    if found:
                        team.objection(tgt.id, exam["lineage"], out, grounded=exam["grounded"])
                        tgt.status = "challenged"
                    elif exam["grounded"]:
                        tgt.status = "validated"
                        team.decisions.append(f"{tgt.id} examined by {exam['lineage']}: ISSUES: NONE with grounds")
                return result(out, st)
            if stage == "revise":
                p = by_model.get((prefer or "").split("#")[0]) or by_model.get(prefer or "")
                before = p.diff
                responding = [o["id"] for o in team.objs if o["open"] and o["target"] == p.id and o["kind"] == "objection"]
                out, st = session(p, author_head + "\n" + prompt + "\nYour final answer is the repository state: change the files if the criticism is right, re-run the relevant tests, then submit.")
                if not isinstance(out, str):
                    p.rev += 1
                    ep.event("REVISION", pos=p.id, rev=p.rev, responding_to=responding, changed_code=out.diff != before, reviser_lineage=st["independence_key"], snapshot=f"{p.id}_rev{p.rev}")
                    p.exams = []
                    team.close_objections(p.id, f"revision {p.rev}")
                    freeze(p, out, f"rev{p.rev}")
                    p.status = "revised"
                    team.decisions.append(f"{p.id} revised after criticism (revision {p.rev}, {'changed' if out.diff != before else 'unchanged'})")
                    out = out.diff
                return result(out, st)
            if stage == "specialist":
                p = new_pos("SP")
                ep.event("SPECIALIST", pos=p.id, lineage=None)
                out, st = session(p, author_head + "\n" + prompt + "\nYour final answer is the repository state: produce your own change, test it, then submit.")
                if not isinstance(out, str):
                    freeze(p, out, "first")
                    team.decisions.append(f"specialist {p.id} produced a gate-accepted diff")
                    out = out.diff
                return result(out, st)
            return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
        except Exception as exc:  # noqa: BLE001
            if _is_stop(exc):
                raise
            ep.event("WORK_ERROR", stage=stage, error=f"{type(exc).__name__}: {str(exc)[:300]}")
            return {"success": False, "output": None, "model_key": None, "independence_key": None, "receipt_id": None, "failure_class": (str(exc) or type(exc).__name__)[:80]}

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
            res = run_rounds(task_prompt=f"Task: resolve this issue in the repository.\n{issue}\n", brief="", work=work, ledger=ContributionLedger(), claim_id=ep.claim.id, signature=signature)
            ep.event("TEAM_ROUNDS", stop=res.stop_reason, calls=res.calls, rounds=res.rounds, issues_found=res.issues_found, revised=res.revised, specialist=res.specialist_used, failures=res.failures)
        elif a.mode == "indep":
            for i in range(a.n_sessions):
                work("", "solve")
        else:
            p = new_pos("S")
            out, st = session(p, author_head)
            if not isinstance(out, str):
                freeze(p, out, "first")
    except BaseException as exc:  # noqa: BLE001 - a stop is recorded; accepted positions stay, nothing is synthesised
        ep.event("RUN_STOPPED", exception=type(exc).__name__, error=str(exc)[:400], budget_stop=_is_stop(exc))

    # joint release (B.4): unanimous grounded APPROVE: EXCELLENT; hidden tests never consulted
    def passing(p):
        o = outcome(p.last_run[2]) if p.last_run else None
        return (o[0] - o[1]) if o else -1

    def best():
        acc = [p for p in positions.values() if p.diff]
        return sorted(acc, key=lambda p: (-passing(p), team.open_count(p.id)))[0] if acc else None

    def vote(p: Pos, model: str, lineage):
        copy = a.out / "vote" / f"{p.id}_r{p.rev}_{len(votes_log)}"
        shutil.copytree(p.ws, copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        saved = ctx.last_session
        out, st = ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + VOTE_HEAD.format(diff=p.diff), ct.Sandbox(copy, a.python, readonly=True), tools_ro, prefer=model, gated=False, team=team)
        gs = ctx.last_session
        runs = gs["test_runs"] + gs["py_runs"]
        ctx.last_session = saved
        if isinstance(out, str) and out.startswith("STOP:"):
            return {"voter": model, "lineage": lineage, "verdict": "NO_VOTE", "counts": "REJECT", "text": out}
        j = judge_vote(out, lineage, team.objs, p.id, gs.get("check_ns", []), getattr(p, "changed_ns", 0), ct.grounded_text(out, gs))
        return {"voter": model, "lineage": st["independence_key"], "verdict": j["verdict"], "counts": j["counts"], "text": out, "test_runs": runs, "grounded": ct.grounded_text(out, gs), "reason": j["reason"], "rev": p.rev, "author_lineages": sorted(p.keys)}

    votes_log: list = []
    cls, chosen, guard, open_at_stop = "NO_PATCH", None, None, []
    if a.mode == "team" and best() is not None:
        from cherryme.brother import CHALLENGE, REVISE
        prompt0 = f"Task: resolve this issue in the repository.\n{issue}\n"
        cycle, no_shrink, prev_open, prev_score, fails = 0, 0, None, -1, 0
        try:
            while True:
                chosen = best()
                votes_now = []
                for model, lineage in list(holders.items()):
                    if lineage in chosen.keys:        # Addendum 6 section 4: nobody votes on a position from the author's own lineage; the author's endorsement is its submission
                        continue
                    v = vote(chosen, model, lineage)
                    votes_log.append({"cycle": cycle, "pos": chosen.id, **{k: v[k] for k in v if k != "text"}})
                    ep.event("RELEASE_VOTE", cycle=cycle, pos=chosen.id, voter=v["voter"], lineage=v["lineage"], verdict=v["verdict"], test_runs=v.get("test_runs"), reason=v.get("reason"), rev=v.get("rev"), author_lineages=v.get("author_lineages"))
                    votes_now.append(v)
                    (a.out / "votes").mkdir(exist_ok=True)
                    (a.out / "votes" / f"c{cycle}_{chosen.id}_{len(votes_log)}.txt").write_text(v["text"] or "")
                if release_tally(votes_now) == "RELEASED_UNANIMOUS_EXCELLENT":
                    cls = "RELEASED_UNANIMOUS_EXCELLENT"
                    break
                fails = fails + 1 if not any(v["verdict"] != "NO_VOTE" for v in votes_now) else 0
                for v in votes_now:
                    if v["counts"] != "EXCELLENT" and v["verdict"] != "NO_VOTE":
                        team.objection(chosen.id, v["lineage"], f"[{v['verdict']}] {v['text']}", grounded=bool(v.get("grounded")) and v["verdict"] != "UNGROUNDED_APPROVAL")
                open_now, score = team.open_count(chosen.id), passing(chosen)         # Addendum 5: GROUNDED open objections shrink, or the best position's visible result improves
                no_shrink = 0 if prev_open is None or open_now < prev_open or score > prev_score else no_shrink + 1
                prev_open, prev_score = open_now, score
                cycle += 1
                if no_shrink >= 3 or cycle >= MAX_VOTE_CYCLES or fails >= 3:
                    guard = "VOTE_NO_SHRINK_3" if no_shrink >= 3 else "VOTE_CYCLES_8" if cycle >= MAX_VOTE_CYCLES else "VOTE_FAILURES_3"
                    break
                crit = "\n---\n".join(o["text"] for o in team.objs if o["open"] and o["target"] == chosen.id)
                r = work(REVISE.format(task=prompt0, own=chosen.diff, critique=crit), "revise", prefer=chosen.model)
                if r["success"]:
                    work(CHALLENGE.format(task=prompt0, work=chosen.diff), "challenge", exclude=tuple(chosen.keys))
        except BaseException as exc:  # noqa: BLE001
            guard = f"STOP:{type(exc).__name__}"
            ep.event("LOOP_GUARD", guard="EPISODE_CIRCUIT_BREAKER", exception=type(exc).__name__, error=str(exc)[:300], budget_stop=_is_stop(exc))
        if cls != "RELEASED_UNANIMOUS_EXCELLENT":
            chosen, cls = best(), "RELEASED_NO_CONSENSUS"
            open_at_stop = [o for o in team.objs if o["open"]]
            ep.event("LOOP_GUARD", guard=guard, open_objections=[o["id"] for o in open_at_stop])
    elif best() is not None:
        chosen, cls = best(), "RELEASED_UNVALIDATED"      # indep / solo: the visible-signal rule (most relevant tests passing)
    final = chosen.diff if chosen else ""
    if chosen:
        (snaps / "RELEASED.diff").write_text(final)
    release = {"guard": guard, "votes": votes_log, "class": cls, "released": chosen.id if chosen else None, "sha256": hashlib.sha256(final.encode()).hexdigest() if final else None}
    ep.event("RELEASE", **release)
    status = cls
    ep.close(status)
    (a.out / "final.diff").write_text(final)
    summary = {"status": status, "release": release, "seconds": round(time.monotonic() - t0, 1), "stats": ep.stats,
               "positions": {p.id: {"model": p.model, "keys": sorted(k for k in p.keys if k), "status": p.status, "revisions": p.rev, "snapshots": p.snapshots,
                                    "exams": [{k: v for k, v in e.items() if k != "text"} for e in p.exams]} for p in positions.values()},
               "rounds": {"stop": res.stop_reason, "calls": res.calls, "specialist": res.specialist_used} if res else None}
    (a.out / "run.json").write_text(json.dumps(summary, indent=1, default=str))
    print(json.dumps({k: summary[k] for k in ("status", "release", "seconds")}, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
