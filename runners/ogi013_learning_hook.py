"""Brother Mode <-> organizational-learning ledger (runners/ogi013_org_discoveries.py). Opt-in: run_T(..., learning=LearningHook(...)); without it nothing changes.

capture   after an episode: model-asserted claims (accepted objections, answers changed by cooperation) are recorded as DISCOVERY with model/lineage/receipt provenance.
          A claim becomes INDEPENDENTLY_CHECKED only through a trusted execution receipt (ground["receipt"], ledger.execution_receipt); a worker's self-reported
          verification / ground level without one is recorded as a MODEL_ASSERTED verification and never makes the claim knowledge.
brief     before a later episode: verified, applicable discoveries (ledger.retrievable, with its leak guard) become the `brief` of cherryme run_rounds (the solve prompt slot
          `{brief}`), labelled as organizational knowledge that must still fit the task. RETRIEVAL and APPLICATION are recorded. apply=False records nothing and injects nothing.
outcomes  after grading, from the grader's side only (never in the live context): applied-vs-control reward per applied discovery. Benchmark keys / grading results are never
          passed to capture or brief.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ogi013_org_discoveries import Ledger, _h, _terms, overlap

_CLAIM = re.compile(r"CLAIM:\s*(.+?)(?:\n\s*(?:EVIDENCE|CONSEQUENCE):|\Z)", re.S)


def format_brief(items: list[dict]) -> str:
    """The brief text shown in the solve prompt's `{brief}` slot (shared by the memory arm and the EVAL-002 sham arm, so both have the same form)."""
    if not items:
        return ""
    lines = "\n".join(f"- {' '.join(i['claim'].split())[:300]} (applies: {i['applicability']}; independently verified)" for i in items)
    return "Organizational knowledge from earlier verified work (check that it fits this task before using it):\n" + lines + "\n\n"


def _answer_tokens(text: str) -> set[str]:
    """Numbers and named options ("option B", "answer C"): the tokens an answer is made of."""
    t = (text or "").lower()
    return set(re.findall(r"\d+(?:\.\d+)?", t)) | {"opt:" + m for m in re.findall(r"\b(?:option|answer(?: is)?)\s+\(?([a-z])\)?(?![a-z0-9])", t)}


def placebo_brief(ledger: Ledger, task: str, run: str, task_text: str, *, length: int, n_items: int, seed, min_overlap: float = 0.34) -> dict:
    """EVAL-002 placebo: format_brief over INDEPENDENTLY_CHECKED, never-contradicted discoveries of OTHER tasks that are not retrievable for this one
    (VERIFIED_TASK_IRRELEVANT). Leak guard with retrieval's own overlap function: a candidate whose overlap with the task prompt or with any of this task's
    verified / retrievable items reaches `min_overlap`, or that shares an answer token with those items, is excluded. Parity with the memory brief: same
    formatter and header, exactly `length` characters (claims trimmed evenly) and `n_items` items when the pool's claims are long enough (otherwise more
    items, up to the pool; the result records both counts and lengths). Read-only (no retrieval/application recorded)."""
    rows = ledger.rows()
    real = ledger.retrievable(task, run, task_text, min_overlap, _rows=rows)
    guard = [i["claim"] for i in real] + [r["claim"] for r in rows if r["kind"] == "DISCOVERY" and r["origin_task"] == task
                                          and any(v["kind"] == "VERIFICATION" and v["id"] == r["id"] and v["verdict"] == "SUPPORTS" for v in rows)]
    answers = set().union(set(), *(_answer_tokens(c) for c in guard))
    prompt, guard_terms, taken = _terms(task_text), [_terms(c) for c in guard], {i["id"] for i in real}
    pool, leaks = [], 0
    for d in (r for r in rows if r["kind"] == "DISCOVERY" and r["origin_task"] != task and r["id"] not in taken):
        _d, _own, sup, _con, ver = ledger._checked(rows, d["id"])
        if not sup or any(v["verdict"] == "CONTRADICTS" for v in ver):
            continue
        if overlap(prompt, d["claim"]) >= min_overlap or any(overlap(g, d["claim"]) >= min_overlap for g in guard_terms) or _answer_tokens(d["claim"]) & answers:
            leaks += 1
            continue
        pool.append({"id": d["id"], "claim": " ".join(d["claim"].split())[:300], "applicability": d["applicability"]})
    # longest claims first, so the length can be matched by trimming; the seed orders equal lengths
    pool.sort(key=lambda i: (-len(i["claim"]), _h([seed, task, i["id"]])))
    items = [dict(i) for i in pool[: max(0, n_items)]] if length > 0 else []
    text = format_brief(items)
    while items and len(text) < length and len(items) < len(pool):       # claims too short for the length: the length wins, one more item at a time
        items.append(dict(pool[len(items)]))
        text = format_brief(items)
    while items and len(text) > length:                                   # level the longest claim down toward the next longest (even trimming); never below one character
        k = max(range(len(items)), key=lambda j: len(items[j]["claim"]))
        c = items[k]["claim"]
        second = max((len(i["claim"]) for j, i in enumerate(items) if j != k), default=0)
        cut = max(1, len(c) - min(len(text) - length, max(1, len(c) - second)))
        if cut >= len(c):
            break
        items[k]["claim"] = c[:cut][:-1] + "\u2026" if c[:cut].endswith(" ") else c[:cut]
        text = format_brief(items)
    return {"text": text, "ids": [i["id"] for i in items], "items": len(items), "chars": len(text), "target_items": n_items, "target_chars": length,
            "pool": len(pool), "leak_excluded": leaks}


