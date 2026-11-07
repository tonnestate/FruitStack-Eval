"""Tests for runners/export_pair_rows.py using a tiny SYNTHETIC campaign (not real evidence).

Synthetic campaign: tasks SYN-1, SYN-2 have both conditions; SYN-3 has only RG2-OFF.
"""
import json, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "runners"))

from export_pair_rows import export, raw_sha  # noqa: E402

CONDS = ("RG2-OFF", "SINGLE")


def _jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def _run(campaign, task, cond, reward=1.0, cost=0.5):
    """One synthetic run dir: <campaign>/<task>/<cond>/ (c1/c2 layout)."""
    run = campaign / task / cond
    tdir = run / "tasks" / task
    tdir.mkdir(parents=True, exist_ok=True)
    result = {"duration": 10.0, "policy": "SYN-POLICY"}
    if reward is not None:
        result["reward_info"] = {"reward": reward}
    (tdir / "official-result.json").write_text(json.dumps(result), encoding="utf-8")
    _jsonl(tdir / "fruitstack-events.jsonl", [
        {"event": "EPISODE_OPENED", "sid": "SYN-SID", "work": "SYN-WORK", "write_tools": ["t1"]},
        {"event": "STEP", "receipt": "SYN-R1", "tag": "a", "model": "syn-model",
         "tokens_in": 3, "tokens_out": 4},
        {"event": "EPISODE_CLOSED", "budget": {"max_calls": 5}},
    ])
    _jsonl(run / "sim-usage.jsonl", [{"success": True, "model_key": "syn-sim", "receipt_id": "SYN-S1"}])
    _jsonl(run / "fruitstack" / "plumme-state" / "receipts.jsonl", [
        {"receipt_id": "SYN-R1", "provider": "syn-prov", "model": "syn-model", "success": True,
         "cost_class": "FREE_TIER", "usage": {"input_tokens": 3, "output_tokens": 4,
                                              "cost_usd": cost, "quota_units": 1},
         "metadata": {"economic": {"entitlement_units": 2}}},
        {"receipt_id": "SYN-S1", "provider": "syn-sim", "model": "syn-sim", "success": True,
         "cost_class": "FREE_TIER", "usage": {"input_tokens": 1, "output_tokens": 1,
                                              "cost_usd": 0.0, "quota_units": 0}},
    ])


def _campaign(tmp_path):
    camp = tmp_path / "synthetic-campaign"
    for task in ("SYN-1", "SYN-2"):
        for cond in CONDS:
            _run(camp, task, cond)
    _run(camp, "SYN-3", "RG2-OFF")  # SINGLE missing -> unmatched
    # SYN-2 SINGLE: unknown cost must stay null, never 0
    _run(camp, "SYN-2", "SINGLE", cost=None)
    (camp / "SYN-1" / "BLOCK.json").write_text(json.dumps(
        {"condition_order": list(CONDS), "simulator_model_key": "syn-sim", "attempt": 1}), encoding="utf-8")
    (camp / "discarded" / "SYN-0-attempt0").mkdir(parents=True)
    return camp


def test_pairs_only_complete_tasks_and_reports_unmatched(tmp_path):
    rows, mapping = export(str(_campaign(tmp_path)), "RG2-OFF", "SINGLE")
    assert mapping["paired"] == ["SYN-1", "SYN-2"]
    assert mapping["unmatched"] == [
        {"task_id": "SYN-3", "missing_conditions": ["SINGLE"], "present_conditions": ["RG2-OFF"]}]
    assert len(rows) == 4
    assert {(r["task_id"], r["arm"]) for r in rows} == {
        ("SYN-1", "FIXED"), ("SYN-1", "ADAPTIVE"), ("SYN-2", "FIXED"), ("SYN-2", "ADAPTIVE")}
    assert mapping["conditions"] == {"A": {"name": "RG2-OFF", "role": "FIXED"},
                                     "B": {"name": "SINGLE", "role": "ADAPTIVE"}}
    assert mapping["discarded"] == ["SYN-0-attempt0"]
    assert mapping["blocks"]["SYN-1"]["attempt"] == 1


