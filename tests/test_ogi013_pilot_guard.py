"""Fail-closed pilot guard (evidence/ogi013-pilot/pilot_guard.py): approval gate, ONE dispatch list (no simulator double count), unknown usage / unknown cash exposure / failure streaks halt, caps
(per arm, cumulative, wall), the pre-dispatch check, the shared session ceilings and a real process-group stop. Synthetic receipts, no inference."""
import hashlib
import json
import subprocess
import sys
import time

from ogi013_pilot_fixtures import ARMS, BUDGET, RESERVE, guard, receipt, write_arm


def test_approval_must_name_exactly_this_budget(tmp_path):
    b = tmp_path / "b.json"
    b.write_text('{"x": 1}')
    ok, bad = tmp_path / "ok", tmp_path / "bad"
    ok.write_text(hashlib.sha256(b.read_bytes()).hexdigest() + "  approved by owner\n")
    bad.write_text("0" * 64)
    assert guard.verify_approval(str(b), str(ok)) and not guard.verify_approval(str(b), str(bad)) and not guard.verify_approval(str(b), str(tmp_path / "missing"))
    assert guard.main(["x", "verify-approval", str(b), str(tmp_path / "missing")]) == 2        # no approval = refusal, never a default


def test_a_simulator_dispatch_is_counted_once_not_twice(tmp_path):
    agent = [receipt(tin=1000, tout=100) for _ in range(6)]
    sim = [receipt(tin=500, tout=50) for _ in range(4)]
    write_arm(tmp_path, ARMS[0], agent + sim, sim_ids=[r["receipt_id"] for r in sim])         # PlumMe wrote ALL ten receipts; sim-usage lists four of them again
    u = guard.usage(str(tmp_path), [ARMS[0]])
    assert u["dispatches"] == 10 and u["tokens"] == 6 * 1100 + 4 * 550                         # the old accounting said 14 and 8,800
    assert [r["simulator"] for r in guard.dispatches(str(tmp_path), ARMS[0])].count(True) == 4
    write_arm(tmp_path, ARMS[0], agent, sim_extra=[{"receipt_id": "orphan", "success": True, "input_tokens": 70, "output_tokens": 7}])     # a simulator row WITHOUT a receipt is still counted ...
    u = guard.usage(str(tmp_path), [ARMS[0]])
    assert u["dispatches"] == 7 and u["unknown_cash_exposure"] == 1                              # ... and its cash exposure is unknown (halts)


def test_a_successful_dispatch_without_usage_halts_and_is_never_counted_as_zero(tmp_path):
    write_arm(tmp_path, ARMS[0], [receipt(), receipt(usage=False), receipt(tin=0, tout=0)])
    u = guard.usage(str(tmp_path), ARMS, RESERVE)
    assert u["receipts_without_usage"] == 2 and u["dispatches"] == 3
    assert any(w.startswith("MISSING_USAGE") for w in guard.exceeded(BUDGET, u))
    assert any(w.startswith("MISSING_USAGE") for w in guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]))


def test_failed_dispatches_are_charged_by_what_is_known_about_them(tmp_path):
    rows = [receipt(), receipt(ok=False, failure="RATE_LIMITED", usage=False), receipt(ok=False, failure="MODEL_NOT_FOUND", usage=False),
            receipt(ok=False, failure="TIMEOUT", usage=False), receipt(ok=False, failure="PROVIDER_UNAVAILABLE", usage=False), receipt(ok=False, failure="SEMANTIC_OUTPUT_FAILURE", tin=300, tout=30)]
    write_arm(tmp_path, ARMS[0], rows)
    u = guard.usage(str(tmp_path), ARMS, RESERVE)
    assert u["rejected_unprocessed"] == 2                                                        # rejected before processing (PlumMe's own REJECTION_CLASSES): known zero tokens
    assert u["unmetered_failures"] == 2 and u["tokens"] == 110 + 330 + 2 * RESERVE               # timeouts / unavailable are UNCERTAIN: charged the reserve, never 0
    assert guard.usage(str(tmp_path), ARMS)["tokens"] == 440                                     # (the plain CLI view without a reserve reports only what was recorded)


