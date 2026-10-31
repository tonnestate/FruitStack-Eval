"""QA-1 scripted tests (no model calls)."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_qa1 as q1  # noqa: E402


def test_unparsable_answers_count_as_incorrect_and_parsing_is_strict_last_occurrence():
    assert q1.parse_letter("reasoning ... ANSWER: B", 4) == "B"
    assert q1.parse_letter("ANSWER: A\nthen on reflection\nANSWER: C", 4) == "C"          # last occurrence
    for bad in ("the answer is B", "answer: B", "ANSWER: b", "ANSWER: (B)", "ANSWER: AB", "", None, "ANSWER:"):
        assert q1.parse_letter(bad, 4) is None
    assert q1.parse_letter("ANSWER: E", 4) is None                                          # outside the option range
    assert q1.grade(q1.parse_letter("no answer line", 4), "A") is False and q1.grade("A", "A") is True


def test_majority_ties_go_to_the_earliest_draft_and_unparsable_drafts_do_not_vote():
    assert q1.majority(["A", "B", "B"]) == "B" and q1.majority(["A", "B"]) == "A" and q1.majority(["B", "A", "A", "B"]) == "B"
    assert q1.majority([None, None]) is None and q1.majority([None, "C"]) == "C"


def test_a_specialist_cannot_introduce_a_new_letter():
    pos = {"S1": "A", "S2": "B"}
    assert q1.final_answer(pos, "B") == ("B", "specialist")
    assert q1.final_answer(pos, "C", earliest="A") == ("A", "specialist_new_letter_rejected")      # C is not an existing final position
    assert q1.final_answer({"S1": "A", "S2": "A"}, None) == ("A", "agreed")
    assert q1.final_answer({"S1": "A", "S2": None}, None, earliest="A")[1] == "no_agreement_no_specialist"


def test_e_draft_count_equals_the_call_count_recorded_for_t():
    assert q1.e_draft_count({"calls": 7}) == 7 and q1.e_draft_count({"calls": "5"}) == 5


DATA = Path("/root/fruits/research/OGI013-QA1/data/study.jsonl")


@pytest.mark.skipif(not DATA.exists(), reason="dataset not present")
def test_no_question_text_in_any_committed_file():
    """Every 10-word window of every question and long option is looked up in every committed text file (one pass over the files)."""
    import re
    repo = Path(__file__).resolve().parent.parent
    windows = set()
    for row in q1.load_jsonl(DATA) + q1.load_jsonl(DATA.with_name("smoke.jsonl")):
        for text in [row["question"]] + [o for o in row["options"] if len(o) >= 40]:
            w = re.findall(r"\w+", text.lower())
            windows |= {" ".join(w[i:i + 10]) for i in range(max(1, len(w) - 9))} if len(w) >= 10 else set()
    files = subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True).stdout.splitlines()
    for f in files:
        p = repo / f
        if not p.is_file() or p.stat().st_size > 5_000_000 or not f.endswith((".py", ".md", ".json", ".jsonl", ".txt", ".sh", ".diff")):
            continue
        w = re.findall(r"\w+", p.read_text(errors="ignore").lower())
        assert not any(" ".join(w[i:i + 10]) in windows for i in range(len(w) - 9)), f"question text found in {f}"


# ---- analyze_qa1.py ---------------------------------------------------------------------------------------------------------------------------------------
import analyze_qa1 as an  # noqa: E402


def test_exact_mcnemar_clopper_pearson_and_holm_known_values():
    assert abs(an.mcnemar_exact(10, 2) - 2 * (1 + 12 + 66) / 4096) < 1e-12 and an.mcnemar_exact(0, 0) == 1.0 and an.mcnemar_exact(5, 5) == 1.0
    lo, hi = an.clopper_pearson(10, 12)
    assert abs(lo - 0.5159) < 1e-3 and abs(hi - 0.9791) < 1e-3
    assert an.clopper_pearson(0, 10)[0] == 0.0 and abs(an.clopper_pearson(10, 10)[1] - 1.0) < 1e-12 and abs(an.clopper_pearson(0, 10)[1] - 0.3085) < 1e-3
    assert [round(x, 4) for x in an.holm([0.01, 0.02, 0.04])] == [0.03, 0.04, 0.04]


def test_paired_difference_and_infrastructure_failure_counts_as_incorrect_with_a_sensitivity_exclusion(tmp_path):
    rows = []
    for i in range(20):
        for arm in an.ARMS:
            right = (arm == "T" and i < 15) or (arm == "S" and i < 10) or (arm == "E" and i < 12) or (arm == "L" and i < 18)
            rows.append({"qid": str(i), "arm": arm, "letter": "A", "key": "A", "correct": right, "status": "OK", "calls": 3, "tokens": 100, "seconds": 1.0, "first_letters": {"S1": "A" if i < 5 else "B"}})
    rows[0]["status"] = "INFRA_FAILED"; rows[0]["correct"] = False          # T on question 0: failed twice -> incorrect
    f = tmp_path / "r.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in rows))
    res = an.analyze(str(f))
    assert res["n_questions"] == 20 and res["sensitivity"]["n_questions"] == 19
    h1 = next(c for c in res["primary"]["comparisons"] if c["hypothesis"] == "H1")
    assert h1["b_T_only"] == 5 and h1["c_other_only"] == 1 and abs(h1["diff"] - 0.2) < 1e-9 and abs(h1["p"] - 0.21875) < 1e-12          # T right on 1..14, S on 0..9; T failed (infra) on 0 -> S-only there


def test_qa_budget_profile_reserves_room_for_the_system_preamble_and_longer_answers():
    from types import SimpleNamespace
    from ogi013_tau2_agent import Episode
    ep = object.__new__(Episode)
    ep.sid, ep.budget_profile = "s", "qa"
    ep.stack = SimpleNamespace(fs=SimpleNamespace(governance=SimpleNamespace(snapshot=lambda sid: {"tokens_remaining": 60000})))
    max_out, reserve = ep.output_budget("Reply with the single word READY.", {})
    assert max_out == 4096 and reserve >= 4096 + 3000                       # a 33-byte prompt no longer yields a 2081-token reservation
    ep.stack.fs.governance.snapshot = lambda sid: {"tokens_remaining": 5000}
    assert ep.output_budget("x", {})[1] == 5000                             # never more than the session has left
