import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_chain as oc  # noqa: E402


def test_complete_chain_and_lineage_diversity(tmp_path):
    ev = [
        {"event": "SESSION_START"}, {"event": "STEP", "tokens_in": 10, "tokens_out": 5}, {"event": "SESSION_END"},
        {"event": "SNAPSHOT", "pos": "S1", "label": "first", "author_lineages": ["A"]},
        {"event": "SNAPSHOT", "pos": "S2", "label": "first", "author_lineages": ["B"]},
        {"event": "SESSION_START"}, {"event": "STEP", "tokens_in": 20, "tokens_out": 5}, {"event": "SESSION_END"},
        {"event": "CHALLENGE", "pos": "S1", "rev": 0, "lineage": "B", "author_lineages": ["A"], "verdict": "FOUND", "test_runs": 1},
        {"event": "OBJECTION", "id": "O1", "target": "S1", "lineage": "B", "kind": "objection", "grounded": True},
        {"event": "SESSION_START"}, {"event": "STEP", "tokens_in": 30, "tokens_out": 5}, {"event": "SESSION_END"},
        {"event": "REVISION", "pos": "S1", "rev": 1, "responding_to": ["O1"], "changed_code": True, "reviser_lineage": "A"},
        {"event": "SNAPSHOT", "pos": "S1", "label": "rev1", "author_lineages": ["A"]},
        {"event": "CHALLENGE", "pos": "S1", "rev": 1, "lineage": "B", "author_lineages": ["A"], "verdict": "NONE", "test_runs": 2},
    ]
    (tmp_path / "fruitstack-events.jsonl").write_text("\n".join(json.dumps(e) for e in ev))
    (tmp_path / "grades.json").write_text(json.dumps({"S1_first.diff": {"f2p_passed": 0, "p2p_passed": 5}, "S1_rev1.diff": {"f2p_passed": 1, "p2p_passed": 5}}))
    rows, d = oc.chain(tmp_path)
    assert [r["status"] for r in rows] == ["COMPLETE"] and rows[0]["tokens"] == 25 + 35
    assert d["solvers_distinct"] and d["own_lineage_contributions"] == 0 and d["top_lineage_share"] == 1.0 and not d["G_dev_lineage_ok"]   # all contributions from one lineage -> fails the 50 % rule
