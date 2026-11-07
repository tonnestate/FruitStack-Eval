"""AMENDMENT-1 regression tests (offline, no model calls): atomic provenance propositions, host excerpt windows, the real EvidenceVerifier with scripted judges,
and the trace report's mapping of verifier evidence. ALL DATA IN THIS FILE IS SYNTHETIC.

Run: cd /root/fruits/integration/ogi013-org && PYTHONPATH=runners:.:<components> /root/fruits/integration/ogi013-hostpython-org/bin/python -m pytest -q tests/test_ogi013_measurement_amendment.py
"""
import asyncio
import hashlib
import json

import pytest

from ogi013_org_bridge import ATOM_WINDOW, atom_sources, atomic_values
from rg2_trace_report import build_report

cherryme = pytest.importorskip("cherryme")
from cherryme.host_grounding import HostGrounding  # noqa: E402
from cherryme.models import Question, QuestionType  # noqa: E402
from cherryme.verification import EvidenceVerifier, WorkerReply  # noqa: E402


# ---------- atomic propositions -------------------------------------------------------------------------------------------------------------------------------

def test_tool_call_yields_identifier_atoms_only_and_is_capped():
    action = {"action": "tool", "name": "cancel_reservation", "arguments": {"reservation_id": "SDZQKO", "reason": "change of plans", "flag": True, "amount": 1234, "x": "ab"}}
    atoms = atomic_values(action)
    assert [a["value"] for a in atoms] == ["SDZQKO", "1234"]               # words, booleans and short tokens are not provenance claims; two atoms at most
    assert atoms[0]["label"] == "cancel_reservation.reservation_id" and atoms[0]["kind"] == "tool_argument"


def test_reply_yields_ids_dates_and_amounts():
    atoms = atomic_values({"action": "message", "content": "Your reservation 4OG6T3 departs on 2024-05-17; the fee is $45.50."})
    assert [a["value"] for a in atoms] == ["4OG6T3", "2024-05-17"]
    assert atomic_values({"action": "message", "content": "Hello, how can I help?"}) == []


# ---------- host excerpt windows ------------------------------------------------------------------------------------------------------------------------------

def test_atom_sources_are_hash_bound_windows_around_the_value():
    user = "USER: my booking is SDZQKO please check it"
    tool = "TOOL RESULT: reservation SDZQKO status confirmed " + "x" * 5000
    sources = atom_sources("2", 0, "SDZQKO", user, tool)
    assert [s.source_group for s in sources] == ["customer", "system-data"]
    for s in sources:
        assert "SDZQKO" in s.excerpt and len(s.excerpt) <= 2 * ATOM_WINDOW + len("SDZQKO")
        assert s.excerpt_sha256 == hashlib.sha256(s.excerpt.encode()).hexdigest()
    assert len({s.source_ref for s in sources}) == 2


def test_unsupported_value_gets_a_tail_source_without_the_value():
    sources = atom_sources("2", 1, "ZZZZZZ", "USER: hello", "TOOL RESULT: reservation SDZQKO")
    assert len(sources) == 1 and "ZZZZZZ" not in sources[0].excerpt


# ---------- the real EvidenceVerifier with scripted judges ----------------------------------------------------------------------------------------------------

def _verify(claim_text: str, sources, judges):
    """judges: list of (independence_key, model_key, reply_json) handed out in order; None = no worker available."""
    queue = list(judges)

    async def run_worker(prompt, excluded):
        while queue:
            item = queue.pop(0)
            if item is None:
                return None
            key, model, reply = item
            if key in excluded:
                continue
            return WorkerReply(text=json.dumps(reply), independence_key=key, model_key=model, receipt_id=f"r-{model}")
        return None

    verifier = EvidenceVerifier(run_worker, claim_lookup=lambda cid: claim_text)
    question = Question(claim_id="C-1", type=QuestionType.SCIENCE, text="q", cognitive_packet={})
    grounding = HostGrounding(question_id=question.id, sources=tuple(sources), search_backend="tau2-environment", corpus_family="t")
    evidence = asyncio.run(verifier.verify(question, grounding))
    return verifier, evidence


ATOM_CLAIM = "The value SDZQKO given as 'cancel_reservation.reservation_id' of the assistant's tool call appears in what the customer said or in a system tool result of this conversation."


def _atom_sources_for_test():
    return atom_sources("2", 0, "SDZQKO", "USER: my booking is SDZQKO please check it", "TOOL RESULT: reservation SDZQKO status confirmed")


