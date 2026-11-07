"""Offline tests for runners/fs_codemode (Code Mode facade, typed contract, sieve, duo, EVC, Shapley). No model calls, no network, no sandbox needed:
the verifier is injected (production: ogi013_argument.classify_argument)."""
import threading
import time

import pytest

from fs_codemode import evc, sieve, shapley
from fs_codemode.contract import Msg, parse_letter, verification_level
from fs_codemode.duo import DuoInfra, run_duo
from fs_codemode.facade import BudgetStop, Facade

LINEAGES = {"luna": "openai", "nemo": "nvidia"}


# ---- contract -------------------------------------------------------------------------------------------------------------------------------------------
def test_contract_parses_parts_and_letter_and_refuses_simulated_uncertainty():
    out = "ISSUES: FOUND\nCLAIM: The colleague's answer A is wrong, order is 2.\nEVIDENCE: 5^2 = 25 = 1 mod 8.\nCONSEQUENCE: option F follows.\nANSWER: F"
    m = Msg.from_output("OBJECTION", "nemo", "nvidia", out, 10, target="luna", msg_id="O1")
    assert m.result == "F" and m.claim.startswith("The colleague") and "25" in m.evidence and m.full_ref
    assert m.verification == "none"                                      # trust is never raised by the message itself
    assert "VERIFICATION (host): none" in m.render()
    with pytest.raises(ValueError):
        Msg("ANSWER", "luna", "openai", uncertainty={"value": 0.9, "source": "simulated"})
    with pytest.raises(ValueError):
        Msg("ANSWER", "luna", "openai", uncertainty={"value": 0.9})
    assert parse_letter("ANSWER: K", 10) is None and parse_letter("ANSWER: B ... ANSWER: C", 4) == "C"
    assert verification_level({"kind": "verified"}) == "reproduced"  # legacy label only proves that the calculation ran
    assert verification_level({"kind": "reproduced"}) == "reproduced"
    assert verification_level({"kind": "independently_confirmed"}) == "none"  # labels alone cannot establish relevance or independent confirmation
    assert verification_level({"kind": "independently_confirmed", "checks": {
        "relevance_assessed": True, "independent_confirmation": True}}) == "independently_confirmed"
    assert verification_level({"kind": "suggestion", "argument": {"executed": True}}) == "failed"


# ---- sieve ----------------------------------------------------------------------------------------------------------------------------------------------
def test_compact_keeps_invariants_or_falls_back():
    long = ("Let me think about this carefully. " * 30) + "The determinant is 42 * (-6) = -252. Objection O1 is right. ANSWER: H"
    body, did = sieve.compact(long, max_chars=300)
    assert did and "-252" in body and "O1" in body and "ANSWER: H" in body and len(body) < len(long)
    assert not sieve.missing_invariants(long, body)
    no_inv = "word " * 400                                               # nothing worth keeping -> full text, never an empty message
    assert sieve.compact(no_inv, 100) == (no_inv, False)


def test_sieve_drops_only_redundant_messages():
    delivered = {}
    a = sieve.sieve([{"id": "O1", "claim": "order is 2", "result": "F", "text": "x"}], delivered, "luna")
    b = sieve.sieve([{"id": "O2", "claim": "Order is 2", "result": "F", "text": "y"}], delivered, "luna")
    c = sieve.sieve([{"id": "A", "claim": "", "result": "F", "text": "first text"}], delivered, "luna")
    d = sieve.sieve([{"id": "A2", "claim": "", "result": "F", "text": "new reasoning"}], delivered, "luna")
    assert a[0]["action"] == "keep" and b[0]["action"] == "drop"
    assert c[0]["action"] == "keep" and d[0]["action"] == "keep"       # changed reasoning with the same letter is not dropped


