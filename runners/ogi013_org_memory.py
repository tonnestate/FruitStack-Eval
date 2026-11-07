"""OrangeMe projection of the organizational-learning ledger (cross-session continuity; OrangeMe is not the source of truth).

The append-only ledger (ogi013_org_discoveries.Ledger) stays authoritative. Each discovery is projected to the OrangeMe ProjectLedger key `knowledge/<id>`
with its derived state, verifiers, contradictions, provenance and reuse counts, so later sessions and other agents (OrangeMe MCP `project_get`) see it.
Every change is a new OrangeMe revision with an immutable history event; falsified and contradicted entries are projected like any other, never removed.
"""
from __future__ import annotations


class OrangeKnowledgeProjection:
    def __init__(self, project_ledger, prefix: str = "knowledge/"):
        self.ledger, self.prefix = project_ledger, prefix

    @staticmethod
    def snapshot(led, did: str) -> dict:
        st = led.status(did)
        rows = [r for r in led.rows() if r.get("id") == did]
        d = next(r for r in rows if r["kind"] == "DISCOVERY")
        ver = [r for r in rows if r["kind"] == "VERIFICATION"]
        return {"id": did, "state": st["state"], "claim": d["claim"], "applicability": d["applicability"], "proposer": d["proposer"],
                "origin_run": d["origin_run"], "origin_task": d["origin_task"], "evidence_ref": d["evidence_ref"], "provenance": d.get("provenance", {}),
                "verifiers": sorted({v["verifier"] for v in ver}), "verifications": [{"verdict": v["verdict"], "verifier": v["verifier"], "evidence_ref": v["evidence_ref"]} for v in ver],
                "retrievals": st["retrievals"], "applications": st["applications"], "outcomes": st["outcomes"], "gain_sum": st["gain_sum"],
                "ledger_seq": max(r["seq"] for r in rows)}

    def publish(self, led, ids=None) -> list[str]:
        """Project changed discoveries; returns the ids written (unchanged ones produce no new revision)."""
        written = []
        for did in ids or [r["id"] for r in led.rows() if r["kind"] == "DISCOVERY"]:
            snap = self.snapshot(led, did)
            cur = self.ledger.get(self.prefix + did)
            if cur is not None and cur["value"] == snap:
                continue
            self.ledger.put(self.prefix + did, snap, expected_revision=cur["revision"] if cur else 0)
            written.append(did)
        return written
