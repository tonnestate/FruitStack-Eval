"""The recorded Groq failure chain (2026-10-29): billing exhaustion -> cooldown -> operator termination -> restart -> reselection. Root cause: credential health lived in one process's state directory and PlumMe resets
the billing counters when a window expires. The carry-forward registry (real PlumMe CredentialBroker underneath) makes the exhaustion survive processes, restarts and new selections, escalate, and end only on a success."""
import json
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("plumme")
from ogi013_credential_health import STATE_FILE, Registry, harvest_all, prepare_state  # noqa: E402
from plumme.credentials import CredentialBroker, CredentialSource, CredentialSourceKind  # noqa: E402
from plumme.failures import BILLING_OR_CREDIT_EXHAUSTED as BILLING  # noqa: E402

HANDLE = "donor-ref:groq:donor:openclaw"


@pytest.fixture(autouse=True)
def _key(monkeypatch):
    monkeypatch.setenv("GROQ_TEST_KEY", "x")                                           # the reference must resolve for the broker to call the profile usable


def episode_state(tmp, name, *, fail=False, succeed=False, at=None, seed=None):
    """One episode's PlumMe state dir with a real broker: Groq registered (optionally seeded), then a success and/or a billing exhaustion recorded by PlumMe itself."""
    d = tmp / name / "fruitstack/plumme-state"
    d.mkdir(parents=True)
    if seed:
        (d / STATE_FILE).write_text(json.dumps(seed))
    broker = CredentialBroker(d / "credentials.enc.json")
    broker.register_source(CredentialSource(provider="groq", kind=CredentialSourceKind.ENV_REFERENCE, handle=HANDLE, ref={"var": "GROQ_TEST_KEY"}))
    if succeed:
        broker.mark_success(HANDLE, "openai/gpt-oss-20b")
    if fail:
        broker.mark_failure(HANDLE, "groq", "openai/gpt-oss-20b", BILLING, None)
    return d, broker


def usable(state_dir, now=None):
    b = CredentialBroker(state_dir / "credentials.enc.json")
    if now is not None:
        import plumme.credentials as c
        real = c.time.time
        c.time.time = lambda: now
        try:
            return bool(b.usable_profiles("groq", model="openai/gpt-oss-20b"))
        finally:
            c.time.time = real
    return bool(b.usable_profiles("groq", model="openai/gpt-oss-20b"))


