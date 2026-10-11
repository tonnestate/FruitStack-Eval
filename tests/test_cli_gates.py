import ast
import json
from pathlib import Path

from fruitstack_eval import inquiry
from fruitstack_eval.cli import main

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = {"plumme", "cherryme", "appleme", "peachme", "mangome", "pomelome", "cogc", "spari", "intakegov",
            "bananame", "strawberryme", "dragonfruitme", "blueberryme", "orangeme", "chomview"}


def test_evaluator_package_never_imports_the_system_under_test():
    offenders = []
    for path in (ROOT / "fruitstack_eval").glob("*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names = [node.module]
            offenders += [f"{path.name}: {n}" for n in names if n.split(".")[0] in PRODUCTS]
    assert offenders == []


def run(capsys, *argv):
    code = main(list(argv))
    out = capsys.readouterr().out
    return code, (json.loads(out) if out.strip() else None)


def test_calib_score_and_independence_cli(tmp_path, capsys):
    tasks = tmp_path / "calib.jsonl"
    code, out = run(capsys, "calib", "generate", "--n", "12", "--seed", "3", "--out", str(tasks))
    assert code == 0 and out["tasks"] == 12
    rows = [json.loads(l) for l in tasks.read_text().splitlines()]
    results = tmp_path / "results.jsonl"
    with results.open("w") as handle:
        for group in ("g1", "g2"):
            for t in rows:
                handle.write(json.dumps({"task_id": t["task_id"], "group": group, "receipt_id": "r", "success": True,
                                         "structural_state": "WELL_FORMED", "output": f"ANSWER: {t['answer']}"}) + "\n")
    scored = tmp_path / "scored.jsonl"
    code, out = run(capsys, "calib", "score", "--tasks", str(tasks), "--results", str(results), "--out", str(scored))
    assert code == 0 and out["correct"] == 24
    code, out = run(capsys, "independence", "--scored", str(scored))
    assert code == 1 and "TOO_FEW_QUALIFIED_GROUPS" in out["blockers"]       # 12 calls < 60 per group


def test_seal_and_logcheck_cli(tmp_path, capsys):
    log = tmp_path / "decisions.jsonl"
    log.write_text(json.dumps({"type": "decision", "data": {"decision_id": "d1"}}) + "\n")
    seal_path = tmp_path / "seal.json"
    code, out = run(capsys, "seal", "create", "--seal", str(seal_path), "--log", f"decisions={log}:decisionlog")
    assert code == 0 and out["logs"] == {"decisions": 1}
    code, out = run(capsys, "seal", "verify", "--seal", str(seal_path))
    assert code == 0 and out["logs"]["decisions"]["status"] == "UNCHANGED"
    code, out = run(capsys, "logcheck", "--log", str(log), "--seal", str(seal_path))
    assert code == 1 and "NO_INTERVENTION_LOG" in out["blockers"] and "FIELD_PROBLEMS" in out["blockers"]
    assert main(["seal", "create", "--seal", str(seal_path), "--log", "broken"]) == 2


def test_inquiry_validate_grade_and_blind_cli(tmp_path, capsys):
    ref = json.dumps({"verdict": "SUPPORTED", "key_type": "integer", "key": "8446", "sources": ["https://www.rfc-editor.org/rfc/rfc8446"]})
    tasks = tmp_path / "tasks.jsonl"
    tasks.write_text("".join(json.dumps({"task_id": f"t{i}", "family": "INQUIRY", "subfamily": "TECH" if i < 2 else "HIST",
                                         "split": "TRAIN" if i < 2 else "HELDOUT",
                                         "prompt": inquiry.prompt("TLS 1.3 is RFC 8446.", "Which RFC number?"),
                                         "reference": ref}) + "\n" for i in range(4)))
    code, out = run(capsys, "inquiry", "validate", "--tasks", str(tasks))
    assert code == 0 and out["verdicts"] == {"SUPPORTED": 4}
    results = tmp_path / "results.jsonl"
    results.write_text("".join(json.dumps({"task_id": f"t{i}", "arm": arm, "output": "VERDICT: SUPPORTED\nKEY: 8446",
                                           "quota_units": 1, "cost_eur": 0, "wall_seconds": 1}) + "\n"
                               for i in range(4) for arm in ("F1", "F3")))
    graded = tmp_path / "graded.jsonl"
    code, out = run(capsys, "inquiry", "grade", "--tasks", str(tasks), "--results", str(results), "--out", str(graded))
    assert code == 0 and out["by_arm"]["F1"]["grade_1"] == 4
    code, out = run(capsys, "compare", "--results", str(graded), "--new", "F3", "--reference", "F1", "--margin", "0.1",
                    "--bootstrap", "200")
    assert code == 0 and out["arms"]["F3"]["success_rate"] == 1.0

    sheet, key, manifest = tmp_path / "sheet.jsonl", tmp_path / "key.jsonl", tmp_path / "manifest.json"
    code, out = run(capsys, "blind", "export", "--tasks", str(tasks), "--results", str(results), "--seed", "1",
                    "--sheet", str(sheet), "--key", str(key), "--manifest", str(manifest))
    assert code == 0 and out["items"] == 8 and oct(key.stat().st_mode)[-3:] == "600"
    rows = [dict(json.loads(l), grade=1.0) for l in sheet.read_text().splitlines()]
    sheet.write_text("".join(json.dumps(r) + "\n" for r in rows))
    labels = tmp_path / "labels.jsonl"
    code, out = run(capsys, "blind", "ingest", "--manifest", str(manifest), "--key", str(key), "--sheet", str(sheet),
                    "--grader", "owner", "--out", str(labels), "--deterministic", str(graded))
    assert code == 0 and out["agreement_with_deterministic"]["exact_agreement"] == 1.0
