"""OGI-013 QA-2D: pre-registered comparison of the Luna + nemotron duo (0 EUR, no Claude member). Arms per question (sequential questions, paired):
  T  duo: blind first answers; equal -> final, 2 calls; different -> cross-critique, replies/concessions (owner rule), at most 2 exchanges, logged position changes;
     unresolved = NO_CONSENSUS: final = the answer of the member whose LAST objection was GROUNDED_VERIFIED, else Luna's
  E  equal effort, no organisation: k blind drafts alternating Luna / nemotron, k = T's calls on that question, majority vote, tie -> Luna
  SL Luna alone (1 call; QA-1 L rows are reused for the 198 QA-1 ids, same prompt)
  SN nemotron alone (1 call)
No hidden retries: every call is made once. Pauses (exit 76, resumable on the same lock): a subscription/provider limit message, an infra-failure share above 10 % in any arm after 40 questions,
the run cap of 3,000 invocations."""
from __future__ import annotations

import argparse
import json
import re
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import ogi013_argument as ag
import ogi013_qa1 as q1
from ogi013_qa1 import (ANSWER_SUFFIX, LUNA_KEY, LUNA_LINEAGE, NEMO_KEY, NEMO_LINEAGE, SMALL_FAIL, Context, Infra, attempt, finish, grade, load_jsonl, luna_step, parse_letter, question_prompt)

RUN_CAP = 3000
PAUSE_CODE = 76
INFRA_SHARE_LIMIT, INFRA_WINDOW = 0.10, 40
MAX_EXCHANGES = 2
NEMO_QUOTA = re.compile(r"quota|usage limit|daily|monthly|exhausted|credit", re.I)
ARMS = ("T", "E", "SL", "SN")


def answer_prompt(q: dict) -> str:
    return question_prompt(q) + ANSWER_SUFFIX


def majority_tie_luna(drafts: list) -> str | None:
    """drafts: [(member, letter)] in call order. Majority of the parsed letters; a tie goes to the tied letter Luna gave first (else the earliest)."""
    letters = [l for _m, l in drafts if l]
    if not letters:
        return None
    top = max(Counter(letters).values())
    tied = {l for l, n in Counter(letters).items() if n == top}
    for m, l in drafts:
        if m == "luna" and l in tied:
            return l
    return next(l for l in letters if l in tied)


def final_unresolved(objections: list, current: dict) -> tuple:
    """NO_CONSENSUS rule: the answer of the member whose LAST objection was GROUNDED_VERIFIED, else Luna's. objections: chronological [{author: member, level}]; current: member -> letter."""
    if objections and objections[-1].get("level") == "verified":
        return current[objections[-1]["author"]], "verified_last_objection"
    return current["luna"], "luna_default"


TERMINAL_HEALTH = {"QUOTA_EXHAUSTED", "AUTH_EXPIRED", "UNAVAILABLE"}


def nemo_terminal(ctx: Context) -> str | None:
    """PlumMe's own availability facts for the pinned model after its network-free requalify(): terminal offer health (exhausted / auth / unavailable) means the model leaves the run
    (a quota-exhausted model is never called again) and the run pauses. Cooldown states are left to the call (it fails once, counted as infrastructure)."""
    try:
        ctx.stack.svc.scheduler.requalify()
    except Exception:  # noqa: BLE001
        pass
    offers = q1.plum_state(ctx, NEMO_KEY)["offers"]
    if offers and all(o["health"] in TERMINAL_HEALTH for o in offers):
        return "NEMOTRON_" + "/".join(sorted({o["health"] for o in offers}))
    return None


MAX_COOLDOWN_WAIT_S = 300


def cooldown_wait(offers: list) -> float:
    """Seconds to wait BEFORE a call while PlumMe reports the pinned model in a short cooldown (not exhausted): the longest PlumMe-reported retry window plus the requalify dwell margin.
    This is scheduling, not a retry: the call is made once, after the window. 0 when the offer is available; a window above MAX_COOLDOWN_WAIT_S is not waited for (the call fails once)."""
    if not offers or any(o["health"] in TERMINAL_HEALTH for o in offers):
        return 0.0
    if all(o["health"] == "AVAILABLE" and not o["circuit_open"] and o["credential_available"] for o in offers):
        return 0.0
    windows = [o.get("retry_after_s") for o in offers if o.get("retry_after_s")]
    wait = (max(windows) if windows else 60.0) + 2.0
    return wait if wait <= MAX_COOLDOWN_WAIT_S else 0.0


