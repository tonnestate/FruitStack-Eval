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
from runners.ogi013_org_discoveries import Ledger, execution_receipt  # noqa: E402
from runners.ogi013_org_memory import OrangeKnowledgeProjection  # noqa: E402


def RC(relation="SUPPORTS"):
    """A trusted execution receipt as host code issues it after running a check (ogi013_org_discoveries.execution_receipt)."""
    return execution_receipt("fs_runtime.CHECKS[test]", {"relation": relation}, verifier_lineage="host-executed-check")


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
    assert ids and all(led.status(i)["state"] == "MODEL_ASSERTED" for i in ids)        # a model's critique is never knowledge by itself
    row = next(r for r in led.rows() if r["kind"] == "DISCOVERY")
    assert row["proposer"] == "nemotron" and "overcounts" in row["claim"]


def test_a_worker_reporting_verified_stays_model_asserted_and_is_never_retrievable(tmp_path):
    """Owner requirement: a worker's verification="verified" (critique_ground -> argument.executed) carries no execution receipt, so it is kept as a
    MODEL_ASSERTED verification and never becomes organizational knowledge."""
    led = Ledger(tmp_path / "l.jsonl")
    out = run_episode(Task("t1", "Sum of the series?", sig, lambda a: 0.0, "executed"), work=scripted([], verification="verified"),
                      hook=LearningHook(led, run_id="R1"), arm="T", roster=ROSTER)
    ids = out["captured"]
    assert ids and all(led.status(i)["state"] == "MODEL_ASSERTED" for i in ids)
    assert [r["receipt"] for r in led.rows() if r["kind"] == "VERIFICATION"] == [None] * len(ids)
    assert led.retrievable("t-other", "R2", "series summation with even terms overcounts") == []
    led2 = Ledger(tmp_path / "l2.jsonl")                                                             # model-asserted critique: still never knowledge
    ids2 = run_episode(Task("t1", "Sum?", sig, lambda a: 0.0, "executed"), work=scripted([], verification="model_asserted"),
                       hook=LearningHook(led2, run_id="R1"), arm="T", roster=ROSTER)["captured"]
    assert ids2 and all(led2.status(i)["state"] == "MODEL_ASSERTED" for i in ids2)


def test_pair_reuses_verified_knowledge_in_the_applied_arm_only_and_records_the_outcome_against_control(tmp_path, monkeypatch, orange):
    monkeypatch.setenv("ORANGEME_NO_PUSH", "1")
    led = Ledger(tmp_path / "l.jsonl")
    d = led.discover(claim="summing the even terms of the series twice overcounts", origin_run="R0", origin_task="t0", proposer="nemotron",
                     applicability="series summation", evidence_ref="tool:pytest#1")
    led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="tool:pytest#1", receipt=RC("SUPPORTS"))
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
    led.verify(a, verdict="CONTRADICTS", verifier="executed", evidence_ref="v", receipt=RC("CONTRADICTS"))
    proj = OrangeKnowledgeProjection(orange)
    assert proj.publish(led) == [a]
    assert proj.publish(led) == []                                                    # unchanged state: no new revision
    led.verify(a, verdict="SUPPORTS", verifier="executed", evidence_ref="w", receipt=RC())
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


