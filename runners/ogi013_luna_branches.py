"""OGI-013 Experiment A (Addendum 2 C): Brother Mode on Luna's real flawed patch P0.

P0 = the recorded Luna patch applied to a fresh base copy (frozen by the gate). Branches from the same P0:
  LSR  Luna reviews its own P0 (coding CHALLENGE prompt), then Luna revises given that critique
  LBR  an independent lineage (PlumMe AUTO, OpenAI lineage excluded, eligibility rule applied) reviews P0 with the same prompt, access and cap, then Luna revises
Every revision passes the gate (source diff + a fresh relevant test run seen in Luna's own command events). Grading is done afterwards with evaluate_v2.py.
usage (host python via ogi013_host_bootstrap.py --runner): ogi013_luna_branches.py --base DIR --task-json agent_task.json --p0 patch.diff --python PY --out OUT --k 5"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import ogi013_code_task as ct
from ogi013_coding_gate import CodingGate
from ogi013_tau2_agent import Episode, Stack

CODEX_HOME = "/root/.plumme/codex-headless-home"
ENV_NOTE = ("Python 3.8 interpreter with Django's dependencies: /root/fruits/research/OGI013-SINGLE-TASK/venv38/bin/python ; run tests with: "
            "PYTHONPATH=. /root/fruits/research/OGI013-SINGLE-TASK/venv38/bin/python tests/runtests.py <module>\n")     # the same environment note Luna received in arm L
CRITIQUE_CAP = 4000                     # characters of critique handed to the reviser, identical in LSR and LBR
CRITIC_TASK = ("You are an independent code reviewer. The repository in the working directory already contains a colleague's proposed change (P0). Inspect it and run the relevant existing "
               "tests yourself. Do NOT edit any file. Then finish with a plain message whose FIRST line is exactly 'ISSUES: NONE' or 'ISSUES: FOUND', followed by the specific problems and the "
               "evidence you observed (test commands and their results, code facts).\n" + ENV_NOTE + "<issue>\n{issue}\n</issue>\n<proposed_change>\n{p0}\n</proposed_change>")
REVISE_TASK = ("You are working in a checkout of the Django repository in the current directory. " + ENV_NOTE + "ISSUE:\n{issue}\nYour earlier change (P0) is in the working directory. A reviewer examined it and reported:\n<review>\n{critique}\n</review>\n"
               "Decide whether the review is right. Change the source code if it is, run the relevant existing tests after your last edit, and finish.")


def luna(prompt: str, workdir: Path, sandbox: str, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "CODEX_HOME": CODEX_HOME}
    t0 = time.monotonic()
    r = subprocess.run(["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", sandbox, "-m", "gpt-6-luna", "-c", 'approval_policy="never"', "-C", str(workdir), "--json", "-"],
                       input=prompt, capture_output=True, text=True, env=env, timeout=1800)
    (out / "events.jsonl").write_text(r.stdout)
    (out / "stderr.txt").write_text(r.stderr[-2000:])
    events = [json.loads(l) for l in r.stdout.splitlines() if l.startswith("{")]
    usage = {"input": 0, "cached": 0, "output": 0}
    for e in events:
        if e.get("type") == "turn.completed":
            u = e.get("usage", {})
            usage["input"] += u.get("input_tokens", 0); usage["cached"] += u.get("cached_input_tokens", 0); usage["output"] += u.get("output_tokens", 0)
    msgs = [e["item"]["text"] for e in events if e.get("type") == "item.completed" and e["item"].get("type") == "agent_message"]
    return {"events": events, "usage": usage, "final": msgs[-1] if msgs else "", "seconds": round(time.monotonic() - t0, 1), "exit": r.returncode}


def feed_gate(gate: CodingGate, events: list) -> None:
    """Replay Luna's own edits and relevant test runs, in stream order, into the gate."""
    for e in events:
        if e.get("type") != "item.completed":
            continue
        it = e["item"]
        if it.get("type") == "file_change":
            for c in it.get("changes", []):
                try:
                    gate.record_edit(c["path"])
                except ValueError:
                    pass
        elif it.get("type") == "command_execution" and "runtests.py" in it.get("command", ""):
            m = re.search(r"runtests\.py(.*?)['\"]?\s*$", it["command"])
            labels = shlex.split(m.group(1)) if m else []
            gate.record_test_run(["python", "tests/runtests.py", *labels], it.get("exit_code") or 0, it.get("aggregated_output", ""))


def grade(ws: Path, out: Path) -> dict:
    task = Path("/root/fruits/research/OGI013-SINGLE-TASK")
    subprocess.run([str(task / "venv38/bin/python"), str(task / "evaluate_v2.py"), str(ws), str(out)], capture_output=True, text=True, timeout=2400)
    return json.loads(out.read_text())


def classify(before: dict, after: dict) -> str:
    if after.get("resolved"):
        return "rescue"
    b, a = (before["f2p_passed"], before["p2p_passed"]), (after.get("f2p_passed", -1), after.get("p2p_passed", -1))
    if a[0] < b[0] or a[1] < b[1]:
        return "harm"
    return "partial_improvement" if a[0] > b[0] else "no_effect"