class Timing:
    """Per-arm timing records (Phase C is built on them): every call with its kind, member, seconds and outcome, plus prompt-building and persistence time."""

    def __init__(self):
        self.calls, self.build_s, self.persist_s, self.init_s = [], 0.0, 0.0, 0.0
        self.lock = threading.Lock()

    def add(self, kind: str, member: str, seconds: float, ok: bool):
        with self.lock:
            self.calls.append({"kind": kind, "member": member, "seconds": round(seconds, 2), "ok": ok})

    def report(self) -> dict:
        return {"calls": self.calls, "prompt_build_s": round(self.build_s, 3), "persist_s": round(self.persist_s, 3), "init_s": round(self.init_s, 2)}


def nemo_step(ctx: Context, ep, prompt: str) -> dict:
    """One nemotron invocation through PlumMe (pinned model, single attempt, no sticky retry; route failover inside the model is PlumMe's and charged to the run budget)."""
    if ctx.stop:
        return {**SMALL_FAIL, "failure_class": "RUN_STOPPED"}
    why = nemo_terminal(ctx)
    if why:
        ctx.stop = why
        return {**SMALL_FAIL, "failure_class": why}
    wait = cooldown_wait(q1.plum_state(ctx, NEMO_KEY)["offers"])
    if wait:
        with ctx.results_lock:
            ctx.cooldown_waits = getattr(ctx, "cooldown_waits", 0) + 1
            ctx.cooldown_wait_s = getattr(ctx, "cooldown_wait_s", 0.0) + wait
        time.sleep(wait)
        nemo_terminal(ctx)                                                 # requalify() after the window
    try:
        d = ep.fork().step(prompt, "author", prefer=NEMO_KEY, sticky_attempts=99, max_attempts=1)
    except Exception as exc:  # noqa: BLE001
        msg = f"{type(exc).__name__}: {str(exc)[:200]}"
        if "RUN_PROVIDER_CALLS" in msg:
            ctx.stop = "RUN_CAP"
        elif NEMO_QUOTA.search(msg):
            ctx.stop = "NEMOTRON_LIMIT: " + msg
        return {**SMALL_FAIL, "failure_class": msg}
    if d.get("success") and d.get("model_key") == NEMO_KEY:
        return d
    return {**SMALL_FAIL, "failure_class": str(d.get("failure_class"))[:200]}


def _fail(kind: str, why: str, calls: int):
    exc = Infra(kind, why)
    exc.calls = calls
    return exc


