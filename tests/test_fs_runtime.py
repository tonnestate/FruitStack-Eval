"""FruitStack host entrypoint (runners/fs_runtime.py): executed checks, the success contract, operational supply shortage, and one offline-fixture run end to end.
No provider or model call: offline-fixture uses the public PlumMe adapter interface, operational uses an injected PlumMe service without adapters."""
from pathlib import Path

import pytest

import fs_runtime as fr

CONFIG = Path(__file__).resolve().parents[1] / "config" / "fs_runtime" / "offline_fixture.toml"
ENV = ("ORANGEME_HOME", "ORANGEME_CHAT_REPO", "ORANGEME_PROJECT_REPO", "ORANGEME_ALLOW_LOCAL_LEDGER", "ORANGEME_NO_PUSH", "ORANGEME_AGENT_ID", "ORANGEME_ADMIN_IDS",
       "ORANGEME_SOURCE_REPO", "PHYSALIS_DATA_DIR", "PHYSALIS_STATE_DIR", "PLUMME_STATE_DIR")


@pytest.fixture
def env(monkeypatch, tmp_path):
    for k in ENV:                                   # registered with monkeypatch so the run's environment changes are undone
        monkeypatch.setenv(k, "")
    monkeypatch.setenv("MANGOME_BACKEND", "memory")
    monkeypatch.setenv("PLUMME_STATE_DIR", str(tmp_path / "plumme-state"))


def test_executed_checks_run_the_candidate():
    assert fr.exact_isqrt("math.isqrt")["relation"] == "SUPPORTS"
    assert fr.exact_isqrt("math.isqrt()")["relation"] == "SUPPORTS"
    assert fr.exact_isqrt("math.sqrt")["relation"] == "CONTRADICTS"            # float, inexact for large n
    assert fr.exact_comb("math.comb")["relation"] == "SUPPORTS"
    assert fr.exact_comb("math.perm")["relation"] == "CONTRADICTS"
    for unsafe in ("os.system", "__import__", "math.__class__", ""):
        assert fr.exact_isqrt(unsafe)["relation"] == "CONTRADICTS"           # only callables of the math module are ever executed


def _record(state="UNRESOLVED", drop=(), extra=(), statuses=("SUPPORTED",), verdict="SUPPORTS"):
    events = [{"type": t} for t in fr.REQUIRED_EVENTS + ("TOOL_EVIDENCE", "CANDIDATE_VERIFIED", "RESEARCH_STEP") if t not in drop] + [{"type": t} for t in extra]
    for e in events:
        if e["type"] == "STATE_RETURNED":
            e["mangome"] = {"checkpoint_id": "CP-1"}
        if e["type"] == "CANDIDATE_VERIFIED":
            e["relation"] = verdict                  # PeachMe research.py emits the verifier verdict as `relation`
    return {"state": state, "events": events, "findings": [{"status": s} for s in statuses]}


def test_unresolved_is_a_valid_integration_path_but_never_success():
    c = fr.success_contract(_record("UNRESOLVED"), analyses=1, check=True, receipts=1)
    assert c["integration_path_ok"] and not c["mission_success"]
    assert fr.success_contract(_record("COMPLETED"), analyses=1, check=True, receipts=1)["mission_success"]
    assert not fr.success_contract(_record("COMPLETED", statuses=("REFUTED",)), analyses=1, check=True, receipts=1)["mission_success"]   # settled, but no verified answer
    assert not fr.success_contract(_record("COMPLETED", statuses=()), analyses=1, check=True, receipts=1)["mission_success"]


def test_mission_success_requires_the_workers_candidate_verified_supports():
    # all findings SUPPORTED, but the workers' candidate answer was CONTRADICTED by the verifier: not a success
    wrong = fr.success_contract(_record("COMPLETED", verdict="CONTRADICTS"), analyses=1, check=True, receipts=1)
    assert wrong["candidate_verdict"] == "CONTRADICTS" and not wrong["mission_success"]
    right = fr.success_contract(_record("COMPLETED", verdict="SUPPORTS"), analyses=1, check=True, receipts=1)
    assert right["candidate_verdict"] == "SUPPORTS" and right["mission_success"]


