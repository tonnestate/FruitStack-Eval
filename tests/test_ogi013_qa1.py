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


def test_controlled_answer_uses_only_a_valid_logged_decision_and_existing_candidates():
    closing = {"rule": "CONSENSUS", "final_model": "S1", "final_answer": "B"}
    assert q1.controlled_answer(closing, {"A", "B"}) == ("B", "controller:CONSENSUS")
    with pytest.raises(ValueError, match="inadmissible"):
        q1.controlled_answer({**closing, "final_answer": "C"}, {"A", "B"})
    with pytest.raises(ValueError, match="inadmissible"):
        q1.controlled_answer({**closing, "final_answer": None}, {None, "A"})
    with pytest.raises(ValueError, match="valid closing"):
        q1.controlled_answer({**closing, "rule": "UNRECOGNIZED"}, {"A", "B"})
    with pytest.raises(ValueError, match="valid closing"):
        q1.controlled_answer(None, {"A", "B"})
    with pytest.raises(ValueError, match="valid closing"):
        q1.controlled_answer([closing], {"A", "B"})


def test_normal_team_arm_activates_brother_controller(monkeypatch, tmp_path):
    calls = []

    def run_team(ctx, question, *, loop=False):
        calls.append(loop)
        return {"letter": "A", "correct": True}

    monkeypatch.setattr(q1, "run_T", run_team)
    monkeypatch.setattr(q1, "load_jsonl", lambda _path: [])
    rows = []
    ctx = type("Ctx", (), {"outage": type("OutageState", (), {"tripped": False})(), "out": tmp_path})()
    q1.process_question(ctx, {"id": "q1", "key": "A"}, {"T"}, set(), rows.append)
    assert calls == [True]
    assert rows[0]["arm"] == "T" and rows[0]["status"] == "OK"


