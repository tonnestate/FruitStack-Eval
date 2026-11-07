"""T / TC parity: same token ceiling, same trailing instructions in critic/reply prompts; failures keep the provider's own message."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
import ogi013_codemode_duo as cm  # noqa: E402
import ogi013_qa1 as q1  # noqa: E402
import ogi013_qa2d as q2  # noqa: E402


def test_t_and_tc_share_one_explicit_token_ceiling():
    assert q1.EPISODE_MAX_TOKENS["TC"] == q1.EPISODE_MAX_TOKENS["T"] == q1.DUO_EPISODE_TOKENS


def test_codemode_critic_and_reply_prompts_end_with_the_same_suffix_as_t(monkeypatch):
    import ogi013_argument as ag
    seen = {}

    def fake_run_duo(*a, **kw):
        seen.update(kw)
        return {"letter": "A", "stop": "AGREED_FIRST", "calls": 2}
    monkeypatch.setattr(cm, "run_duo", fake_run_duo)
    from types import SimpleNamespace
    ep = SimpleNamespace(work="w", actor="a", turn_id="t", sid="s", stats={"tokens_in": 0, "tokens_out": 0})
    ctx = SimpleNamespace(episode=lambda arm, qid: ep, stack=SimpleNamespace(fs=SimpleNamespace(mango=None)), stop=None, luna_tokens=0)
    monkeypatch.setattr("ogi013_mango_ledger.MangoLedger", lambda *a, **k: SimpleNamespace(writes=0, reads=0, write=lambda *a, **k: None))
    cm.run_T_codemode(ctx, {"id": "1", "question": "q", "options": ["a", "b"], "key": "A"})
    assert seen["critic_instructions"] == ag.CRITIC_INSTRUCTIONS + q1.ANSWER_SUFFIX
    assert seen["reply_instructions"] == ag.REPLY_INSTRUCTIONS + q1.ANSWER_SUFFIX


def test_failure_reason_carries_the_provider_message():
    assert q2.reason({"failure_class": "EXECUTION_NOT_PERFORMED_PROVIDER_UNAVAILABLE", "provider_message": "HTTP 502 timeout x1"}) == \
        "EXECUTION_NOT_PERFORMED_PROVIDER_UNAVAILABLE | HTTP 502 timeout x1"
    assert q2.reason({"failure_class": "X"}) == "X"
