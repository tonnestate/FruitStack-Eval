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


def scripted(seen, *, l_first="7", n_first="9", n_critique=True, l_concedes=True):
    """Lineage L (luna) solves first; N (nemotron) solves second; each challenge comes from the other lineage; a revision goes back to its author."""
    def work(prompt, stage, prefer=None, exclude=()):
        seen.append((stage, prompt))
        other = "N" if "luna" in exclude else "L"
        if stage == "solve":
            return ok(other, f"ANSWER: {l_first if other == 'L' else n_first}")
        if stage == "challenge":
            if other == "N" and n_critique:
                return ok("N", "ISSUES: FOUND\nCLAIM: summing the even terms twice overcounts the series\nEVIDENCE: recount\nANSWER: 9")
            return ok(other, "ISSUES: NONE")
        if stage == "revise":
            who = "L" if prefer == "L-model" else "N"
            return ok(who, "ANSWER: 9" if (who == "L" and l_concedes) else f"ANSWER: {l_first if who == 'L' else n_first}")
        return {"success": False, "output": None, "failure_class": f"STAGE_NOT_USED:{stage}"}
    return work


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
