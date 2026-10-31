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
