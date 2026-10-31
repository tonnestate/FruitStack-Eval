"""QA-2D pure logic: E majority with Luna tie-break, the NO_CONSENSUS rule, the infra-share pause, analysis maths on synthetic rows."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
import analyze_qa2d as an  # noqa: E402
import ogi013_qa2d as q2  # noqa: E402


def test_majority_ties_go_to_luna():
    assert q2.majority_tie_luna([("luna", "A"), ("nemo", "B")]) == "A"
    assert q2.majority_tie_luna([("luna", "A"), ("nemo", "B"), ("luna", "B")]) == "B"            # majority wins
    assert q2.majority_tie_luna([("luna", "A"), ("nemo", "B"), ("luna", "C"), ("nemo", "B")]) == "B"
    assert q2.majority_tie_luna([("luna", None), ("nemo", "B")]) == "B" and q2.majority_tie_luna([("luna", None)]) is None


def test_no_consensus_rule():
    cur = {"luna": "A", "nemo": "B"}
    assert q2.final_unresolved([{"author": "nemo", "level": "verified"}], cur) == ("B", "verified_last_objection")
    assert q2.final_unresolved([{"author": "nemo", "level": "verified"}, {"author": "luna", "level": "formal"}], cur) == ("A", "luna_default")     # only the LAST objection counts
    assert q2.final_unresolved([], cur) == ("A", "luna_default")


def test_infra_share_pause_needs_40_rows_and_more_than_10_percent():
    ok, bad = {"status": "OK"}, {"status": "INFRA_FAILED"}
    assert q2.infra_share_exceeded({"T": [ok] * 35 + [bad] * 4}) is None                       # fewer than 40 rows
    assert q2.infra_share_exceeded({"T": [ok] * 36 + [bad] * 4}) is None                       # exactly 10 %: not above
    assert q2.infra_share_exceeded({"T": [ok] * 35 + [bad] * 5, "E": [ok] * 40}) == "T"


def _rows(tmp_path):
    rows = []
    for i in range(20):
        key = "A"
        for arm, right in (("T", i < 18), ("E", i < 10), ("SL", i < 10), ("SN", i < 8)):
            rows.append({"qid": str(i), "arm": arm, "key": key, "letter": key if right else "B", "correct": right, "status": "OK", "calls": 3, "tokens": 100,
                         **({"stop": "AGREED_FIRST", "first_by_pos": {"S1": "A", "S2": "A"}} if arm == "T" else {})})
    p = tmp_path / "r.jsonl"
    p.write_text("\n".join(json.dumps(r) for r in rows))
    return p


def test_analysis_runs_the_two_confirmatory_tests_with_holm(tmp_path):
    res = an.analyze(_rows(tmp_path))
    assert res["n_questions"] == 20 and [a["correct"] for a in res["arms"]] == [18, 10, 10, 8]
    h1l, h1c = res["confirmatory"]
    assert (h1l["b_T_only"], h1l["c_other_only"]) == (8, 0) and h1l["p_holm"] >= h1l["p"] and h1c["hypothesis"] == "H1c"
    assert "QA-2D analysis" in an.render(res)


def test_arm_table_reports_latency_percentiles_and_cost_per_success(tmp_path):
    res = an.analyze(_rows(tmp_path))
    t = res["arms"][0]
    assert t["calls_per_success"] == 60 / 18 and t["tokens_per_success"] == 2000 / 18
    assert an.pct([1, 2, 3, 4, 100], 0.5) == 3 and an.pct([], 0.5) is None
    assert "latency P50/P95" in an.render(res)


def test_first_answer_prompt_is_byte_identical_in_every_arm(tmp_path, monkeypatch):
    import inspect
    from types import SimpleNamespace
    q = {"id": "1", "question": "What is 2+2?", "options": ["3", "4", "5"], "key": "B"}
    seen = []

    def fake(ctx, *a):
        seen.append(a[-1])
        return {"success": True, "output": "ANSWER: B", "model_key": q2.NEMO_KEY}
    monkeypatch.setattr(q2, "luna_step", lambda ctx, prompt: fake(ctx, prompt))
    monkeypatch.setattr(q2, "nemo_step", lambda ctx, ep, prompt: fake(ctx, ep, prompt))
    ep = SimpleNamespace(stats={"tokens_in": 0, "tokens_out": 0}, work="w")
    ctx = SimpleNamespace(luna_tokens=0, out=tmp_path, episode=lambda arm, qid: ep)
    q2.run_SL(ctx, q)
    q2.run_SN(ctx, q)
    q2.run_E(ctx, q, 2)                                               # one Luna and one nemotron draft
    assert len(seen) == 4 and len(set(seen)) == 1 and seen[0] == q2.answer_prompt(q)
    src = inspect.getsource(q2.run_T)
    assert src.count('answer_prompt(q), "first"') == 2                # both T members get the same prompt


def test_cooldown_wait_is_scheduling_for_short_cooldowns_only():
    ok = {"health": "AVAILABLE", "circuit_open": False, "credential_available": True, "retry_after_s": None}
    assert q2.cooldown_wait([ok]) == 0.0
    assert q2.cooldown_wait([{**ok, "health": "RATE_LIMITED", "circuit_open": True, "retry_after_s": 47.0}]) == 49.0
    assert q2.cooldown_wait([{**ok, "health": "DEGRADED", "retry_after_s": None}]) == 62.0
    assert q2.cooldown_wait([{**ok, "health": "QUOTA_EXHAUSTED"}]) == 0.0                 # exhausted: no wait (the run pauses instead)
    assert q2.cooldown_wait([{**ok, "health": "RATE_LIMITED", "retry_after_s": 4000.0}]) == 0.0   # too long to wait for
