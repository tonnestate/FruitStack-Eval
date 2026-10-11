import json
from pathlib import Path

import pytest

from conftest import decision_row
from fruitstack_eval import integrity, logcheck, seal
from fruitstack_eval.decision_log import load_views
from fruitstack_eval.interventions import Intervention, append
from test_git_tools import commit_file, run

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------- G1 integrity

@pytest.fixture
def clones(tmp_path):
    """An upstream repository with main, sync/local-truth and a proposal, plus a clone of it."""
    upstream = tmp_path / "upstream" / "plumme"
    upstream.mkdir(parents=True)
    run(upstream, "init", "-q", "-b", "main")
    commit_file(upstream, "src/plumme/__init__.py", '__version__ = "0.1.7"\n', "v0.1.7")
    run(upstream, "branch", "sync/local-truth")
    run(upstream, "checkout", "-q", "-b", "web/claude")
    proposal = commit_file(upstream, "src/plumme/__init__.py", '__version__ = "0.1.8"\n', "v0.1.8")
    commit_file(upstream, "src/plumme/fingerprint.py", "x = 1\n", "fingerprint")
    proposal_head = run(upstream, "rev-parse", "HEAD")
    run(upstream, "checkout", "-q", "main")
    work = tmp_path / "clones"
    work.mkdir()
    run(work, "clone", "-q", str(upstream), "plumme")
    return {"upstream": upstream, "clones": work, "proposal": proposal, "proposal_head": proposal_head}


def requirement(**kw):
    base = dict(name="plumme", version_file="src/plumme/__init__.py", min_version="0.1.8",
                required_paths=("src/plumme/fingerprint.py",))
    base.update(kw)
    return integrity.RepoRequirement(**base)


def test_g1_fails_before_merge_and_passes_after(clones):
    req = requirement(required_commits=(clones["proposal_head"],))
    before = integrity.check([req], clones["clones"])
    problems = before["repos"][0]["problems"]
    assert not before["passed"]
    assert any("version 0.1.7 < required 0.1.8" in p for p in problems)
    assert any("required path missing" in p for p in problems)
    assert any("not contained in main" in p for p in problems)

    up = clones["upstream"]
    run(up, "merge", "-q", "--ff-only", "web/claude")
    run(up, "branch", "-f", "sync/local-truth", "main")
    stale = integrity.check([req], clones["clones"])
    assert not stale["passed"]                       # local refs are stale until fetched
    fresh = integrity.check([req], clones["clones"], fetch=True)
    repo = fresh["repos"][0]
    assert fresh["passed"], repo["problems"]
    assert repo["version"] == "0.1.8" and repo["main_sha"] == repo["mirror_sha"] == clones["proposal_head"]
    assert repo["checks"]["required_commits"] == {clones["proposal_head"]: "CONTAINED"}


def test_g1_mirror_divergence_is_truth_not_normalized(clones):
    up = clones["upstream"]
    run(up, "merge", "-q", "--ff-only", "web/claude")       # main moves, sync stays behind
    result = integrity.check([requirement()], clones["clones"], fetch=True)
    assert not result["passed"]
    assert any(p.startswith("TRUTH_NOT_NORMALIZED") for p in result["repos"][0]["problems"])


def test_g1_missing_clone_and_unknown_commit(clones, tmp_path):
    missing = integrity.check([requirement(name="cherryme")], clones["clones"])
    assert not missing["passed"] and "no git clone" in missing["repos"][0]["problems"][0]
    unknown = integrity.check([requirement(min_version=None, version_file=None, required_paths=(),
                                           required_commits=("deadbeef",))], clones["clones"])
    assert unknown["repos"][0]["checks"]["required_commits"] == {"deadbeef": "UNKNOWN_COMMIT"}


def test_g1_requirements_file_is_valid():
    reqs = integrity.load_requirements(ROOT / "config" / "g1_requirements.toml")
    names = {r.name for r in reqs}
    assert {"plumme", "cherryme", "appleme"} <= names
    plumme = next(r for r in reqs if r.name == "plumme")
    assert plumme.min_version == "0.1.8" and plumme.mirror == "sync/local-truth"