def test_executed_check_tool_runs_the_candidate_the_claim_names():
    from types import SimpleNamespace as NS
    from cherryme.models import EvidenceVerdict
    tool = fr.ExecutedCheckTool("exact_isqrt", fr.exact_isqrt)
    good, bad = NS(text="math.isqrt computes the exact integer square root."), NS(text="math.sqrt computes the exact integer square root.")
    assert tool.applies(good, {}) and tool.applies(bad, {})
    (e,) = tool.run(good, {})
    assert (e.verdict, e.grounded, e.source_ref) == (EvidenceVerdict.PASS, True, fr.exact_isqrt("math.isqrt")["evidence_id"])
    assert [x.verdict for x in tool.run(bad, {})] == [EvidenceVerdict.CONTRADICT]
    for vague in ("The square root is computed exactly.", "math.isqrt or math.sqrt computes it.", "os.system computes it."):
        assert not tool.applies(NS(text=vague), {})                          # no candidate (or no single one): the check does not apply, nothing is invented


@pytest.mark.parametrize("record,receipts,problem", [
    (_record(drop=("STATE_RETURNED",)), 1, "missing:STATE_RETURNED"),
    (_record(drop=("CANDIDATE_VERIFIED",)), 1, "missing:CANDIDATE_VERIFIED"),
    (_record(extra=("RESEARCH_STEP_FAILED",)), 1, "failed:RESEARCH_STEP_FAILED"),
    (_record(), 0, "tool_receipts:0<1"),
    (_record("ERROR"), 1, "state:ERROR"),
])
def test_a_broken_integration_path_is_never_converted_into_success(record, receipts, problem):
    c = fr.success_contract(record, analyses=1, check=True, receipts=receipts)
    assert not c["integration_path_ok"] and problem in c["integration_problems"]


def test_operational_without_supply_reports_the_shortage_and_starts_no_mission(env, tmp_path):
    from plumme.config import Settings
    from plumme.service import PlumMeService

    def no_supply():
        svc = PlumMeService(Settings.load(), adapters=[])
        import asyncio
        asyncio.run(svc.discover())
        return svc
    summary = fr.run(fr.load_config(CONFIG), tmp_path / "out", "operational", service_factory=no_supply)
    assert [m["state"] for m in summary["missions"]] == ["NOT_STARTED", "NOT_STARTED"]
    assert all(m["error_code"] == "SUPPLY_UNAVAILABLE" and "work_ref" not in m for m in summary["missions"])
    assert fr.exit_code(summary) == 2 and not summary["integration_path_ok"]
    assert summary["learning"]["report"]["discoveries"] == 0 and "orange_projected" not in summary["learning"]
    assert not (tmp_path / "out" / "A").exists()


def test_offline_fixture_end_to_end_learning_lifecycle_without_scripted_benefit(env, tmp_path):
    summary = fr.run(fr.load_config(CONFIG), tmp_path / "out", "offline-fixture")
    assert summary["mode"].startswith("OFFLINE_FIXTURE")
    assert [m["tag"] for m in summary["missions"]] == ["A", "B", "B-control"]
    assert summary["integration_path_ok"], [m["integration_problems"] for m in summary["missions"]]
    assert fr.exit_code(summary) == 0
    a, b, ctl = summary["missions"]
    # the executed check reaches the claim through CherryMe's evidence gate: verified candidate -> COMPLETED through the real run_mission lifecycle
    assert [(m["state"], m["mission_success"], [f["status"] for f in m["findings"]]) for m in summary["missions"]] == [("COMPLETED", True, ["SUPPORTED"])] * 3
    rec = __import__("json").loads((tmp_path / "out" / "A" / "mission_record.json").read_text())
    assert [e["source_ref"] for e in rec["findings"][0]["evidence"]] == [rec["research"]["verification"]["evidence_id"]]    # same executed check, same evidence id
    rows = summary["learning"]["events"]
    assert [r["kind"] for r in rows if r["kind"] != "DISCOVERY" and r["kind"] != "VERIFICATION"] == ["RETRIEVAL", "APPLICATION", "OUTCOME"]
    assert {r["task"] for r in rows if r["kind"] in ("RETRIEVAL", "APPLICATION", "OUTCOME")} == {"B"}          # the host task id, not the mission id
    assert a["captured_discoveries"] and b["knowledge_applied"] == a["captured_discoveries"] and ctl["knowledge_applied"] == []
    states = summary["learning"]["report"]["by_state"]
    assert states.get("NO_EFFECT_OBSERVED") == 1 and "BENEFIT_OBSERVED" not in states
    out = summary["learning"]["outcomes"][0]
    assert out["reward"] == out["control_reward"] and out["grader"] == "executed"


