import json
import shutil
from pathlib import Path

import pytest

from fruitstack_eval import deposit
from fruitstack_eval.cli import main

ROOT = Path(__file__).resolve().parent.parent


def run(capsys, *argv):
    code = main(list(argv))
    return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def evidence(tmp_path, capsys):
    ev = tmp_path / "evidence"
    (ev / "g2").mkdir(parents=True)
    rows = []
    for group, wrong in (("A", range(0, 18)), ("B", range(20, 38)), ("C", range(40, 58))):
        for t in range(60):
            ok = t not in wrong
            rows.append({"task_id": f"t{t}", "group": group, "offer_id": f"o{group}", "model": group, "receipt_id": "r",
                         "model_fingerprint": "f", "executed": True, "parsed": True, "correct": ok,
                         "answer_given": "ok" if ok else f"bad{group}"})
    (ev / "g2" / "scored.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    code, out = run(capsys, "independence", "--scored", str(ev / "g2" / "scored.jsonl"))
    assert code == 0
    (ev / "g2" / "independence.json").write_text(json.dumps(out))
    (ev / "replay.toml").write_text('[[step]]\nname = "g2"\ncommand = ["independence", "--scored", "g2/scored.jsonl"]\n'
                                    'expected = "g2/independence.json"\n')
    return ev


def test_replay_reproduces_and_detects_a_doctored_report(evidence, capsys):
    code, out = run(capsys, "replay", "--evidence", str(evidence))
    assert code == 0 and out["steps"][0]["status"] == "REPRODUCED"
    report = json.loads((evidence / "g2" / "independence.json").read_text())
    report["groups"]["A"]["accuracy"] = 0.9
    (evidence / "g2" / "independence.json").write_text(json.dumps(report))
    code, out = run(capsys, "replay", "--evidence", str(evidence))
    assert code == 1 and out["steps"][0]["status"] == "DIFFERS"
    assert any("accuracy" in d for d in out["steps"][0]["differences"])


def test_deposit_build_verify_and_doi(tmp_path):
    files = {}
    for label in ("protocol", "task_manifest", "pilot_procedure"):
        files[label] = tmp_path / f"{label}.txt"
        files[label].write_text(label)
    files["g2_thresholds"] = ROOT / "config" / "g2_thresholds.toml"
    freeze = tmp_path / "freeze.toml"
    template = (ROOT / "deposit" / "FREEZE_TEMPLATE.toml").read_text()
    freeze.write_text(template)
    files["freeze"] = freeze
    with pytest.raises(ValueError, match="discordance_psi"):
        deposit.build(files)                                      # template values must be replaced
    freeze.write_text(template.replace("discordance_psi = 0.0", "discordance_psi = 0.3")
                      .replace("paired_tasks = 0 ", "paired_tasks = 236 "))
    manifest = deposit.build(files, created_at="2026-10-11T00:00:00+00:00")
    result = deposit.verify(manifest, files)
    assert not result["passed"] and result["problems"] == ["NO_DOI: the owner has not recorded a deposit DOI yet"]
    manifest["doi"] = "10.17605/OSF.IO/EXAMPLE"
    assert deposit.verify(manifest, files)["passed"]
    files["protocol"].write_text("changed after deposit")
    assert not deposit.verify(manifest, files)["passed"]
    with pytest.raises(ValueError, match="deposit needs"):
        deposit.build({"protocol": files["protocol"]})
