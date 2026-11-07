"""Brother Mode <-> organizational-learning ledger (runners/ogi013_org_discoveries.py). Opt-in: run_T(..., learning=LearningHook(...)); without it nothing changes.

capture   after an episode: model-asserted claims (accepted objections, answers changed by cooperation) are recorded as DISCOVERY with model/lineage/receipt provenance.
          A claim becomes VERIFIED only through an independent verifier that ran in that episode (objection ground executed); model agreement never verifies.
brief     before a later episode: verified, applicable discoveries (ledger.retrievable, with its leak guard) become the `brief` of cherryme run_rounds (the solve prompt slot
          `{brief}`), labelled as organizational knowledge that must still fit the task. RETRIEVAL and APPLICATION are recorded. apply=False records nothing and injects nothing.
outcomes  after grading, from the grader's side only (never in the live context): applied-vs-control reward per applied discovery. Benchmark keys / grading results are never
          passed to capture or brief.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from ogi013_org_discoveries import Ledger

_CLAIM = re.compile(r"CLAIM:\s*(.+?)(?:\n\s*(?:EVIDENCE|CONSEQUENCE):|\Z)", re.S)


@dataclass
class LearningHook:
    ledger: Ledger
    run_id: str
    apply: bool = False
    max_items: int = 3

    def brief(self, task_ref: str, task_text: str) -> tuple[str, list[str]]:
        if not self.apply:
            return "", []
        items = self.ledger.retrievable(task_ref, self.run_id, task_text)[: self.max_items]
        for it in items:
            self.ledger.retrieve(it["id"], run=self.run_id, task=task_ref)
            self.ledger.apply(it["id"], run=self.run_id, task=task_ref, how="shown as brief in the solve prompt")
        if not items:
            return "", []
        lines = "\n".join(f"- {i['claim']} (applies: {i['applicability']}; independently verified by {', '.join(i['verifiers'])})" for i in items)
        return "Organizational knowledge from earlier verified work (check that it fits this task before using it):\n" + lines + "\n\n", [i["id"] for i in items]

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
            g = o.get("ground") or {}
            if (g.get("argument") or {}).get("executed") and g.get("level") in ("reproduced", "independently_confirmed"):
                self.ledger.verify(did, verdict="SUPPORTS", verifier="executed", evidence_ref=f"objection:{o.get('id')}:executed")
            made.append(did)
        if final_letter and first_letter and final_letter != first_letter and not accepted:
            made.append(self.ledger.discover(claim=f"the answer moved from {first_letter} to {final_letter} through cooperation", origin_run=self.run_id,
                                             origin_task=task_ref, proposer="collaboration", applicability="same question only", evidence_ref="closing", provenance=prov))
        return made

    def outcomes(self, task_ref: str, *, reward: float, control_reward: float, control_run: str, grader: str) -> list[str]:
        """Called by the grading side. One OUTCOME per discovery applied in this run for this task."""
        done = []
        for r in self.ledger.rows():
            if r["kind"] == "APPLICATION" and r["run"] == self.run_id and r["task"] == task_ref:
                self.ledger.outcome(r["id"], run=self.run_id, task=task_ref, reward=reward, control_reward=control_reward, grader=grader, control_run=control_run)
                done.append(r["id"])
        return done
