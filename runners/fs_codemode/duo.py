"""The QA duo executed through the Code Mode facade, with a pluggable activation policy.

With `AlwaysCritique` the decision semantics equal the QA-2D T arm (blind parallel first answers; on disagreement cross-critique, replies/concessions
under the owner rule, at most 2 exchanges; NO_CONSENSUS -> the member whose last objection was independently confirmed, else Luna). What changes is communication:
messages are typed (contract.Msg), long reasoning is compacted under invariants (sieve), duplicates to the same receiver are dropped, verification runs
deterministically in the host verifier, and every operation is in the facade's provenance. With an `EVCPolicy` the first exchange is activated only
when its estimated EVC is positive.

Production adapter: `ask(member, prompt)` = ogi013_qa1.luna_step / ogi013_qa2d.nemo_step; `verifier` = ogi013_argument.classify_argument;
`on_event` = a MangoMe ledger write. Prompts for the first answer must be byte-identical to QA-2D's (pass `answer_prompt` from ogi013_qa2d)."""
from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional

from . import sieve as sv
from .contract import Msg, Resources, parse_letter, sha, verification_level
from .evc import CRITIQUE, AlwaysCritique
from .facade import Facade

CRITIC_FALLBACK = ("\nIf you find an error, write 'ISSUES: FOUND' and then CLAIM:, EVIDENCE:, CONSEQUENCE:. If you find no error, write 'ISSUES: NONE'.\n")
REPLY_FALLBACK = ("\nIf you answer an objection, use CLAIM, EVIDENCE, CONSEQUENCE. End with 'ANSWER: <letter>'.\n")


class DuoInfra(RuntimeError):
    def __init__(self, why: str, calls: int):
        super().__init__(why)
        self.calls = calls