def test_cash_exposure_is_known_zero_or_it_halts_and_entitlements_are_reported(tmp_path):
    write_arm(tmp_path, ARMS[0], [receipt(cost_class="ANONYMOUS_FREE"), receipt(cost_class="TRIAL_CREDIT"), receipt(cost_class="INCLUDED", tin=50, tout=5)])
    u = guard.usage(str(tmp_path), ARMS)
    assert u["unknown_cash_exposure"] == 0 and u["cash_usd"] == 0.0 and u["entitlement"] == {"TRIAL_CREDIT": {"dispatches": 1, "tokens": 110}, "INCLUDED": {"dispatches": 1, "tokens": 55}}
    assert guard.exceeded(BUDGET, u) == []
    for bad in (receipt(cost_class=None), receipt(cost_class="UNKNOWN"), receipt(cost_class="NORMAL")):             # unknown or paid class, no recorded cost: exposure cannot be shown to be zero
        write_arm(tmp_path, ARMS[0], [bad])
        assert any(w.startswith("UNKNOWN_CASH_EXPOSURE") for w in guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS)))
    write_arm(tmp_path, ARMS[0], [receipt(cost_class="NORMAL", cost_usd=0.002)])                  # a recorded cost is known - and above the authorised 0.00
    assert any(w.startswith("cash 0.002000") for w in guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS)))


def test_a_failure_streak_stops_the_retries_and_a_success_resets_it(tmp_path):
    limit = BUDGET["max_consecutive_failures"]
    fails = [receipt(ok=False, usage=False) for _ in range(limit)]
    write_arm(tmp_path, ARMS[0], [receipt()] + fails[: limit - 1])
    assert guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS)) == []
    write_arm(tmp_path, ARMS[0], [receipt()] + fails)
    assert any("consecutive failed dispatches" in w for w in guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]))
    write_arm(tmp_path, ARMS[0], fails[: limit - 1] + [receipt()] + fails[: limit - 1])             # two streaks of limit-1 separated by a success never reach the limit
    assert guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS)) == []


def test_caps_are_detected_per_arm_cumulatively_and_by_wall_clock(tmp_path):
    cap = BUDGET["arms"][ARMS[0]]["max_dispatches"]
    write_arm(tmp_path, ARMS[0], [receipt() for _ in range(cap + 1)])                             # over the SINGLE arm cap, under the cumulative cap
    assert any(f"arm {ARMS[0]} over its cap" in w for w in guard.exceeded(BUDGET, guard.usage(str(tmp_path), [ARMS[0]])))      # keyed by the REAL arm directory: it used to never match
    write_arm(tmp_path, ARMS[1], [receipt() for _ in range(BUDGET["arms"][ARMS[1]]["max_dispatches"] + 1)])
    assert any(w.startswith("dispatches") for w in guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS)))
    assert guard.exceeded(BUDGET, {"dispatches": 1, "tokens": 1, "per_arm": {}}, started_at=time.time() - (BUDGET["cumulative"]["max_wall_minutes"] + 1) * 60) == ["wall clock over the cap"]


def test_precheck_refuses_the_dispatch_that_would_cross_a_cap(tmp_path):
    cap = BUDGET["arms"][ARMS[0]]["max_dispatches"]
    write_arm(tmp_path, ARMS[0], [receipt() for _ in range(cap - 1)])
    assert guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]) == []                             # dispatch number `cap` is still allowed
    write_arm(tmp_path, ARMS[0], [receipt() for _ in range(cap)])
    why = guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0])
    assert why and all("would exceed" in w for w in why) and not guard.exceeded(BUDGET, guard.usage(str(tmp_path), ARMS))      # nothing is over yet: the NEXT dispatch is what is refused
    tok_cap = BUDGET["arms"][ARMS[0]]["max_tokens"]
    write_arm(tmp_path, ARMS[0], [receipt(tin=tok_cap - RESERVE, tout=1)])                         # the reserve for the next dispatch would cross the token cap
    assert any("tokens" in w and "would exceed" in w for w in guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]))
    write_arm(tmp_path, ARMS[0], [receipt(tin=tok_cap - RESERVE - 2, tout=1)])
    assert guard.precheck(BUDGET, str(tmp_path), ARMS, ARMS[0]) == []


