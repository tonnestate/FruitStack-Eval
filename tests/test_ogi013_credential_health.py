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


def test_the_exhausted_credential_is_known_to_the_next_process_and_stays_known_until_a_success(tmp_path, monkeypatch):
    runs = tmp_path / "runs"
    monkeypatch.setenv("OGI013_PILOT_RUNS", str(runs))
    first, _ = episode_state(runs, "e1", fail=True)                                # the episode in which Groq returned BILLING_OR_CREDIT_EXHAUSTED
    assert not usable(first)                                                         # (within that one process PlumMe already knew)
    fresh, _ = episode_state(runs, "fresh")                                          # what the next process used to see: a clean state directory
    assert usable(fresh)                                                             # the defect: Groq looks healthy again
    second = runs / "e2/fruitstack/plumme-state"
    second.mkdir(parents=True)
    prepare_state(second)                                                            # a NEW process / episode / block attempt
    assert not usable(second)                                                        # before: Groq looked healthy again
    # the window expires without any evidence of renewed credit: the registry, not the clock, decides - one probe is allowed after the window, never silently more
    reg = Registry(runs / "credential_health.json")
    last = reg.billing[HANDLE]["last_at"]
    assert reg.seed_rows(now=last + 300)[0]["health"]["disabled_until"] > last + 300           # inside the 10-minute window: disabled
    assert reg.seed_rows(now=last + 700)[0]["health"].get("disabled_until", 0) < last + 700     # after it: eligible for ONE probe
    # the probe fails again: the window doubles (PlumMe's own policy: 10 min, 20, 40 ...) instead of repeating the same 600 s
    third, _ = episode_state(runs, "e3", fail=True, seed=reg.seed_rows(now=last + 700))
    reg2 = Registry(runs / "credential_health.json")
    harvest_all(reg2, runs)
    assert reg2.billing[HANDLE]["events"] == 2
    again = reg2.seed_rows(now=reg2.billing[HANDLE]["last_at"] + 900)[0]["health"]["disabled_until"]
    assert again > reg2.billing[HANDLE]["last_at"] + 900                             # 900 s after the second exhaustion it is still disabled (window 1200 s)
    # only a success is evidence of renewed credit
    ok, _ = episode_state(runs, "e4", succeed=True)
    time.sleep(0.01)
    reg3 = Registry(runs / "credential_health.json")
    harvest_all(reg3, runs)
    assert reg3.billing[HANDLE]["events"] == 0


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


def pool(tmp, rows, svc):
    import ogi013_sim_supply as sim
    (tmp / "sim_allowlist.json").write_text(json.dumps({"model_keys": ["gpt-oss-20b@default", "laguna-s-2.1@default"]}))
    (tmp / "sim_exhausted.jsonl").write_text("".join(json.dumps({"ts": time.time(), "until": time.time() + 600, **r}) + "\n" for r in rows))
    return sim._selection_pool(tmp, svc)


def test_a_model_another_provider_can_serve_is_not_blacklisted(tmp_path):
    svc = offers(("gpt-oss-20b@default", "groq"), ("gpt-oss-20b@default", "nvidia"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path, [{"model_key": "gpt-oss-20b@default", "providers": ["groq"]}], svc) == ["gpt-oss-20b@default", "laguna-s-2.1@default"]


def test_a_model_whose_every_provider_is_exhausted_is_excluded_and_legacy_rows_exclude_it_as_before(tmp_path):
    only_groq = offers(("gpt-oss-20b@default", "groq"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path, [{"model_key": "gpt-oss-20b@default", "providers": ["groq"]}], only_groq) == ["laguna-s-2.1@default"]
    both = offers(("gpt-oss-20b@default", "groq"), ("gpt-oss-20b@default", "nvidia"), ("laguna-s-2.1@default", "openrouter"))
    assert pool(tmp_path / "x" if (tmp_path / "x").mkdir() is None else tmp_path, [{"model_key": "gpt-oss-20b@default", "providers": ["groq", "nvidia"]}], both) == ["laguna-s-2.1@default"]
    legacy = tmp_path / "legacy"
    legacy.mkdir()
    assert pool(legacy, [{"model_key": "gpt-oss-20b@default"}], both) == ["laguna-s-2.1@default"]