# ---- facade ---------------------------------------------------------------------------------------------------------------------------------------------
def test_facade_parallel_order_provenance_budget_and_fail_closed_verify():
    def call(member, prompt):
        time.sleep(0.2)
        return {"success": True, "output": f"{member}:{prompt}", "tokens": 10}
    events = []
    fac = Facade(call, on_event=events.append, max_parallel=2)
    t0 = time.monotonic()
    res = fac.parallel([("luna", "p1", "a"), ("nemo", "p2", "b")])
    assert time.monotonic() - t0 < 0.35                                 # ran at the same time
    assert [r["output"] for r in res] == ["luna:p1", "nemo:p2"]
    assert fac.totals.calls == 2 and fac.totals.tokens == 20
    assert [e["op"] for e in events] == ["call", "call"] and all(e["prompt_sha"] for e in events)
    assert fac.verify("anything")["kind"] == "suggestion"                # no verifier -> nothing executed
    assert fac.compare({"luna": "A", "nemo": "F"})["agree"] is False and fac.compare({"luna": "F", "nemo": "F"})["agree"] is True
    budget = {"left": 1}

    def ok():
        budget["left"] -= 1
        return budget["left"] >= 0
    fac2 = Facade(call, budget_ok=ok)
    fac2.call("luna", "x")
    with pytest.raises(BudgetStop):
        fac2.call("luna", "y")


def test_facade_chain_is_ordered_and_stops():
    fac = Facade(lambda m, p: {"success": True, "output": ""})
    seen = []

    def s1(v):
        seen.append(1)
        return 1

    def s2(v):
        seen.append(2)
        return v + 1

    def s3(v):
        seen.append(3)
        return v + 1
    assert fac.chain([s1, s2, s3], stop=lambda v: v == 2) == 2 and seen == [1, 2]


# ---- duo ------------------------------------------------------------------------------------------------------------------------------------------------
class Script:
    """Scripted members: responses keyed by (member, phase)."""

    def __init__(self, responses):
        self.responses, self.prompts, self.lock = responses, [], threading.Lock()

    def __call__(self, member, prompt):
        with self.lock:
            self.prompts.append((member, prompt))
        phase = "first" if "A colleague" not in prompt and "Objection" not in prompt else ("critique" if "A colleague" in prompt else "reply")
        r = self.responses[(member, phase)]
        return r if isinstance(r, dict) else {"success": True, "output": r, "tokens": 100}


VERIFIED = lambda text: {"kind": "reproduced", "argument": {"executed": True}} if "```python" in text else {"kind": "formal", "argument": {"executed": False}}  # noqa: E731
OBJ = ("ISSUES: FOUND\nCLAIM: The colleague's answer A is wrong because the order of 5 mod 8 is 2.\nEVIDENCE: 5^2 = 25 = 1 mod 8.\n```python\nprint(2)\n```\n"
       "RESULT: 2\nCONSEQUENCE: The correct answer is option F, not option A.\nANSWER: F")


def test_duo_agreement_costs_two_calls_and_identical_first_prompts():
    s = Script({("luna", "first"): "ANSWER: C", ("nemo", "first"): "reason ANSWER: C"})
    r = run_duo("task", "PROMPT", 10, s, lineages=LINEAGES, verifier=VERIFIED)
    assert r["stop"] == "AGREED_FIRST" and r["letter"] == "C" and r["calls"] == 2
    assert s.prompts[0][1] == s.prompts[1][1] == "PROMPT"


def test_duo_chain_like_8512_accepted_concession_and_consensus():
    s = Script({("luna", "first"): "ANSWER: A", ("nemo", "first"): "order 2. ANSWER: F",
                ("luna", "critique"): "ISSUES: NONE", ("nemo", "critique"): OBJ,
                ("luna", "reply"): "O1 accepted: my order 3 was wrong. ANSWER: F"})
    r = run_duo("task", "PROMPT", 10, s, lineages=LINEAGES, verifier=VERIFIED)
    assert r["letter"] == "F" and r["stop"] == "CONSENSUS_EXCHANGE_1" and r["how"] == "agreed"
    assert r["reproduced_objections"] == 1 and r["independently_confirmed_objections"] == 0
    assert r["accepted_concessions"] == 1 and r["objection_states"] == ["ACCEPTED"]
    assert r["calls"] == 5 and r["phase_tokens"]["first"] == 200 and r["phase_tokens"]["exchange"] == 300
    assert any(e["op"] == "verify" for e in r["provenance"])


def test_duo_never_critique_policy_finishes_on_luna_without_exchange():
    s = Script({("luna", "first"): "ANSWER: A", ("nemo", "first"): "ANSWER: F"})
    r = run_duo("task", "PROMPT", 10, s, lineages=LINEAGES, verifier=VERIFIED, policy=evc.NeverCritique())
    assert r["stop"] == "POLICY_FINISH" and r["letter"] == "A" and r["how"] == "luna_default" and r["calls"] == 2


