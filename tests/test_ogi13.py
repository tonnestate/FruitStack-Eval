"""Independent OGI-013 analysis: resource parity, missing evidence and honest ROI."""
import pytest
import json

from fruitstack_eval.cli import main

from fruitstack_eval.ogi13 import compare_paired, SCHEMA


def observation(task, arm, *, grade=1, edges=None, calls=1, tokens=100,
                quota=1, wall=3.0, cost=0.0, minutes=0.0, **changes):
    row = {
        "task_id": task, "arm": arm,
        "benchmark_id": "GAIA", "benchmark_revision": "r-frozen",
        "task_manifest_digest": "manifest:known", "grader_digest": "grader:known",
        "model_pool_digest": "models:identical", "skills_digest": "skills:identical",
        "tools_digest": "tools:identical", "budget_digest": "budget:identical",
        "supply_regime_id": "supply:identical",
        "work_ref": f"mango:{task}:{arm}", "trace_ref": f"trace:{task}:{arm}",
        "grade_status": "VERIFIED", "grade": grade,
        "grader_receipt_ref": f"external-grader:{task}:{arm}",
        "independent_verifier": "verifier:trusted-host",
        "competence_edges": list(edges or []),
        "provider_calls": calls, "provider_receipt_refs": [
            f"provider:{task}:{arm}:{i}" for i in range(calls)
        ],
        "total_tokens": tokens, "quota_units": quota,
        "cost_usd": cost, "wall_seconds": wall, "human_minutes": minutes,
    }
    row.update(changes)
    return row


def test_paired_cost_of_success_is_not_raw_token_average():
    rows = [
        observation("t1", "FIXED", grade=0, tokens=100),
        observation("t1", "ADAPTIVE", grade=1, tokens=180,
                    edges=["competence:research>verify"]),
        observation("t2", "FIXED", grade=1, tokens=100),
        observation("t2", "ADAPTIVE", grade=1, tokens=140,
                    edges=["competence:research>verify"]),
    ]
    out = compare_paired(rows)
    assert out["schema"] == SCHEMA
    assert out["paired_tasks"] == 2
    assert out["overall"]["successes"] == {"FIXED": 1, "ADAPTIVE": 2}
    assert out["overall"]["success_rate_delta"] == 0.5
    by_success = out["overall"]["resources_per_verified_success"]["total_tokens"]
    assert by_success == {"FIXED": 200, "ADAPTIVE": 160, "delta": -40}
    assert out["by_one_added_edge"]["competence:research>verify"]["pairs"] == 2
    assert out["organisational_advantage_proven"] is False
    assert out["causal_effect_proven"] is False
    assert out["grader_provenance_attested"] is False


def test_no_success_means_roi_undefined_not_zero_or_infinity():
    result = compare_paired([
        observation("t1", "FIXED", grade=0),
        observation("t1", "ADAPTIVE", grade=0),
    ])
    assert result["overall"]["resources_per_verified_success"]["total_tokens"] == {
        "FIXED": None, "ADAPTIVE": None, "delta": None,
    }


def test_incomplete_is_counted_as_nonsuccess_and_disclosed():
    rows = [
        observation("t1", "FIXED", grade=1),
        observation("t1", "ADAPTIVE", grade=None, grade_status="INCOMPLETE"),
    ]
    result = compare_paired(rows)
    assert result["paired_tasks"] == 1
    assert result["overall"]["successes"] == {"FIXED": 1, "ADAPTIVE": 0}
    assert result["incomplete_grade_tasks"] == ["t1"]
    assert "INCOMPLETE_OR_UNVERIFIED_GRADING" in result["limitations"]


def test_differing_budget_supply_model_or_grader_never_compares():
    for field in (
        "benchmark_id", "benchmark_revision", "task_manifest_digest",
        "grader_digest", "model_pool_digest", "skills_digest",
        "tools_digest", "budget_digest", "supply_regime_id",
    ):
        r = compare_paired([
            observation("t1", "FIXED"),
            observation("t1", "ADAPTIVE", **{field: "different"}),
        ])
        assert r["paired_tasks"] == 0
        assert r["confounded_tasks"] == ["t1"]


