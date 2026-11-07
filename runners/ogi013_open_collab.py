#!/usr/bin/env python3
"""Open-question cooperation test (owner, 2026-11-07): Luna + nemotron answer one question that has no right/wrong answer; the claim tested is that the cooperation (blind drafts -> cross-critique ->
named replies/revisions -> closing plan) yields a plan the two models would not have produced alone. Real stack (Context/Episode, PlumMe supply, MangoMe episode), hard run-cap, no retries.
Usage: ogi013_open_collab.py --out DIR --question FILE --brief FILE [--run-cap 40]"""
import argparse
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ogi013_qa1 import Context, LUNA_KEY, NEMO_KEY, luna_step

FORMAT = ("Format: a numbered plan, at most 8 items. Each item: ACTION (concrete), WHY (evidence from the brief), VERIFY (how the owner would know it worked), COST (tokens/effort, zero cash). "
          "No flattery, no restating the brief.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--question", type=Path, required=True)
    ap.add_argument("--brief", type=Path, required=True)
    ap.add_argument("--run-cap", type=int, default=40)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, None, 2)
    from plumme.budget import RunBudget
    ctx.run_budget = RunBudget(max_provider_calls=a.run_cap, max_cost_usd=0.0)
    ctx.stack.svc.set_run_budget(ctx.run_budget)
    q, brief = a.question.read_text().strip(), a.brief.read_text().strip()
    ep = ctx.episode("T", "open1")
    log: list[dict] = []

    def ask(who: str, stage: str, prompt: str) -> str:
        d = luna_step(ctx, prompt) if who == "luna" else ep.fork().step(prompt, stage, prefer=NEMO_KEY, sticky_attempts=99)
        ok = bool(d.get("success")) and d.get("model_key") == (LUNA_KEY if who == "luna" else NEMO_KEY)
        log.append({"who": who, "stage": stage, "ok": ok, "model": d.get("model_key"), "failure": d.get("failure_class"), "text": d.get("output") if ok else None})
        (a.out / "transcript.json").write_text(json.dumps(log, indent=1))
        if not ok:
            raise SystemExit(f"STOP: {who}/{stage} failed ({d.get('failure_class')}); no retry, no substitute model")
        return d["output"]

    base = f"BRIEF\n{brief}\n\nQUESTION\n{q}\n\n{FORMAT}"
    with ThreadPoolExecutor(2) as pool:                                              # R1: blind, parallel; neither sees the other
        fl, fn = pool.submit(ask, "luna", "draft", base), pool.submit(ask, "nemotron", "draft", base)
        draft = {"luna": fl.result(), "nemotron": fn.result()}
    crit_fmt = ("Critique the OTHER plan. Give 1-3 objections, each exactly: CLAIM: <what is wrong or missing> / EVIDENCE: <from the brief or checkable fact> / CONSEQUENCE: <what goes wrong if unfixed>. "
                "Then ADOPT: list items of the other plan you would take over. Be specific; no praise.")
    with ThreadPoolExecutor(2) as pool:                                              # R2: cross-critique
        cl = pool.submit(ask, "luna", "critique", f"{base}\n\nYOUR OWN PLAN\n{draft['luna']}\n\nTHE OTHER PLAN\n{draft['nemotron']}\n\n{crit_fmt}")
        cn = pool.submit(ask, "nemotron", "critique", f"{base}\n\nYOUR OWN PLAN\n{draft['nemotron']}\n\nTHE OTHER PLAN\n{draft['luna']}\n\n{crit_fmt}")
        crit = {"luna": cl.result(), "nemotron": cn.result()}                         # luna's critique targets nemotron's plan and vice versa
    rep_fmt = ("The other model critiqued YOUR plan. For each objection answer ACCEPT or REJECT with a reason (an objection you cannot refute must be ACCEPTED). Then give your REVISED plan "
               "(same format), marking each item NEW (changed because of the critique), KEPT, or ADOPTED-FROM-OTHER.")
    with ThreadPoolExecutor(2) as pool:                                              # R3: named replies and revisions
        rl = pool.submit(ask, "luna", "reply", f"{base}\n\nYOUR PLAN\n{draft['luna']}\n\nCRITIQUE OF YOUR PLAN\n{crit['nemotron']}\n\n{rep_fmt}")
        rn = pool.submit(ask, "nemotron", "reply", f"{base}\n\nYOUR PLAN\n{draft['nemotron']}\n\nCRITIQUE OF YOUR PLAN\n{crit['luna']}\n\n{rep_fmt}")
        rev = {"luna": rl.result(), "nemotron": rn.result()}
    close = (f"{base}\n\nTWO REVISED PLANS after cross-critique.\nPLAN L:\n{rev['luna']}\n\nPLAN N:\n{rev['nemotron']}\n\n"
             "Write the FINAL joint plan (same format). Rules: keep an item only if justified; where the plans conflict, decide and say why; tag each final item [L], [N], [BOTH] or [MERGED] "
             "(merged = combines parts of both). End with REJECTED: items dropped and why.")
    final = ask("luna", "close", close)                                              # R4: Luna closes (QA-2D rule: Luna unless a verified objection stands)
    check = ask("nemotron", "final_check", f"{base}\n\nFINAL JOINT PLAN\n{final}\n\nAnswer AGREE or OBJECT (one CLAIM/EVIDENCE/CONSEQUENCE objection max), then one line: is this plan better than your own first draft, and why?")
    pack = {"draft": draft, "critique": crit, "revised": rev, "final": final, "nemotron_final_check": check, "calls": ctx.run_budget.provider_attempt_count}
    (a.out / "result.json").write_text(json.dumps(pack, indent=1))
    keys = ["final", "luna_draft", "nemotron_draft"]
    random.Random(7).shuffle(keys)                                                   # blind comparison pack: labels A/B/C, key kept separately
    texts = {"final": final, "luna_draft": draft["luna"], "nemotron_draft": draft["nemotron"]}
    (a.out / "blind_pack.md").write_text("\n\n".join(f"## PLAN {c}\n\n{texts[k]}" for c, k in zip("ABC", keys)))
    (a.out / "blind_key.json").write_text(json.dumps(dict(zip("ABC", keys))))
    print(json.dumps({"ok": True, "calls": pack["calls"], "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"] + ctx.luna_tokens}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