@pytest.mark.parametrize(
    ("initial", "challenged", "revision", "expected", "expected_rule", "changed", "accepted_concession"),
    [
        ({"model.alpha": "A", "model.beta": "B"}, "A", "B", "B", "FORMAL_CONCESSION_KEEPS_FIRST_ANSWER_CANDIDATE", 1, 1),
        ({"model.alpha": "B", "model.beta": "A"}, "B", "B", "B", "WEIGHTS_DECIDE_UNVERIFIED", 0, 0),
    ],
)
def test_normal_brother_path_corrects_errors_and_resists_false_criticism(
    monkeypatch, tmp_path, initial, challenged, revision, expected, expected_rule, changed, accepted_concession
):
    """Synthetic host/provider: exercise run_T and CherryMe's real closed loop, not only the decision helper."""
    import threading
    from types import SimpleNamespace
    from cherryme import brother

    contribution_decisions = []
    add_contribution = brother._add

    def capture_decision_id(*args, **kwargs):
        contribution_decisions.append(args[3].get("decision_id"))
        return add_contribution(*args, **kwargs)

    monkeypatch.setattr(brother, "_add", capture_decision_id)

    class MangoService:
        def __init__(self):
            self.latest = {}

        def checkpoint(self, work_ref, actor_id, kind, body, *, turn_id):
            self.latest[work_ref] = {"progressive": {"latest_checkpoint": {"kind": kind, "payload": body}}}

        def work_context(self, work_ref):
            return self.latest.get(work_ref, {})

    class Episode:
        def __init__(self):
            self.work, self.actor, self.turn_id, self.sid = "synthetic-work", "synthetic-actor", "synthetic-turn", "synthetic-session"
            self.claim, self.stats = SimpleNamespace(id="claim-1"), {"tokens_in": 0, "tokens_out": 0}
            self.timing = SimpleNamespace(report=lambda: {})
            self.lock, self.events, self.calls = threading.Lock(), [], 0

        def fork(self):
            return self

        def event(self, name, **details):
            self.events.append((name, details))

        def _flags(self):
            return {}

        def step(self, prompt, tag, *, exclude=(), prefer=None, **_kwargs):
            if "single word READY" in prompt:
                model = prefer or next((m for m in ("model.alpha", "model.beta") if m not in exclude), "model.alpha")
            else:
                model = prefer or "model.critic"
            with self.lock:
                self.calls += 1
                self.stats["tokens_in"] += len(prompt.split())
                self.stats["tokens_out"] += 2
            if "single word READY" in prompt:
                output = "READY"
            elif "Solve the task yourself, independently." in prompt:
                output = f"ANSWER: {initial[model]}"
            elif "Your earlier solution:" in prompt:
                    output = f"O1: the supplied task facts support the revision.\nANSWER: {revision}"
            elif "A colleague proposed this solution (UNVERIFIED):" in prompt:
                import re
                match = re.search(r"--- colleague solution ---\s*(.*?)\s*--- end ---", prompt, re.S)
                target = q1.parse_letter(match.group(1) if match else "", 2)
                if target == challenged:
                    other = "B" if target == "A" else "A"
                    output = (f"ISSUES: FOUND\nCLAIM: Answer {target} is incorrect based on the stated task facts.\n"
                              f"EVIDENCE: The supplied task facts support answer {other} as the correct option.\n"
                              f"CONSEQUENCE: Therefore option ({other}) follows instead of option ({target}).")
                else:
                    output = "ISSUES: NONE"
            else:
                output = "ANSWER: B"
            return {"success": True, "output": output,
                    "model_key": model, "independence_key": model, "receipt_id": f"receipt-{model}", "decision_id": f"decision-{self.calls}"}

    (tmp_path / "events").mkdir()
    service, episode = MangoService(), Episode()
    monkeypatch.setattr(q1.time, "sleep", lambda _seconds: None)
    monkeypatch.setattr(q1, "check_budget", lambda _episode: None)
    adapter = SimpleNamespace(service=service, checkpoint=service.checkpoint)
    ctx = SimpleNamespace(out=tmp_path, s_model="model.alpha", luna_tokens=0, stop=None,
                          episode=lambda *_args, **_kwargs: episode,
                          stack=SimpleNamespace(fs=SimpleNamespace(mango=adapter)))

    result = q1.run_T_brother(ctx, {"id": "offline", "question": "Choose the supported option.",
                                    "options": ["A is unsupported", "B is supported"]})

    assert result["letter"] == expected and result["how"].startswith("controller:")
    assert result["loop_closing"]["final_answer"] == result["letter"]
    assert result["loop_closing"]["rule"] == expected_rule, result["loop_closing"]
    assert len(result["loop_closing"]["concessions"]) == changed
    assert result["rounds"] >= 1 and result["objections"] >= 1
    assert result["answer_changes"] == changed and result["accepted_concessions"] == accepted_concession
    assert result["formal_objections"] >= 1 and result["independently_confirmed_objections"] == 0
    assert result["loop_decisions"] and all(d["choice"] in d["options"] for d in result["loop_decisions"])
    assert result["loop_decisions"][0]["choice"] == "CRITIQUE"
    assert result["calls"] > 0 and episode.calls >= result["calls"]  # READY roster checks are included in episode calls, not loop calls
    assert result["tokens"] == episode.stats["tokens_in"] + episode.stats["tokens_out"]
    assert result["mango_writes"] > 0 and result["mango_reads"] > 0
    assert result["roster_models"][:2] == ["model.alpha", "model.beta"]
    assert len(contribution_decisions) >= 2 and all(contribution_decisions)


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
    pytest.importorskip("tau2", reason="needs the official tau2-bench runtime")
    from types import SimpleNamespace
    from ogi013_tau2_agent import Episode
    ep = object.__new__(Episode)
    ep.sid, ep.budget_profile = "s", "qa"
    ep.stack = SimpleNamespace(fs=SimpleNamespace(governance=SimpleNamespace(snapshot=lambda sid: {"tokens_remaining": 60000})))
    max_out, reserve = ep.output_budget("Reply with the single word READY.", {})
    assert max_out == 4096 and reserve >= 4096 + 3000                       # a 33-byte prompt no longer yields a 2081-token reservation
    ep.stack.fs.governance.snapshot = lambda sid: {"tokens_remaining": 5000}
    assert ep.output_budget("x", {})[1] == 5000                             # never more than the session has left


