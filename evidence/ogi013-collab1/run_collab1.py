#!/usr/bin/env python3
"""OGI-013-COLLAB-1 launcher: runs the frozen 48-task x {SINGLE, COLLAB, SINGLE-E} campaign through the EXISTING pilot machinery (run_arm.sh -> bootstrap -> ogi013_tau2_run.py -> official tau2 grader; the
pre-dispatch gate and PlumMe ParentBudget of ogi013_pilot_gate; pilot_guard for usage/halts). Nothing runs without the owner's approval file for exactly collab1_budget.json.
usage: run_collab1.py --approval FILE [--base DIR] [--budget FILE] [--manifest FILE] [--campaign NAME] [--plan]
exit: 0 campaign complete | 2 refused (nothing started) | 3 halted by a campaign-level limit | 5 an episode failed to execute (campaign stopped, evidence kept) | 130 interrupted.
Never restarts a halted campaign by itself. Restarting THIS command after an interruption continues unfinished work only: completed episodes (episode record DONE / BUDGET_STOP / TIMEOUT) are never run again,
an interrupted episode's directory is archived under discarded/ (its usage keeps counting) and run afresh. Whole-block simulator failures: block archived, up to 3 attempts, then INFRA_INCOMPLETE (non-success)."""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1]
PILOT = CODE / "evidence/ogi013-pilot"
REAL_BASE = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013")
MODE = {"SINGLE": "single", "COLLAB": "rg2", "SINGLE-E": "single_e"}
DONE_STATES = {"DONE", "BUDGET_STOP", "TIMEOUT"}                        # scored (non-success unless the official grade says otherwise); never run again
HOSTPY = "/root/fruits/integration/ogi013-hostpython-org/bin/python"
COMPONENTS = Path("/root/fruits/integration/ogi013-org-components")
SUPPLY_RECHECK_S = 120                                                  # between verified-capacity checks while nothing can serve the simulator (no block is consumed)
LOCKS = [CODE / "evidence/ogi013-phase2/STUDY_LOCK.txt", HERE / "AMENDMENT_LOCK.txt"]


class Interrupted(Exception):
    pass


def load_guard():
    spec = importlib.util.spec_from_file_location("pilot_guard", PILOT / "pilot_guard.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lock_mismatches() -> list[str]:
    """The implementation and protocol files must be byte-identical to the LATEST entry of the study lock + its amendment locks (files without an entry are not covered)."""
    latest = {}
    for lock in LOCKS:
        if lock.is_file():
            for line in lock.read_text().splitlines():
                if line.strip() and not line.startswith("#"):
                    digest, rel = line.split(None, 1)
                    latest[rel.strip()] = digest
    return [rel for rel, d in sorted(latest.items()) if not (CODE / rel).is_file() or hashlib.sha256((CODE / rel).read_bytes()).hexdigest() != d]


def sh(*cmd, env=None, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), env=env, cwd=cwd, capture_output=True, text=True)


