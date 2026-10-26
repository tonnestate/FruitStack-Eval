"""Host adapter checks; no provider, database, or benchmark run."""

import sys
from pathlib import Path

import pytest


def test_output_guard_accepts_empty_and_rejects_nonempty(tmp_path):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
    from ogi013_run_guard import ensure_empty_output

    empty = tmp_path / "empty"
    empty.mkdir()
    ensure_empty_output(empty)
    ensure_empty_output(tmp_path / "new-output")

    (empty / "existing-result.json").write_text("{}", encoding="utf-8")
    with pytest.raises(FileExistsError, match="output directory must be empty"):
        ensure_empty_output(empty)


def test_action_parser_preserves_nested_json_and_braces_in_strings():
    pytest.importorskip("tau2")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
    from ogi013_tau2_agent import parse_action

    assert parse_action('reply: {"action":"tool","name":"x","arguments":{"value":"a } b"}}') == {
        "action": "tool", "name": "x", "arguments": {"value": "a } b"}
    }


def test_unconfigured_peach_budget_does_not_create_a_plum_token_ceiling():
    pytest.importorskip("tau2")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
    from ogi013_tau2_agent import Episode

    episode = object.__new__(Episode)
    episode.sid = "existing-session"
    episode.stack = type("Stack", (), {"fs": type("FS", (), {
        "governance": type("Budget", (), {"snapshot": lambda _, sid: None})()
    })()})()
    assert episode.reserve("short prompt") is None


def test_arm_policy_is_explicit_and_single_still_has_no_ensemble_review():
    pytest.importorskip("tau2")
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
    from ogi013_tau2_agent import should_organize

    message = {"action": "message", "content": "done"}
    read = {"action": "tool", "name": "lookup"}
    write = {"action": "tool", "name": "submit"}
    writes = {"submit"}
    assert not should_organize("single", write, writes)
    assert should_organize("fixed", message, writes)
    assert should_organize("adaptive", write, writes)
    assert not should_organize("adaptive", read, writes)
    assert not should_organize("adaptive", message, writes)


def test_runner_requires_existing_host_pomelo_bridge(monkeypatch):
    import importlib.util

    runners = Path(__file__).resolve().parents[1] / "runners"
    monkeypatch.syspath_prepend(str(runners))
    spec = importlib.util.spec_from_file_location("ogi013_tau2_run", runners / "ogi013_tau2_run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.delenv("OGI013_POMELO_AUTHORITY", raising=False)
    with pytest.raises(RuntimeError, match="POMELOME_HOST_BRIDGE_REQUIRED"):
        module._host_effects(type("Peach", (), {"effects": None})())

    bridge = object()
    assert module._host_effects(type("Peach", (), {"effects": bridge})()) is bridge


def test_runner_attaches_trusted_host_effects_before_task_execution(monkeypatch, tmp_path):
    import importlib.util

    runners = Path(__file__).resolve().parents[1] / "runners"
    monkeypatch.syspath_prepend(str(runners))
    spec = importlib.util.spec_from_file_location("ogi013_tau2_run", runners / "ogi013_tau2_run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class Peach:
        effects = None
        def attach_host_effects(self, **kwargs):
            assert kwargs == host_effects
            self.effects = bridge
    bridge = object()
    host_effects = {"gateway": object(), "authority_provider": lambda *_: None,
                    "plan_provider": lambda *_: None}
    peach = Peach()
    monkeypatch.setattr(module.FruitStack, "get", lambda _: type("Stack", (), {"fs": peach})())
    def stop_at_task(_):
        assert peach.effects is bridge
        raise LookupError("task reached")
    monkeypatch.setattr(module, "get_tasks", stop_at_task)
    with pytest.raises(LookupError, match="task reached"):
        module.run_one("task", "domain", "single", tmp_path, host_effects=host_effects)


def test_cli_passes_host_composition_to_runner(monkeypatch, tmp_path):
    import importlib.util
    import types

    runners = Path(__file__).resolve().parents[1] / "runners"
    monkeypatch.syspath_prepend(str(runners))
    spec = importlib.util.spec_from_file_location("ogi013_tau2_run", runners / "ogi013_tau2_run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    host_effects = {"gateway": object(), "authority_provider": lambda *_: None,
                    "plan_provider": lambda *_: None}
    monkeypatch.setitem(sys.modules, "trusted_ogi013_host", types.SimpleNamespace(host_effects=lambda: host_effects))
    calls = []
    monkeypatch.setattr(module, "run_one", lambda *args, **kwargs: calls.append((args, kwargs)))
    module.main(["--task", "task", "--domain", "retail", "--mode", "single",
                 "--out", str(tmp_path / "run"), "--host-composer", "trusted_ogi013_host",
                 "--llm-user", "groq/llama-3.3-70b-versatile"])
    assert calls[0][1]["host_effects"] is host_effects
    assert calls[0][1]["llm_user"] == "groq/llama-3.3-70b-versatile"


def test_stack_refuses_to_admit_its_own_mango_identity(monkeypatch):
    import importlib.util

    runners = Path(__file__).resolve().parents[1] / "runners"
    monkeypatch.syspath_prepend(str(runners))
    spec = importlib.util.spec_from_file_location("ogi013_tau2_agent", runners / "ogi013_tau2_agent.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    class Mango:
        def enter_work(self, **kwargs):
            raise AssertionError("runner must not self-admit")
    stack = object.__new__(module.Stack)
    stack.mango = Mango()
    for key in ("OGI013_WORK_REF", "OGI013_TURN_ID", "OGI013_ACTOR_ID", "OGI013_PROJECT_REF"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(RuntimeError, match="HOST_BOUND_WORK_REQUIRED"):
        stack.project("ignored")


def test_stack_proof_routes_harmless_effect_through_durable_pomelo_bridge(tmp_path):
    try:
        import pomelome  # noqa: F401
        import peachme  # noqa: F401
    except ImportError as exc:
        pytest.skip(f"local PeachMe/PomeloMe integration unavailable: {exc}")
    import importlib.util

    runner_dir = Path(__file__).resolve().parents[1] / "runners"
    sys.path.insert(0, str(runner_dir))
    runner = runner_dir / "ogi013_stack_proof.py"
    spec = importlib.util.spec_from_file_location("ogi013_stack_proof", runner)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run_local_pomelo_proof(tmp_path, "test-work", actor="test")
    assert result["dispatched"] and result["state"] == "RECONCILED"
    assert result["receipt_id"] and result["durable_state"] == "RECONCILED"