def test_unknown_cost_stays_null_and_digests_are_plumme_auto(tmp_path):
    rows, mapping = export(str(_campaign(tmp_path)), "RG2-OFF", "SINGLE")
    by = {(r["task_id"], r["arm"]): r for r in rows}
    assert by[("SYN-2", "ADAPTIVE")]["cost_usd"] is None
    assert by[("SYN-2", "FIXED")]["cost_usd"] == 0.5
    assert by[("SYN-1", "FIXED")]["human_minutes"] is None
    assert all(r["model_pool_digest"] == raw_sha("plumme-auto") for r in rows)
    assert all(r["supply_regime_id"] == raw_sha("plumme-auto") for r in rows)
    assert mapping["model_mix"]["SYN-1"]["FIXED"]["successful"] == {"syn-prov|syn-model": 1}
    assert mapping["economic"]["SYN-1"]["FIXED"]["dimensions"] == {"entitlement_units": 2}
    assert mapping["economic_totals"]["FIXED"] == {"entitlement_units": 4}


def test_ungraded_run_is_not_verified(tmp_path):
    camp = _campaign(tmp_path)
    _run(camp, "SYN-1", "SINGLE", reward=None)  # official result without reward
    rows, _ = export(str(camp), "RG2-OFF", "SINGLE")
    grades = {(r["task_id"], r["arm"]): r["grade_status"] for r in rows}
    assert grades[("SYN-1", "ADAPTIVE")] == "INCOMPLETE"
    assert grades[("SYN-1", "FIXED")] == "VERIFIED"


def test_cli_compare_accepts_rows(tmp_path):
    camp = _campaign(tmp_path)
    rows_path = tmp_path / "rows.jsonl"
    mapping_path = tmp_path / "mapping.json"
    rc = subprocess.run(
        [sys.executable, str(REPO / "runners" / "export_pair_rows.py"), "--campaign", str(camp),
         "--cond-a", "RG2-OFF", "--cond-b", "SINGLE", "--out", str(rows_path),
         "--mapping-out", str(mapping_path)], capture_output=True, text=True, timeout=120)
    assert rc.returncode == 0, rc.stderr
    proc = subprocess.run(
        [sys.executable, "-m", "fruitstack_eval.cli", "ogi13", "compare",
         "--observations", str(rows_path)],
        cwd=str(REPO), env={"PYTHONPATH": str(REPO), "PATH": "/usr/bin:/bin"},
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["observation_rows"] == 4
    assert summary["paired_tasks"] == 2


def test_four_arm_design_exports_each_pair_for_confirmatory_analysis(tmp_path):
    arms = ("SINGLE", "SINGLE-E", "FIXED", "BROTHER")
    camp = tmp_path / "four-arm-campaign"
    for task_idx, task in enumerate(("SYN-1", "SYN-2")):
        for i, arm in enumerate(arms):
            _run(camp, task, arm, reward=1.0 if (i + task_idx) % 2 == 0 else 0.0)

    pair_paths = {}
    for i, left in enumerate(arms):
        for right in arms[i + 1:]:
            rows, mapping = export(str(camp), left, right)
            assert mapping["paired"] == ["SYN-1", "SYN-2"]
            assert mapping["conditions"] == {
                "A": {"name": left, "role": "FIXED"},
                "B": {"name": right, "role": "ADAPTIVE"},
            }
            name = f"{left}__{right}"
            path = tmp_path / f"{name}.jsonl"
            path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
            pair_paths[name] = path

    expected = {
        "SINGLE__SINGLE-E", "SINGLE__FIXED", "SINGLE__BROTHER",
        "SINGLE-E__FIXED", "SINGLE-E__BROTHER", "FIXED__BROTHER",
    }
    assert set(pair_paths) == expected
    result_path = tmp_path / "confirmatory.json"
    proc = subprocess.run(
        [sys.executable, str(REPO / "runners" / "ogi013_confirmatory.py"),
         "--out", str(result_path),
         *(f"{name}={path}" for name, path in pair_paths.items())],
        capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert set(result["results"]) == expected
    assert all(row["pairs"] == 2 for row in result["results"].values())
