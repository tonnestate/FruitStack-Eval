"""T = the full FruitStack team through CherryMe's research path (fs_org_driver.run_team): component switches, ablation rows, identity guard on auxiliary calls,
token parity. Offline: scripted workers, no provider call; the visible check is host code, never the grader."""
import pytest

pytest.importorskip("cherryme.research_tree")
pytest.importorskip("appleme")

from runners.fs_org_driver import TEAM_COMPONENTS, Task, run_samples, run_team  # noqa: E402
from runners.ogi013_learning_hook import LearningHook  # noqa: E402
from runners.ogi013_org_discoveries import Ledger  # noqa: E402

ROSTER = {"L-model": "luna", "N-model": "nemotron"}
LINEAGE = {"L-model": "luna", "N-model": "nemotron", "X-model": "outsider"}


def sig(text):
    for line in reversed((text or "").splitlines()):
        if line.startswith("ANSWER:"):
            return line.split(":", 1)[1].strip()
    return None


def scripted(seen, outsider_stage=None):
    """prefer wins; otherwise the first roster member whose lineage is not excluded (stands in for PlumMe's AUTO pick). L solves 7, N solves 9, N's critique finds the
    error, L concedes. `outsider_stage`: that stage's calls are served by a model outside the roster."""
    def work(prompt, stage, prefer=None, exclude=()):
        seen.append((stage, prompt, prefer))
        who = prefer or next(m for m in ROSTER if ROSTER[m] not in exclude)
        if outsider_stage and stage.startswith(outsider_stage):
            who = "X-model"
        out = {"solve": "ANSWER: 7" if who == "L-model" else "ANSWER: 9",
               "challenge": "ISSUES: FOUND\nthe even terms are counted twice\nANSWER: 9" if who != "L-model" else "ISSUES: NONE",
               "revise": "ANSWER: 9", "specialist": "ANSWER: 9"}.get(stage.split(":")[0],
                                                                    "HYPOTHESIS: the sum is 9\nRATIONALE: recount the terms\nTEST: add the series term by term")
        return {"success": True, "output": out, "model_key": who, "independence_key": LINEAGE[who], "receipt_id": f"r{len(seen)}", "input_tokens": 100, "output_tokens": 10}
    return work


def task(check=True):
    return Task("t1", "Sum the series. Final line: ANSWER: <n>", sig, lambda a: float(a == "9"), "executed",
                check=(lambda cand: f"visible test sum([1,2,6]) -> {sig(cand)}") if check else None)


def team(tmp_path, seen, components=TEAM_COMPONENTS, **kw):
    hook = LearningHook(Ledger(tmp_path / "learning.jsonl"), run_id="run-1", apply=True)
    return run_team(task(kw.pop("check", True)), work=scripted(seen, kw.pop("outsider_stage", None)), hook=hook, roster=ROSTER, components=components, **kw)


def types(row):
    return {e["type"] for e in row["events"]}


MARKERS = {"appleme": {"COGNITIVE_DIAGNOSIS", "ADVICE_APPLIED"}, "lsd": {"LSD_ROOM"}, "research_tree": {"RESEARCH_STARTED", "RESEARCH_FINALIZED", "ADVICE_APPLIED"},
           "memory": {"MEMORY_BRIEF"}, "executed_critique": {"EXECUTED_CRITIQUE"}, "plumme_selection": set()}


def test_the_full_team_runs_every_component(tmp_path):
    seen = []
    row = team(tmp_path, seen)
    assert row["arm"] == "T" and row["ablated"] is None and row["components"] == sorted(TEAM_COMPONENTS)
    assert set().union(*MARKERS.values()) <= types(row)
    assert {"lsd", "solve", "challenge", "revise"} <= set(row["stages"])
    assert row["answer"] == "9" and row["identity_valid"] is True
    assert next(e for e in row["events"] if e["type"] == "SELECTION")["mode"] == "plumme"
    assert next(e for e in row["events"] if e["type"] == "COGNITIVE_DIAGNOSIS")["source"] == "research_tree"


@pytest.mark.parametrize("component", sorted(TEAM_COMPONENTS))
def test_each_ablation_turns_exactly_its_component_off_and_records_it(tmp_path, component):
    seen = []
    row = team(tmp_path, seen, components=TEAM_COMPONENTS - {component})
    assert row["arm"] == f"T-{component}" and row["ablated"] == component and component not in row["components"]
    assert row["identity_valid"] is True
    present = types(row)
    assert not (MARKERS[component] & present)
    for other in TEAM_COMPONENTS - {component}:                     # every other component still leaves its events
        expected = MARKERS[other] - (MARKERS[component] if component != "research_tree" else {"ADVICE_APPLIED"})
        assert expected <= present, (other, expected - present)
    if component == "lsd":
        assert "lsd" not in row["stages"]
    if component == "research_tree":                                # AppleMe stays on, through CherryMe's tree-free AdvisoryControl
        assert next(e for e in row["events"] if e["type"] == "COGNITIVE_DIAGNOSIS")["source"] == "AdvisoryControl"
    if component == "plumme_selection":
        assert next(e for e in row["events"] if e["type"] == "SELECTION")["mode"] == "fixed_roster"
        assert all(r["prefer"] in ROSTER for r in row["receipts"])
    if component == "executed_critique":
        assert not any("EXECUTED" in p for s, p, _ in seen if s == "challenge")
    if component == "memory":
        assert row["brief_chars"] == 0 and row["captured"] == []


def test_executed_critique_shows_the_visible_check_to_the_critic_and_marks_it_executed(tmp_path):
    seen = []
    row = team(tmp_path, seen)
    challenges = [p for s, p, _ in seen if s == "challenge"]
    assert challenges and all("visible test sum([1,2,6])" in p for p in challenges)
    assert row["executed_critique"] == "ON"
    row = team(tmp_path, [], check=False)
    assert row["executed_critique"] == "NO_VISIBLE_CHECK" and "EXECUTED_CRITIQUE" not in types(row)


def test_plumme_selection_leaves_the_pick_to_the_worker(tmp_path):
    row = team(tmp_path, [])
    assert any(r["prefer"] is None for r in row["receipts"] if r["stage"] in ("solve", "challenge") or r["stage"].startswith("lsd"))


@pytest.mark.parametrize("stage", ["lsd", "challenge", "revise"])
def test_the_identity_guard_covers_auxiliary_calls(tmp_path, stage):
    row = team(tmp_path, [], outsider_stage=stage)
    assert row["identity_valid"] is False and row["exclusion"] == "INFRA_IDENTITY:LINEAGE_OUTSIDE_ROSTER"


def test_more_than_one_component_off_needs_an_explicit_arm(tmp_path):
    with pytest.raises(ValueError):
        team(tmp_path, [], components=TEAM_COMPONENTS - {"lsd", "appleme"})
    with pytest.raises(ValueError):
        team(tmp_path, [], components=TEAM_COMPONENTS | {"oracle"})


def test_token_parity_with_the_controls_is_computed_from_receipts(tmp_path):
    row = team(tmp_path, [])
    budget = row["tokens"]["input"] + row["tokens"]["output"]
    assert row["tokens"]["calls_without_tokens"] == 0 and budget == 110 * row["calls"]
    ctl = run_samples(task(), work=scripted([]), arm="E_div", roster=ROSTER, cycle=list(ROSTER), k=row["calls"], token_budget=budget)
    spent = ctl["tokens"]["input"] + ctl["tokens"]["output"]
    assert budget <= spent < budget + 110 and ctl["identity_valid"] is True