def test_version_comparison():
    assert integrity.version_tuple("0.1.10") > integrity.version_tuple("0.1.8")
    assert integrity.version_tuple("0.2.0rc1") >= integrity.version_tuple("0.2.0")
    with pytest.raises(ValueError):
        integrity.version_tuple("dev")


# ---------------------------------------------------------------- G5 seal

def write_rows(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def test_seal_detects_append_retention_and_tampering(tmp_path):
    log = tmp_path / "decisions.jsonl"
    write_rows(log, [decision_row(f"d{i}") for i in range(3)])
    manifest, rows = seal.seal({"decisions": (log, "decisionlog")})
    out, rows_path = seal.write(manifest, rows, tmp_path / "seal.json")
    manifest, rows = seal.read(out)
    assert seal.verify(manifest, rows)["logs"]["decisions"]["status"] == "UNCHANGED"

    with log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(decision_row("d3")) + "\n")
    appended = seal.verify(manifest, rows)
    assert appended["passed"] and appended["logs"]["decisions"] == {"status": "APPEND_ONLY", "dropped": 0, "appended": 1}

    # rotation: the oldest row moves out of the retained window
    lines = log.read_text(encoding="utf-8").splitlines(keepends=True)
    (tmp_path / "decisions.jsonl.1").write_text("".join(lines[1:3]), encoding="utf-8")
    log.write_text("".join(lines[3:]), encoding="utf-8")
    rotated = seal.verify(manifest, rows)
    assert rotated["passed"] and rotated["logs"]["decisions"]["status"] == "RETENTION_DROPPED"
    assert rotated["logs"]["decisions"]["dropped"] == 1
    assert not seal.verify(manifest, rows, allow_retention=False)["passed"]

    # an edited sealed row is tampering
    (tmp_path / "decisions.jsonl.1").write_text(lines[1].replace("d1", "dX") + lines[2], encoding="utf-8")
    tampered = seal.verify(manifest, rows)
    assert not tampered["passed"] and tampered["logs"]["decisions"]["status"] == "TAMPERED"


def test_seal_file_itself_is_tamper_evident(tmp_path):
    log = tmp_path / "interventions.jsonl"
    write_rows(log, [{"a": 1}])
    manifest, rows = seal.seal({"interventions": (log, "jsonl")})
    forged = dict(manifest, created_at="2020-01-01T00:00:00+00:00")
    assert "seal digest does not match the seal" in seal.verify(forged, rows)["problems"]
    rows_forged = {"interventions": ["0" * 64]}
    assert not seal.verify(manifest, rows_forged)["passed"]


def test_seal_requires_existing_logs(tmp_path):
    with pytest.raises(ValueError):
        seal.seal({"x": (tmp_path / "missing.jsonl", "jsonl")})
    with pytest.raises(ValueError):
        seal.seal({})


# ---------------------------------------------------------------- G5 logcheck

def full_decision(decision_id, *, kind="ACQUIRE", cost_class="FREE_TIER", policy="FREE_ONLY"):
    row = decision_row(decision_id, kind=kind, cost_classes={"A": cost_class, "B": "FREE_TIER"})
    row["data"].update({"created_at": "2026-10-11T10:00:00+00:00", "policy_name": "static", "policy_version": "0.1.6",
                        "selector_name": "deterministic", "eligible_offer_ids": ["A", "B"], "hard_rejected": {}})
    row["data"]["request_features"]["cost_policy"] = policy
    return row


def executed_outcome(decision_id, **overrides):
    data = {"decision_id": decision_id, "receipt_id": f"r-{decision_id}", "executed_offer_id": "A",
            "structural_state": "WELL_FORMED", "success": True, "model_fingerprint": "abcd1234abcd1234",
            "input_tokens": 10, "output_tokens": 5, "latency_ms": 12.0, "actual_cost_usd": 0.0}
    data.update(overrides)
    return {"type": "outcome", "data": data}


def verified_feedback(decision_id):
    return {"type": "feedback", "data": {"feedback_id": f"f-{decision_id}", "decision_id": decision_id,
                                         "epistemic_state": "VERIFIED", "verified_utility": 1.0,
                                         "verifier": "fse-blind/INQUIRY", "recorded_at": "2026-10-11T11:00:00+00:00"}}