# ---- descriptive trace addendum (synthetic data only; no look at study outcomes) ----------------------------------------------------------------------------------
import analyze_qa1_trace as tr  # noqa: E402


def test_descriptive_trace_addendum_on_synthetic_rows(tmp_path):
    S = "poolside-laguna-s-2.1@default"
    rows = []
    for i in range(6):
        t = {"qid": str(i), "arm": "T", "key": "A", "status": "OK", "correct": i % 2 == 0, "letter": "A" if i % 2 == 0 else "B", "first_letters": {"S1": "B" if i == 0 else "A", "S2": "C" if i == 0 else "A"},
             "stop": "NO_SECOND_SOLVER" if i == 5 else "NO_ISSUES", "answer_changes": 1 if i == 3 else 0, "how": "specialist" if i == 0 else "agreed", "specialist_letter": "A" if i == 0 else None, "roster": {"roster": {"solver1": S}, "changes": []}}
        rows += [t] + [{"qid": str(i), "arm": a, "key": "A", "status": "OK", "correct": (i in (0, 1)) if a == "S" else True} for a in ("E", "S", "L")]
    f = tmp_path / "r.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in rows))
    out = tr.trace(str(f), S)
    assert out["t_stop_reasons"] == {"specialist_decided": 1, "revision_changed_an_answer": 1, "NO_SECOND_SOLVER": 1, "both_solvers_agreed_challenge_found_nothing": 3}
    assert out["final_differs_from_both_first_answers"] == 4                         # question 0 (final A vs B, C) and questions 1, 3, 5 (final B vs A, A)
    assert out["s_pinned_as_solver1_on_every_ok_question"] is True and out["discordant_pairs"]["T vs S"]["discordant_pairs"] > 0


def test_progress_line_contains_counts_only_no_outcome(tmp_path):
    from datetime import datetime, timezone
    import qa1_progress as pg
    rows = [{"qid": str(i), "arm": "TESL"[i % 4], "status": "OK" if i % 5 else "INFRA_FAILED", "correct": True, "letter": "B", "key": "A"} for i in range(40)]
    f = tmp_path / "r.jsonl"
    f.write_text("\n".join(json.dumps(r) for r in rows))
    line = pg.progress(str(f), "2026-10-31T00:00:00Z", now=datetime(2026, 10, 31, 2, 0, tzinfo=timezone.utc))
    assert "rows 40/792" in line and "20.0 rows/h" in line and "ETA 37.6 h" in line and "infra failures 8" in line
    assert "correct" not in line and "letter" not in line and "True" not in line


# ---- QA-1b: systemic-outage rule (deviation D4) ----------------------------------------------------------------------------------------------------------------------------
def _row(qid, arm, ok):
    return {"qid": qid, "arm": arm, "status": "OK" if ok else "INFRA_FAILED"}


def test_outage_isolated_failure_is_written_when_the_arm_succeeds_again():
    o = q1.Outage()
    assert o.offer(_row("1", "S", False)) == ([], [])
    rows, gone = o.offer(_row("2", "S", True))
    assert [r["qid"] for r in rows] == ["1", "2"] and gone == [] and not o.tripped


def test_outage_five_consecutive_failures_discard_and_trip_then_retry_is_final():
    o = q1.Outage()
    for i in range(4):
        assert o.offer(_row(str(i), "T", False)) == ([], [])
    rows, gone = o.offer(_row("4", "T", False))
    assert rows == [] and o.tripped and gone == [(str(i), "T") for i in range(5)]
    o2 = q1.Outage(retried=gone)                                        # fresh process: a retried pair that fails again is final at once
    rows, gone2 = o2.offer(_row("0", "T", False))
    assert [r["qid"] for r in rows] == ["0"] and gone2 == [] and not o2.tripped