@pytest.mark.parametrize(("level", "expected", "how"), [
    ("reproduced", "A", "luna_default"),
    ("independently_confirmed", "F", "independently_confirmed_last_objection"),
])
def test_only_independently_confirmed_objection_can_settle_unresolved_conflict(level, expected, how):
    s = Script({("luna", "first"): "ANSWER: A", ("nemo", "first"): "ANSWER: F",
                ("luna", "critique"): "ISSUES: NONE", ("nemo", "critique"): OBJ,
                ("luna", "reply"): "I retain my answer. ANSWER: A"})
    verifier = lambda _text: {"kind": level, "argument": {"executed": True}, "checks": {  # noqa: E731
        "relevance_assessed": level == "independently_confirmed",
        "independent_confirmation": level == "independently_confirmed"}}
    r = run_duo("task", "PROMPT", 10, s, lineages=LINEAGES, verifier=verifier)
    assert r["stop"] == "NO_CONSENSUS" and r["letter"] == expected and r["how"] == how
    assert r["verified_objections"] == 2 * int(level == "independently_confirmed")


def test_facade_does_not_treat_reproduced_objection_as_settled():
    fac = Facade(lambda _m, _p: {"success": True, "output": ""})
    points = fac.conflicts({"luna": "A", "nemo": "F"}, [{"target": "luna", "level": "reproduced"}])
    assert points[0]["verified_against"] == 0
    points = fac.conflicts({"luna": "A", "nemo": "F"}, [{"target": "luna", "level": "independently_confirmed"}])
    assert points[0]["verified_against"] == 1


def test_duo_infra_failure_is_raised_not_hidden():
    s = Script({("luna", "first"): {"success": False, "failure_class": "LIMIT"}, ("nemo", "first"): "ANSWER: F"})
    with pytest.raises(DuoInfra):
        run_duo("task", "PROMPT", 10, s, lineages=LINEAGES)


# ---- EVC ------------------------------------------------------------------------------------------------------------------------------------------------
def _rows():
    rows = []
    for i in range(400):
        cat = "math" if i % 2 else "law"
        agree = i % 5 == 0
        luna = "A" if (i % 3) else "B"
        key = "A"
        if agree:
            rows.append({"qid": f"q{i}", "category": cat, "key": key, "first_by_member": {"luna": luna, "nemo": luna}, "letter": luna,
                         "tokens": 200, "seconds": 2, "calls": 2, "phase_tokens": {"first": 200}, "phase_seconds": {"first": 2}})
            continue
        if cat == "math":                       # critique fixes Luna's errors
            final = "A"
        else:                                   # critique makes things worse
            final = "C" if luna == "A" else "B"
        rows.append({"qid": f"q{i}", "category": cat, "key": key, "first_by_member": {"luna": luna, "nemo": "Z"}, "letter": final,
                     "tokens": 1200, "seconds": 12, "calls": 5, "phase_tokens": {"first": 200}, "phase_seconds": {"first": 2}})
    return rows


def test_evc_learns_where_critique_pays_and_beats_baseline_on_held_out_half():
    res = evc.evaluate(_rows())
    pts = {p["policy"]: p for p in res["points"]}
    base, best = pts["baseline_always_critique"], pts["evc_c0.0_t0.0"]
    assert res["n_fit"] > 0 and res["n_eval"] > 0
    assert best["accuracy"] >= base["accuracy"] and best["tokens"] < base["tokens"]
    assert best["critiques"] < base["critiques"]
    assert any(p["pareto"] for p in res["points"])
    assert evc.split_half("q1") == evc.split_half("q1")


def test_mcnemar_exact_values():
    assert evc.mcnemar_exact(0, 0) == 1.0
    assert abs(evc.mcnemar_exact(10, 0) - 2 / 1024) < 1e-12


# ---- Shapley --------------------------------------------------------------------------------------------------------------------------------------------
def test_shapley_efficiency_and_duo_game():
    v = {frozenset(): 0, frozenset({"a"}): 1, frozenset({"b"}): 2, frozenset({"a", "b"}): 4}
    phi = shapley.shapley(("a", "b"), lambda s: v[frozenset(s)])
    assert abs(sum(phi.values()) - 4) < 1e-12 and abs(phi["a"] - 1.5) < 1e-12
    rows = [r for r in (evc.normalize(x) for x in _rows()) if r]
    g = shapley.duo_game(rows)
    total = sum(g["shapley"].values())
    assert abs(total - g["coalitions"]["link,luna,nemo"]) < 0.05 and g["assumption"]
