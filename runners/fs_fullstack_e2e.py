#!/usr/bin/env python3
"""FruitStack full-stack integration run: two missions through ONE runtime lifecycle (PEACH-MISSION/1 + research phase).

Real components: MangoMe (service, InMemoryStore backend: WorkIdentity + EXECUTE turn + checkpoints), OrangeMe (git ledgers in OUT, local, no push), PlumMe (PlumMeService +
scheduler + receipts; lineage exclusion), PeachMe (sessions, budgets, governed steps, autonomy policy, MCP ToolGateway), CherryMe (engine/RG/2 inquiry, Research Tree, LSD Room,
Brother Mode, tool evidence), AppleMe (assurance + cognitive Doctor), PhysalisMe (real MCP server over stdio), FruitStack-Eval learning ledger + OrangeMe projection.
Mode --offline (default): the providers BEHIND PlumMe are scripted (fixed texts); everything else is the real code path. Mode --live: real PlumMe supply (needs owner authorization:
provider calls). Neither mode is scientific evidence about organizational gain: this proves the integrated path runs and records what it did.
Usage: fs_fullstack_e2e.py OUT_DIR [--live]
"""
from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

ACTOR = "fruitstack-e2e"
NUMS = (12, 7, 19, 4)


def respond(task: str) -> str:
    """Scripted provider text for --offline. Format-correct, deliberately unremarkable."""
    if "HYPOTHESIS: <one sentence>" in task:
        return "HYPOTHESIS: The total is 42.\nRATIONALE: 12+7=19, 19+19=38, 38+4=42.\nTEST: recompute the sum by machine."
    if "A colleague proposed this solution" in task:
        return "ISSUES: NONE\nRecomputed: 12+7+19+4 = 42."
    if "A colleague criticised it" in task:
        return "ANSWER: 42"
    if "Solve the task yourself" in task:
        return "12+7+19+4 = 42.\nANSWER: 42"
    return "VERDICT: SUPPORTED\nThe sum of 12, 7, 19 and 4 is 42.\nANSWER: 42"


def scripted_plumme(tmp: Path):
    """The REAL PlumMeService/SwarmScheduler/ReceiptStore over a scripted route adapter (PlumMe's own offline test harness): selection, lineage exclusion, PINNED_MODEL, receipts are PlumMe code."""
    import plumme
    sys.path.insert(0, str(Path(plumme.__file__).resolve().parents[2] / "tests"))
    from plumme.adapters.base import AdapterResult
    from plumme.decisions import DecisionLog
    from plumme.market import cost_policy_classes
    from plumme.models import CostClass, Usage
    from test_v0111_hierarchy import RouteAdapter, offer
    from test_v014_correctness_and_uni import _scheduler, _service

    class Scripted(RouteAdapter):
        executed: list = []

        async def execute(self, route_, messages, max_output_tokens, credential):
            task = "\n".join(str(m.get("content", "")) for m in messages)
            self.executed.append(route_.model_key)
            return AdapterResult(text=respond(task), usage=Usage(input_tokens=300, output_tokens=60, total_tokens=360, cost_usd=None), provider_request_id=f"req-{len(self.executed)}",
                                 metadata={"finish_reason": "stop"})

    adapter = Scripted([offer(m, f"prov-{m.split('-')[0]}", cost=CostClass.FREE_TIER, ctx=32000) for m in ("alpha-1", "beta-1", "gamma-1")])
    sched = _scheduler(tmp, adapter)
    sched.allowed_cost_classes, sched.cost_policy = cost_policy_classes("AUTO"), "AUTO"
    for o in adapter._offers:
        sched.credentials.put(o["provider"], "k")
    sched.decisions = DecisionLog(tmp / "decisions.jsonl")
    svc = _service(sched)
    svc.credentials = sched.credentials
    asyncio.run(sched.store.discover())
    return svc, adapter


def git_repo(path: Path) -> str:
    path.mkdir(parents=True, exist_ok=True)
    for cmd in (["git", "init", "-q", "-b", "main"], ["git", "config", "user.name", "e2e"], ["git", "config", "user.email", "e2e@example.invalid"]):
        subprocess.run(cmd, cwd=path, check=True)
    (path / "README.md").write_text("ledger\n")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=path, check=True)
    return str(path)