def test_genuine_atomic_claim_is_promoted_by_two_independent_judges():
    srcs = _atom_sources_for_test()
    quote = {"relation": "SUPPORTS", "quote": "my booking is SDZQKO please check it"}
    quote2 = {"relation": "SUPPORTS", "quote": "reservation SDZQKO status confirmed"}
    verifier, evidence = _verify(ATOM_CLAIM, srcs[:1], [("lineage-a", "model-a", quote), ("lineage-b", "model-b", quote)])
    assert verifier.log[0]["promoted"] is True and verifier.log[0]["reason"] == "PROMOTED"
    assert evidence[0].verdict.value == "PASS"
    rows = verifier.ledger.for_claim("C-1")
    assert {(r.kind, r.verdict, r.epistemic_status, r.disposition) for r in rows} == {("VERIFIER", "SUPPORTS", "VERIFIED", "ACCEPTED")}
    assert {r.identity["independence_key"] for r in rows} == {"lineage-a", "lineage-b"}
    _ = quote2


def test_unsupported_claims_are_rejected():
    srcs = atom_sources("2", 0, "ZZZZZZ", "USER: hello", "TOOL RESULT: reservation SDZQKO")          # value absent everywhere
    claim = ATOM_CLAIM.replace("SDZQKO", "ZZZZZZ")
    honest = {"relation": "NOT_ADDRESSED", "quote": "reservation SDZQKO"}
    verifier, evidence = _verify(claim, srcs, [("lineage-a", "a", honest), ("lineage-b", "b", honest)])
    assert not verifier.log[0]["promoted"] and evidence[0].verdict.value == "INFO"
    # dishonest judges: SUPPORTS with a quote that is not verbatim in the excerpt is not accepted either
    fake = {"relation": "SUPPORTS", "quote": "the value ZZZZZZ was stated by the customer"}
    verifier, evidence = _verify(claim, srcs, [("lineage-a", "a", fake), ("lineage-b", "b", fake)])
    assert not verifier.log[0]["promoted"] and evidence[0].verdict.value == "INFO"


def test_single_judge_or_one_lineage_never_promotes():
    srcs = _atom_sources_for_test()[:1]
    good = {"relation": "SUPPORTS", "quote": "my booking is SDZQKO please check it"}
    verifier, evidence = _verify(ATOM_CLAIM, srcs, [("lineage-a", "a", good), None])
    assert not verifier.log[0]["promoted"] and verifier.log[0]["reason"] == "VERIFIER_WORKER_MISSING"
    verifier, evidence = _verify(ATOM_CLAIM, srcs, [("lineage-a", "a", good), ("lineage-a", "a2", good)])   # same lineage twice: the second is not accepted as independent
    assert not verifier.log[0]["promoted"]


def test_documented_defect_compound_claim_cannot_be_promoted_by_a_policy_chunk():
    """The original decision claim (whole reply/tool call with ids) against a policy chunk: even two honest SUPPORTS judges cannot promote it, because the ids are not in the quote."""
    compound = "The assistant's tool call cancel_reservation({\"reservation_id\": \"4OG6T3\", \"refund\": 250}) follows the policy and is justified by the customer's request and the observed system data."
    policy = type("S", (), {})
    srcs = atom_sources("2", 0, "SDZQKO", "USER: x", "TOOL RESULT: y")[:0]
    from cherryme.host_grounding import RetrievedSource
    text = "Reservations can be cancelled within 24 hours of booking. The agent must confirm the reservation id before cancelling."
    digest = hashlib.sha256(text.encode()).hexdigest()
    srcs = [RetrievedSource(source_ref="https://tau2-environment.invalid/2/policy/0", excerpt=text, excerpt_sha256=digest, retrieval_receipt_id="tau2-env:p", source_group="policy")]
    reply = {"relation": "SUPPORTS", "quote": "Reservations can be cancelled within 24 hours of booking."}
    verifier, _ = _verify(compound, srcs, [("lineage-a", "a", reply), ("lineage-b", "b", reply)])
    assert not verifier.log[0]["promoted"] and verifier.log[0]["reason"] in ("PARTIAL_SUPPORT_VALUE_MISSING", "IDENTIFIER_NOT_IN_SOURCE")
    _ = policy


# ---------- trace report mapping --------------------------------------------------------------------------------------------------------------------------------

