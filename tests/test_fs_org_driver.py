"""Non-frozen organizational-learning driver (offline; scripted workers, no provider call).

Lifecycle under test: episode 1 produces a discovery -> independent (executed) verification -> persistent ledger + OrangeMe projection + MangoMe mirror
-> episode 2 (different task, different run) retrieves and applies it in the applied arm only -> independent grader -> outcome against a control arm."""
import json
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("cherryme.brother")
orangeme = pytest.importorskip("orangeme.project")

from runners.fs_org_driver import Task, run_episode, run_pair, capture_brother  # noqa: E402
from runners.ogi013_learning_hook import LearningHook  # noqa: E402
from runners.ogi013_org_discoveries import Ledger  # noqa: E402
from runners.ogi013_org_memory import OrangeKnowledgeProjection  # noqa: E402


def sig(text):
    for line in reversed((text or "").splitlines()):
        if line.startswith("ANSWER:"):
            return line.split(":", 1)[1].strip()
    return None


def scripted(seen, *, l_first="7", n_first="9", n_critique=True, l_concedes=True, verification=None):
    """Lineage L (luna) solves first; N (nemotron) solves second; each challenge comes from the other lineage; a revision goes back to its author."""
    def work(prompt, stage, prefer=None, exclude=()):
        seen.append((stage, prompt))
        other = "N" if "luna" in exclude else "L"
        if stage == "solve":
            return ok(other, f"ANSWER: {l_first if other == 'L' else n_first}")
        if stage == "challenge":
            if other == "N" and n_critique:
                return {**ok("N", "ISSUES: FOUND\nCLAIM: summing the even terms twice overcounts the series\nEVIDENCE: recount\nANSWER: 9"),
                        **({"verification": verification} if verification else {})}
            return ok(other, "ISSUES: NONE")
        if stage == "revise":
            who = "L" if prefer == "L-model" else "N"
            return ok(who, "ANSWER: 9" if (who == "L" and l_concedes) else f"ANSWER: {l_first if who == 'L' else n_first}")
        return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
    return work


ROSTER = {"L-model": "luna", "N-model": "nemotron"}


def ok(who, out):
    return {"success": True, "output": out, "model_key": f"{who}-model", "independence_key": {"L": "luna", "N": "nemotron"}[who], "receipt_id": f"r-{who}"}


@pytest.fixture
def orange(tmp_path):
    from orangeme.gitstore import GitRepo
    from orangeme.identity import AgentIdentity
    path = tmp_path / "orange"
    path.mkdir()
    for cmd in (["git", "init", "-b", "main"], ["git", "config", "user.name", "T"], ["git", "config", "user.email", "t@example.invalid"]):
        subprocess.run(cmd, cwd=path, check=True, capture_output=True)
    (path / ".keep").write_text("x")
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, capture_output=True)
    repo = GitRepo(path)
    return orangeme.ProjectLedger(repo, AgentIdentity("fruitstack", "test"), repo.path / "projects/fs")


def test_brother_episode_captures_a_critique_that_changed_the_answer_as_an_unverified_discovery(tmp_path, monkeypatch):
    monkeypatch.setenv("ORANGEME_NO_PUSH", "1")
    led = Ledger(tmp_path / "l.jsonl")
    hook = LearningHook(led, run_id="R1", apply=True)
    seen = []
    out = run_episode(Task("t1", "Sum of the series?", sig, lambda a: 1.0 if a == "9" else 0.0, "executed"), work=scripted(seen), hook=hook, arm="applied")
    assert out["answer"] in {"7", "9"} and out["calls"] >= 2 and out["arm"] == "applied"
    ids = out["captured"]
    assert ids and all(led.status(i)["state"] == "ASSERTED" for i in ids)              # a model's critique is never knowledge by itself
    row = next(r for r in led.rows() if r["kind"] == "DISCOVERY")
    assert row["proposer"] == "nemotron" and "overcounts" in row["claim"]