# ---- arm T --------------------------------------------------------------------------------------------------------------------------------------------------
def run_T(ctx: Context, q: dict) -> dict:
    from ogi013_mango_ledger import MangoLedger
    from ogi013_team_code import TeamState
    t0, luna0 = time.monotonic(), ctx.luna_tokens
    tm = Timing()
    ep = ctx.episode("T", q["id"])
    tm.init_s = time.monotonic() - t0
    tok_now = lambda: ep.stats["tokens_in"] + ep.stats["tokens_out"] + (ctx.luna_tokens - luna0)  # noqa: E731 - EVC logging: tokens / seconds per phase
    phase_tokens, phase_seconds, per_exchange = {}, {}, []
    n_opt, task = len(q["options"]), question_prompt(q)
    team = TeamState(task, ctx.out / "events" / f"{q['id']}_T_team_state.md")
    team.mango = MangoLedger(ctx.stack.fs.mango, ep.work, ep.actor, ep.turn_id, ep.sid)
    team.roster_changes_provider = lambda: []
    team.independent = True
    members = {"luna": SimpleNamespace(name="luna", id="S1", slot="solver1", model=LUNA_KEY, lineage=LUNA_LINEAGE, status="open", rev=0, diff="", test_tail=""),
               "nemo": SimpleNamespace(name="nemo", id="S2", slot="solver2", model=NEMO_KEY, lineage=NEMO_LINEAGE, status="open", rev=0, diff="", test_tail="")}
    for m in members.values():
        team.pos[m.id] = m
    cnt, clock = Counter(), threading.Lock()
    other = {"luna": "nemo", "nemo": "luna"}

    def view(base: str) -> str:
        t = time.monotonic()
        ts = team.prompt(None)                                           # MangoMe is the live workspace
        tm.build_s += time.monotonic() - t
        return base + (f"\n<team_state>\n{ts}\n</team_state>\n" if ts else "")

    def persist():
        t = time.monotonic()
        team.persist()
        tm.persist_s += time.monotonic() - t

    def ask(name: str, prompt: str, kind: str = "call") -> dict:
        with clock:
            cnt["calls"] += 1
        t = time.monotonic()
        d = luna_step(ctx, prompt) if name == "luna" else nemo_step(ctx, ep, prompt)
        tm.add(kind, name, time.monotonic() - t, bool(d.get("success")))
        return d

    def letter_of(name: str):
        return parse_letter(members[name].diff, n_opt)

    # blind first answers (parallel; 2 calls)
    with ThreadPoolExecutor(2) as tp:
        fl, fn = tp.submit(ask, "luna", answer_prompt(q), "first"), tp.submit(ask, "nemo", answer_prompt(q), "first")
        first = {"luna": fl.result(), "nemo": fn.result()}
    for name, d in first.items():
        if not d["success"]:
            raise _fail("INFRA_STEP_FAILED", f"{name} first answer: {d.get('failure_class')}", cnt["calls"])
        members[name].diff, members[name].status = d["output"], "submitted"
    persist()
    phase_tokens["first"], phase_seconds["first"] = tok_now(), round(time.monotonic() - t0, 2)
    first_letters = {name: letter_of(name) for name in members}
    first_by_pos = {members[n].id: first_letters[n] for n in members}
    team.independent = False
    objs_chrono: list = []
    stop, exchanges = "AGREED_FIRST", 0
    if not (first_letters["luna"] and first_letters["luna"] == first_letters["nemo"]):
        stop = "NO_CONSENSUS"
        for ex in range(1, MAX_EXCHANGES + 1):
            exchanges = ex
            ex_t0, ex_tok0, before = time.monotonic(), tok_now(), {n: letter_of(n) for n in members}
            ex_levels = []
            # cross-critique: each member judges the other's position
            def critique(judge: str, target: str):
                pos = members[target]
                return judge, target, ask(judge, view(f"{task}\n\nA colleague's answer to this question:\n{pos.diff}\n" + ag.CRITIC_INSTRUCTIONS + ANSWER_SUFFIX), "critique")
            with ThreadPoolExecutor(2) as tp:
                crits = [f.result() for f in [tp.submit(critique, "luna", "nemo"), tp.submit(critique, "nemo", "luna")]]
            filed = []
            for judge, target, d in crits:
                if not d["success"]:
                    raise _fail("INFRA_STEP_FAILED", f"{judge} critique: {d.get('failure_class')}", cnt["calls"])
                text = d["output"]
                if re.match(r"\s*ISSUES:\s*NONE", text, re.I) or not (re.match(r"\s*ISSUES:\s*FOUND", text, re.I) or len(text) > 40):
                    continue
                ground = ag.ledger_ground(ag.classify_argument(text, task))
                oid = team.objection(members[target].id, members[judge].lineage, text, grounded=ground["kind"] in ("quote", "command"), ground=ground)
                cnt["objections"] += 1
                cnt["grounded_objections"] += int(ground["kind"] in ("quote", "command"))
                objs_chrono.append({"oid": oid, "author": judge, "target": target, "level": ground.get("level")})
                ex_levels.append({"author": judge, "target": target, "level": ground.get("level")})
                filed.append((oid, judge, target))
            persist()

            # replies: each objected member answers once, naming the objection
            def reply(oid: str, target: str):
                o = next(x for x in team.objs if x["id"] == oid)
                pos = members[target]
                prompt = view(f"{task}\n\nYour answer so far:\n{pos.diff}\n\nObjection {oid} against your answer:\n{o['text']}\n\nYou are answering objection {oid}: name it by its id.\n" + ag.REPLY_INSTRUCTIONS + ANSWER_SUFFIX)
                return oid, target, ask(target, prompt, "reply")
            with ThreadPoolExecutor(2) as tp:
                answers = [f.result() for f in [tp.submit(reply, oid, target) for oid, _j, target in filed]]
            for oid, target, d in answers:
                if not d["success"]:
                    raise _fail("INFRA_STEP_FAILED", f"{target} reply: {d.get('failure_class')}", cnt["calls"])
                pos, o = members[target], next(x for x in team.objs if x["id"] == oid)
                old, new = parse_letter(pos.diff, n_opt), parse_letter(d["output"], n_opt)
                if new != old:
                    team.reply(oid, "author", "concede", d["output"])
                    cnt["answer_changes"] += 1
                    if q1.accepted_concession(d["output"], o, pos.lineage, old, new):
                        o["concession"] = {"named": True, "from": old, "to": new}
                        team.accept(oid, concession={"from": old, "to": new})
                        cnt["accepted_concessions"] += 1
                else:
                    r = team.reply(oid, "author", "evidence", d["output"], ag.ledger_ground(ag.classify_argument(d["output"], task)))
                    cnt["kept_replies"] += 1
                    cnt["evidenced_replies"] += int(bool(r.get("ok")))
                pos.diff, pos.rev, pos.status = d["output"], pos.rev + 1, "revised"
                team.decisions.append(f"{pos.id} revised (letter {old} -> {new}) responding to {oid}")
            persist()
            per_exchange.append({"exchange": ex, "letters_before": before, "letters_after": {n: letter_of(n) for n in members}, "objection_levels": ex_levels,
                                 "tokens": tok_now() - ex_tok0, "seconds": round(time.monotonic() - ex_t0, 2)})
            if letter_of("luna") and letter_of("luna") == letter_of("nemo"):
                stop = f"CONSENSUS_EXCHANGE_{ex}"
                break
    current = {n: letter_of(n) for n in members}
    if stop == "AGREED_FIRST" or stop.startswith("CONSENSUS"):
        letter, how = current["luna"], "agreed"
    else:
        letter, how = final_unresolved(objs_chrono, current)
    team.release = {"class": "QA2D_FINAL", "letter": letter, "how": how, "stop": stop}
    team.decisions.append(f"final answer {letter} ({how}, {stop})")
    team.persist()
    lv = lambda o, k: (o.get("ground") or {}).get("level") == k  # noqa: E731
    row = {"letter": letter, "how": how, "stop": stop, "exchanges": exchanges, "calls": cnt["calls"], "first_letters": {members[n].id: first_letters[n] for n in members}, "first_by_pos": first_by_pos,
           "final_positions": {members[n].id: current[n] for n in members}, "objections": cnt["objections"], "grounded_objections": cnt["grounded_objections"],
           "independent_grounded_objections": cnt["grounded_objections"], "formal_objections": sum(1 for o in team.objs if lv(o, "formal")), "verified_objections": sum(1 for o in team.objs if lv(o, "verified")),
           "evidenced_replies": cnt["evidenced_replies"], "formal_replies": sum(1 for o in team.objs for r in o.get("replies", []) if r.get("evidence") == "quote"),
           "verified_replies": sum(1 for o in team.objs for r in o.get("replies", []) if r.get("evidence") == "command"), "accepted_concessions": cnt["accepted_concessions"],
           "answer_changes": cnt["answer_changes"], "evidenced_withdrawn": 0, "independence_ok": True,
           "objection_target_first": [first_by_pos.get(o["target"]) for o in team.objs], "objection_states": [o["state"] for o in team.objs],
           "lineages": {"positions": {m.id: m.lineage for m in members.values()}, "critics": sorted({o["lineage"] for o in team.objs if o.get("lineage")})},
           "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"] + (ctx.luna_tokens - luna0), "seconds": round(time.monotonic() - t0, 1),
           "mango_writes": team.mango.writes, "mango_reads": team.mango.reads, "work_ref": ep.work, "timing": tm.report(),
           "category": q.get("category"), "phase_tokens": {"first": phase_tokens["first"], "exchange": tok_now() - phase_tokens["first"]},
           "phase_seconds": {"first": phase_seconds["first"], "exchange": round(time.monotonic() - t0 - phase_seconds["first"], 2)}, "per_exchange": per_exchange}
    (ctx.out / "exchange").mkdir(exist_ok=True)
    (ctx.out / "exchange" / f"{q['id']}.json").write_text(json.dumps({"first_answers": {n: first[n]["output"] for n in first}, "objections": team.objs, "decisions": team.decisions, "final": team.release}, default=str))
    return row