def test_contradicted_candidate_is_never_success_and_without_a_check_model_claims_settle_nothing(env, tmp_path):
    cfg = fr.load_config(CONFIG)
    a = cfg["tasks"][0]
    cfg["tasks"] = [dict(a, id="W", claim="math.sqrt computes the exact integer square root of a non-negative integer.", fixture_answer="math.sqrt"),
                    {k: v for k, v in a.items() if k != "check"} | {"id": "N"}]
    summary = fr.run(cfg, tmp_path / "out", "offline-fixture")
    w, n = summary["missions"]
    assert w["integration_path_ok"] and not w["mission_success"] and [f["status"] for f in w["findings"]] == ["REFUTED"]
    assert w["research"]["verification"]["relation"] == "CONTRADICTS" and w["research"]["verification"]["status"] == "FALSIFIED"
    assert (n["state"], n["mission_success"], [f["status"] for f in n["findings"]]) == ("UNRESOLVED", False, ["UNKNOWN"])   # no check + UNKNOWN investigator


# ---- live defect 2026-11-07: one unsuitable worker, then an unconfirmed timeout, locked the whole mission (no candidate, no success) ----
def _scripted_service(families, fixture_answer="math.isqrt"):
    """Operational supply over the public PlumMe adapter interface, scripted per lineage: `dots` returns no content (reasoning ate the output budget), `qwen` times out,
    every other lineage answers like the offline fixture. No provider call."""
    import asyncio
    import json

    from plumme.adapters.base import AdapterError, AdapterResult, ProviderAdapter
    from plumme.config import Settings
    from plumme.models import AuthMode, CostClass, RouteOffer, Usage
    from plumme.service import PlumMeService

    def respond(prompt):
        if '"protocol":"CHERRY-INVESTIGATOR/3"' in prompt:
            return json.dumps({"status_proposal": "UNKNOWN", "evidence": [], "note": "scripted: no grounded source"})
        if "HYPOTHESIS: <one sentence>" in prompt:
            return f"HYPOTHESIS: {fixture_answer} is the call asked for.\nRATIONALE: scripted.\nTEST: execute {fixture_answer} on known values."
        if "A colleague proposed this solution" in prompt:
            return "ISSUES: NONE"
        return f"ANSWER: {fixture_answer}"

    class Scripted(ProviderAdapter):
        name = "scripted"
        priority = 1
        calls: list = []

        async def discover(self, credential=None):
            return [RouteOffer(adapter="scripted", provider=f"{i}-{fam}", model=f"{fam}-1", model_family=fam, endpoint="scripted://local", supports_text_generation=True,
                               executable=True, auth_mode=AuthMode.KEYLESS, cost_class=CostClass.FREE_TIER, input_cost_per_million=0.0, output_cost_per_million=0.0,
                               context_window=32000) for i, fam in enumerate(families)]

        async def execute(self, offer, messages, max_output_tokens, credential):
            Scripted.calls.append(offer.model)
            if offer.model_family == "dots":
                raise AdapterError("SEMANTIC_OUTPUT_FAILURE", "EMPTY_CONTENT finish_reason=length reasoning_present=True",
                                   usage=Usage(input_tokens=200, output_tokens=2000, total_tokens=2200, cost_usd=0.0), metadata={"finish_reason": "length"})
            if offer.model_family == "qwen":
                raise AdapterError("TIMEOUT", "")
            text = respond("\n".join(str(m.get("content", "")) for m in messages))
            return AdapterResult(text=text, usage=Usage(input_tokens=300, output_tokens=60, total_tokens=360, cost_usd=0.0), provider_request_id=f"s{len(Scripted.calls)}")

    def factory():
        svc = PlumMeService(Settings.load(), adapters=[Scripted()])
        asyncio.run(svc.discover())
        svc.scripted_calls = Scripted.calls
        return svc
    return factory


def test_an_unsuitable_worker_and_an_unconfirmed_free_timeout_are_replaced_and_the_mission_still_verifies_its_candidate(env, tmp_path, monkeypatch):
    monkeypatch.setenv("PLUMME_SELECTION_SPREAD", "0")             # deterministic: the scripted bad lineages are leased first, as in the live run
    cfg = fr.load_config(CONFIG)
    cfg["tasks"] = cfg["tasks"][:1]
    made = []
    factory = _scripted_service(("dots", "qwen", "gpt", "mistral"))
    summary = fr.run(cfg, tmp_path / "out", "operational", service_factory=lambda: made.append(factory()) or made[-1])
    (a,) = summary["missions"]
    assert a["mission_success"] and a["candidate_verdict"] == "SUPPORTS", (a["integration_problems"], a.get("failures"))
    assert a["integration_path_ok"], a["integration_problems"]
    calls = made[0].scripted_calls
    assert calls.count("qwen-1") <= 1                                # an unconfirmed execution is never replayed
    lineages = [w["lineage"] for w in a["research"]["workers"]]
    assert {"gpt", "mistral"} <= set(lineages)                        # n_solvers = 2 distinct qualified lineages after the failed ones were retired
    assert a["worker_failures_recovered"] >= 1