class Campaign:
    def __init__(self, a):
        self.a = a
        self.base = Path(a.base).resolve()
        self.R = self.base / "runs"
        self.C = self.R / a.campaign
        self.budget_path = Path(a.budget).resolve()
        self.budget = json.loads(self.budget_path.read_text())
        self.manifest = json.loads(Path(a.manifest).read_text())
        self.guard = load_guard()
        self.child = None

    # ---- bookkeeping ---------------------------------------------------------------------------------------------------------------------------------------------
    def log(self, text: str):
        with (self.C / "progress.txt").open("a") as f:
            f.write(f"{time.strftime('%FT%TZ', time.gmtime())} {text}\n")

    def rec_path(self, ref: str, cond: str) -> Path:
        return self.C / ref.replace(":", "_") / f"{cond}.episode.json"

    def read_rec(self, ref, cond):
        p = self.rec_path(ref, cond)
        return json.loads(p.read_text()) if p.is_file() else None

    def write_rec(self, ref, cond, **kw):
        p = self.rec_path(ref, cond)
        p.parent.mkdir(parents=True, exist_ok=True)
        rec = json.loads(p.read_text()) if p.is_file() else {}
        rec.update(kw)
        p.write_text(json.dumps(rec, indent=1, sort_keys=True))

    def arms(self) -> list[str]:
        """Every episode directory of the campaign - finished, running and archived - so its usage counts against the campaign totals."""
        return sorted(str(p.with_name(p.name[: -len(".episode.json")]).relative_to(self.R)) for p in self.C.rglob("*.episode.json"))

    # ---- preconditions -------------------------------------------------------------------------------------------------------------------------------------------
    def refuse(self, why: str) -> int:
        print("REFUSED: " + why, file=sys.stderr)
        return 2

    def preconditions(self) -> int | None:
        if not self.guard.verify_approval(str(self.budget_path), self.a.approval):
            return self.refuse("no approval for exactly this budget file")
        if os.environ.get("PILOT_OFFLINE_TRANSPORT") and self.base == REAL_BASE.resolve():
            return self.refuse("the offline provider transport is never allowed against the real evaluation base")
        if hashlib.sha256(Path(self.a.manifest).read_bytes()).hexdigest() != self.budget.get("manifest_sha256"):
            return self.refuse("manifest does not match the manifest hash in the approved budget")
        bad = lock_mismatches()
        if bad:
            return self.refuse("implementation differs from the frozen lock: " + ", ".join(bad))
        if sh("git", "-C", str(CODE), "status", "--porcelain").stdout.strip():
            return self.refuse(f"code checkout {CODE} is not clean")
        if (self.R / "PILOT_HALT").exists():
            return self.refuse("a halt file exists in the runs directory; a halted campaign is never restarted by itself (inspect and archive it)")
        env = {**os.environ, "PILOT_CODE": str(CODE), "PILOT_BASE": str(self.base)}
        if sh(str(PILOT / "run_arm.sh"), "--verify-components", env=env).returncode:
            return self.refuse("components do not resolve from the canonical checkouts")
        c = sh(str(PILOT / "run_arm.sh"), "--contract", str(self.budget_path), str(PILOT / "pilot_guard.py"), env=env)
        if c.returncode:
            return self.refuse("lease-contract check failed: " + c.stdout[-400:])
        return None

    # ---- one episode ---------------------------------------------------------------------------------------------------------------------------------------------
    def episode_env(self, task, cond, arm, ep_dir, start):
        env = {k: v for k, v in os.environ.items() if not k.startswith(("OGI013_ORG_", "OGI013_SINGLE_E", "OGI013_PILOT_", "PILOT_SESSION"))}
        env.update({"PILOT_CODE": str(CODE), "PILOT_BASE": str(self.base), "OGI013_PILOT_BUDGET": str(self.budget_path), "OGI013_PILOT_GUARD": str(PILOT / "pilot_guard.py"),
                    "OGI013_PILOT_RUNS": str(self.R), "OGI013_PILOT_ARMS": ",".join(self.arms()), "OGI013_PILOT_ARM": arm, "OGI013_PILOT_START": str(start),
                    "OGI013_ORG_STATE_DIR": str(ep_dir.parent / f"{cond}-state")})
        for k, v in self.guard.session_env(self.budget, arm).items():
            env[k.replace("OGI013_", "PILOT_", 1)] = v
        if cond == "COLLAB":
            env.update({"OGI013_ORG_COLLAB": "1", "OGI013_ORG_POLICY_MODE": "OFF"})
        if cond == "SINGLE-E":
            se = self.manifest["single_e"]
            env.update({"OGI013_SINGLE_E_K": str(se["k"]), "OGI013_SINGLE_E_SCOPE": se["scope"]})
        return env

    def run_episode(self, t, cond, attempt) -> str:
        ref, domain, tid = t["task_ref"], t["domain"], t["task_id"]
        dirname = ref.replace(":", "_")
        arm = f"{self.a.campaign}/{dirname}/{cond}"
        ep_dir = self.R / arm
        pair = f"{self.a.campaign}-{dirname}"
        slot = self.C / dirname / f"{cond}-slot"
        for n in ("chat", "project"):                                          # fresh isolated organisational state per episode, all cloned from the same frozen snapshot
            (slot / "ledgers").mkdir(parents=True, exist_ok=True)
            r = sh("git", "clone", "-q", "--bare", str(self.base / "slots/D/ledgers" / f"{n}.git"), str(slot / "ledgers" / f"{n}.git"))
            if r.returncode:
                raise RuntimeError("ledger clone failed: " + r.stderr[-200:])
        (slot / "orangeme-home").mkdir(exist_ok=True)
        start = json.loads((self.C / "campaign.json").read_text())["started_at"]
        self.write_rec(ref, cond, task=ref, condition=cond, attempt=attempt, status="RUNNING", started_at=time.time(), code_head=sh("git", "-C", str(CODE), "rev-parse", "HEAD").stdout.strip(),
                       slot_heads={n: sh("git", "--git-dir", str(slot / "ledgers" / f"{n}.git"), "rev-parse", "HEAD").stdout.strip() for n in ("chat", "project")},
                       flags={"mode": MODE[cond], "OGI013_ORG_COLLAB": "1" if cond == "COLLAB" else None, "single_e": self.manifest["single_e"] if cond == "SINGLE-E" else None})
        env = self.episode_env(t, cond, arm, ep_dir, start)
        log = self.C / dirname / f"{cond}.log"
        pids = self.C / dirname / f"{cond}.pids"
        with log.open("w") as lf:
            self.child = subprocess.Popen([str(PILOT / "run_arm.sh"), arm, tid, domain, MODE[cond], pair, str(slot)], env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
            pids.write_text(str(self.child.pid))
            watch = subprocess.Popen([sys.executable, str(PILOT / "pilot_guard.py"), "watch", str(self.budget_path), str(self.R), str(pids), *self.arms()], env={**env, "PILOT_POLL_S": env.get("PILOT_POLL_S", "10")},
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                rc = self.child.wait(timeout=self.budget["max_episode_minutes"] * 60)
                timed_out = False
            except subprocess.TimeoutExpired:
                os.killpg(self.child.pid, signal.SIGTERM)
                try:
                    rc = self.child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    os.killpg(self.child.pid, signal.SIGKILL)
                    rc = self.child.wait()
                timed_out = True
            finally:
                watch.terminate()
                self.child = None
        text = log.read_text(errors="replace")
        heads = dict(line.split()[1].split("=", 1) for line in text.splitlines() if line.startswith("OGI013_SOURCE "))
        official = ep_dir / "tasks" / tid / "official-result.json"
        status, halt = None, self.R / "PILOT_HALT"
        if "SIM_ROUTE_FAILED:SUPPLY_UNAVAILABLE" in text and not official.exists():
            status = "SUPPLY_UNAVAILABLE"                                                              # no simulator model had an eligible route at block start: not an attempt of the block
        elif "SIM_ROUTE_FAILED" in text and not official.exists():
            status = "SIM_ROUTE_FAILED"
        elif halt.exists():
            why = json.loads(halt.read_text()).get("why", [])
            if why and all(w.startswith(f"arm {arm}") or f"arm {arm} over its cap" in w for w in why):
                shutil.move(str(halt), str(ep_dir / "EPISODE_HALT.json")) if ep_dir.exists() else halt.unlink()
                status = "BUDGET_STOP"                                                             # this episode's own cap: scored non-success, the campaign goes on
            else:
                status = "CAMPAIGN_HALT"
        elif timed_out:
            status = "TIMEOUT"
        elif rc == 0 and official.exists() and "reward_info" in json.loads(official.read_text()):
            status = "DONE"
        elif rc != 0 and self.episode_budget_stop(ep_dir, tid) and not official.exists():
            status = "BUDGET_STOP"                                                                 # per-episode session ceiling / step ceiling stop raised inside the run
        else:
            status = "FAILED_EXEC"
        self.write_rec(ref, cond, status=status, ended_at=time.time(), exit_code=rc, component_heads=heads, official_result=official.exists())
        self.log(f"{ref} {cond} attempt={attempt} {status} exit={rc}")
        return status

    @staticmethod
    def episode_budget_stop(ep_dir: Path, tid: str) -> bool:
        f = ep_dir / "tasks" / tid / "fruitstack-events.jsonl"
        return f.is_file() and any(json.loads(x).get("event") == "BUDGET_STOP" for x in f.read_text().splitlines() if x.strip())

    # ---- blocks --------------------------------------------------------------------------------------------------------------------------------------------------
    def archive(self, t, conds, label):
        dirname = t["task_ref"].replace(":", "_")
        dest = self.C / "discarded" / f"{dirname}-{label}"
        for cond in conds:
            src = self.R / self.a.campaign / dirname / cond
            for suffix in ("", ".log", ".episode.json", "-state", "-slot", ".pids"):
                p = src.with_name(src.name + suffix)
                if p.exists():
                    (dest / dirname).mkdir(parents=True, exist_ok=True)
                    shutil.move(str(p), str(dest / dirname / p.name))
            rec = dest / dirname / f"{cond}.episode.json"
            if rec.exists():
                d = json.loads(rec.read_text())
                d["archived_as"] = label
                rec.write_text(json.dumps(d, indent=1, sort_keys=True))
        return dest

    def supply_gate(self, route: Path) -> bool:
        """A REAL tiny zero-cash completion through PlumMe on allowlisted models until one answers; that model becomes the block's pinned simulator model (supply_gate.py). False = no executable simulator path."""
        if os.environ.get("PILOT_OFFLINE_TRANSPORT"):                                              # offline acceptance (scripted provider transport, refused against the real base): nothing real to probe
            return True
        cr = str(COMPONENTS)
        path = ":".join([str(CODE / "runners"), str(CODE), f"{cr}/CherryMe"] + [f"{cr}/{c}/src" for c in ("PeachMe", "PlumMe", "AppleMe", "MangoMe", "OrangeMe", "PomeloMe")] + [str(self.base / "benchmarks/tau2-bench/src")])
        env = {**os.environ, "PYTHONPATH": path}
        work = self.R / "work.env"
        if work.exists():
            env.update(dict(l.split("=", 1) for l in work.read_text().replace("export ", "").split() if "=" in l))
        return sh(HOSTPY, str(HERE / "supply_gate.py"), str(self.R), str(route), env=env).returncode == 0

    def run_block(self, t) -> str:
        ref, order = t["task_ref"], t["order"]
        dirname = ref.replace(":", "_")
        if (self.C / "discarded" / f"{dirname}-INFRA_INCOMPLETE.txt").exists():
            return "INFRA_INCOMPLETE"
        for attempt in range(len([p for p in (self.C / "discarded").glob(f"{dirname}-attempt*")]) + 1, 4):
            if not any(self.read_rec(ref, c) for c in order):                                           # a fresh block attempt: the simulator model is chosen once and then shared by its conditions
                (self.R / f"{self.a.campaign}-{dirname}.route").unlink(missing_ok=True)
                if not self.supply_gate(self.R / f"{self.a.campaign}-{dirname}.route"):                  # no executable simulator path: nothing is started, no task or attempt is consumed
                    self.log(f"{ref} SUPPLY_UNAVAILABLE (verified: no simulator model answered a real request; block not started, no attempt consumed)")
                    return "SUPPLY_UNAVAILABLE"
            self.log(f"{ref} block attempt={attempt} order={'>'.join(order)}")
            for cond in order:
                rec = self.read_rec(ref, cond)
                if rec and rec.get("status") in DONE_STATES:
                    continue                                                                          # completed work is never repeated
                if rec:                                                                                # RUNNING / interrupted: archive the unfinished directory (its usage stays counted), run afresh
                    self.archive(t, [cond], ("operator-infra" if rec.get("status") == "OPERATOR_TERMINATED_INFRA" else "interrupted") + str(int(time.time())))
                    if not any(self.read_rec(ref, c) for c in order):                                  # nothing of this block survives: the simulator model is chosen afresh
                        (self.R / f"{self.a.campaign}-{dirname}.route").unlink(missing_ok=True)
                if json.loads((self.C / "campaign.json").read_text()).get("halted"):
                    return "HALTED"
                if time.time() - json.loads((self.C / "campaign.json").read_text())["started_at"] > self.budget["cumulative"]["max_wall_minutes"] * 60:
                    self.halt("campaign wall-clock limit")
                    return "HALTED"
                status = self.run_episode(t, cond, attempt)
                if status == "SUPPLY_UNAVAILABLE":
                    self.archive(t, order, f"supply{int(time.time())}")                               # kept as evidence; does not count towards the 3 attempts
                    self.log(f"{ref} SUPPLY_UNAVAILABLE (no eligible simulator route; block deferred, no attempt consumed)")
                    return "SUPPLY_UNAVAILABLE"
                if status == "SIM_ROUTE_FAILED":
                    self.archive(t, order, f"attempt{attempt}")
                    break
                if status == "CAMPAIGN_HALT":
                    self.halt("campaign-level budget limit (see PILOT_HALT)")
                    return "HALTED"
                if status == "FAILED_EXEC":
                    return "FAILED_EXEC"
            else:
                (self.C / dirname / "BLOCK_DONE").write_text(time.strftime("%FT%TZ", time.gmtime()))
                return "DONE"
        (self.C / "discarded").mkdir(exist_ok=True)
        (self.C / "discarded" / f"{dirname}-INFRA_INCOMPLETE.txt").write_text("simulator route failed in 3 attempts; the block is scored non-success\n")
        self.log(f"{ref} INFRA_INCOMPLETE")
        return "INFRA_INCOMPLETE"

    def halt(self, why: str):
        c = json.loads((self.C / "campaign.json").read_text())
        c.update({"halted": True, "halt_reason": why, "halted_at": time.time()})
        (self.C / "campaign.json").write_text(json.dumps(c, indent=1))
        self.log("HALTED " + why)

    # ---- main ----------------------------------------------------------------------------------------------------------------------------------------------------
    def plan(self) -> int:
        print(json.dumps({"campaign": self.a.campaign, "episodes": [{"task": t["task_ref"], "condition": c, "stratum": t["stratum"]} for t in self.manifest["tasks"] for c in t["order"]],
                          "caps": {"per_episode": self.budget["default_arm_cap"], "per_step_tokens": self.budget["max_tokens_per_step"], "cumulative": self.budget["cumulative"]}}, indent=1))
        return 0

    def run(self) -> int:
        refused = self.preconditions()
        if refused:
            return refused
        self.C.mkdir(parents=True, exist_ok=True)
        (self.C / "discarded").mkdir(exist_ok=True)
        cj = self.C / "campaign.json"
        if not cj.exists():
            cj.write_text(json.dumps({"started_at": time.time(), "budget_sha256": hashlib.sha256(self.budget_path.read_bytes()).hexdigest(), "code_head": sh("git", "-C", str(CODE), "rev-parse", "HEAD").stdout.strip()}, indent=1))
        elif json.loads(cj.read_text()).get("halted"):
            return self.refuse("this campaign was halted; a halted campaign is not restarted by itself")
        signal.signal(signal.SIGTERM, self.on_signal)
        signal.signal(signal.SIGINT, self.on_signal)
        tasks = [t for t in self.manifest["tasks"] if not self.a.only or t["task_ref"] in self.a.only.split(",")]
        try:
            queue = list(tasks)
            while queue:
                t = queue.pop(0)
                result = self.run_block(t)
                if result == "SUPPLY_UNAVAILABLE":
                    queue.insert(0, t)                                                                # supply is global: the same block waits at the front; nothing else is consumed
                    time.sleep(SUPPLY_RECHECK_S)
                    continue
                if result == "HALTED":
                    return 3
                if result == "FAILED_EXEC":
                    self.log(f"{t['task_ref']} stopped: an episode failed to execute")
                    return 5
        except Interrupted:
            self.log("INTERRUPTED by signal; unfinished episode archived on the next start")
            return 130
        self.log("CAMPAIGN_DONE")
        sys.path.insert(0, str(HERE))
        import analyze_study
        analyze_study.write_report(self.C, self.manifest, self.budget, self.base / "benchmarks/tau2-bench/data/tau2")
        return 0

    def on_signal(self, signum, frame):
        if self.child is not None:
            try:
                os.killpg(self.child.pid, signal.SIGTERM)
            except OSError:
                pass
        raise Interrupted()


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--approval", default="/nonexistent")
    p.add_argument("--base", default=str(REAL_BASE))
    p.add_argument("--budget", default=str(HERE / "collab1_budget.json"))
    p.add_argument("--manifest", default=str(HERE / "study_manifest_v2.json"))
    p.add_argument("--campaign", default="collab1")
    p.add_argument("--only", default=None, help="comma list of task refs (tests / resumption of named blocks only)")
    p.add_argument("--plan", action="store_true")
    a = p.parse_args(argv)
    c = Campaign(a)
    return c.plan() if a.plan else c.run()


if __name__ == "__main__":
    sys.exit(main())
