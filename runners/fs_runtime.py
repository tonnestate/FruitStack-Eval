#!/usr/bin/env python3
"""FruitStack host entrypoint: configured PEACH-MISSION/1 missions through the installed components (one runtime lifecycle).

MangoMe (WorkIdentity, EXECUTE turn, checkpoints) - OrangeMe (project memory ledgers) - PlumMe (supply, receipts, lineage) - PeachMe (sessions, budgets, governed steps,
ToolGateway, research phase) - CherryMe (RG/2 inquiry, Research Tree, LSD Room, Brother Mode) - AppleMe (assurance, cognitive diagnosis) - PhysalisMe (MCP analyses) -
FruitStack-Eval learning ledger (discovery -> executed verification -> retrieval -> application -> applied-vs-control outcome).

Modes
  offline-fixture  PlumMe runs over a scripted fixture adapter (public plumme.adapters.base.ProviderAdapter, isolated PLUMME_STATE_DIR). Scripted texts are fixed per task and
                   identical in applied and control runs: the honest learning outcome offline is NO_EFFECT_OBSERVED. Not evidence of capability or organizational gain.
  operational      real PlumMe supply (Settings.load() + default adapters). If no eligible route exists, the affected mission is reported as SUPPLY_UNAVAILABLE and never
                   started (no MangoMe/OrangeMe write). There is no simulated fallback.

Success contract (per mission)
  integration_path_ok  every stage executed (required events), no BLOCKED/ERROR, no failed research step, tool receipts for every configured analysis, a MangoMe checkpoint,
                       and - when a check is configured - the executed verifier ran.
  mission_success      run_mission state COMPLETED (settled claims via admissible evidence AND completed mandatory responsibilities) AND every claim SUPPORTED. A claim the
                       executed check contradicts is REFUTED: run_mission settles it (COMPLETED), but the objective has no verified answer, so it is never success.
                       UNRESOLVED is a valid research outcome, never success.
  Executed checks      a task's `check` runs (a) as a CherryMe deterministic tool on the candidate the CLAIM names (ExecutedCheckTool: grounded PASS/CONTRADICT through
                       CherryMe's evidence gate, zero provider calls) and (b) as ResearchPlan.verifier on Brother Mode's candidate (Research Tree `executed` evidence).
                       Same check + same candidate = same evidence id. Without a check, model statements alone never settle a claim.
  Exit code: 0 iff every mission's integration path is ok; 2 if supply was unavailable; 1 otherwise. mission_success never changes the exit code.

Usage: fs_runtime.py --config CONFIG.toml|json OUT_DIR [--mode offline-fixture|operational]
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import subprocess
import sys
import tomllib
import uuid
from pathlib import Path

REQUIRED_EVENTS = ("TASK_ACCEPTED", "TURN_BOUND", "SESSION_OPENED", "BUDGET_CONFIGURED", "CONTEXT_RESTORED", "INQUIRY_EXECUTED", "RESEARCH_STARTED", "LSD_ROOM",
                   "BROTHER_MODE", "COGNITIVE_DIAGNOSIS", "RESEARCH_FINALIZED", "SIGNALS", "KNOWLEDGE_PUBLISHED", "STATE_RETURNED")
FIXTURE_LABEL = "OFFLINE_FIXTURE: scripted provider texts behind the public PlumMe adapter interface; not evidence of capability or organizational gain"


# ---- host-owned executed checks (independent of every model: they run the candidate) ----
def _math_callable(candidate: str):
    name = candidate.strip().strip("`").removesuffix("()")
    mod, _, attr = name.rpartition(".")
    if mod != "math" or not attr.isidentifier() or attr.startswith("_") or not callable(getattr(math, attr, None)):
        raise LookupError(f"{name!r} is not a callable of the standard-library math module")
    return getattr(math, attr)


def _executed(check: str, candidate: str, cases, ok) -> dict:
    """Run the candidate on every case; any wrong result, exception or unknown name CONTRADICTS."""
    try:
        fn = _math_callable(candidate)
        bad = [c for c in cases if not ok(c, fn(*c))]
        summary = f"executed {candidate} on {len(cases)} cases: " + ("all exact" if not bad else f"{len(bad)} wrong, first {bad[0]!r}")
    except Exception as exc:  # noqa: BLE001 - a candidate that cannot run fails the check
        bad, summary = [None], f"executing {candidate!r} failed: {type(exc).__name__}: {str(exc)[:120]}"
    eid = "EXEC-" + hashlib.sha256(f"{check}|{candidate}".encode()).hexdigest()[:16]
    return {"relation": "CONTRADICTS" if bad else "SUPPORTS", "evidence_id": eid, "summary": summary, "source": f"fs_runtime.CHECKS[{check}] (python {sys.version.split()[0]})"}


def exact_isqrt(candidate: str) -> dict:
    cases = [(n,) for n in (0, 1, 2, 3, 4, 15, 16, 17, 10**30 + 7, (10**20 + 1) ** 2, (10**20 + 1) ** 2 - 1)]
    return _executed("exact_isqrt", candidate, cases, lambda c, r: type(r) is int and r * r <= c[0] < (r + 1) ** 2)


def exact_comb(candidate: str) -> dict:
    ref = lambda n, k: math.factorial(n) // (math.factorial(k) * math.factorial(n - k)) if k <= n else 0
    cases = [(5, 2), (10, 0), (10, 10), (60, 30), (200, 73), (3, 5)]
    return _executed("exact_comb", candidate, cases, lambda c, r: type(r) is int and r == ref(*c))


CHECKS = {"exact_isqrt": exact_isqrt, "exact_comb": exact_comb}


class ExecutedCheckTool:
    """The host's executed check offered to CherryMe as a deterministic tool (CherryMe `deterministic_tools`), so it reaches the claim through CherryMe's own evidence gate.
    It applies only to a claim naming exactly one runnable candidate, executes that candidate and returns ONE grounded PASS (SUPPORTS) or CONTRADICT (CONTRADICTS) evidence item
    whose source_ref is the executed check's evidence id. A model's statement never enters here."""
    skills = None

    def __init__(self, name: str, check):
        self.name, self.check = name, check

    def candidate(self, text: str) -> str | None:
        found = set()
        for tok in text.split():
            try:
                _math_callable(tok.strip(".,;:()'\"`"))
                found.add(tok.strip(".,;:()'\"`").removesuffix("()"))
            except LookupError:
                pass
        return found.pop() if len(found) == 1 else None

    def applies(self, claim, node) -> bool:
        return self.candidate(claim.text) is not None

    def run(self, claim, node) -> list:
        from cherryme.models import Evidence, EvidenceVerdict
        res = self.check(self.candidate(claim.text))
        verdict = {"SUPPORTS": EvidenceVerdict.PASS, "CONTRADICTS": EvidenceVerdict.CONTRADICT}[res["relation"]]
        return [Evidence(source_ref=res["evidence_id"], summary=f"{res['summary']} [{res['source']}]", verdict=verdict, grounded=True, independent_group="host-executed-check")]


# ---- configuration ----
def load_config(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    cfg = tomllib.loads(raw) if path.suffix == ".toml" else json.loads(raw)
    cfg["_dir"] = str(path.resolve().parent)
    return cfg


def _path(value: str, base: str | Path) -> Path:
    p = Path(os.path.expandvars(value)).expanduser()
    return p if p.is_absolute() else Path(base) / p


# ---- supply ----
def fixture_service(state_dir: Path, current: dict):
    """PlumMe offline over the public ProviderAdapter interface (PlumMe README 'Offline development with a custom provider adapter'). Three LOCAL routes of distinct lineage."""
    os.environ["PLUMME_STATE_DIR"] = str(state_dir)
    from plumme.adapters.base import AdapterResult, ProviderAdapter
    from plumme.config import Settings
    from plumme.models import CostClass, RouteOffer, Usage
    from plumme.service import PlumMeService

    def respond(prompt: str) -> str:
        """Fixed text per task: the answer of the task the host is running (`current["answer"]`), whatever the prompt contains (a brief cannot change it), so applied and
        control runs get identical texts. Format-correct for each CherryMe contract; the investigator answer is UNKNOWN without evidence because the fixture has no grounded
        source (claims therefore stay unsettled offline)."""
        if '"protocol":"CHERRY-INVESTIGATOR/3"' in prompt:
            return json.dumps({"status_proposal": "UNKNOWN", "evidence": [], "note": "offline fixture: no grounded source available"})
        ans = current.get("answer") or "UNKNOWN"
        if "HYPOTHESIS: <one sentence>" in prompt:
            return f"HYPOTHESIS: {ans} is the call asked for.\nRATIONALE: offline fixture text.\nTEST: execute {ans} on known values."
        if "A colleague proposed this solution" in prompt:
            return "ISSUES: NONE"
        return f"ANSWER: {ans}"

    class FixtureAdapter(ProviderAdapter):
        name = "fixture"
        calls = 0

        async def discover(self, credential=None):
            return [RouteOffer(adapter=self.name, source_id=self.name, provider=f"fixture-{m}", model=f"{m}-1", model_family=m, endpoint="fixture://local",
                               cost_class=CostClass.LOCAL, supports_text_generation=True, context_window=32000) for m in ("alpha", "beta", "gamma")]

        async def execute(self, offer, messages, max_output_tokens, credential):
            FixtureAdapter.calls += 1
            text = respond("\n".join(str(m.get("content", "")) for m in messages))
            return AdapterResult(text=text, usage=Usage(input_tokens=300, output_tokens=60, total_tokens=360), provider_request_id=f"fixture-{FixtureAdapter.calls}",
                                 metadata={"finish_reason": "stop"})

    svc = PlumMeService(Settings.load(), adapters=[FixtureAdapter()])
    asyncio.run(svc.store.discover())
    return svc


def operational_service():
    """Real PlumMe supply. Discovery lists offers only; no inference happens here."""
    from plumme.config import Settings
    from plumme.service import PlumMeService, default_adapters
    settings = Settings.load()
    svc = PlumMeService(settings, adapters=default_adapters(settings))
    asyncio.run(svc.discover())
    return svc


def supply_shortage(svc, n_solvers: int) -> dict | None:
    r = svc.adapter_readiness()
    eligible = sum(e["routes_eligible_now"] for e in r["entries"])
    if not r["discovery_completed"] or eligible < 1:
        return {"code": "SUPPLY_UNAVAILABLE", "eligible_routes": eligible, "adapters": [{k: e[k] for k in ("adapter", "state", "reasons")} for e in r["entries"]],
                "needed": f">=1 eligible route ({n_solvers} distinct lineages for Brother Mode)"}
    return None


# ---- contract ----
def success_contract(record: dict, *, analyses: int, check: bool, receipts: int) -> dict:
    types = [e["type"] for e in record["events"]]
    missing = [t for t in REQUIRED_EVENTS if t not in types]
    if analyses:
        missing += [] if "TOOL_EVIDENCE" in types else ["TOOL_EVIDENCE"]
    if check:
        missing += [] if "CANDIDATE_VERIFIED" in types else ["CANDIDATE_VERIFIED"]
    failed = [e for e in record["events"] if e["type"] in ("RESEARCH_STEP_FAILED", "MISSION_BLOCKED", "MISSION_ERROR", "VERIFIER_FAILED")]
    checkpoint = next((e.get("mangome") or {} for e in record["events"] if e["type"] == "STATE_RETURNED"), {}).get("checkpoint_id")
    steps = types.count("RESEARCH_STEP")
    problems = ([f"missing:{m}" for m in missing] + [f"failed:{e['type']}" for e in failed] + ([] if checkpoint else ["no_mangome_checkpoint"])
                + ([] if receipts >= analyses else [f"tool_receipts:{receipts}<{analyses}"]) + ([] if steps else ["no_research_step"])
                + ([] if record["state"] not in ("BLOCKED", "ERROR") else [f"state:{record['state']}"]))
    answered = bool(record.get("findings")) and all(f["status"] == "SUPPORTED" for f in record["findings"])   # a REFUTED claim settles the mission but answers nothing
    return {"integration_path_ok": not problems, "integration_problems": problems, "mission_success": record["state"] == "COMPLETED" and answered, "mission_state": record["state"],
            "research_steps": steps, "tool_receipts": receipts, "checkpoint_id": checkpoint}


def _git_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    for cmd in (["git", "init", "-q", "-b", "main"], ["git", "config", "user.name", "fs-runtime"], ["git", "config", "user.email", "fs-runtime@example.invalid"]):
        subprocess.run(cmd, cwd=path, check=True)
    (path / "README.md").write_text("ledger\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=path, check=True)
    return str(path)


# ---- runtime ----
def run(cfg: dict, out: Path, mode: str, *, service_factory=None) -> dict:
    """Runs every configured task (plus its control) and returns the summary. `service_factory()` overrides the operational PlumMe service (tests)."""
    if mode not in ("offline-fixture", "operational"):
        raise ValueError(f"unknown mode {mode!r}")
    out.mkdir(parents=True, exist_ok=True)
    base, actor = cfg["_dir"], cfg.get("actor", "fruitstack-runtime")
    tasks, plan_cfg, mcfg = cfg["tasks"], cfg.get("plan", {}), cfg.get("mission", {})
    if backend := cfg.get("mangome", {}).get("backend"):
        os.environ.setdefault("MANGOME_BACKEND", backend)
    if cfg.get("orangeme", {}).get("local_ledger", True):
        os.environ.update({"ORANGEME_HOME": str(out / "orange-home"), "ORANGEME_CHAT_REPO": _git_repo(out / "chat-src"), "ORANGEME_PROJECT_REPO": _git_repo(out / "project-src"),
                           "ORANGEME_ALLOW_LOCAL_LEDGER": "1", "ORANGEME_NO_PUSH": "1", "ORANGEME_AGENT_ID": actor, "ORANGEME_ADMIN_IDS": actor,
                           "ORANGEME_SOURCE_REPO": str(out / "project-src")})
    phys = cfg.get("physalis", {})
    if phys:
        state = _path(phys.get("state_dir", "physalis-state"), out)
        state.mkdir(parents=True, exist_ok=True)
        os.environ.update(PHYSALIS_DATA_DIR=str(_path(phys["data_dir"], base)), PHYSALIS_STATE_DIR=str(state))

    from cherryme.appleme_bridge import connect_appleme
    from cherryme.engine import CherryMeEngine
    from cherryme.knowledge import KnowledgeStore
    from cherryme.models import QuestionType
    from cherryme.orchestrator import ResolutionAwareOrchestrator
    from cherryme.plumme_bridge import connect_plumme
    from cherryme.runtime import responsibility_runtime
    from mangome.runtime import get_service
    from orangeme.runtime import OrangeRuntime
    from peachme import SessionStore
    from peachme.autonomy import StandingAuthority
    from peachme.fruitstack import AppleAssuranceAdapter, CherryBrainAdapter, FruitStackSession, MangoWorkAdapter, OrangeMemoryAdapter
    from peachme.mission import MissionAuthority, MissionRequest, run_mission
    from peachme.plumme import PlumMeProvider
    from peachme.research import ResearchPlan

    from ogi013_learning_hook import LearningHook
    from ogi013_org_discoveries import Ledger
    from ogi013_org_memory import OrangeKnowledgeProjection

    summary: dict = {"mode": FIXTURE_LABEL if mode == "offline-fixture" else "OPERATIONAL: real PlumMe supply", "missions": [], "learning": {}}
    n_solvers = int(plan_cfg.get("n_solvers", 2))
    fixture: dict = {}                                        # offline-fixture: the task currently running
    if mode == "offline-fixture":
        svc = fixture_service(out / "plumme-state", fixture)
    else:
        svc = (service_factory or operational_service)()
    registry = None
    if cfg.get("registry"):
        registry = json.loads(_path(cfg["registry"], base).read_text())
        for server in registry["servers"].values():          # resolve server commands inside the active environment
            local = Path(sys.executable).parent / server["command"]
            if local.exists():
                server["command"] = str(local)
    analyses = tuple((a["server"], a["tool"], a["arguments"], a["relation"]) for a in plan_cfg.get("analyses", ())) if registry else ()
    mango, ort = get_service(), OrangeRuntime()
    learning = Ledger(_path(cfg.get("learning", {}).get("ledger", "learning.jsonl"), out))
    knowledge = KnowledgeStore(_path(cfg.get("learning", {}).get("knowledge", "knowledge.jsonl"), out))
    sig = lambda t: (t or "").rsplit("ANSWER:", 1)[-1].strip() or None if "ANSWER:" in (t or "") else None

    def mission(task: dict, tag: str, apply: bool, capture: bool) -> dict:
        fixture["answer"] = task.get("fixture_answer")
        shortage = supply_shortage(svc, n_solvers)
        if shortage:                                          # checked BEFORE MangoMe/OrangeMe are touched: nothing is entered, nothing is written
            row = {"tag": tag, "task": task["id"], "state": "NOT_STARTED", "error_code": shortage["code"], "shortage": shortage, "integration_path_ok": False,
                   "mission_success": False}
            summary["missions"].append(row)
            return row
        entered = mango.enter_work(workspace_id=f"/fruitstack-runtime/{tag}-{uuid.uuid4().hex[:6]}", workspace_title=f"FruitStack runtime {tag}", actor_id=actor,
                                   request_text=task["objective"])
        work, project = entered["work_identity"]["entity_id"], entered["project"]["project_key"]
        try:
            ort.register_project(project, os.environ["ORANGEME_SOURCE_REPO"], "main", {"vps": os.environ["ORANGEME_SOURCE_REPO"]})
        except Exception:  # noqa: BLE001 - already registered
            pass
        led = ort.project_ledger(project)
        if led.get("memory/working") is None:
            led.put("memory/working", {"verified_findings": []}, expected_revision=0)
        registry_ci, investigator = connect_plumme(service=svc, refresh=True)
        nodes = [{"id": "ANSWER", "mandate": "answer the question and state the claim's status", "skills": ["reasoning"]},
                 {"id": "CHECK", "mandate": "check the claim independently and judge it", "skills": ["falsify"], "function": "VERIFY", "depends_on": ["ANSWER"]}]
        check = CHECKS[task["check"]] if task.get("check") else None
        tools = (ExecutedCheckTool(task["check"], check),) if check else ()      # the executed check reaches the claim through CherryMe's evidence gate (zero provider calls)
        runtime = responsibility_runtime(tools=tools, frame={"responsibility_context": {"responsibilities": nodes}})
        frame = {k: v for k, v in runtime["frame"].items() if k != "responsibility_triage"}
        rdir = out / tag
        assurance = connect_appleme(workspace_root=rdir / "cherry")

        class Falsify:
            def choose(self, claim_, state_features):
                return QuestionType.FALSIFY

        engine = CherryMeEngine(workspace_root=rdir / "cherry", registry=registry_ci, investigator=investigator, assurance_tier=assurance,
                                orchestrator=ResolutionAwareOrchestrator(Falsify()), orchestration_skill=runtime["orchestration_skill"], frame=frame)
        rt = FruitStackSession(SessionStore(rdir / "peachme.sqlite3"), PlumMeProvider(svc), MangoWorkAdapter(mango), OrangeMemoryAdapter(ort), brain=CherryBrainAdapter(engine),
                               assurance=AppleAssuranceAdapter(assurance.service), authorize_model_input=lambda text, view: text)
        authority = MissionAuthority(work_ref=work, project_ref=project, memory_ref="memory/working", actor_id=actor, authorized_by=actor)
        request = MissionRequest(mission_id=f"{tag}-{uuid.uuid4().hex[:6]}", objective=task["objective"], claims=((task["claim"], 0.5),), budget=int(mcfg.get("budget", 2)),
                                 call_budget=int(mcfg.get("call_budget", 10)), session_budget=mcfg.get("session_budget", {"max_calls": 14, "max_tokens": 120000, "max_cost_usd": 1.0}))
        standing = StandingAuthority(work_ref=work, allowed={"READ": ("physalis_*",)}, max_autonomous_effect="READ")
        hook = LearningHook(learning, run_id=request.mission_id, apply=apply, task=task["id"])
        tree_path = rdir / "research_tree.jsonl"
        captured: list = []
        plan = ResearchPlan(worker_budget=plan_cfg.get("worker_budget", {"max_calls": 12, "max_tokens": 60000, "max_cost_usd": 0.5}), lsd=bool(plan_cfg.get("lsd", True)),
                            n_solvers=n_solvers, max_rounds=int(plan_cfg.get("max_rounds", 1)), analyses=analyses, registry=registry, authority=standing,
                            journal_path=str(rdir / "tool_receipts.jsonl"), tree_path=str(tree_path), learning=hook, signature=sig, verifier=check,
                            after=(lambda tree, **_: captured.extend(hook.capture_tree(task["id"], tree, evidence_ref=str(tree_path.relative_to(out))))) if capture else None)
        record = run_mission(rt, authority, request, knowledge_store=knowledge, research=plan)
        (rdir / "mission_record.json").write_text(json.dumps(record, indent=1, default=str))
        receipts_file = rdir / "tool_receipts.jsonl"
        receipts = sum(1 for line in receipts_file.read_text().splitlines() if line.strip()) if receipts_file.exists() else 0
        contract = success_contract(record, analyses=len(analyses), check=check is not None, receipts=receipts)
        verification = (record.get("research") or {}).get("verification") or {}
        row = {"tag": tag, "task": task["id"], "mission_id": request.mission_id, "apply_knowledge": apply, "state": record["state"], "error_code": record["error_code"], **contract,
               "events": [e["type"] for e in record["events"]], "research": record.get("research"), "findings": [{k: f[k] for k in ("claim", "status")} for f in record.get("findings") or []],
               "work_ref": work, "project": project, "captured_discoveries": captured, "knowledge_applied": next((e["discoveries"] for e in record["events"] if e["type"] == "KNOWLEDGE_APPLIED"), []),
               "failures": [e for e in record["events"] if e["type"] in ("RESEARCH_STEP_FAILED", "MISSION_ERROR", "MISSION_BLOCKED", "VERIFIER_FAILED")][:5],
               "_hook": hook, "_candidate": verification.get("candidate")}
        summary["missions"].append(row)
        return row

    def grade(task: dict, row: dict) -> float:
        """The task's executed check, run by the grading side on the mission's candidate. No candidate = 0."""
        return 1.0 if row.get("_candidate") and CHECKS[task["check"]](row["_candidate"])["relation"] == "SUPPORTS" else 0.0

    for task in tasks:
        row = mission(task, task["id"], apply=True, capture=True)
        if task.get("control") and row["state"] != "NOT_STARTED":
            ctl = mission(task, task["id"] + "-control", apply=False, capture=False)
            if ctl["state"] != "NOT_STARTED" and task.get("check"):
                reward, control_reward = grade(task, row), grade(task, ctl)
                outcomes = row["_hook"].outcomes(task["id"], reward=reward, control_reward=control_reward, control_run=ctl["mission_id"], grader="executed")
                summary["learning"].setdefault("outcomes", []).append({"task": task["id"], "run": row["mission_id"], "control_run": ctl["mission_id"], "reward": reward,
                                                                      "control_reward": control_reward, "grader": "executed", "discoveries": outcomes})
    projects = [m["project"] for m in summary["missions"] if m.get("project")]
    if projects:
        summary["learning"]["orange_projected"] = OrangeKnowledgeProjection(ort.project_ledger(projects[-1])).publish(learning)
    summary["learning"]["report"] = learning.report()
    summary["learning"]["events"] = [{k: r.get(k) for k in ("seq", "kind", "id", "origin_run", "run", "task", "verdict", "verifier", "reward", "control_reward")} for r in learning.rows()]
    for m in summary["missions"]:
        m.pop("_hook", None), m.pop("_candidate", None)
    oks = [m["integration_path_ok"] for m in summary["missions"]]
    summary["integration_path_ok"] = bool(oks) and all(oks)
    summary["mission_success"] = {m["tag"]: m["mission_success"] for m in summary["missions"]}
    summary["supply_shortage"] = any(m.get("error_code") == "SUPPLY_UNAVAILABLE" for m in summary["missions"])
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    return summary


def exit_code(summary: dict) -> int:
    return 0 if summary["integration_path_ok"] else 2 if summary["supply_shortage"] else 1


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--config", required=True, type=Path)
    p.add_argument("out", type=Path)
    p.add_argument("--mode", choices=("offline-fixture", "operational"))
    a = p.parse_args(argv)
    cfg = load_config(a.config)
    summary = run(cfg, a.out, a.mode or cfg.get("mode", "offline-fixture"))
    print(json.dumps({k: summary[k] for k in ("mode", "integration_path_ok", "mission_success", "supply_shortage")} | {"learning": summary["learning"].get("report", {}).get("by_state")},
                     indent=1, default=str))
    return exit_code(summary)


if __name__ == "__main__":
    sys.exit(main())