def test_outage_streaks_are_per_arm():
    o = q1.Outage()
    for i in range(4):
        o.offer(_row(str(i), "S", False))
        o.offer(_row(str(i), "E", False))
    assert not o.tripped


def test_chain_stages_stop_at_the_first_missing_stage():
    row = {"first_letters": {"S1": "A", "S2": "B"}, "independent_grounded_objections": 1, "evidenced_replies": 1, "answer_changes": 0, "evidenced_withdrawn": 0, "letter": "A"}
    assert q1.chain_stages(row)["reached"] == "abc" and not q1.chain_stages(row)["complete"]
    row["evidenced_withdrawn"] = 1
    assert q1.chain_stages(row)["complete"]
    assert q1.chain_stages({"first_letters": {"S1": "A"}})["reached"] == "-"


def test_chain_needs_independent_lineages_and_is_classified_against_the_key():
    row = {"first_letters": {"S1": "A", "S2": "B"}, "independent_grounded_objections": 0, "grounded_objections": 1, "evidenced_replies": 1, "answer_changes": 1, "letter": "A"}
    assert q1.chain_stages(row)["reached"] == "a"                        # an objection from the judged position's own lineage does not count
    ok = {"key": "A", "letter": "A", "first_by_pos": {"S1": "B", "S2": "A"}, "objection_target_first": ["A"]}
    assert q1.chain_class(ok) == "IMPROVING"
    assert q1.chain_class({**ok, "first_by_pos": {"S1": "A", "S2": "A"}}) == "PROTECTIVE"
    assert q1.chain_class({**ok, "letter": "C"}) == "HARMFUL"
    assert q1.chain_class({"key": "A", "letter": "C", "first_by_pos": {"S1": "B", "S2": "D"}, "objection_target_first": []}) == "NEUTRAL"


# ---- owner concession rule and the three labels ---------------------------------------------------------------------------------------------------------------------
def test_concession_counts_only_when_independent_substantive_named_and_changed():
    o = {"id": "O1", "lineage": "qwen3.5", "ground": {"level": "formal"}}
    assert q1.accepted_concession("O1 is right, the matrix is block triangular. ANSWER: H", o, "qwen2.5", "D", "H")
    assert not q1.accepted_concession("O1 is right. ANSWER: H", {**o, "ground": {"level": "reproduced"}}, "qwen2.5", "D", "H")
    assert not q1.accepted_concession("You are right. ANSWER: H", o, "qwen2.5", "D", "H")                       # does not name the objection
    assert not q1.accepted_concession("O1 is right. ANSWER: D", o, "qwen2.5", "D", "D")                       # no position change
    assert not q1.accepted_concession("O1 is right. ANSWER: H", o, "qwen3.5", "D", "H")                        # same lineage: not independent
    assert not q1.accepted_concession("O1 is right. ANSWER: H", {**o, "ground": {"level": None}}, "qwen2.5", "D", "H")   # not substantive


def test_stage_c_accepts_an_accepted_concession_and_the_labels_stay_separate():
    row = {"first_letters": {"S1": "H", "S2": "D"}, "independent_grounded_objections": 1, "evidenced_replies": 0, "accepted_concessions": 1, "answer_changes": 1, "letter": "H",
           "key": "H", "first_by_pos": {"S1": "H", "S2": "D"}, "objection_target_first": ["D"], "verified_objections": 0, "verified_replies": 0}
    assert q1.chain_stages(row)["complete"]
    assert q1.chain_labels(row) == {"CRITIQUE_ACCEPTED": True, "INDEPENDENTLY_VERIFIED": False, "QUALITY_IMPROVED": True}
    assert q1.chain_labels({**row, "verified_objections": 1})["INDEPENDENTLY_VERIFIED"] is False
    assert q1.chain_labels({**row, "independently_confirmed_objections": 1})["INDEPENDENTLY_VERIFIED"] is True
    assert not q1.chain_stages({**row, "accepted_concessions": 0})["complete"]
