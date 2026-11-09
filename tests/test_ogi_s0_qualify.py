"""S0 runner offline (fixture PlumMe service, three local lineages, no provider call): rows, identity, VERIFIED feedback, resume, cap."""
import json

import pytest

pytest.importorskip("peachme.research")
pytest.importorskip("math_verify")

import ogi_s0_qualify as S0  # noqa: E402
from fs_runtime import fixture_service  # noqa: E402


def test_s0_pipeline_rows_feedback_resume_and_cap(tmp_path, monkeypatch):
    monkeypatch.setenv("PLUMME_SELECTION_SPREAD", "0")
    svc = fixture_service(tmp_path / "plumme", {"answer": "\\boxed{2}"})
    monkeypatch.setattr(S0, "operational_service", lambda: svc)
    out = tmp_path / "s0"
    assert S0.main(["--out", str(out), "--items", "2", "--candidates", "3", "--max-calls", "4"]) == 3      # cap reached -> BUDGET_STOP
    rows = [json.loads(x) for x in (out / "rows.jsonl").read_text().splitlines()]
    assert len(rows) == 4 and all(r["status"] == "GRADED" for r in rows)
    assert all(r["served_lineage"] == r["declared_lineage"] for r in rows)
    assert all(r["feedback"] for r in rows)
    assert len(json.loads((out / "candidates.json").read_text())) == 3
    assert S0.main(["--out", str(out), "--items", "2", "--candidates", "3", "--max-calls", "100"]) == 0   # resumes, never re-runs a row
    rows = [json.loads(x) for x in (out / "rows.jsonl").read_text().splitlines()]
    assert len(rows) == 6 and len({(r["candidate"], r["item"]) for r in rows}) == 6
    assert "profiles" in json.loads((out / "S0_REPORT.json").read_text())


def test_host_defect_rows_are_rerun_once_and_kept(tmp_path, monkeypatch):
    monkeypatch.setenv("PLUMME_SELECTION_SPREAD", "0")
    svc = fixture_service(tmp_path / "plumme", {"answer": "\\boxed{2}"})
    monkeypatch.setattr(S0, "operational_service", lambda: svc)
    out = tmp_path / "s0"
    assert S0.main(["--out", str(out), "--items", "1", "--candidates", "1"]) == 0
    f = out / "rows.jsonl"
    r = json.loads(f.read_text())
    f.write_text(json.dumps({**r, "status": "INFRA", "failure_class": "INVALID_OBJECTIVE"}) + "\n")
    for _ in range(2):
        assert S0.main(["--out", str(out), "--items", "1", "--candidates", "1", "--rerun-host-defect", "INVALID_OBJECTIVE"]) == 0
    rows = [json.loads(x) for x in f.read_text().splitlines()]
    assert [x["status"] for x in rows] == ["INFRA", "GRADED"] and rows[1]["rerun_of"] == "INVALID_OBJECTIVE"