def sealed(tmp_path, log, interventions):
    manifest, rows = seal.seal({"decisions": (log, "decisionlog"), "interventions": (interventions, "jsonl")})
    return seal.verify(manifest, rows)


def test_complete_log_passes_g5(tmp_path, write_log):
    log = write_log([full_decision("d1"), executed_outcome("d1"), verified_feedback("d1")])
    interventions = tmp_path / "interventions.jsonl"
    append(interventions, Intervention(actor="owner", kind="AUTHORITY", action="SIGN", minutes=2, phase="PILOT"))
    views, warnings = load_views(log)
    result = logcheck.check(views.values(), warnings, interventions_path=interventions,
                            seal_result=sealed(tmp_path, log, interventions), expect_cost_policy="FREE_ONLY",
                            require_feedback=True)
    assert result["passed"], result["blockers"]
    assert result["decision_log"]["distinct_fingerprints"] == 1
    assert result["decision_log"]["verifiers"] == {"fse-blind/INQUIRY": 1}


def test_missing_evidence_is_never_a_pass(tmp_path, write_log):
    log = write_log([full_decision("d1", policy="ANY"),
                     executed_outcome("d1", model_fingerprint=None, input_tokens=None)])
    views, warnings = load_views(log)
    result = logcheck.check(views.values(), warnings, interventions_path=None, seal_result=None,
                            expect_cost_policy="FREE_ONLY", require_feedback=True)
    assert not result["passed"]
    assert set(result["blockers"]) >= {"FIELD_PROBLEMS", "NO_INTERVENTION_LOG", "NOT_SEALED", "NO_VERIFIED_FEEDBACK"}
    counts = result["decision_log"]["problem_counts"]
    assert counts["OUTCOME_FIELD_MISSING"] == 2 and counts["UNEXPECTED_COST_POLICY"] == 1


def test_empty_log_and_unknown_cost_of_paid_offer(tmp_path, write_log):
    empty = logcheck.check([], [], interventions_path=None, seal_result=None)
    assert {"NO_DECISIONS", "NO_EXECUTED_OUTCOMES"} <= set(empty["blockers"])
    log = write_log([full_decision("d1", cost_class="PREMIUM"), executed_outcome("d1", actual_cost_usd=None)])
    views, warnings = load_views(log)
    counts = logcheck.check_decision_log(views.values(), warnings)["problem_counts"]
    assert counts == {"COST_UNKNOWN_FOR_NON_FREE_OFFER": 1}


def test_ensemble_decisions_need_their_propensity(write_log):
    good = full_decision("e1", kind="ENSEMBLE")
    good["data"]["ensemble_choice"] = {"topology": "SINGLE", "worker_count": 1, "available_counts": [0, 1],
                                       "propensity": 1.0, "probability_basis": "DETERMINISTIC"}
    bad = full_decision("e2", kind="ENSEMBLE")
    bad["data"]["ensemble_choice"] = {"topology": "SINGLE", "worker_count": 1, "available_counts": [0, 1],
                                      "propensity": 0.0, "probability_basis": "DETERMINISTIC"}
    views, warnings = load_views(write_log([good, bad]))
    counts = logcheck.check_decision_log(views.values(), warnings)["problem_counts"]
    assert counts == {"PROPENSITY_INVALID": 1}


def test_executed_offer_must_be_a_chosen_offer(write_log):
    views, warnings = load_views(write_log([full_decision("d1"), executed_outcome("d1", executed_offer_id="B")]))
    counts = logcheck.check_decision_log(views.values(), warnings)["problem_counts"]
    assert counts == {"EXECUTED_OFFER_NOT_CHOSEN": 1}


def test_refused_pin_is_a_complete_decision_without_choice(write_log):
    row = full_decision("p1")
    row["data"].update({"selector_name": "PINNED_DENIED", "choices": [],
                        "hard_rejected": {"X": ["COST_CLASS_PREMIUM_NOT_ALLOWED"]}})
    views, warnings = load_views(write_log([row]))
    result = logcheck.check_decision_log(views.values(), warnings)
    assert result["problem_counts"] == {} and result["stats"]["pinned_denied"] == 1
