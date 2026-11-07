"""Objection lifecycle: a reproduced computation alone cannot be accepted as a grounded concession."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
import ogi013_argument as ag  # noqa: E402
import ogi013_qa1 as q1  # noqa: E402
from ogi013_vote import OPEN, WITHDRAWN, Ledger  # noqa: E402

O1 = """ISSUES: FOUND
CLAIM: The colleague's answer (A) is incorrect because the order of 5 in U_8 is 2, not 3.
EVIDENCE: Compute powers of 5 modulo 8: 5^1 = 5, 5^2 = 25 = 1. ```python
print(pow(5, 2, 8))
```
RESULT: 1
CONSEQUENCE: The correct answer is F (order 2), which differs from the colleague's answer A (order 3)."""


def test_reproduced_computation_alone_does_not_accept_an_objection(monkeypatch):
    monkeypatch.setattr(ag, "run_code", lambda code: (True, "1\n"))
    led = Ledger()
    g = ag.ledger_ground(ag.classify_argument(O1))
    oid = led.objection("S1", "nemotron", O1, grounded=True, ground=g)
    assert g["level"] == "reproduced" and led.objs[0]["state"] == OPEN
    led.reply(oid, "author", "concede", "O1 is right. ANSWER: F")
    o = led.objs[0]
    assert not q1.accepted_concession("O1 is right. ANSWER: F", o, "luna", "A", "F")
    assert o["state"] == OPEN and o["open"] is True


def test_a_withdrawn_objection_ends_withdrawn():
    led = Ledger()
    oid = led.objection("S2", "luna", "x", grounded=True, ground={"kind": "quote", "level": "formal"})
    led.reply(oid, "author", "evidence", "the task says 'y'", {"kind": "quote", "level": "formal"})
    led.reply(oid, "critic", "withdraw", "agreed", {"kind": "quote", "level": "formal"})
    assert led.objs[0]["state"] == WITHDRAWN and led.objs[0]["open"] is False
