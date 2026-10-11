import json

from conftest import decision_row, feedback_row
from fruitstack_eval.cli import main


def test_power_command(capsys):
    assert main(["power", "paired", "--margin", "0.1", "--discordance", "0.2"]) == 0
    assert json.loads(capsys.readouterr().out) == {"design": "paired", "tasks": 157}


def test_costaudit_exit_code(write_log, capsys):
    log = write_log([decision_row("d1", cost_classes={"A": "PREMIUM", "B": "FREE_TIER"})])
    assert main(["costaudit", "--log", str(log)]) == 1
    assert json.loads(capsys.readouterr().out)["passed"] is False


def test_ope_evaluate_command(write_log, capsys):
    rows = []
    for i in range(4):
        rows += [decision_row(f"d{i}", propensity=1.0), feedback_row(f"d{i}", 0.5)]
    log = write_log(rows)
    assert main(["ope", "evaluate", "--log", str(log), "--bootstrap", "0", "--min-support", "1", "--min-ess", "1"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["snips"] == 0.5 and out["usable_decisions"] == 4


def test_interventions_add_requires_fields(tmp_path, capsys):
    log = tmp_path / "i.jsonl"
    assert main(["interventions", "add", "--log", str(log), "--actor", "owner"]) == 2
    assert main(["interventions", "add", "--log", str(log), "--actor", "owner", "--kind", "AUTHORITY",
                 "--intervention", "SIGN", "--minutes", "2", "--phase", "PILOT"]) == 0
    capsys.readouterr()
    assert main(["interventions", "summary", "--log", str(log)]) == 0
    assert json.loads(capsys.readouterr().out)["count_by_kind"]["AUTHORITY"] == 1


def test_tasks_commit_writes_private_salts(tmp_path, capsys):
    tasks_path = tmp_path / "tasks.jsonl"
    tasks_path.write_text(json.dumps({"task_id": "t1", "family": "INQUIRY", "subfamily": "s", "split": "HELDOUT",
                                      "prompt": "p", "reference": "r"}) + "\n", encoding="utf-8")
    manifest, salts = tmp_path / "manifest.json", tmp_path / "salts.json"
    assert main(["tasks", "commit", "--tasks", str(tasks_path), "--manifest", str(manifest), "--salts", str(salts)]) == 0
    assert oct(salts.stat().st_mode & 0o777) == "0o600"
    assert main(["tasks", "verify", "--tasks", str(tasks_path), "--manifest", str(manifest), "--salts", str(salts)]) == 0
