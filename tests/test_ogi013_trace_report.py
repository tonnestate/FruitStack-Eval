"""Tests for runners/rg2_trace_report.py.

(a) REAL-DATA NEGATIVE CONTROL: read-only run on the org-smoke/t1 run dir. Skipped if absent.
(b) SYNTHETIC: tiny run dir built in tmp_path. ALL DATA IN THIS TEST IS SYNTHETIC.

Run: cd /root/fruits/integration/ogi013-org && PYTHONPATH=runners:. /root/fruits/integration/ogi013-hostpython-org/bin/python -m pytest -q tests/test_ogi013_trace_report.py
"""
import json
from pathlib import Path

import pytest

from rg2_trace_report import NOT_ACCEPTED, build_report, render_markdown

REAL_RUN = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013/runs/org-smoke/t1")


@pytest.mark.skipif(not REAL_RUN.is_dir(), reason="real org-smoke/t1 run dir not present")
def test_real_data_negative_control(capsys):
    rep = build_report(REAL_RUN)
    v = rep["verdict"]
    assert v["worker_contribution"] is False, rep["evidence"]["worker_contribution"]
    assert v["organisational_success"] is False
    assert rep["attempt_error_codes"].get("SEMANTIC_OUTPUT_FAILURE", 0) >= 1
    assert all(t["official_reward"] == 1.0 for t in rep["tasks"])
    assert any(i.get("action") == "SWITCH_WORKER" for i in rep["interventions"])
    md = render_markdown(rep)
    assert NOT_ACCEPTED in md
    print(md)
    out = capsys.readouterr().out
    print(out)


def _write(p: Path, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(r) for r in rows)
    p.write_text(text + "\n", encoding="utf-8")


def test_synthetic_positive_case(tmp_path):
    # SYNTHETIC: one delivered PROPOSAL, one ORG_REVISION with action_changed=true, reward 1.0.
    run = tmp_path / "synthetic-run"
    task = run / "tasks" / "synthetic_task_1"
    _write(task / "fruitstack-events.jsonl", [
        {"event": "ORG_DECISION", "claim": "C-SYN-1", "action": "draft_action", "status": "UNKNOWN",
         "triage": "SKIPPED_SIMPLE_TASK", "workers": ["synthetic-worker@default"], "rows": 1},
        {"event": "ORG_REVISION", "claim": "C-SYN-1", "action_changed": True,
         "draft_action": "draft_action", "final_action": "final_action", "synthetic": True},
    ])
    _write(task / "org" / "cherry" / "contributions.jsonl", [
        {"claim_id": "C-SYN-1", "kind": "PROPOSAL", "epistemic_status": "UNVERIFIED", "verdict": None,
         "identity": {"model_key": "synthetic-worker@default"}, "synthetic": True},
    ])
    (task / "official-result.json").write_text(json.dumps({"reward_info": {"reward": 1.0}}), encoding="utf-8")

    rep = build_report(run)
    v = rep["verdict"]
    assert v["worker_contribution"] is True
    assert v["causal_effect_on_decision"] is True
    assert v["organisational_success"] is True
    assert rep["note"] is None
    assert NOT_ACCEPTED not in render_markdown(rep)