def store_outputs(ctx: Context, qid: str, arm: str, outputs: dict) -> None:
    """Every answer is stored in full (not in results.jsonl; never committed)."""
    (ctx.out / "exchange").mkdir(exist_ok=True)
    (ctx.out / "exchange" / f"{qid}_{arm}.json").write_text(json.dumps(outputs))


# ---- arms E / SL / SN ---------------------------------------------------------------------------------------------------------------------------------------
def run_E(ctx: Context, q: dict, k: int) -> dict:
    t0, luna0 = time.monotonic(), ctx.luna_tokens
    ep = ctx.episode("E", q["id"])
    n_opt, prompt = len(q["options"]), answer_prompt(q)
    order = ["luna" if i % 2 == 0 else "nemo" for i in range(k)]            # alternating, Luna first

    tm = Timing()

    def draft(name):
        t = time.monotonic()
        d = luna_step(ctx, prompt) if name == "luna" else nemo_step(ctx, ep, prompt)
        tm.add("draft", name, time.monotonic() - t, bool(d.get("success")))
        return d
    with ThreadPoolExecutor(2) as tp:
        ds = list(tp.map(draft, order))
    bad = [(n, d.get("failure_class")) for n, d in zip(order, ds) if not d["success"]]
    if bad:
        raise _fail("INFRA_STEP_FAILED", f"draft failed: {bad[0]}", k)
    drafts = [(n, parse_letter(d["output"], n_opt)) for n, d in zip(order, ds)]
    store_outputs(ctx, q["id"], "E", {n + str(i): d["output"] for i, (n, d) in enumerate(zip(order, ds))})
    return {"letter": majority_tie_luna(drafts), "draft_letters": [l for _n, l in drafts], "k": k, "calls": k, "timing": tm.report(), "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"] + (ctx.luna_tokens - luna0),
            "seconds": round(time.monotonic() - t0, 1), "work_ref": ep.work}