@dataclass
class LearningHook:
    ledger: Ledger
    run_id: str
    apply: bool = False
    max_items: int = 3
    errors: list = None
    task: str | None = None                                               # the host's task id; overrides the task_ref a caller passes to brief (PeachMe passes its mission id)

    def __post_init__(self):
        self.errors = []

    def brief(self, task_ref: str, task_text: str) -> tuple[str, list[str]]:
        if not self.apply:
            return "", []
        task_ref = self.task or task_ref
        try:                                                              # learning must never cost a question: any failure means "no brief" and is recorded
            items = self.ledger.retrievable(task_ref, self.run_id, task_text)[: self.max_items]
            for it in items:
                self.ledger.retrieve(it["id"], run=self.run_id, task=task_ref)
                self.ledger.apply(it["id"], run=self.run_id, task=task_ref, how="shown as brief in the solve prompt")
        except Exception as exc:  # noqa: BLE001
            self.errors.append(f"{type(exc).__name__}: {str(exc)[:160]}")
            return "", []
        return format_brief(items), [i["id"] for i in items]

    def capture(self, task_ref: str, *, objections: list[dict], final_letter: str | None, first_letter: str | None, how: str, identities: dict) -> list[str]:
        """objections = the episode's objection records (team.objs). Returns the ids of the discoveries recorded."""
        prov = {"final_how": how, "identities": identities}
        made = []
        accepted = [o for o in objections if o.get("state") == "ACCEPTED" or o.get("decided_by") == "accepted_by_concession"]
        for o in accepted:
            m = _CLAIM.search(o.get("text") or "")
            claim = (m.group(1).strip() if m else (o.get("text") or "").strip())[:300]
            if not claim:
                continue
            did = self.ledger.discover(claim=claim, origin_run=self.run_id, origin_task=task_ref, proposer=o.get("lineage") or "unknown",
                                       applicability="the situation described in the claim; re-check against the task",
                                       evidence_ref=f"objection:{o.get('id')}", provenance={**prov, "objection": o.get("id"), "target": o.get("target"),
                                                                                              "ground_level": (o.get("ground") or {}).get("level")})
            self._verify(did, o.get("ground") or {}, f"objection:{o.get('id')}:executed")
            made.append(did)
        if final_letter and first_letter and final_letter != first_letter and not accepted:
            made.append(self.ledger.discover(claim=f"the answer moved from {first_letter} to {final_letter} through cooperation", origin_run=self.run_id,
                                             origin_task=task_ref, proposer="collaboration", applicability="same question only", evidence_ref="closing", provenance=prov))
        return made

    def _verify(self, did: str, ground: dict, ref: str) -> None:
        """A trusted receipt verifies with the verdict of its own executed payload; a claimed execution without one is kept as a MODEL_ASSERTED verification.
        A rejected receipt (forged, proposer's lineage, untrusted tool) records nothing and is reported in `errors`."""
        receipt = ground.get("receipt")
        claimed = (ground.get("argument") or {}).get("executed") and ground.get("level") in ("reproduced", "independently_confirmed")
        if receipt is None and not claimed:
            return
        payload = receipt.get("payload") if isinstance(receipt, dict) else None
        verdict = "SUPPORTS" if receipt is None else payload.get("relation") if isinstance(payload, dict) else None
        try:
            if verdict not in ("SUPPORTS", "CONTRADICTS"):
                raise ValueError("RECEIPT_REJECTED: the executed payload states no relation")
            self.ledger.verify(did, verdict=verdict, verifier="executed", evidence_ref=ref, receipt=receipt)
        except ValueError as exc:
            self.errors.append(f"{did}: {str(exc)[:160]}")

    def capture_tree(self, task_ref: str, tree, *, evidence_ref: str, receipts: dict | None = None) -> list[str]:
        """After a research phase (ResearchPlan.after): every Research Tree node SUPPORTED or FALSIFIED by executed / independently_confirmed evidence becomes a DISCOVERY;
        falsified nodes are kept as negative findings. The tree's level string is not trust: the verification is INDEPENDENT only with the trusted execution receipt
        `receipts[evidence id]` (issued by the host code that ran the check), otherwise it is kept as MODEL_ASSERTED. Idempotent."""
        made = []
        for n in tree.nodes.values():
            rel = "SUPPORTS" if n.status == "SUPPORTED" else "CONTRADICTS" if n.status == "FALSIFIED" else None
            strong = [e for e in n.evidence if e["relation"] == rel and e["level"] in ("executed", "independently_confirmed")]
            if n.kind == "ROOT" or not strong:
                continue
            did = self.ledger.discover(claim=n.text, origin_run=self.run_id, origin_task=task_ref, proposer=n.origin, applicability="related questions; re-check against the task",
                                       evidence_ref=f"{evidence_ref}#{n.id}", provenance={"node": n.id, "status": n.status, "evidence": strong[0]["id"]})
            e = next((x for x in strong if (receipts or {}).get(x["id"]) is not None), strong[0])
            ref = f"{evidence_ref}#{n.id}:{e['id']}"
            if not any(r["kind"] == "VERIFICATION" and r["id"] == did and r["evidence_ref"] == ref for r in self.ledger.rows()):
                rc = (receipts or {}).get(e["id"])
                if rc is not None and (rc.get("payload") or {}).get("relation") not in (None, rel):
                    self.errors.append(f"{did}: RECEIPT_REJECTED: receipt relation differs from the node's")
                    rc = None
                try:
                    self.ledger.verify(did, verdict=rel, verifier="executed", evidence_ref=ref, receipt=rc)
                except ValueError as exc:
                    self.errors.append(f"{did}: {str(exc)[:160]}")
            made.append(did)
        return made

    def outcomes(self, task_ref: str, *, reward: float, control_reward: float, control_run: str, grader: str) -> list[str]:
        """Called by the grading side. One OUTCOME per discovery applied in this run for this task."""
        done = []
        for r in self.ledger.rows():
            if r["kind"] == "APPLICATION" and r["run"] == self.run_id and r["task"] == task_ref and r["id"] not in done:
                self.ledger.outcome(r["id"], run=self.run_id, task=task_ref, reward=reward, control_reward=control_reward, grader=grader, control_run=control_run)
                done.append(r["id"])
        return done
