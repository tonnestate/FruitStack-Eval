import json

import pytest

mpmath = pytest.importorskip("mpmath")

from ogi_rh import items, numerics  # noqa: E402
from ogi_rh.claims import NUMERICAL_EVIDENCE  # noqa: E402


def test_first_zeros_match_mpmath_zetazero_consistency_only():
    zeros = numerics.zeros_by_gram(6, dps=25)
    assert [z["index"] for z in zeros] == [1, 2, 3, 4, 5, 6]
    with mpmath.workdps(25):
        for z in zeros:
            assert abs(mpmath.mpf(z["gamma"]) - mpmath.zetazero(z["index"]).imag) < mpmath.mpf("1e-18")
    for z in zeros:
        assert z["label"] == NUMERICAL_EVIDENCE
        assert z["precision"].startswith("NON-RIGOROUS") and "no certified error bound" in z["precision"]
        assert z["agreeing_digits_between_precisions"] >= 18


def test_gram_law_records_are_numerical_evidence():
    r = numerics.gram_law_holds(0)
    assert r["label"] == NUMERICAL_EVIDENCE and r["holds"] is True


def test_no_prompt_file_contains_grader_only_text():
    assert items.leaks() == []


def test_leak_guard_catches_a_planted_leak(tmp_path):
    (tmp_path / "prompts").mkdir()
    (tmp_path / "grader").mkdir()
    (tmp_path / "grader" / "g.json").write_text(json.dumps({"items": [{"id": "X", "label": "FLAWED"}]}))
    (tmp_path / "prompts" / "p.json").write_text(json.dumps({"items": [{"id": "X", "hint": "flawed"}]}))
    assert items.leaks(tmp_path) == [("p.json", "flawed")]


def test_item_files_match_lock():
    lock = json.loads(items.LOCK_PATH.read_text())
    assert lock["files"] == items.file_hashes()


def test_every_prompt_item_has_grader_entry_and_vice_versa():
    for fam, grader in [("f1_ladder", "f1_ladder_grader"), ("f2_flaw", "f2_flaw_grader"),
                        ("f3_overclaim", "f3_overclaim_grader")]:
        p = json.loads((items.ITEMS_DIR / "prompts" / f"{fam}.json").read_text())
        g = json.loads((items.ITEMS_DIR / "grader" / f"{grader}.json").read_text())
        assert [i["id"] for i in p["items"]] == [i["id"] for i in g["items"]]
        assert g["grader_only"] is True