def test_a_critique_backed_by_an_executed_check_becomes_a_verified_retrievable_discovery(tmp_path):
    """EVAL-002 defect: capture_brother passed ground={'level': ...} only, so LearningHook (which needs argument.executed) never verified a Brother Mode discovery."""
    led = Ledger(tmp_path / "l.jsonl")
    out = run_episode(Task("t1", "Sum of the series?", sig, lambda a: 0.0, "executed"), work=scripted([], verification="verified"),
                      hook=LearningHook(led, run_id="R1"), arm="T", roster=ROSTER)
    ids = out["captured"]
    assert ids and all(led.status(i)["state"] == "STORED_NOT_REUSED" for i in ids)                   # verified, not yet reused
    assert {r["verifier"] for r in led.rows() if r["kind"] == "VERIFICATION"} == {"executed"}
    assert led.retrievable("t-other", "R2", "series summation with even terms overcounts")         # reusable on a later task by another run
    led2 = Ledger(tmp_path / "l2.jsonl")                                                             # model-asserted critique: still never knowledge
    ids2 = run_episode(Task("t1", "Sum?", sig, lambda a: 0.0, "executed"), work=scripted([], verification="model_asserted"),
                       hook=LearningHook(led2, run_id="R1"), arm="T", roster=ROSTER)["captured"]
    assert ids2 and all(led2.status(i)["state"] == "ASSERTED" for i in ids2)


def test_pair_reuses_verified_knowledge_in_the_applied_arm_only_and_records_the_outcome_against_control(tmp_path, monkeypatch, orange):
    monkeypatch.setenv("ORANGEME_NO_PUSH", "1")
    led = Ledger(tmp_path / "l.jsonl")
    d = led.discover(claim="summing the even terms of the series twice overcounts", origin_run="R0", origin_task="t0", proposer="nemotron",
                     applicability="series summation", evidence_ref="tool:pytest#1")
    led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="tool:pytest#1")
    seen = []
    res = run_pair(Task("t2", "Sum of the series with even terms?", sig, lambda a: 1.0 if a == "9" else 0.0, "executed"),
                   work=scripted(seen, n_critique=False), ledger=led, tag="P1", projection=OrangeKnowledgeProjection(orange))
    control_prompts = [p for s, p in res["prompts"]["control"] if s == "solve"]
    applied_prompts = [p for s, p in res["prompts"]["applied"] if s == "solve"]
    assert not any("Organizational knowledge" in p for p in control_prompts)          # the control never sees stored knowledge
    assert any("overcounts" in p for p in applied_prompts)
    st = led.status(d)
    assert st["retrievals"] == 1 and st["applications"] == 1 and st["outcomes"] == 1
    assert res["control"]["run"] != res["applied"]["run"] and res["applied"]["retrieved"] == [d]
    snap = orange.get(f"knowledge/{d}")["value"]
    assert snap["state"] == st["state"] and snap["verifiers"] == ["executed"]


def test_orange_projection_keeps_falsified_and_contradicted_and_is_append_only(tmp_path, monkeypatch, orange):
    monkeypatch.setenv("ORANGEME_NO_PUSH", "1")
    led = Ledger(tmp_path / "l.jsonl")
    a = led.discover(claim="alpha holds", origin_run="R0", origin_task="q", proposer="p", applicability="any", evidence_ref="e")
    led.verify(a, verdict="CONTRADICTS", verifier="executed", evidence_ref="v")
    proj = OrangeKnowledgeProjection(orange)
    assert proj.publish(led) == [a]
    assert proj.publish(led) == []                                                    # unchanged state: no new revision
    led.verify(a, verdict="SUPPORTS", verifier="official_grader", evidence_ref="w")
    assert proj.publish(led) == [a]
    assert orange.get(f"knowledge/{a}")["value"]["state"] == "CONTRADICTED" and len(orange.history(f"knowledge/{a}")) == 2