def lineage_keys(stack: Stack) -> list:
    from plumme.knowledge import independence_key
    return sorted({independence_key(o) for o in stack.svc.store.market.offers.values() if re.search(r"(?i)openai|gpt|luna|codex", f"{o.provider} {o.model} {o.model_family}")})


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=Path, required=True)
    ap.add_argument("--task-json", type=Path, required=True)
    ap.add_argument("--p0", type=Path, required=True)
    ap.add_argument("--python", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--branches", default="LSR,LBR")
    a = ap.parse_args(argv)
    task = json.loads(a.task_json.read_text())
    issue = task["problem_statement"]
    a.out.mkdir(parents=True, exist_ok=True)
    stack = Stack.get(a.out / "fruitstack")
    import ogi013_host_composer
    stack.fs.attach_host_effects(**ogi013_host_composer.host_effects())
    effects = stack.fs.effects

    p0_ws = a.out / "p0_ws"                     # fresh base copy + Luna's recorded patch, frozen through the gate (P0)
    shutil.copytree(a.base, p0_ws)
    subprocess.run(["git", "apply", "--whitespace=nowarn", str(a.p0.resolve())], cwd=p0_ws, check=True)
    gate0 = CodingGate(p0_ws, task["base_commit"], a.out / "gate_p0")
    for f in re.findall(r"^\+\+\+ b/(\S+)", a.p0.read_text(), re.M):
        gate0.record_edit(f)
    sb0 = ct.Sandbox(p0_ws, a.python)
    sb0.run_tests(["forms_tests.tests.test_media"])
    gate0.record_test_run(*sb0.last_run)
    dec0 = gate0.check_submit()
    gate0.snapshot("P0", dec0)
    p0_text = gate0.review_target()
    before = grade(p0_ws, a.out / "p0_grade.json")
    print("P0", dec0.accepted, before.get("f2p_passed"), before.get("p2p_passed"), flush=True)
    results = []
    for k in range(1, a.k + 1):
        for br in a.branches.split(","):
            d = a.out / f"{br}_r{k:02d}"
            rec = {"branch": br, "replicate": k}
            try:
                crit_ws = d / "critic_ws"
                shutil.copytree(p0_ws, crit_ws, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                if br == "LSR":
                    c = luna(CRITIC_TASK.format(issue=issue, p0=p0_text), crit_ws, "workspace-write", d / "critic")
                    critique, rec["critic"] = c["final"], {"model": "gpt-6-luna", "lineage": "openai", "usage": c["usage"], "seconds": c["seconds"]}
                    rec["critic_edited_code"] = subprocess.run(["git", "diff", "--stat", "--", "django"], cwd=crit_ws, capture_output=True, text=True).stdout != subprocess.run(["git", "diff", "--stat", "--", "django"], cwd=p0_ws, capture_output=True, text=True).stdout
                else:
                    ep = Episode(stack, "lbr", f"{task['instance_id']}-{br}{k}", "django", d / "fruitstack-events.jsonl")
                    stack.fs.governance.configure(ep.sid, ep.store_revision(stack), max_calls=110, max_tokens=200000, max_cost_usd=0.0)
                    ctx = ct.Ctx(ep, effects, None, time.monotonic() + 3600, d)
                    excl = tuple(lineage_keys(stack))
                    rec["excluded_keys"] = list(excl)
                    out, st = ct.agent_loop(ctx, "critic", ct.CRITIC_HEAD.format(issue=issue) + "\n<proposed_change>\n" + p0_text + "\n</proposed_change>",
                                            ct.Sandbox(crit_ws, a.python, readonly=True), {"list_dir", "read_file", "search", "run_tests"}, exclude=excl, gated=False)
                    ep.close("CRITIQUE_DONE")
                    critique = out if not (isinstance(out, str) and out.startswith("STOP:")) else ""
                    rec["critic"] = {"model": st and st["model_key"], "lineage": st and st["independence_key"], "stats": ep.stats, "stop": out if not critique else None}
                rec["critique"] = critique[:CRITIQUE_CAP]
                (d / "critique.txt").write_text(rec["critique"])
                if not critique:
                    rec["outcome"] = "NO_CRITIQUE"
                    results.append(rec); continue
                rev_ws = d / "rev_ws"
                shutil.copytree(p0_ws, rev_ws, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
                gate = CodingGate(rev_ws, task["base_commit"], d / "gate")
                r = luna(REVISE_TASK.format(issue=issue, critique=rec["critique"]), rev_ws, "workspace-write", d / "revision")
                feed_gate(gate, r["events"])
                dec = gate.check_submit()
                rec["revision"] = {"usage": r["usage"], "seconds": r["seconds"], "gate": dec.reason, "accepted": dec.accepted, "changed_vs_p0": dec.diff != p0_text}
                if dec.accepted and dec.diff != p0_text:
                    gate.snapshot("P1", dec)
                    rec["grade"] = grade(rev_ws, d / "grade.json")
                    rec["classification"] = classify(before, rec["grade"])
                    rec["outcome"] = "REVISED"
                else:
                    rec["classification"] = "no_effect"; rec["outcome"] = "P0_UNCHANGED" if dec.accepted else "REVISION_REJECTED_BY_GATE"
            except Exception as exc:  # noqa: BLE001
                rec["outcome"] = f"ERROR:{type(exc).__name__}:{str(exc)[:200]}"
            (d.parent / f"{br}_r{k:02d}.json").write_text(json.dumps(rec, indent=1, default=str))
            results.append(rec)
            print(br, k, rec.get("outcome"), rec.get("classification"), rec.get("grade", {}).get("f2p_passed"), flush=True)
    (a.out / "summary.json").write_text(json.dumps({"p0_grade": {k: before.get(k) for k in ("f2p_passed", "p2p_passed", "resolved")}, "results": results}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