def test_exhaustion_is_a_state_it_survives_processes_restarts_and_any_amount_of_time_until_positive_evidence(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    first, _ = episode_state(runs, "e1", fail=True)                                # the episode in which Groq returned BILLING_OR_CREDIT_EXHAUSTED
    assert not usable(first)
    fresh, _ = episode_state(runs, "fresh")
    assert usable(fresh)                                                             # a clean state directory would look healthy: the registry must not
    second = runs / "e2/fruitstack/plumme-state"
    second.mkdir(parents=True)
    prepare_state(second)                                                            # a NEW process / episode / block attempt / restart
    assert not usable(second)
    row = json.loads((second / STATE_FILE).read_text())[0]["health"]
    assert row["status"] == "EXHAUSTED" and row["disabled_reason"] == "exhausted"
    for later in (700, 1300, 2500, 86400 * 30):                                      # 600 s, 1,200 s, 2,400 s, a month: no clock re-enables it, no automatic probe
        assert not usable(second, now=time.time() + later)
    third = runs / "e3/fruitstack/plumme-state"                                       # restart of the registry itself (read from disk again)
    third.mkdir(parents=True)
    prepare_state(third)
    assert not usable(third, now=time.time() + 86400 * 30)
    # only positive evidence ends it: an operator renewal ...
    from ogi013_credential_health import renew
    renew(runs, HANDLE)
    fourth = runs / "e4/fruitstack/plumme-state"
    fourth.mkdir(parents=True)
    prepare_state(fourth)
    assert usable(fourth)
    # ... and a later exhaustion is a NEW exhaustion
    episode_state(runs, "e5", fail=True)
    fifth = runs / "e6/fruitstack/plumme-state"
    fifth.mkdir(parents=True)
    prepare_state(fifth)
    assert not usable(fifth)


def test_a_success_after_the_exhaustion_is_positive_evidence(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    episode_state(runs, "e1", fail=True)
    time.sleep(0.01)
    episode_state(runs, "e2", succeed=True)
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    assert HANDLE not in reg.exhausted


def test_failure_kinds_are_kept_apart_and_only_exhausted_credit_is_sticky(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    d, broker = episode_state(runs, "e1")
    broker.mark_failure(HANDLE, "groq", "openai/gpt-oss-20b", "RATE_LIMITED", None)
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    assert reg.kinds[HANDLE] == {"rate_limit": 1} and HANDLE not in reg.exhausted     # a rate limit is model-scoped PlumMe handling, not exhaustion
    d2, broker2 = episode_state(runs, "e2")
    broker2.mark_failure(HANDLE, "groq", "openai/gpt-oss-20b", "AUTH_FAILED", None)
    d3, broker3 = episode_state(runs, "e3")
    broker3.mark_failure(HANDLE, "groq", "openai/gpt-oss-20b", "TIMEOUT", None)
    d4, broker4 = episode_state(runs, "e4", fail=True)
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    assert set(reg.kinds[HANDLE]) == {"rate_limit", "auth", "network", "exhausted_credit"} and HANDLE in reg.exhausted


def test_the_running_process_latches_exhaustion_at_once(tmp_path, monkeypatch):
    from ogi013_credential_health import latch_exhaustion
    d, broker = episode_state(tmp_path, "e1")
    latch_exhaustion(SimpleNamespace(credentials=broker))
    broker.mark_failure(HANDLE, "groq", "openai/gpt-oss-20b", BILLING, None)           # PlumMe alone would disable it for 600 s only
    assert not usable(d, now=time.time() + 86400 * 30)


def _policy(runs, **p):
    runs.mkdir(parents=True, exist_ok=True)
    (runs / "credential_renewal_policy.json").write_text(json.dumps({HANDLE: p}))


def test_unknown_or_non_renewing_credentials_are_never_probed(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    episode_state(runs, "e1", fail=True)                                             # no renewal policy configured = UNKNOWN
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    ex = reg.exhausted[HANDLE]
    assert ex["policy"]["cycle"] == "UNKNOWN" and ex["next_probe_at"] is None and ex["reason"] == BILLING
    assert reg.claim_probes(time.time() + 86400 * 400) == set()                      # a year later: still no automatic retry
    _policy(runs, cycle="MONTHLY")                                                   # monthly without a KNOWN renewal date
    assert Registry(runs / "credential_health.json").next_probe(HANDLE, "groq", 1000.0) is None


def test_one_probe_per_cycle_failed_probe_waits_for_the_next_cycle_successful_probe_restores_availability(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    _policy(runs, cycle="DAILY", source="provider docs")
    episode_state(runs, "e1", fail=True)
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    at = reg.exhausted[HANDLE]["at"]
    assert reg.exhausted[HANDLE]["next_probe_at"] == pytest.approx(at + 86400)
    e2 = runs / "e2/fruitstack/plumme-state"                                          # 10 minutes, 1 hour, 23 h later: still EXHAUSTED, nothing is offered
    e2.mkdir(parents=True)
    prepare_state(e2)
    assert not usable(e2, now=time.time() + 82800)
    # 25 h later: ONE probe is claimed and the credential is seeded usable for that episode only
    real = time.time
    monkeypatch.setattr(time, "time", lambda: real() + 90000)
    e3 = runs / "e3/fruitstack/plumme-state"
    e3.mkdir(parents=True)
    prepare_state(e3)
    assert usable(e3)
    row = json.loads((e3 / STATE_FILE).read_text())[0]["health"]
    assert row["status"] == "PROBE"
    e4 = runs / "e4/fruitstack/plumme-state"                                          # a second episode in the same cycle: the probe is spent/claimed, no repeat
    e4.mkdir(parents=True)
    prepare_state(e4)
    monkeypatch.setattr(time, "time", real)
    reg = Registry(runs / "credential_health.json")
    assert reg.exhausted[HANDLE]["last_probe"]["result"] == "PROBE_UNUSED"        # e3 never used it: released, not spent (e4 then holds the claim)
    # the probe FAILS: exhausted again until the next cycle, last probe result persisted
    monkeypatch.setattr(time, "time", lambda: real() + 90000)
    d, broker = episode_state(runs, "e5", fail=True, seed=json.loads((e4 / STATE_FILE).read_text()))
    monkeypatch.setattr(time, "time", real)
    reg = Registry(runs / "credential_health.json")
    harvest_all(reg, runs)
    ex = reg.exhausted[HANDLE]
    assert ex["probe_claimed_at"] is None and ex["last_probe"]["result"] == "EXHAUSTED" and ex["next_probe_at"] > ex["at"] + 86000
    # the next cycle's probe succeeds: AVAILABLE
    monkeypatch.setattr(time, "time", lambda: real() + 90000 + 86400 * 2)
    ok, _ = episode_state(runs, "e6", succeed=True)
    reg = Registry(tmp_path / "fresh.json")
    reg.exhausted[HANDLE] = {"at": real() + 90000, "kind": "exhausted_credit", "probe_claimed_at": real() + 90001}      # that cycle's probe was claimed ...
    reg.merge_state(ok / STATE_FILE)                                                # ... and its episode recorded a success
    assert HANDLE not in reg.exhausted and reg.probes[HANDLE]["result"] == "AVAILABLE"


def test_a_known_reset_time_is_used_and_rolled_forward():
    reg = Registry(Path("/nonexistent/x.json"))
    reg.policy = {HANDLE: {"cycle": "WEEKLY", "reset_at": 5000.0}}
    assert reg.next_probe(HANDLE, "groq", 100.0) == 5000.0
    assert reg.next_probe(HANDLE, "groq", 5001.0) == 5000.0 + 604800
    reg.policy = {"groq": {"cycle": "DAILY"}}                                          # provider-level configuration, no known reset: 24 h
    assert reg.next_probe(HANDLE, "groq", 100.0) == 100.0 + 86400


def test_without_a_campaign_nothing_changes(tmp_path, monkeypatch):
    monkeypatch.delenv("OGI013_PILOT_RUNS", raising=False)
    d = tmp_path / "state"
    d.mkdir()
    prepare_state(d)
    assert not (d / STATE_FILE).exists()                                             # the frozen conditions are untouched


def test_an_interrupted_or_archived_episode_still_informs_the_next_one(tmp_path, monkeypatch):
    """The operator-terminated attempt never wrote an exhaustion row of its own; its credential health is harvested from its state directory anyway (also from archived directories)."""
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    episode_state(runs / "collab1/discarded/airline_7-operator-infra123/airline_7", "SINGLE", fail=True)
    nxt = runs / "collab1/airline_7/SINGLE/fruitstack/plumme-state"
    nxt.mkdir(parents=True)
    prepare_state(nxt)
    assert not usable(nxt)


# ---- simulator selection ---------------------------------------------------------------------------------------------------------------------------------------
def offers(*pairs):
    return SimpleNamespace(store=SimpleNamespace(offers={f"o{i}": SimpleNamespace(model_key=m, provider=p) for i, (m, p) in enumerate(pairs)}))


def pool(tmp, exhausted_handles, svc, providers=None):
    """Allowlist of two models; the registry marks the given providers' credentials exhausted."""
    pytest.importorskip("tau2", reason="the runner imports the official tau2-bench runtime at module level")
    import ogi013_sim_supply as sim
    (tmp / "sim_allowlist.json").write_text(json.dumps({"model_keys": ["gpt-oss-20b@default", "laguna-s-2.1@default"]}))
    srcs = {f"h-{p}": {"provider": p, "handle": f"h-{p}"} for p in (providers or ["groq", "nvidia", "openrouter"])}
    (tmp / "credential_health.json").write_text(json.dumps({"sources": srcs, "exhausted": {f"h-{p}": {"at": 1.0, "kind": "exhausted_credit"} for p in exhausted_handles}}))
    return sim._selection_pool(tmp, svc)


def test_a_model_another_provider_can_serve_is_not_blacklisted(tmp_path):
    svc = offers(("gpt-oss-20b@default", "groq"), ("gpt-oss-20b@default", "nvidia"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path, ["groq"], svc) == ["gpt-oss-20b@default", "laguna-s-2.1@default"]


def test_a_model_whose_every_provider_is_exhausted_is_excluded_regardless_of_time(tmp_path):
    svc = offers(("gpt-oss-20b@default", "groq"), ("gpt-oss-20b@default", "nvidia"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path, ["groq", "nvidia"], svc) == ["laguna-s-2.1@default"]
    # a provider with a healthy second credential is not exhausted
    (tmp_path / "credential_health.json").write_text(json.dumps({"sources": {"a": {"provider": "groq"}, "b": {"provider": "groq"}}, "exhausted": {"a": {"at": 1.0}}}))
    import ogi013_sim_supply as sim
    assert sim._selection_pool(tmp_path, svc) == ["gpt-oss-20b@default", "laguna-s-2.1@default"]
    from ogi013_credential_health import renew
    only = offers(("gpt-oss-20b@default", "groq"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path, ["groq"], only) == ["laguna-s-2.1@default"]
    renew(tmp_path, "h-groq")                                                        # operator renewal (a time later than the exhaustion) re-admits it
    assert sim._selection_pool(tmp_path, only) == ["gpt-oss-20b@default", "laguna-s-2.1@default"]
