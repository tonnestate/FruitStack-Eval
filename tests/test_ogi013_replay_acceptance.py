"""Repair order 1, R7 replay acceptance: the stored micro-pilot T records through the new logic (no model calls)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_replay as rp  # noqa: E402

pytestmark = pytest.mark.skipif(not (rp.MICRO / "micro__duration-1").exists(), reason="micro task trees not present")


def test_duration_o4_never_enters_a_revision_rev2_is_not_adopted_and_the_output_is_the_first_candidate():
    r = rp.replay("micro__duration-1")
    assert "O4" not in r["grounded_objections"] and "O4" in r["ungrounded_or_suggestion"]
    d = {x[0]: x for x in r["decisions"]}
    assert d["S3_rev1"][1] == "REJECTED_REVISION" and d["S3_rev2"][1] == "REJECTED_REVISION"
    assert d["S3_rev2"][3]["grounded_claimed"] == []                              # rev2 claimed only O4/O5, neither grounded
    assert r["selected_output"] == "S3:first" and r["selected_hidden_grade"]["resolved"] is True


@pytest.mark.parametrize("task", ["micro__intervals-1", "micro__lru-1"])
def test_intervals_and_lru_output_is_the_first_correct_candidate_and_no_revision_is_adopted(task):
    r = rp.replay(task)
    assert r["selected_output"].endswith(":first") and r["selected_hidden_grade"]["resolved"] is True
    assert all(x[1] != "ADOPTED" or x[2] == "FIRST_CANDIDATE" for x in r["decisions"])