def _write(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")


def _vrow(claim, verdict, status, disposition, key, ref="https://tau2-environment.invalid/2/atom0/customer"):
    return {"claim_id": claim, "kind": "VERIFIER", "worker": key, "verdict": verdict, "epistemic_status": status, "disposition": disposition,
            "evidence_refs": [ref], "identity": {"model_key": key, "independence_key": key}}


def _run(tmp_path, rows, other_task_claims=(), closed_revisions=None):
    run = tmp_path / "run"
    _write(run / "tasks" / "2" / "fruitstack-events.jsonl", [
        {"event": "EPISODE_OPENED", "task": "2"},
        {"event": "ORG_DECISION", "claim": "C-1", "action": "cancel_reservation", "status": "UNKNOWN", "atoms": [{"claim": "A-1", "value": "SDZQKO"}]},
        *([{"event": "EPISODE_CLOSED", "reason": "TASK_ENDED", "stats": {"revisions": closed_revisions}}] if closed_revisions is not None else [])])
    (run / "tasks" / "2" / "official-result.json").write_text(json.dumps({"reward_info": {"reward": 1.0}}))
    state = tmp_path / "state"
    _write(state / "contributions.jsonl", [{"claim_id": "C-1", "kind": "PROPOSAL", "worker": "m", "verdict": "UNKNOWN", "epistemic_status": "UNVERIFIED", "disposition": "RETAINED_UNVERIFIED"}, *rows])
    _write(state / "events.jsonl", [])
    return build_report(run, state)


def test_report_detects_quorum_promoted_verification(tmp_path):
    rep = _run(tmp_path, [_vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-a"), _vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-b")])
    v = rep["verdict"]
    assert v["worker_contribution"] is True and v["independent_verification"] is True and v["organisational_success"] is not True   # verification alone never establishes success (ERRATUM-1)


def test_report_rejects_unpromoted_judgments(tmp_path):
    not_addressed = [_vrow("A-1", "NOT_ADDRESSED", "SOURCE_BACKED", "REJECTED", "lineage-a"), _vrow("A-1", "NOT_ADDRESSED", "SOURCE_BACKED", "REJECTED", "lineage-b")]
    assert _run(tmp_path, not_addressed)["verdict"]["independent_verification"] is False
    single = [_vrow("A-1", "SUPPORTS", "SOURCE_BACKED", "DEFERRED", "lineage-a"), _vrow("A-1", "NOT_ADDRESSED", "SOURCE_BACKED", "REJECTED", "lineage-b")]
    assert _run(tmp_path / "b", single)["verdict"]["independent_verification"] is False


def test_report_requires_distinct_independence_keys(tmp_path):
    same = [_vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-a"), _vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-a")]
    rep = _run(tmp_path, same)
    assert rep["verdict"]["independent_verification"] is False and rep["verdict"]["organisational_success"] is not True


def test_report_ignores_claims_of_other_runs_in_the_shared_state(tmp_path):
    foreign = [_vrow("A-OTHER", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-a"), _vrow("A-OTHER", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-b")]
    rep = _run(tmp_path, foreign)
    assert rep["verdict"]["independent_verification"] is None          # none of this run's claims was judged


def test_report_accepts_the_legacy_labels(tmp_path):
    legacy = [_vrow("A-1", "CONTRADICTS", "VERIFIED", "ACCEPTED", "lineage-a"), _vrow("A-1", "CONTRADICTS", "VERIFIED", "ACCEPTED", "lineage-b")]
    assert _run(tmp_path, legacy)["verdict"]["independent_verification"] is True


# ---------- simulator cooldown logic (infrastructure; offline, fake service objects) -------------------------------------------------------------------------

def test_earliest_retry_uses_plumme_gate_and_cooldown_state():
    import sys
    import types
    from ogi013_sim_supply import _earliest_retry
    sys.modules.setdefault("plumme.models", types.SimpleNamespace(ExecutionRequest=lambda **kw: types.SimpleNamespace(**kw)))

    def offer(key, health="AVAILABLE", name=None):
        return types.SimpleNamespace(model_key=key, health=health, name=name or key)

    class Sched:
        def __init__(self, eligible_names, waits):
            self.eligible_names, self.waits = eligible_names, waits

        def screen(self, request):
            return [o for o in self.offers if o.name in self.eligible_names], {}

        def availability(self, o):
            return {"retry_after_seconds": self.waits.get(o.name)}

    def svc(offers, eligible_names=(), waits=None):
        sched = Sched(set(eligible_names), waits or {})
        sched.offers = offers
        return types.SimpleNamespace(store=types.SimpleNamespace(offers=dict(enumerate(offers))), scheduler=sched)

    assert _earliest_retry(svc([offer("a"), offer("b")], ["b"], {"a": 30.0}), ["a", "b"]) == 0.0           # b passes the hard gate now: rotate, do not wait
    assert _earliest_retry(svc([offer("a"), offer("b")], [], {"a": 30.0, "b": 120.0}), ["a", "b"]) == 30.0   # nothing eligible: the shortest known window
    assert _earliest_retry(svc([offer("a", name="a-cooling"), offer("a", name="a-nocred")], [], {"a-cooling": 598.0}), "a") == 598.0   # an offer with no credential does not count as available
    assert _earliest_retry(svc([offer("a")], [], {}), "a") is None                                        # no known recovery time
    assert _earliest_retry(svc([offer("a")], [], {"a": 9000.0}), "a") == 9000.0                           # daily-quota style window: the caller fails the block


