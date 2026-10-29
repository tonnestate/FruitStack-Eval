"""COLLAB-1 evaluator on a synthetic campaign (recorded-evidence shapes, no model, no network): exact McNemar + Holm, missing episodes, decision outcomes, determinism, evaluator-only reference."""
import json
from pathlib import Path

from ogi013_pilot_fixtures import ROOT, load, receipt, write_arm

C1 = ROOT / "evidence/ogi013-collab1"
an = load("analyze_study", C1 / "analyze_study.py")
BOOK = {"name": "book_reservation", "arguments": {"user_id": "u"}}
CANCEL = {"name": "cancel_reservation", "arguments": {"reservation_id": "R"}}
CONDS = ["SINGLE", "COLLAB", "SINGLE-E"]


def data_dir(tmp, n):
    d = tmp / "data/domains/airline"
    d.mkdir(parents=True)
    (d / "tasks.json").write_text(json.dumps([{"id": i, "evaluation_criteria": {"actions": [BOOK]}} for i in range(1, n + 1)]))
    return tmp / "data"


def manifest(n, nowrite=0):
    tasks = [{"stratum": "write-opportunity", "domain": "airline", "task_id": str(i), "task_ref": f"airline:{i}", "order": CONDS} for i in range(1, n + 1)]
    tasks += [{"stratum": "no-write-control", "domain": "airline", "task_id": str(100 + i), "task_ref": f"airline:{100 + i}", "order": CONDS} for i in range(nowrite)]
    return {"study": "T", "conditions": CONDS, "tasks": tasks, "single_e": {"k": 3, "scope": "writes"}}


BUDGET = {"reserve_tokens_per_dispatch": 4000}


