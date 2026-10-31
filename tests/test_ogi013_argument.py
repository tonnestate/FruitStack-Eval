"""classify_argument: the evidence rule for knowledge questions (QA runner only)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
import ogi013_argument as ag  # noqa: E402

DERIVATION = """ISSUES: FOUND
CLAIM: Option D is wrong because the matrix is block lower triangular, not upper triangular.
EVIDENCE: The top-right 3x3 block is zero, so det = det(B) * det(D) = 42 * (2 * (2*6 - 5*3)) = 42 * (-6).
CONSEQUENCE: The determinant is -252, which is option H, not option D (0)."""

RULE = """CLAIM: Answer C is wrong: the statute requires a signed writing for a sale of land.
EVIDENCE: The statute of frauds (the cited rule) makes an oral contract for the sale of land unenforceable.
CONSEQUENCE: Option B follows (unenforceable), unlike the judged answer C (enforceable)."""

NO_EVIDENCE = """ISSUES: FOUND
CLAIM: Option D is wrong and the author clearly made a mistake somewhere in the solution.
CONSEQUENCE: Option H is the better choice here."""

NO_CONSEQUENCE = """CLAIM: Option D is wrong because the matrix is not upper triangular at all.
EVIDENCE: The entries below the diagonal are non-zero, for example A21 = 2 and A31 = 3."""

COMPUTATION = """CLAIM: Option D is wrong because the determinant of the lower-right block is not zero.
EVIDENCE: ```python
print(2*(2*6-5*3))
```
RESULT: 7
CONSEQUENCE: Option H follows, unlike the judged option D."""


def kind(text):
    return ag.classify_argument(text, "task")["kind"]


def test_grounded_derivation():
    assert kind(DERIVATION) == "quote"                                     # stated evidence, nothing runnable


def test_grounded_rule_citation():
    assert kind(RULE) == "quote"


def test_claim_without_evidence_is_not_grounded():
    assert kind(NO_EVIDENCE) == "suggestion"


def test_evidence_without_consequence_is_not_grounded():
    assert kind(NO_CONSEQUENCE) == "suggestion"


def test_a_non_reproducing_computation_is_ungrounded_and_a_reproducing_one_is_executed():
    assert kind(COMPUTATION) == "suggestion"                               # prints -6, states 7
    assert kind(COMPUTATION.replace("RESULT: 7", "RESULT: -6")) == "command"


def test_approval_is_never_an_objection_and_unsafe_code_is_not_run():
    assert kind("ISSUES: NONE") == "suggestion" and kind("[APPROVE: EXCELLENT]") == "suggestion"
    evil = COMPUTATION.replace("print(2*(2*6-5*3))", "import os\nprint(os.getcwd())")
    assert ag.classify_argument(evil)["kind"] == "suggestion"