def test_operational_supply_needs_n_solvers_distinct_qualified_lineages(env, tmp_path):
    cfg = fr.load_config(CONFIG)
    cfg["tasks"] = cfg["tasks"][:1]
    summary = fr.run(cfg, tmp_path / "out", "operational", service_factory=_scripted_service(("gpt",)))
    (a,) = summary["missions"]
    assert (a["state"], a["error_code"]) == ("NOT_STARTED", "SUPPLY_UNAVAILABLE")
    assert a["shortage"]["qualified_lineages"] == 1 and a["shortage"]["shortfall"] == 1 and "work_ref" not in a
    assert fr.exit_code(summary) == 2


# ---- review findings on PR #15: "recovered" needs a replacement's success in the same stage; uncertain spend on a route that can bill is never recovered ----
def _with(*evs):
    rec = _record()
    rec["events"] += [dict(e) for e in evs]
    return fr.success_contract(rec, analyses=0, check=False, receipts=0)


FAIL = {"type": "RESEARCH_STEP_FAILED", "stage": "solve", "error_code": "EXECUTION_OUTPUT_UNUSABLE_SEMANTIC_OUTPUT_FAILURE"}
RETIRED = {"type": "RESEARCH_WORKER_RETIRED", "lineage": "dots", "reason": "EXECUTION_OUTPUT_UNUSABLE_SEMANTIC_OUTPUT_FAILURE"}


def test_a_failure_is_recovered_only_by_a_replacement_success_in_the_same_stage():
    ok = _with(FAIL, RETIRED, {"type": "RESEARCH_STEP", "stage": "solve", "lineage": "gpt", "success": True})
    assert ok["integration_path_ok"] and ok["worker_failures_recovered"] == 1
    for later in ({"type": "RESEARCH_STEP", "stage": "challenge", "lineage": "gpt", "success": True},      # other stage
                  {"type": "RESEARCH_STEP", "stage": "solve", "lineage": "gpt", "success": False},         # replacement failed too
                  {"type": "RESEARCH_STEP", "stage": "solve", "lineage": "dots", "success": True}):        # not a replacement
        c = _with(FAIL, RETIRED, later)
        assert not c["integration_path_ok"] and c["worker_failures_recovered"] == 0, later
    assert not _with(FAIL, RETIRED)["integration_path_ok"]
    lsd = {**FAIL, "stage": "lsd:psychedelic_researcher"}                                               # LSD personas are one stage: another persona's success recovers it
    assert _with(lsd, RETIRED, {"type": "RESEARCH_STEP", "stage": "lsd:worst_mathematician", "lineage": "gpt", "success": True})["integration_path_ok"]


def test_uncertain_spend_on_a_route_that_can_bill_is_never_recovered():
    replaced = ({"type": "RESEARCH_WORKER_RETIRED", "lineage": "qwen"}, {"type": "RESEARCH_STEP", "stage": "solve", "lineage": "gpt", "success": True})
    unsettled = {"type": "RESEARCH_STEP_FAILED", "stage": "solve", "error_code": "EXECUTION_NOT_CONFIRMED_TIMEOUT"}
    assert not _with(unsettled, *replaced)["integration_path_ok"]
    settled = {**unsettled, "settled": "ZERO_CHARGE_CLASS"}                                             # PeachMe settled it under the egress-route cost-class rule
    assert _with(settled, *replaced)["integration_path_ok"]
    halted = _with({"type": "RESEARCH_STEP_FAILED", "stage": "solve", "error_code": "UNCERTAIN_CHARGEABLE"}, {"type": "RESEARCH_HALTED", "reason": "UNCERTAIN_CHARGEABLE"})
    assert not halted["integration_path_ok"] and "failed:RESEARCH_HALTED" in halted["integration_problems"]


def test_supply_check_reads_the_same_effective_worker_budget_as_the_plan(env, tmp_path):
    seen = []

    class Svc:
        def adapter_readiness(self):
            return {"discovery_completed": True, "entries": []}

        def workforce_supply(self, role, count, max_cost_usd=None):
            seen.append(max_cost_usd)
            return {"qualified": 0, "proven": 0, "lineages": {}}

    cfg = fr.load_config(CONFIG)
    cfg["tasks"] = cfg["tasks"][:1]
    cfg.setdefault("plan", {}).pop("worker_budget", None)
    fr.run(cfg, tmp_path / "out", "operational", service_factory=Svc)
    assert seen == [fr.DEFAULT_WORKER_BUDGET["max_cost_usd"]]
