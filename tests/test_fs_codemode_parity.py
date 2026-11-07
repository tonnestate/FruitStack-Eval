"""Code Mode information parity: in parity mode every prompt carries the task-relevant information T's shared state gives (own answer, colleague's answer, objection), nothing is
dropped or compacted across (stateless) calls, and savings can then be attributed to typing/compaction only."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runners"))
from fs_codemode.duo import run_duo  # noqa: E402

OBJECTION = "ISSUES: FOUND\nCLAIM: Option A is wrong because the order of 5 in U_8 is 2.\nEVIDENCE: 5^2 = 25 = 1 mod 8, so the smallest k is 2.\nCONSEQUENCE: Option F follows, not option A."


def scripted(prompts):
    def ask(member, prompt):
        prompts.append((member, prompt))
        if "A colleague's answer" in prompt:
            return {"success": True, "output": "ISSUES: NONE" if member == "luna" else OBJECTION, "tokens": 10}
        if "Objection O1" in prompt:
            return {"success": True, "output": "O1: you are right. ANSWER: F", "tokens": 10}
        return {"success": True, "output": "I think ANSWER: A" if member == "luna" else "The order is 2. ANSWER: F", "tokens": 10}
    return ask


def run(parity):
    prompts = []
    r = run_duo("TASK TEXT", "ANSWER PROMPT", 10, scripted(prompts), lineages={"luna": "luna", "nemo": "nemotron"}, parity=parity)
    return r, prompts


def test_without_parity_the_critic_does_not_see_its_own_answer():
    _r, prompts = run(False)
    crit = [p for m, p in prompts if m == "luna" and "A colleague's answer" in p][0]
    assert "I think ANSWER: A" not in crit                                   # the information difference to T


def test_parity_mode_gives_critic_and_author_the_same_task_relevant_information_as_t():
    r, prompts = run(True)
    crit_luna = [p for m, p in prompts if m == "luna" and "A colleague's answer" in p][0]
    assert "I think ANSWER: A" in crit_luna and "The order is 2. ANSWER: F" in crit_luna        # own and colleague's answer
    reply = [p for m, p in prompts if m == "luna" and "Objection O1" in p][0]
    assert "I think ANSWER: A" in reply and "The order is 2. ANSWER: F" in reply and "CLAIM: Option A is wrong" in reply
    assert r["letter"] == "F" and r["communication"]["dropped"] == 0 and r["communication"]["compacted"] == 0


def test_parity_mode_never_drops_or_compacts_across_stateless_calls():
    prompts = []
    long = "x " * 2000 + "ANSWER: A"
    def ask(member, prompt):
        prompts.append(prompt)
        if "A colleague's answer" in prompt:
            return {"success": True, "output": "ISSUES: NONE", "tokens": 1}
        return {"success": True, "output": long if member == "luna" else "ANSWER: F", "tokens": 1}
    run_duo("T", "P", 10, ask, lineages={"luna": "luna", "nemo": "nemotron"}, parity=True)
    assert any(long in p for p in prompts if "A colleague's answer" in p)    # the long answer reaches the critic uncompacted