def run_duo(task: str, answer_prompt: str, n_options: int, ask: Callable[[str, str], dict], *, lineages: Dict[str, str],
            verifier: Optional[Callable[[str], dict]] = None, policy=None, category: str = "all", on_event=None, budget_ok=None,
            critic_instructions: str = CRITIC_FALLBACK, reply_instructions: str = REPLY_FALLBACK, max_exchanges: int = 2,
            compact_chars: int = 1200, members=("luna", "nemo"), parity: bool = False) -> dict:
    # parity=True: the prompts carry the task-relevant information the T arm's shared state gives (own answer, colleague's answer, objection); nothing is dropped or compacted, because
    # every call is stateless ("already shown" never holds across calls). Savings can then be attributed to typing and compaction only (parity=False is the lead's original mode).
    policy = policy or AlwaysCritique()
    fac = Facade(ask, verifier=verifier, on_event=on_event, budget_ok=budget_ok, max_parallel=2)
    other = {members[0]: members[1], members[1]: members[0]}
    delivered: Dict[str, set] = {}
    stats = {"compacted": 0, "dropped": 0, "chars_saved": 0}

    def send(receiver: str, mid: str, text: str, claim: str = "", result: Optional[str] = None) -> str:
        if parity:
            return text
        res = sv.sieve([{"id": mid, "claim": claim, "result": result, "text": text}], delivered, receiver, compact_chars)[0]
        if res["action"] == "drop":
            stats["dropped"] += 1
            return f"[{mid}: same claim and answer as already shown to you]"
        if res["action"] == "compact":
            stats["compacted"] += 1
            stats["chars_saved"] += len(text) - len(res["text"])
        return res["text"]

    # 1. blind first answers, independent -> parallel
    first = fac.parallel([(m, answer_prompt, "first") for m in members])
    for m, d in zip(members, first):
        if not d.get("success"):
            raise DuoInfra(f"{m} first answer: {d.get('failure_class')}", fac.totals.calls)
    text = {m: d["output"] for m, d in zip(members, first)}
    first_letters = {m: parse_letter(text[m], n_options) for m in members}
    first_tokens, first_seconds = fac.totals.tokens, fac.totals.seconds
    msgs: List[dict] = [Msg.from_output("ANSWER", m, lineages[m], text[m], n_options, msg_id=f"A-{m}").to_dict() for m in members]
    objections: List[dict] = []
    counts = {"objections": 0, "formal_objections": 0, "reproduced_objections": 0, "independently_confirmed_objections": 0,
              "verified_objections": 0, "replies": 0, "accepted_concessions": 0, "answer_changes": 0}
    letters = dict(first_letters)
    stop, exchanges = "AGREED_FIRST", 0

    if not fac.compare(letters)["agree"]:
        stop = "NO_CONSENSUS"
        for ex in range(1, max_exchanges + 1):
            if policy.decide({"exchange": ex - 1, "category": category, "letters": dict(letters)}) != CRITIQUE:
                stop = "POLICY_FINISH" if ex == 1 else stop
                break
            exchanges = ex
            jobs = []
            for judge in members:
                target = other[judge]
                body = send(judge, f"A-{target}-r{ex}", text[target], result=letters[target])
                own_note = f"\nYour own current answer (for reference):\n{text[judge]}\n" if parity else ""
                jobs.append((judge, f"{task}\n\nA colleague's answer to this question:\n{body}\n{own_note}" + critic_instructions, f"critique-{ex}"))
            crits = fac.parallel(jobs)
            filed = []
            for (judge, _p, _t), d in zip(jobs, crits):
                if not d.get("success"):
                    raise DuoInfra(f"{judge} critique: {d.get('failure_class')}", fac.totals.calls)
                out = d["output"]
                if re.match(r"\s*ISSUES:\s*NONE", out, re.I) or not (re.match(r"\s*ISSUES:\s*FOUND", out, re.I) or len(out) > 40):
                    continue
                level = verification_level(fac.verify(out))
                oid = f"O{len(objections) + 1}"
                m = Msg.from_output("OBJECTION", judge, lineages[judge], out, n_options, target=other[judge], msg_id=oid)
                m.verification = level
                o = {"id": oid, "author": judge, "target": other[judge], "level": level, "text": out, "full_ref": sha(out), "lineage": lineages[judge]}
                objections.append(o)
                msgs.append(m.to_dict())
                counts["objections"] += 1
                counts["formal_objections"] += int(level == "formal")
                counts["reproduced_objections"] += int(level == "reproduced")
                counts["independently_confirmed_objections"] += int(level == "independently_confirmed")
                counts["verified_objections"] += int(level == "independently_confirmed")
                filed.append(o)
            if not filed:
                break
            rjobs = []
            for o in filed:
                tgt = o["target"]
                own = send(tgt, f"own-{tgt}-r{ex}", text[tgt], result=letters[tgt])
                ob = send(tgt, o["id"], o["text"], claim=Msg.from_output("OBJECTION", o["author"], o["lineage"], o["text"], n_options).claim)
                colleague = f"Colleague's current answer:\n{text[o['author']]}\n\n" if parity else ""
                rjobs.append((tgt, f"{task}\n\nYour answer so far:\n{own}\n\n{colleague}Objection {o['id']} against your answer:\n{ob}\n\n"
                                   f"You are answering objection {o['id']}: name it by its id.\n" + reply_instructions, f"reply-{ex}"))
            replies = fac.parallel(rjobs)
            for o, (tgt, _p, _t), d in zip(filed, rjobs, replies):
                if not d.get("success"):
                    raise DuoInfra(f"{tgt} reply: {d.get('failure_class')}", fac.totals.calls)
                old, new = letters[tgt], parse_letter(d["output"], n_options)
                counts["replies"] += 1
                if new != old:
                    counts["answer_changes"] += 1
                    named = bool(re.search(rf"\b{re.escape(o['id'])}\b", d["output"]))
                    if named and o["lineage"] != lineages[tgt] and o["level"] in ("formal", "reproduced", "independently_confirmed"):
                        o["state"] = "ACCEPTED"
                        counts["accepted_concessions"] += 1
                letters[tgt], text[tgt] = new, d["output"]
                msgs.append(Msg.from_output("REPLY", tgt, lineages[tgt], d["output"], n_options, target=o["id"], msg_id=f"R-{o['id']}").to_dict())
            if fac.compare(letters)["agree"]:
                stop = f"CONSENSUS_EXCHANGE_{ex}"
                break

    if stop == "AGREED_FIRST" or stop.startswith("CONSENSUS"):
        letter, how = letters[members[0]], "agreed"
    elif objections and objections[-1]["level"] == "independently_confirmed":
        letter, how = letters[objections[-1]["author"]], "independently_confirmed_last_objection"
    else:
        letter, how = letters[members[0]], "luna_default"
    return {"letter": letter, "how": how, "stop": stop, "exchanges": exchanges, "policy": getattr(policy, "name", str(policy)),
            "first_by_member": first_letters, "final_positions": letters, **counts,
            "calls": fac.totals.calls, "tokens": fac.totals.tokens, "seconds": fac.totals.seconds,
            "phase_tokens": {"first": first_tokens, "exchange": fac.totals.tokens - first_tokens},
            "phase_seconds": {"first": first_seconds, "exchange": round(fac.totals.seconds - first_seconds, 3)},
            "communication": stats, "parity": parity, "messages": msgs, "objection_states": [o.get("state", "OPEN") for o in objections],
            "provenance": fac.provenance}