def make_episode(C, task, cond, *, reward, calls, review=None, status="DONE", tokens=1000, attempts=1, official=True, termination="user_stop"):
    tid = task.split(":")[1]
    d = C / task.replace(":", "_") / cond
    rec = {"task": task, "condition": cond, "status": status, "started_at": 100.0, "ended_at": 160.0}
    (d.parent).mkdir(parents=True, exist_ok=True)
    (d.parent / f"{cond}.episode.json").write_text(json.dumps(rec))
    r = receipt(tin=tokens, tout=0)
    r["metadata"] = {"provider_attempt_count": attempts}
    write_arm(C.parent, f"{C.name}/{task.replace(':', '_')}/{cond}", [r])
    if not official:
        return
    msgs, n = [], 0
    for c in calls:
        n += 1
        msgs += [{"role": "assistant", "tool_calls": [{"id": f"c{n}", "name": c["name"], "arguments": c["arguments"]}]}, {"role": "tool", "id": f"c{n}", "content": "ok", "error": False}]
    tdir = d / "tasks" / tid
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / "official-result.json").write_text(json.dumps({"termination_reason": termination, "messages": msgs, "reward_info": {"reward": reward, "db_check": {"db_match": reward == 1.0}, "nl_assertions": None}}))
    ev = []
    if review:
        ev.append({"event": "ORG_COLLAB", "purpose": "consequential_effect", "changed": review["changed"], "independent_review": True, "final_reviewed": True, "calls": 3,
                   "trail": [{"stage": "SOLUTION", "text": json.dumps({"action": "tool", **review["draft"]})}, {"stage": "REVISION", "text": json.dumps({"action": "tool", **review["final"]})}]})
    (tdir / "fruitstack-events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in ev))


def campaign(tmp, n=10, outcomes=None):
    C = tmp / "runs" / "collab1"
    for i in range(1, n + 1):
        t = f"airline:{i}"
        for cond in CONDS:
            ok = (outcomes or {}).get((i, cond), cond == "COLLAB")
            review = {"changed": True, "draft": CANCEL, "final": BOOK} if cond == "COLLAB" and ok else None
            make_episode(C, t, cond, reward=1.0 if ok else 0.0, calls=[BOOK] if ok else [CANCEL], review=review, attempts=3 if cond == "COLLAB" else 1)
    return C


def test_confirmatory_tests_use_exact_mcnemar_and_holm(tmp_path):
    C = campaign(tmp_path, 10)                                                      # COLLAB succeeds on all 10, SINGLE and SINGLE-E on none
    rep = an.evaluate(C, manifest(10), BUDGET, data_dir(tmp_path, 10))
    e1 = rep["confirmatory"]["E1"]
    assert e1["a_only"] == 10 and e1["b_only"] == 0 and abs(e1["p_exact_mcnemar_two_sided"] - 2 * 0.5 ** 10) < 1e-6 and abs(e1["p_holm"] - 3 * 2 * 0.5 ** 10) < 1e-5
    assert rep["confirmatory"]["E2"]["a_only"] == 10
    e3 = rep["confirmatory"]["E3"]                                                  # SINGLE executed an unexpected cancel on every task, COLLAB none
    assert e3["a_only"] == 10 and e3["discordant"] == 10
    assert rep["decision_outcomes"] == {"PREVENTED_WRITE_ERROR": 10} and len(rep["critique_helped"]) == 10 and rep["critique_made_worse"] == []
    assert rep["resources"]["COLLAB"]["requests"] == 30 and rep["resources"]["SINGLE"]["requests"] == 10          # one receipt behind three provider requests counts three


def test_equal_outcomes_are_inconclusive_and_missing_episodes_are_non_success(tmp_path):
    out = {(i, c): True for i in range(1, 7) for c in CONDS}
    C = campaign(tmp_path, 6, out)
    for cond in ("SINGLE",):                                                          # one missing and one never-graded episode in SINGLE
        (C / "airline_1" / f"{cond}.episode.json").unlink()
        import shutil
        shutil.rmtree(C / "airline_1" / cond)
    (C / "airline_2" / "SINGLE" / "tasks" / "2" / "official-result.json").unlink()
    rep = an.evaluate(C, manifest(6), BUDGET, data_dir(tmp_path, 6))
    e1 = rep["confirmatory"]["E1"]
    assert e1["a_only"] == 2 and e1["b_only"] == 0 and rep["episode_status"].get("MISSING") == 1               # missing/ungraded SINGLE = non-success against a COLLAB success
    assert rep["confirmatory"]["E3"]["excluded_pairs"] == 2 and rep["confirmatory"]["E2"]["p_exact_mcnemar_two_sided"] == 1.0
    assert not rep["confirmatory"]["E2"]["significant_at_0.05"]


def test_correct_actions_blocked_and_error_replacements_are_reported(tmp_path):
    C = tmp_path / "runs" / "collab1"
    for cond in CONDS:
        make_episode(C, "airline:1", cond, reward=0.0, calls=[CANCEL], review={"changed": True, "draft": BOOK, "final": CANCEL} if cond == "COLLAB" else None)       # correct draft rejected, replaced by a wrong write
    rep = an.evaluate(C, manifest(1), BUDGET, data_dir(tmp_path, 1))
    assert rep["decision_outcomes"] == {"CORRECT_BLOCKED": 1} and rep["critique_made_worse"] == [{"task": "airline:1", "outcome": "CORRECT_BLOCKED"}]
    assert rep["decision_quality"]["COLLAB"]["state_changing_deviation_episodes"] == 1


def test_report_is_deterministic_and_the_reference_stays_in_the_evaluator(tmp_path):
    C = campaign(tmp_path, 4)
    m, d = manifest(4), data_dir(tmp_path, 4)
    an.write_report(C, m, BUDGET, d)
    first = (C / "report.json").read_bytes(), (C / "report.md").read_bytes()
    an.write_report(C, m, BUDGET, d)
    assert first == ((C / "report.json").read_bytes(), (C / "report.md").read_bytes())
    for src in (ROOT / "runners").glob("*.py"):                                      # no agent/runner code reads the reference actions or imports the metrics
        text = src.read_text()
        assert "evaluation_criteria" not in text and "decision_metrics" not in text, src.name


def test_the_simulator_layer_waits_only_for_a_short_plummereported_window_of_the_pinned_route():
    text = (ROOT / "runners" / "ogi013_sim_supply.py").read_text()
    assert "MAX_WAIT_S" not in text and text.count("time.sleep") == 1 and "PINNED_RETRY_WINDOW_S" in text


def test_an_operator_terminated_first_episode_is_archived_and_the_block_chooses_its_simulator_afresh(tmp_path, monkeypatch):
    import argparse
    ns = load("run_collab1", C1 / "run_collab1.py")
    base = tmp_path / "base"
    (base / "runs/collab1/discarded").mkdir(parents=True)
    (base / "runs/collab1/campaign.json").write_text(json.dumps({"started_at": 4e9}))
    a = argparse.Namespace(approval="x", base=str(base), budget=str(C1 / "collab1_budget.json"), manifest=str(C1 / "study_manifest_v2.json"), campaign="collab1", only=None, plan=False)
    camp = ns.Campaign(a)
    task = next(t for t in camp.manifest["tasks"])
    ref, d = task["task_ref"], task["task_ref"].replace(":", "_")
    first = task["order"][0]
    (camp.R / f"collab1-{d}.route").write_text('{"model_key": "unusable@default"}')
    (camp.C / d / first).mkdir(parents=True)
    camp.write_rec(ref, first, status="OPERATOR_TERMINATED_INFRA", task=ref, condition=first)
    ran = []
    monkeypatch.setattr(camp, "run_episode", lambda t, cond, attempt: ran.append(cond) or (camp.write_rec(t["task_ref"], cond, status="DONE"), "DONE")[1])
    assert camp.run_block(task) == "DONE" and ran == task["order"]                                  # the block is run again in full, nothing completed is repeated
    assert not (camp.R / f"collab1-{d}.route").exists()                                             # the unusable simulator model is not pinned any more
    archived = list((camp.C / "discarded").glob(f"{d}-operator-infra*/{d}/{first}.episode.json"))
    assert archived and json.loads(archived[0].read_text())["archived_as"].startswith("operator-infra")


def test_simulator_suitability_is_decided_from_the_model_id_alone():
    import sys
    sys.path.insert(0, str(ROOT / "evidence/ogi013-collab1"))
    from supply_gate import simulator_suitable
    assert all(simulator_suitable(m) for m in ("gpt-oss-120b", "llama-3.3-70b", "qwen3.5-397b", "north-mini-code", "dots3-note-preview", "mistral-small-3.2-24b"))
    assert not any(simulator_suitable(m) for m in ("qwen3guard-gen-0.6b", "qwen3.5-0.8b", "llama-3-2-1b-instruct", "gemma-4-e4b-uncensored-aggressive", "lfm2.5-2.6b"))
