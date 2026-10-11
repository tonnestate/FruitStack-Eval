import pytest

from fruitstack_eval.interventions import Intervention, append, load, summarize


def make(**overrides):
    values = dict(actor="owner", kind="AUTHORITY", action="PROMOTE_POLICY", minutes=3, phase="PILOT",
                  recorded_at="2026-11-02T10:00:00+00:00")
    values.update(overrides)
    return Intervention(**values)


@pytest.mark.parametrize("overrides", [{"kind": "AUTHORITY", "action": "HINT"}, {"minutes": True},
                                       {"minutes": -1}, {"phase": "LIVE"}, {"actor": " "},
                                       {"recorded_at": "2026-11-02T10:00:00"}])
def test_invalid_interventions_rejected(overrides):
    with pytest.raises(ValueError):
        make(**overrides)


def test_cognitive_act_in_confirmatory_phase_is_deviation():
    assert make(kind="COGNITIVE", action="REPAIR", phase="CONFIRMATORY").is_deviation
    assert not make(kind="COGNITIVE", action="REPAIR", phase="PILOT").is_deviation
    assert not make(phase="CONFIRMATORY").is_deviation


def test_roundtrip_and_summary(tmp_path):
    log = tmp_path / "interventions.jsonl"
    items = [make(), make(kind="COGNITIVE", action="HINT", minutes=10, phase="CONFIRMATORY",
                          recorded_at="2026-12-01T09:00:00+01:00", refs=("task-7",))]
    for item in items:
        append(log, item)
    log.write_text(log.read_text(encoding="utf-8") + "garbage\n", encoding="utf-8")
    loaded, warnings = load(log)
    assert [i.intervention_id for i in loaded] == [i.intervention_id for i in items]
    assert loaded[1].refs == ("task-7",)
    assert len(warnings) == 1
    summary = summarize(loaded, verified_tasks=50)
    assert summary["count_by_kind"] == {"AUTHORITY": 1, "COGNITIVE": 1}
    assert summary["total_minutes"] == 13
    assert summary["confirmatory_deviations"] == [items[1].intervention_id]
    assert summary["per_100_verified_tasks"] == {"AUTHORITY": 2.0, "COGNITIVE": 2.0}
    assert summary["monthly"] == {"2026-11": {"AUTHORITY": 1}, "2026-12": {"COGNITIVE": 1}}