def run_SL(ctx: Context, q: dict) -> dict:
    t0, luna0 = time.monotonic(), ctx.luna_tokens
    d = luna_step(ctx, answer_prompt(q))                                     # the identical prompt of the QA-1 L arm and of every first answer
    if not d["success"]:
        raise _fail("INFRA_LUNA_FAILED", str(d.get("failure_class")), 1)
    store_outputs(ctx, q["id"], "SL", {"luna": d["output"]})
    return {"letter": parse_letter(d["output"], len(q["options"])), "calls": 1, "tokens": ctx.luna_tokens - luna0, "seconds": round(time.monotonic() - t0, 1),
            "timing": {"calls": [{"kind": "answer", "member": "luna", "seconds": round(time.monotonic() - t0, 2), "ok": True}]}}


def run_SN(ctx: Context, q: dict) -> dict:
    t0 = time.monotonic()
    ep = ctx.episode("SN", q["id"])
    d = nemo_step(ctx, ep, answer_prompt(q))
    if not d["success"]:
        raise _fail("INFRA_STEP_FAILED", str(d.get("failure_class")), 1)
    store_outputs(ctx, q["id"], "SN", {"nemo": d["output"]})
    return {"letter": parse_letter(d["output"], len(q["options"])), "calls": 1, "tokens": ep.stats["tokens_in"] + ep.stats["tokens_out"], "seconds": round(time.monotonic() - t0, 1), "work_ref": ep.work,
            "timing": {"calls": [{"kind": "answer", "member": "nemo", "seconds": round(time.monotonic() - t0, 2), "ok": True}]}}


