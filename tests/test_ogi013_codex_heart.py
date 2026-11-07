"""The fixed single-model competitor: one pinned model, receipts in PlumMe's format, scaffold-net accounting, failure classification (a fake `codex` executable stands in for the CLI)."""
import asyncio
import json
import stat
import sys

import pytest

import ogi013_codex_heart as ch

FAKE = '''#!/usr/bin/env python3
import json, sys
p = sys.stdin.read()
if "NOMODEL" in p:
    print(json.dumps({"type": "error", "message": "The 'x' model is not supported when using Codex with a ChatGPT account"})); sys.exit(1)
n = 13039 + (6 if p.startswith("Reply with: OK") else len(p) // 4)
print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "ANSWER"}}))
print(json.dumps({"type": "turn.completed", "usage": {"input_tokens": n, "cached_input_tokens": 100, "output_tokens": 7}}))
'''


@pytest.fixture
def heart(tmp_path, monkeypatch):
    exe = tmp_path / "codex"
    exe.write_text(FAKE)
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setattr(ch, "CODEX", str(exe))
    monkeypatch.setenv("OGI013_CODEX_WORKDIR", str(tmp_path / "w"))
    return ch.CodexHeadlessHeart("gpt-6-luna", tmp_path / "state" / "receipts.jsonl")


def test_one_pinned_model_receipt_in_plummes_format_and_net_accounting(heart, tmp_path):
    lease = asyncio.run(heart.acquire(role_id="REASONING", objective="x", required_skill_ids=()))
    assert lease["model_id"] == "gpt-6-luna" and lease["cost_class"] == "INCLUDED" and heart.lease_facts(lease["lease_id"])["model_key"] == "gpt-6-luna@fixed"
    res = asyncio.run(heart.execute(lease_id=lease["lease_id"], task="x" * 400))
    assert res["success"] and res["output"] == "ANSWER" and res["model"] == "gpt-6-luna" and res["execution"] == "EXECUTED"
    assert res["input_tokens"] == ch.CodexHeadlessHeart.count_tokens("x" * 400) and res["output_tokens"] == 7      # the prompt as the other arms count it, not Codex's scaffold
    row = json.loads((tmp_path / "state/receipts.jsonl").read_text().splitlines()[-1])
    assert row["provider"] == "chatgpt-codex" and row["cost_class"] == "INCLUDED" and row["usage"]["cost_usd"] == 0.0 and row["metadata"]["provider_attempt_count"] == 1
    assert row["metadata"]["raw_input_tokens"] == 13139 and (tmp_path / "state/codex-prompts" / f"{row['receipt_id']}.txt").read_text() == "x" * 400


def test_an_unsupported_model_is_a_classified_failure_not_a_silent_substitution(heart):
    lease = asyncio.run(heart.acquire(role_id="REASONING", objective="x", required_skill_ids=()))
    res = asyncio.run(heart.execute(lease_id=lease["lease_id"], task="NOMODEL"))
    assert not res["success"] and res["failure_class"] == "MODEL_NOT_FOUND" and res["model"] == "gpt-6-luna" and res["execution"] == "NOT_EXECUTED"
