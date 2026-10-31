"""Production adapter: the QA duo through the Code Mode facade on the real stack (Luna via codex heart, nemotron via PlumMe, MangoMe ledger,
sandbox verifier). Status: IMPLEMENTED only. It needs the VPS stack and is verified there (HOST_VERIFIED) by the host check in the master order.

Same first-answer prompt as QA-2D (ogi013_qa2d.answer_prompt, byte-identical), same critic/reply instructions (ogi013_argument), same calls
(ogi013_qa1.luna_step, ogi013_qa2d.nemo_step: no hidden retries, RunBudget-charged). Every facade operation is written to MangoMe."""
from __future__ import annotations

import time

from fs_codemode.duo import DuoInfra, run_duo
from fs_codemode.evc import AlwaysCritique


def run_T_codemode(ctx, q: dict, policy=None, parity: bool = False) -> dict:
    import ogi013_argument as ag
    from ogi013_mango_ledger import MangoLedger
    from ogi013_qa1 import ANSWER_SUFFIX, LUNA_LINEAGE, NEMO_LINEAGE, Infra, grade, luna_step, question_prompt
    from ogi013_qa2d import answer_prompt, nemo_step

    t0 = time.monotonic()
    ep = ctx.episode("TC", q["id"])
    led = MangoLedger(ctx.stack.fs.mango, ep.work, ep.actor, ep.turn_id, ep.sid)

    def ask(member: str, prompt: str) -> dict:
        if member == "luna":
            before = ctx.luna_tokens
            d = dict(luna_step(ctx, prompt))
            d["tokens"] = ctx.luna_tokens - before
        else:
            before = ep.stats["tokens_in"] + ep.stats["tokens_out"]
            d = dict(nemo_step(ctx, ep, prompt))
            d["tokens"] = ep.stats["tokens_in"] + ep.stats["tokens_out"] - before
        return d

    def on_event(ev: dict) -> None:
        led.write("CODEMODE_OP", f"{q['id']}:{ev['seq']}:{ev['op']}", dict(ev))

    try:
        r = run_duo(question_prompt(q), answer_prompt(q), len(q["options"]), ask, lineages={"luna": LUNA_LINEAGE, "nemo": NEMO_LINEAGE},
                    verifier=ag.classify_argument, policy=policy or AlwaysCritique(), category=q.get("category") or "all", on_event=on_event,
                    budget_ok=lambda: not ctx.stop, critic_instructions=ag.CRITIC_INSTRUCTIONS + ANSWER_SUFFIX, reply_instructions=ag.REPLY_INSTRUCTIONS + ANSWER_SUFFIX, parity=parity)    # same trailing text as the QA-2D T prompts
    except DuoInfra as exc:
        e = Infra("INFRA_STEP_FAILED", str(exc))
        e.calls = exc.calls
        raise e
    r.update({"qid": q["id"], "key": q["key"], "correct": grade(r["letter"], q["key"]), "work_ref": ep.work,
              "mango_writes": led.writes, "mango_reads": led.reads, "wall_seconds": round(time.monotonic() - t0, 1)})
    return r