def test_pilot_cap_binds_on_its_own_and_unknown_arms_or_reserves_refuse(tmp_path):
    tight = {**BUDGET, "cumulative": {**BUDGET["cumulative"], "max_dispatches": 100}}
    write_arm(tmp_path, ARMS[0], [receipt() for _ in range(40)])
    write_arm(tmp_path, ARMS[1], [receipt() for _ in range(59)])
    assert guard.precheck(tight, str(tmp_path), ARMS, ARMS[1]) == []
    write_arm(tmp_path, ARMS[1], [receipt() for _ in range(60)])
    assert any(w.startswith("pilot: next dispatch would exceed 100") for w in guard.precheck(tight, str(tmp_path), ARMS, ARMS[1]))
    assert any("no cap" in w for w in guard.precheck(BUDGET, str(tmp_path), ARMS, "pilot-1/other"))
    assert guard.precheck({k: v for k, v in BUDGET.items() if k != "reserve_tokens_per_dispatch"}, str(tmp_path), ARMS, ARMS[0]) == ["budget declares no reserve_tokens_per_dispatch (fail closed)"]


def test_the_session_ceilings_come_from_the_same_budget_file(tmp_path, capsys):
    env = guard.session_env(BUDGET, ARMS[1])
    assert env == {"OGI013_SESSION_MAX_CALLS": str(BUDGET["arms"][ARMS[1]]["max_dispatches"]), "OGI013_SESSION_MAX_TOKENS": str(BUDGET["arms"][ARMS[1]]["max_tokens"]),
                   "OGI013_SESSION_MAX_COST_USD": "0.0"}                                         # authorised cash is 0.00, not "unset"
    path = tmp_path / "b.json"
    path.write_text(json.dumps(BUDGET))
    assert guard.main(["x", "env", str(path), ARMS[0]]) == 0 and "export OGI013_SESSION_MAX_CALLS=" in capsys.readouterr().out


def test_watch_stops_the_running_process_group_and_keeps_the_evidence(tmp_path, monkeypatch):
    write_arm(tmp_path, ARMS[0], [receipt() for _ in range(BUDGET["arms"][ARMS[0]]["max_dispatches"] + 5)])
    budget = tmp_path / "budget.json"
    budget.write_text(json.dumps(BUDGET))
    victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"], start_new_session=True)
    (tmp_path / "pids").write_text(str(victim.pid))
    monkeypatch.setenv("PILOT_POLL_S", "0.1")
    rc = guard.main(["x", "watch", str(budget), str(tmp_path), str(tmp_path / "pids"), ARMS[0]])
    victim.wait(timeout=10)
    assert rc == 3 and victim.returncode is not None and json.loads((tmp_path / "PILOT_HALT").read_text())["by"] == "watch"
    assert (tmp_path / ARMS[0] / "fruitstack/plumme-state/receipts.jsonl").is_file()                # nothing was deleted


def test_a_receipt_counts_as_all_the_provider_requests_behind_it(tmp_path):
    from ogi013_pilot_fixtures import ARMS, BUDGET, receipt, write_arm
    r = receipt(tin=100, tout=10)
    r["metadata"] = {"provider_attempt_count": 3}                                          # an answer delivered in three requests
    plain, absent = receipt(), receipt(ok=False)
    absent["metadata"] = {"provider_attempt_count": 0}                                     # refused before egress: still one dispatch, never fewer than before
    write_arm(tmp_path, ARMS[1], [r, plain, absent])
    u = guard.usage(str(tmp_path), [ARMS[1]], BUDGET["reserve_tokens_per_dispatch"])
    assert u["dispatches"] == 5 and u["per_arm"][ARMS[1]]["dispatches"] == 5
    cap = dict(BUDGET, cumulative=dict(BUDGET["cumulative"], max_dispatches=4))
    assert any("dispatches 5 > 4" in w for w in guard.exceeded(cap, u))                   # and the limit is enforced on requests