def main(out: Path, live: bool) -> int:
    out.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MANGOME_BACKEND", "memory")
    os.environ.update({"ORANGEME_HOME": str(out / "orange-home"), "ORANGEME_CHAT_REPO": git_repo(out / "chat-src"), "ORANGEME_PROJECT_REPO": git_repo(out / "project-src"),
                       "ORANGEME_ALLOW_LOCAL_LEDGER": "1", "ORANGEME_NO_PUSH": "1", "ORANGEME_AGENT_ID": ACTOR, "ORANGEME_ADMIN_IDS": ACTOR,
                       "ORANGEME_SOURCE_REPO": str(out / "project-src")})
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
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ogi013_learning_hook import LearningHook
    from ogi013_org_discoveries import Ledger
    from ogi013_org_memory import OrangeKnowledgeProjection

    if live:
        from plumme.config import Settings
        from plumme.service import PlumMeService, default_adapters
        settings = Settings.load()
        svc = PlumMeService(settings, adapters=default_adapters(settings))
        asyncio.run(svc.discover())
    else:
        svc, _adapter = scripted_plumme(out / "plumme")

    mango = get_service()
    ort = OrangeRuntime()
    learning = Ledger(out / "learning.jsonl")
    registry = json.loads(Path(os.environ.get("PHYSALIS_REGISTRY", "/root/fruits/fsi/PeachMe/examples/physalisme_registry.json")).read_text())
    # PhysalisMe reads only a host-owned dataset directory: here its own synthetic generator (fabricated demonstration data, never evidence about FruitStack)
    phys = Path(os.environ.get("PHYSALIS_REPO", "/root/fruits/fsi/PhysalisMe"))
    (out / "physalis-state").mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(phys / "examples/generate_synthetic.py"), str(out / "physalis-data" / "synthetic_runs.csv")], check=True)
    os.environ.update(PHYSALIS_DATA_DIR=str(out / "physalis-data"), PHYSALIS_STATE_DIR=str(out / "physalis-state"))
    for server in registry["servers"].values():          # host configuration: resolve server commands inside the active environment
        local = Path(sys.executable).parent / server["command"]
        if local.exists():
            server["command"] = str(local)
    summary = {"mode": "LIVE" if live else "OFFLINE_SCRIPTED_PROVIDERS", "missions": []}

    def mission(tag: str, objective: str, claim: str) -> dict:
        entered = mango.enter_work(workspace_id=f"/fruitstack-e2e/{tag}-{uuid.uuid4().hex[:6]}", workspace_title=f"FruitStack e2e {tag}", actor_id=ACTOR, request_text=objective)
        work, project = entered["work_identity"]["entity_id"], entered["project"]["project_key"]
        try:
            ort.register_project(project, os.environ["ORANGEME_SOURCE_REPO"], "main", {"vps": os.environ["ORANGEME_SOURCE_REPO"]})
        except Exception:  # noqa: BLE001 - already registered
            pass
        led = ort.project_ledger(project)
        if led.get("memory/working") is None:
            led.put("memory/working", {"verified_findings": []}, expected_revision=0)
        registry_ci, investigator = connect_plumme(service=svc, refresh=True)
        nodes = [{"id": "SUM", "mandate": "add the numbers and state the total", "skills": ["reasoning"]},
                 {"id": "CHECK", "mandate": "re-compute the total independently and judge the claim", "skills": ["falsify"], "function": "VERIFY", "depends_on": ["SUM"]}]
        runtime = responsibility_runtime(tools=(), frame={"responsibility_context": {"responsibilities": nodes}})
        frame = {k: v for k, v in runtime["frame"].items() if k != "responsibility_triage"}
        assurance = connect_appleme(workspace_root=out / tag / "cherry")

        class Falsify:
            def choose(self, claim_, state_features):
                return QuestionType.FALSIFY

        engine = CherryMeEngine(workspace_root=out / tag / "cherry", registry=registry_ci, investigator=investigator, assurance_tier=assurance,
                                orchestrator=ResolutionAwareOrchestrator(Falsify()), orchestration_skill=runtime["orchestration_skill"], frame=frame)
        rt = FruitStackSession(SessionStore(out / tag / "peachme.sqlite3"), PlumMeProvider(svc), MangoWorkAdapter(mango), OrangeMemoryAdapter(ort), brain=CherryBrainAdapter(engine),
                               assurance=AppleAssuranceAdapter(assurance.service), authorize_model_input=lambda text, view: text)
        authority = MissionAuthority(work_ref=work, project_ref=project, memory_ref="memory/working", actor_id=ACTOR, authorized_by=ACTOR)
        request = MissionRequest(mission_id=f"{tag}-{uuid.uuid4().hex[:6]}", objective=objective, claims=((claim, 0.5),), budget=2, call_budget=10,
                                 session_budget={"max_calls": 14, "max_tokens": 120000, "max_cost_usd": 1.0})
        standing = StandingAuthority(work_ref=work, allowed={"READ": ("physalis_*",)}, max_autonomous_effect="READ")
        hook = LearningHook(learning, run_id=request.mission_id, apply=True)
        plan = ResearchPlan(worker_budget={"max_calls": 12, "max_tokens": 60000, "max_cost_usd": 0.5}, lsd=True, n_solvers=2, max_rounds=1,
                            analyses=(("physalisme", "physalis_analyze", {"dataset_id": "synthetic_runs", "method": "random_forest", "task": "classification", "target": "verified_success",
                                                                          "features": ["complexity", "context_quality", "workers", "tokens"], "group_column": "task_id", "seed": 42}, "SUPPORTS"),),
                            registry=registry, authority=standing, journal_path=str(out / tag / "tool_receipts.jsonl"), tree_path=str(out / tag / "research_tree.jsonl"),
                            learning=hook, signature=lambda t: (t or "").rsplit("ANSWER:", 1)[-1].strip() if "ANSWER:" in (t or "") else None)
        record = run_mission(rt, authority, request, knowledge_store=KnowledgeStore(out / "knowledge.jsonl"), research=plan)
        (out / tag / "mission_record.json").write_text(json.dumps(record, indent=1, default=str))
        types = [e["type"] for e in record["events"]]
        row = {"tag": tag, "state": record["state"], "error_code": record["error_code"], "events": types, "research": record.get("research"),
               "checkpoint": next((e.get("mangome") for e in record["events"] if e["type"] == "STATE_RETURNED"), None), "work_ref": work, "project": project, "mission_id": request.mission_id,
               "failures": [e for e in record["events"] if e["type"] in ("RESEARCH_STEP_FAILED", "MISSION_ERROR", "MISSION_BLOCKED")][:5]}
        summary["missions"].append(row)
        return row

    a = mission("A", "Is the sum of 12, 7, 19 and 4 equal to 42?", "The sum of 12, 7, 19 and 4 equals 42.")
    # episode boundary: a finding of mission A becomes organizational knowledge only through an INDEPENDENT executed check (never the models' agreement)
    did = learning.discover(claim="the sum of 12, 7, 19 and 4 is 42", origin_run=a["mission_id"], origin_task="A", proposer="mission A research consensus",
                            applicability="arithmetic over 12, 7, 19 and 4", evidence_ref=json.dumps(a["checkpoint"], default=str))
    learning.verify(did, verdict="SUPPORTS" if sum(NUMS) == 42 else "CONTRADICTS", verifier="executed", evidence_ref="python sum((12, 7, 19, 4))")
    b = mission("B", "What is the sum of 12, 7, 19, 4 and 10, and is it 52?", "The sum of 12, 7, 19, 4 and 10 equals 52.")
    projected = OrangeKnowledgeProjection(ort.project_ledger(b["project"])).publish(learning)
    summary["learning"] = {"discovery": learning.status(did), "retrieved_in_B": "KNOWLEDGE_APPLIED" in b["events"], "orange_projected": projected}
    print(json.dumps(summary, indent=1, default=str))
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    return 0 if all(m["state"] in ("COMPLETED", "UNRESOLVED") for m in summary["missions"]) else 1


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), "--live" in sys.argv))
