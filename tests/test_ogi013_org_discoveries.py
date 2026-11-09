import pytest
from runners.ogi013_org_discoveries import Ledger


def RC(led, relation="SUPPORTS"):
    """A trusted execution receipt as host code issues it after running a check (ogi013_org_discoveries.execution_receipt)."""
    return led.issue_receipt("fs_runtime.CHECKS[test]", {"relation": relation}, verifier_lineage="host-executed-check")


def mk(tmp_path):
    led = Ledger(tmp_path / "l.jsonl")
    d = led.discover(claim="B is right", origin_run="R0", origin_task="q1", proposer="nemotron", applicability="same question", evidence_ref="x.json")
    return led, d


def test_model_assertion_alone_is_not_knowledge(tmp_path):
    led, d = mk(tmp_path)
    assert led.status(d)["state"] == "MODEL_ASSERTED"
    with pytest.raises(ValueError):
        led.verify(d, verdict="SUPPORTS", verifier="nemotron", evidence_ref="y")      # a model cannot verify


def test_verified_but_unused_is_not_learning(tmp_path):
    led, d = mk(tmp_path)
    led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="k", receipt=RC(led))
    assert led.status(d)["state"] == "INDEPENDENTLY_CHECKED" and led.report()["organizational_learning_instances"] == []


def test_same_run_reuse_does_not_count(tmp_path):
    led, d = mk(tmp_path)
    led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="k", receipt=RC(led, "SUPPORTS"))
    led.retrieve(d, run="R0", task="q1")
    assert led.status(d)["state"] == "INDEPENDENTLY_CHECKED"


def test_full_cycle_benefit_harm_and_falsified(tmp_path):
    led, d = mk(tmp_path)
    led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="k", receipt=RC(led))
    led.retrieve(d, run="R1", task="q2")
    assert led.status(d)["state"] == "RETRIEVED"
    led.apply(d, run="R1", task="q2", how="in prompt")
    assert led.status(d)["state"] == "APPLIED"
    with pytest.raises(ValueError):
        led.outcome(d, run="R2", task="q2", reward=1, control_reward=0, grader="official_grader", control_run="C")   # no application in R2
    led.outcome(d, run="R1", task="q2", reward=1, control_reward=0, grader="official_grader", control_run="C1")
    assert (led.status(d)["state"], led.status(d)["effect"]) == ("OUTCOME_MEASURED", "BENEFIT_OBSERVED") and led.report()["organizational_learning_instances"] == [d]
    led.apply(d, run="R1", task="q3", how="x")
    led.apply(d, run="R1", task="q4", how="x")
    led.outcome(d, run="R1", task="q3", reward=0, control_reward=1, grader="official_grader", control_run="C1")
    led.outcome(d, run="R1", task="q4", reward=0, control_reward=1, grader="official_grader", control_run="C1")
    assert led.status(d)["effect"] == "HARM_OBSERVED"
    led.verify(d, verdict="CONTRADICTS", verifier="executed", evidence_ref="k2", receipt=RC(led, "CONTRADICTS"))
    assert led.status(d)["state"] == "CONTRADICTED"                                   # both verifications kept


def test_falsified_is_kept(tmp_path):
    led, d = mk(tmp_path)
    led.verify(d, verdict="CONTRADICTS", verifier="executed", evidence_ref="k", receipt=RC(led, "CONTRADICTS"))
    assert led.status(d)["state"] == "FALSIFIED" and len(led.rows()) == 2


def test_chain_detects_tampering(tmp_path):
    led, d = mk(tmp_path)
    led.verify(d, verdict="SUPPORTS", verifier="dataset_key", evidence_ref="k")
    p = tmp_path / "l.jsonl"
    p.write_text(p.read_text().replace("SUPPORTS", "CONTRADICTS"))
    with pytest.raises(ValueError, match="CHAIN_BROKEN"):
        led.rows()