def test_selection_pool_without_exhausted_credentials_is_the_whole_allowlist_and_old_windows_exclude_nothing(tmp_path):
    from ogi013_sim_supply import _selection_pool
    (tmp_path / "sim_allowlist.json").write_text(json.dumps({"model_keys": ["b", "a", "c"]}))
    (tmp_path / "sim_exhausted.jsonl").write_text(json.dumps({"ts": 1, "model_key": "a", "until": 9e12}) + "\n")      # evidence only: no time-based exclusion
    assert _selection_pool(tmp_path) == ["a", "b", "c"]


# ---------- worker roster refresh and verifier log tagging (offline, fakes) ---------------------------------------------------------------------------------

def _bridge(tmp_path, live_models):
    import types
    from dataclasses import dataclass
    from ogi013_org_bridge import OrgBridge

    @dataclass(frozen=True)
    class Card:
        id: str
        model_key: str
        enabled: bool = True

    offers = [types.SimpleNamespace(model_key=m) for m in live_models]
    scheduler = types.SimpleNamespace(screen=lambda request: (offers, {}))
    stack = types.SimpleNamespace(svc=types.SimpleNamespace(scheduler=scheduler))
    bridge = OrgBridge(stack, "sid", "2", "policy", tmp_path)
    bridge._base_cards = {k: Card(k, k) for k in ("a@default", "b@default", "c@default")}
    bridge._sim_key = "c@default"
    registry = types.SimpleNamespace(_agents=dict(bridge._base_cards))
    return bridge, registry, scheduler, offers


def test_worker_roster_follows_plumme_eligibility_and_excludes_the_simulator_model(tmp_path):
    bridge, registry, scheduler, offers = _bridge(tmp_path, ["a@default", "c@default"])
    bridge._restrict_to_executable(registry)
    assert {k for k, c in registry._agents.items() if c.enabled} == {"a@default"}          # b is not executable, c is the simulator's model
    import types
    offers[:] = [types.SimpleNamespace(model_key="a@default"), types.SimpleNamespace(model_key="b@default")]                 # a model that recovered returns, one that cooled down leaves
    bridge._restrict_to_executable(registry)
    assert {k for k, c in registry._agents.items() if c.enabled} == {"a@default", "b@default"}


def test_verifier_log_rows_are_tagged_with_the_claim_that_produced_them(tmp_path):
    import types
    bridge, _r, _s, _o = _bridge(tmp_path, [])
    verifier = types.SimpleNamespace(log=[])
    bridge.investigator = types.SimpleNamespace(evidence_verifier=verifier)
    verifier.log.append({"source_ref": "s1", "promoted": False})
    bridge._flush_verifier_log("C-primary")
    verifier.log.append({"source_ref": "s2", "promoted": True})
    bridge._flush_verifier_log("A-atom")
    rows = [json.loads(line) for line in (tmp_path / "verifier.log").read_text().splitlines()]
    assert [(r["claim"], r["source_ref"]) for r in rows] == [("C-primary", "s1"), ("A-atom", "s2")]


def test_unchanged_accepted_draft_is_never_organisational_success(tmp_path):
    """ERRATUM-1 regression: reward 1.0 + a valid quorum verification + delivered worker contribution + ZERO revisions => organisational_success is False, observations stay reported."""
    rep = _run(tmp_path, [_vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-a"), _vrow("A-1", "SUPPORTS", "VERIFIED", "ACCEPTED", "lineage-b")], closed_revisions=0)
    v = rep["verdict"]
    assert (v["worker_contribution"], v["independent_verification"], v["causal_effect_on_decision"]) == (True, True, False)
    assert v["organisational_success"] is False and rep["tasks"][0]["official_reward"] == 1.0
    assert rep["note"] == "original draft accepted - not organisational success"