def test_missing_usage_does_not_turn_unknown_cost_into_free():
    output = compare_paired([
        observation("t1", "FIXED", cost=None, tokens=None),
        observation("t1", "ADAPTIVE", tokens=150, cost=0.0),
    ])
    assert output["missing_usage_tasks"] == ["t1"]
    assert output["overall"]["complete_usage_pairs"] == 0
    assert output["overall"]["resources_per_verified_success"]["cost_usd"]["delta"] is None


def test_missed_receipt_is_disclosed_even_if_grade_passed():
    output = compare_paired([
        observation("t1", "FIXED", calls=1, provider_receipt_refs=[]),
        observation("t1", "ADAPTIVE", calls=1),
    ])
    assert output["missing_usage_tasks"] == ["t1"]
    assert output["overall"]["complete_usage_pairs"] == 0


def test_two_added_edges_or_replaced_edge_have_no_individual_credit():
    result = compare_paired([
        observation("t1", "FIXED", edges=["a>b"]),
        observation("t1", "ADAPTIVE", edges=["a>b", "b>c", "c>d"]),
        observation("t2", "FIXED", edges=["a>b"]),
        observation("t2", "ADAPTIVE", edges=["a>c"]),
    ])
    assert result["paired_tasks"] == 2
    assert result["by_one_added_edge"] == {}
    assert result["edge_ambiguous_tasks"] == ["t1", "t2"]


def test_unmatched_arms_remain_visible():
    result = compare_paired([observation("t1", "ADAPTIVE")])
    assert result["unmatched_tasks"] == ["t1"]
    assert result["paired_tasks"] == 0


@pytest.mark.parametrize("change,code", [
    ({"grade_status": "VERIFIED", "grade": None}, "INVALID_VERIFIED_GRADE"),
    ({"grade_status": "UNKNOWN", "grade": 0}, "UNVERIFIED_GRADE_PROVIDED"),
    ({"grade_status": "VERIFIED", "grader_receipt_ref": None}, "MISSING_GRADER_RECEIPT_REF"),
    ({"provider_calls": -1}, "INVALID_PROVIDER_CALLS"),
    ({"provider_calls": 0.5}, "INVALID_PROVIDER_CALLS"),
    ({"total_tokens": -10}, "INVALID_TOTAL_TOKENS"),
    ({"cost_usd": float("nan")}, "INVALID_COST_USD"),
    ({"competence_edges": ["edge", "edge"]}, "DUPLICATE_COMPETENCE_EDGE"),
    ({"provider_receipt_refs": ["same", "same"], "provider_calls": 2}, "DUPLICATE_PROVIDER_RECEIPT"),
    ({"provider_receipt_refs": ["r1", "r2"], "provider_calls": 1}, "RECEIPTS_EXCEED_CALLS"),
])
def test_refuse_false_scientific_evidence(change, code):
    with pytest.raises(ValueError, match=code):
        compare_paired([observation("t1", "FIXED", **change)])


def test_duplicate_arms_cannot_dilute_denominators():
    with pytest.raises(ValueError, match="DUPLICATE_TASK_ARM"):
        compare_paired([
            observation("t1", "FIXED"),
            observation("t1", "FIXED"),
        ])

def test_fse_ogi13_cli_parses_actual_export_shape(tmp_path, capsys):
    observations = tmp_path / "observations.jsonl"
    pairs = [
        observation("t1", "FIXED", grade=0),
        observation("t1", "ADAPTIVE", grade=1, edges=["analysis>verification"]),
    ]
    observations.write_text("".join(json.dumps(row) + "\\n" for row in pairs), encoding="utf-8")
    assert main(["ogi13", "compare", "--observations", str(observations)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["paired_tasks"] == 1
    assert result["overall"]["success_rate_delta"] == 1.0
    assert result["organisational_advantage_proven"] is False


def test_fse_ogi13_cli_gates_missing_usage_without_hiding_results(tmp_path, capsys):
    observations = tmp_path / "observations.jsonl"
    pairs = [
        observation("t1", "FIXED", provider_receipt_refs=[]),
        observation("t1", "ADAPTIVE", grade=1),
    ]
    observations.write_text("".join(json.dumps(row) + "\\n" for row in pairs), encoding="utf-8")
    assert main(["ogi13", "compare", "--observations", str(observations),
                 "--require-complete"]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["missing_usage_tasks"] == ["t1"]
    assert result["complete_pairs_only"] is False