def test_capture_brother_ignores_same_lineage_critique(tmp_path):
    from cherryme.contributions import ContributionLedger
    cl = ContributionLedger()
    s = cl.add(claim_id="c", question_id=None, kind="SOLUTION", worker="L-model", verdict=None, epistemic_status="UNVERIFIED", disposition="RETAINED_UNVERIFIED",
               reason="INDEPENDENT_SOLUTION", answer_text="ANSWER: 7", identity={"independence_key": "luna"})
    c = cl.add(claim_id="c", question_id=None, kind="CRITIQUE", worker="L2-model", verdict=None, epistemic_status="DISSENT", disposition="RETAINED_UNVERIFIED",
               reason="CRITIQUE", answer_text="ISSUES: FOUND\nCLAIM: wrong\nANSWER: 9", detail={"targets": s.id}, identity={"independence_key": "luna"})
    cl.add(claim_id="c", question_id=None, kind="REVISION", worker="L-model", verdict=None, epistemic_status="UNVERIFIED", disposition="RETAINED_UNVERIFIED",
           reason="REVISION", answer_text="ANSWER: 9", detail={"revises": s.id, "responding_to": [c.id]}, identity={"independence_key": "luna"})
    led = Ledger(tmp_path / "l.jsonl")
    assert capture_brother(LearningHook(led, "R1"), "t", cl.rows, sig) == []


def test_the_selector_is_order_independent_and_identical_for_every_arm():
    """Selector parity: the first solver's position no longer wins a disagreement; ties are broken by a fixed hash of (task, answer), not by order or model."""
    from types import SimpleNamespace
    from runners.fs_org_driver import final_answer, select_answer
    a, b = "ANSWER: 7", "ANSWER: 9"
    tie_ab, tie_ba = select_answer("t1", [a, b], sig), select_answer("t1", [b, a], sig)
    assert tie_ab == tie_ba and tie_ab[1] == "SELECTED_HASH_TIE"
    assert select_answer("t1", [a, b, b], sig) == select_answer("t1", [b, a, b], sig) == ("9", "SELECTED")       # plurality
    assert select_answer("t1", [a, a], sig) == ("7", "CONSENSUS")
    assert select_answer("t1", ["no answer", b], sig) == ("9", "SELECTED")                                       # unparseable never beats a parsed answer
    assert select_answer("t1", [a, b, b], sig, score=lambda t: 1.0 if "7" in t else 0.0) == ("7", "SELECTED")    # visible checks first
    for order in ({"L": a, "N": b}, {"N": b, "L": a}):                                                            # T uses the same selector
        assert final_answer(SimpleNamespace(positions=order), sig, "t1") == tie_ab


def test_a_luna_twice_team_row_is_invalid_and_excluded_from_analysis(tmp_path):
    """S1 replay: the roster declares luna + nemotron, but every executed receipt is luna. The row must be INFRA_IDENTITY, not a 'multi-model' result."""
    from runners.fs_org_driver import split_valid
    def luna_twice(prompt, stage, prefer=None, exclude=()):
        return ok("L", "ISSUES: NONE" if stage == "challenge" else "ANSWER: 7")
    task = Task("t1", "Sum?", sig, lambda a: 0.0, "executed")
    bad = run_episode(task, work=luna_twice, hook=LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R"), arm="T", roster=ROSTER)
    good = run_episode(task, work=scripted([]), hook=LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R"), arm="T", roster=ROSTER)
    assert bad["identity_valid"] is False and bad["exclusion"] == "INFRA_IDENTITY:SINGLE_LINEAGE_ROW"
    assert good["identity_valid"] is True and good["exclusion"] is None
    assert split_valid([bad, good]) == ([good], [bad])
    with pytest.raises(ValueError):                                                     # a study arm cannot skip the check
        run_episode(task, work=scripted([]), hook=LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R"), arm="T")