def test_controls_are_compute_matched_to_t_and_share_its_selector_and_identity_guard(tmp_path):
    """E_div = same models round-robin, R_mono = one model repeated, both with T's call/token budget and the uniform selector; a handover is PLAN_MISMATCH."""
    from runners.fs_org_driver import run_samples, select_answer
    def drafts(prompt, stage, prefer=None, exclude=()):
        who = "L" if prefer == "L-model" else "N"
        return {**ok(who, f"ANSWER: {7 if who == 'L' else 9}"), "input_tokens": 100, "output_tokens": 50}
    task = Task("t1", "Sum?", sig, lambda a: 0.0, "executed")
    t_row = run_episode(task, work=lambda p, s, **kw: {**scripted([])(p, s, **kw), "input_tokens": 100, "output_tokens": 50},
                        hook=LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R"), arm="T", roster=ROSTER)
    k, budget = t_row["calls"], t_row["tokens"]["input"] + t_row["tokens"]["output"]
    e = run_samples(task, work=drafts, arm="E_div", roster=ROSTER, cycle=list(ROSTER), k=k, token_budget=budget)
    r = run_samples(task, work=drafts, arm="R_mono", roster={"N-model": "nemotron"}, cycle=["N-model"], k=k, token_budget=budget)
    for row in (e, r):
        assert row["identity_valid"] is True and row["calls"] == k and row["tokens"]["input"] + row["tokens"]["output"] == budget
    assert [x["independence_key"] for x in e["receipts"]][:2] == ["luna", "nemotron"] and {x["independence_key"] for x in r["receipts"]} == {"nemotron"}
    texts = [f"ANSWER: {7 if i % 2 == 0 else 9}" for i in range(k)]
    assert (e["answer"], e["how"]) == select_answer("t1", texts, sig)                    # the same selector T uses
    assert run_samples(task, work=drafts, arm="E_div", roster=ROSTER, cycle=list(ROSTER), k=3)["calls"] == 3      # no token counts -> call budget
    handover = run_samples(task, work=lambda p, s, prefer=None, exclude=(): ok("L", "ANSWER: 7"), arm="R_mono",
                           roster={"N-model": "nemotron"}, cycle=["N-model"], k=2)
    assert handover["exclusion"] == "INFRA_IDENTITY:LINEAGE_OUTSIDE_ROSTER"
    e_mono = run_samples(task, work=lambda p, s, prefer=None, exclude=(): ok("L", "ANSWER: 7"), arm="E_div", roster=ROSTER, cycle=list(ROSTER), k=2)
    assert e_mono["exclusion"] == "INFRA_IDENTITY:PLAN_MISMATCH"                        # a one-model 'diversity' control no longer passes silently


def test_corrected_and_damage_are_counted_from_graded_first_answers_after_the_episode(tmp_path):
    """L answers 7, N answers 9, N's critique makes L concede to 9. If 9 is right: L was corrected (wrong->right). If 7 is right: collaboration damage (right->wrong)."""
    from runners.fs_org_driver import grade_after
    def episode(right):
        task = Task("t1", "Sum?", sig, lambda a: 1.0 if a == right else 0.0, "executed")
        row = run_episode(task, work=scripted([]), hook=LearningHook(Ledger(tmp_path / f"{right}.jsonl"), run_id="R"), arm="T", roster=ROSTER)
        assert "reward" not in row and "effect" not in row                               # nothing graded inside the episode
        assert sorted((m["lineage"], m["first"], m["final"]) for m in row["members"]) == [("luna", "7", "9"), ("nemotron", "9", "9")]
        return grade_after(row, task)["effect"]
    assert episode("9") == {"class": "HELD", "corrected_members": 1, "damaged_members": 0, "first_correct": 1, "members": 2}
    assert episode("7") == {"class": "DAMAGED", "corrected_members": 0, "damaged_members": 1, "first_correct": 1, "members": 2}
    t = Task("t", "q", sig, lambda a: 1.0 if a == "3" else 0.0, "executed")
    assert grade_after({"answer": "3", "members": [{"first": "1", "final": "3"}, {"first": "2", "final": "3"}]}, t)["effect"]["class"] == "CORRECTED"
    assert grade_after({"answer": "1", "members": [{"first": "1", "final": "1"}, {"first": "3", "final": "3"}]}, t)["effect"]["class"] == "DAMAGED"   # control: right draft not selected


ROSTER3 = {**ROSTER, "S-model": "sage"}                                                   # the same roster for every arm, specialist declared (prereg §6)


def with_specialist(base, lineage="sage"):
    def work(prompt, stage, prefer=None, exclude=()):
        if stage == "specialist":
            return {"success": True, "output": "ANSWER: 9", "model_key": prefer or "?", "independence_key": lineage, "receipt_id": "r-S"}
        return base(prompt, stage, prefer=prefer, exclude=exclude)
    return work


def test_specialist_is_a_declared_roster_member_of_every_arm(tmp_path):
    """T rows that use the specialist stay valid, a T row that converges without it stays valid, and a control that never calls it stays valid on the same roster."""
    from runners.fs_org_driver import run_samples
    task = Task("t1", "Sum?", sig, lambda a: 0.0, "executed")
    hook = lambda: LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R")             # noqa: E731
    used = run_episode(task, work=with_specialist(scripted([], l_concedes=False)), hook=hook(), arm="T", roster=ROSTER3, specialist="S-model")
    assert used["specialist_used"] and used["identity_valid"] is True
    assert next(r for r in used["receipts"] if r["stage"] == "specialist")["prefer"] == "S-model"        # routed to the declared member
    calm = run_episode(task, work=with_specialist(scripted([])), hook=hook(), arm="T", roster=ROSTER3, specialist="S-model")
    assert not calm["specialist_used"] and calm["identity_valid"] is True
    drafts = lambda p, s, prefer=None, exclude=(): ok("L" if prefer == "L-model" else "N", "ANSWER: 7")   # noqa: E731
    e = run_samples(task, work=drafts, arm="E_div", roster=ROSTER3, cycle=list(ROSTER), k=2, specialist="S-model")
    assert e["identity_valid"] is True                                                 # never calls the specialist, still valid
    assert run_samples(task, work=drafts, arm="E_div", roster=ROSTER3, cycle=list(ROSTER), k=2)["exclusion"] == "INFRA_IDENTITY:ROSTER_NOT_REALISED"
    old = run_episode(task, work=with_specialist(scripted([], l_concedes=False)), hook=hook(), arm="T", roster=ROSTER)
    assert old["exclusion"] == "INFRA_IDENTITY:LINEAGE_OUTSIDE_ROSTER"                  # an undeclared extra model is never a valid team row
    wrong = run_episode(task, work=with_specialist(scripted([], l_concedes=False), lineage="nemotron"), hook=hook(), arm="T", roster=ROSTER3, specialist="S-model")
    assert wrong["exclusion"] == "INFRA_IDENTITY:ROLE_MISMATCH"


def test_generic_multi_agent_control_is_token_matched_guarded_and_has_no_critique(tmp_path):
    from runners.fs_org_driver import run_multi, select_answer
    seen = []

    def team(prompt, stage, prefer=None, exclude=()):
        seen.append((stage, prompt))
        who = {"L-model": "L", "N-model": "N"}[prefer]
        out = {"lead": "Split the series into odd and even terms.", "synthesize": "ANSWER: 9"}.get(stage, f"ANSWER: {7 if who == 'L' else 9}")
        return {**ok(who, out), "input_tokens": 100, "output_tokens": 50}
    task = Task("t1", "Sum?", sig, lambda a: 0.0, "executed")
    t_row = run_episode(task, work=lambda p, s, **kw: {**scripted([])(p, s, **kw), "input_tokens": 100, "output_tokens": 50},
                        hook=LearningHook(Ledger(tmp_path / "l.jsonl"), run_id="R"), arm="T", roster=ROSTER)
    budget = t_row["tokens"]["input"] + t_row["tokens"]["output"]
    g = run_multi(task, work=team, roster=ROSTER, cycle=list(ROSTER), k=t_row["calls"], token_budget=budget)
    spent = g["tokens"]["input"] + g["tokens"]["output"]
    assert g["identity_valid"] is True and abs(spent - budget) <= 0.1 * budget                       # token parity within the ±10% tolerance
    assert set(g["stages"]) == {"lead", "solve", "synthesize"} and g["stages"]["lead"] == g["stages"]["synthesize"] == 1
    assert not {"challenge", "revise", "specialist"} & {s for s, _ in seen}                           # no critique / revision events
    assert all("Split the series" in p for s, p in seen if s == "solve")                              # the lead's brief reaches every worker
    texts = [p for s, p in seen if s == "solve"]
    assert not any("ANSWER: " in p for p in texts)                                                     # a worker never sees another's draft
    drafts = [f"ANSWER: {7 if i % 2 == 0 else 9}" for i in range(g["drafts"])]
    assert (g["answer"], g["how"]) == select_answer("t1", drafts + ["ANSWER: 9"], sig) and g["synthesis"] == "9"
    assert run_multi(task, work=team, roster=ROSTER, cycle=list(ROSTER), k=5)["calls"] == 5            # no token counts -> call budget, synthesis included
    luna = run_multi(task, work=lambda p, s, prefer=None, exclude=(): ok("L", "ANSWER: 7"), roster=ROSTER, cycle=list(ROSTER), k=4)
    assert luna["identity_valid"] is False and luna["exclusion"].startswith("INFRA_IDENTITY:")       # the row-level guard applies


def test_eval002_sham_brief_is_length_matched_never_verified_for_the_task_and_order_is_seeded(tmp_path):
    from runners.fs_org_driver import sham_brief, task_order, run_transfer
    led = Ledger(tmp_path / "l.jsonl")
    good = led.discover(claim="summing the even terms of the series twice overcounts", origin_run="R0", origin_task="t0", proposer="nemotron",
                        applicability="series summation", evidence_ref="tool:pytest#1")
    led.verify(good, verdict="SUPPORTS", verifier="executed", evidence_ref="tool:pytest#1", receipt=RC("SUPPORTS"))
    for i, claim in enumerate(["a cached DNS entry outlives its TTL", "sorting is stable in this library"]):   # verified but unrelated: the placebo pool
        d = led.discover(claim=claim, origin_run="R0", origin_task=f"u{i}", proposer="luna", applicability="any", evidence_ref="e")
        led.verify(d, verdict="SUPPORTS", verifier="executed", evidence_ref="e", receipt=RC("SUPPORTS"))
    led.discover(claim="unverified rumour about caches", origin_run="R0", origin_task="u8", proposer="luna", applicability="any", evidence_ref="e")
    bad = led.discover(claim="falsified claim about sorting", origin_run="R0", origin_task="u9", proposer="luna", applicability="any", evidence_ref="e")
    led.verify(bad, verdict="CONTRADICTS", verifier="executed", evidence_ref="e", receipt=RC("CONTRADICTS"))
    own = led.discover(claim="the series answer is 9", origin_run="R0", origin_task="t2", proposer="luna", applicability="any", evidence_ref="e")
    task = Task("t2", "Sum of the series with even terms?", sig, lambda a: 1.0 if a == "9" else 0.0, "executed")
    sham = sham_brief(led, task, "P:applied", 200, seed=1, n_items=2)["text"]
    assert len(sham) == 200 and sham.count("\n- ") == 2 and "overcounts" not in sham and "answer is 9" not in sham               # never the task's verified (or own) items
    assert "rumour" not in sham and "falsified" not in sham                                          # clean placebo: no misinformation
    assert sham == sham_brief(led, task, "P:applied", 200, seed=1, n_items=2)["text"]
    seen = []
    res = run_pair(task, work=scripted(seen, n_critique=False), ledger=led, tag="P", sham=True, seed=7)
    assert res["applied"]["retrieved"] == [good] and res["sham"]["retrieved"] == [] and res["control"]["brief_chars"] == 0
    assert res["sham"]["brief_chars"] == res["applied"]["brief_chars"] > 0 
    assert res["applied"]["brief_items"] == res["sham"]["sham_brief"]["target_items"] == 1 and res["sham"]["brief_items"] == 2   # pool claims too short: length wins
    assert sorted(res["order"]) == ["applied", "control", "sham"] and res["order"] == run_pair(task, work=scripted([], n_critique=False), ledger=led, tag="Q",
                                                                                                sham=True, seed=7)["order"]
    sham_prompts = [p for a, s, p in ((a, s, p) for a in ("sham",) for s, p in res["prompts"][a]) if s == "solve"]
    assert sham_prompts and not any("overcounts" in p for p in sham_prompts) and led.status(own)["retrievals"] == 0
    refs = [f"t{i}" for i in range(10)]
    assert task_order(refs, 3) == task_order(refs, 3) != task_order(refs, 4) and sorted(task_order(refs, 3)) == refs
    tasks = [Task(r, "Sum?", sig, lambda a: 0.0, "executed") for r in ("a", "b", "c")]
    out = run_transfer(tasks, seed=3, tag="X", work=scripted([]), ledger=Ledger(tmp_path / "x.jsonl"), sham=True)
    assert out["order"] == task_order(["a", "b", "c"], 3) == [p["task"] for p in out["pairs"]]