# ---- driver -------------------------------------------------------------------------------------------------------------------------------------------------
def infra_share_exceeded(rows_by_arm: dict, window: int = INFRA_WINDOW, limit: float = INFRA_SHARE_LIMIT) -> str | None:
    for arm, rows in rows_by_arm.items():
        if len(rows) >= window and sum(1 for r in rows if r["status"] != "OK") / len(rows) > limit:
            return arm
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--qa1-results", type=Path, required=True, help="QA-1 results.jsonl: its L rows are reused as SL for the QA-1 ids")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--call-cap", type=int, default=2)
    a = ap.parse_args(argv)
    a.out.mkdir(parents=True, exist_ok=True)
    ctx = Context(a.out, None, a.call_cap)
    from plumme.budget import RunBudget
    used_path = a.out / "invocations.json"
    budget = RunBudget(max_provider_calls=RUN_CAP, max_cost_usd=0.0)
    budget.provider_attempt_count = json.loads(used_path.read_text())["used"] if used_path.exists() else 0
    ctx.stack.svc.set_run_budget(budget)
    ctx.run_budget = budget
    import ogi013_vote
    ogi013_vote.TEXT_CAP_OBJECTION = ogi013_vote.TEXT_CAP_REPLY = 10 ** 6
    why = nemo_terminal(ctx)
    if why:                                                               # nothing is called: the pinned model is unavailable at start (e.g. a gateway cooldown at discovery)
        print(json.dumps({"pause": why, "after_question": None, "used": budget.provider_attempt_count, "plumme": q1.plum_state(ctx, NEMO_KEY)}, default=str), flush=True)
        return PAUSE_CODE
    qs = load_jsonl(a.data)[: a.limit or None]
    res_path = a.out / "results.jsonl"
    res_path.parent.mkdir(parents=True, exist_ok=True)
    rows = load_jsonl(res_path) if res_path.exists() else []
    by = {(r["qid"], r["arm"]): r for r in rows}
    sink_lock = threading.Lock()

    def sink(row):
        with sink_lock:
            with res_path.open("a") as fh:
                fh.write(json.dumps(row) + "\n")
            used_path.write_text(json.dumps({"used": budget.provider_attempt_count}))
        by[(row["qid"], row["arm"])] = row
        print(json.dumps({k: row.get(k) for k in ("qid", "arm", "letter", "correct", "status", "calls", "tokens", "seconds")}), flush=True)

    for r in load_jsonl(a.qa1_results):                                      # SL for the QA-1 ids = the QA-1 L rows (same prompt, same model)
        if r["arm"] == "L" and (r["qid"], "SL") not in by and any(q["id"] == r["qid"] for q in qs):
            sink({**{k: r.get(k) for k in ("qid", "key", "letter", "correct", "status", "calls", "tokens", "seconds")}, "arm": "SL", "infra_detail": r.get("infra_detail"), "rerun": False, "reused_from": "QA-1 L"})
    window: dict = {arm: [] for arm in ARMS}
    processed = 0
    for q in qs:
        for arm in ARMS:
            if (q["id"], arm) in by:
                continue
            if ctx.stop:
                break
            if arm == "T":
                res = attempt(run_T, ctx, q)
            elif arm == "E":
                t = by.get((q["id"], "T"))
                res = attempt(run_E, ctx, q, max(2, int((t or {}).get("calls") or 2)))
            elif arm == "SL":
                res = attempt(run_SL, ctx, q)
            else:
                res = attempt(run_SN, ctx, q)
            if ctx.stop:                                                  # a limit message mid-arm: the row is not finished, it is discarded and re-run after the pause
                break
            row = finish(q, arm, res, False)
            if arm == "T":
                from ogi013_qa1 import chain_class, chain_labels, chain_stages
                st = chain_stages(row) if row["status"] == "OK" else None
                if st:
                    row.update(chain=st, chain_class=chain_class(row) if st["complete"] else None, chain_labels=chain_labels(row))
            sink(row)
            window[arm].append(row)
        if ctx.stop:
            print(json.dumps({"pause": ctx.stop, "after_question": q["id"], "used": budget.provider_attempt_count}), flush=True)
            return PAUSE_CODE
        processed += 1
        if processed >= INFRA_WINDOW:
            bad = infra_share_exceeded(window)
            if bad:
                print(json.dumps({"pause": f"INFRA_SHARE_ABOVE_10PCT:{bad}", "after_question": q["id"], "used": budget.provider_attempt_count}), flush=True)
                return PAUSE_CODE
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
