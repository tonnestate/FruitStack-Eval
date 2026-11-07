"""OGI-013 organizational-learning ledger: discovery -> verification -> storage -> retrieval -> application -> measured outcome.

Append-only, hash-chained JSONL. Nothing here calls a model or a provider. It sits NEXT TO CherryMe's KnowledgeStore (which stores quote-grounded
source facts and counts reuse, but links no later outcome) and never edits it or any archived row.

A discovery is only ever *derived* into one state (see `status`); no caller can assert "learned":
  ASSERTED          model-asserted claim, nothing independent behind it (never counts as knowledge)
  VERIFIED          an independent check supports it (verifier kind: dataset_key | executed | official_grader); a model's own agreement is not a verifier
  FALSIFIED         an independent check contradicts it (kept as a negative finding, never deleted)
  CONTRADICTED      verified, but a later verified contradiction exists (both kept)
  STORED_NOT_REUSED verified, never retrieved for a later run
  RETRIEVED         retrieved for a later run, not shown to have been applied
  APPLIED           applied in a later run, no outcome with a control yet
  BENEFIT_OBSERVED / NO_EFFECT_OBSERVED / HARM_OBSERVED   measured applied-vs-control outcome(s) on later runs (counts only, no significance claim)
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import math
import threading
import time
from pathlib import Path

VERIFIERS = {"dataset_key", "executed", "official_grader"}        # independent of the model that made the claim
KINDS = {"DISCOVERY", "VERIFICATION", "RETRIEVAL", "APPLICATION", "OUTCOME"}


def _terms(text: str) -> set[str]:
    import re
    return {t for t in re.findall(r"[a-z0-9][a-z0-9.\-]+", (text or "").lower()) if len(t) > 2}


def _h(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class Ledger:
    def __init__(self, path, mirror=None):
        """`mirror(kind, key, payload)` (optional) copies every appended row to MangoMe (MangoLedger.write); the local chain is written first and stays the source of truth."""
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.mirror = mirror
        self.mirror_errors: list[str] = []
        self._tl, self._depth = threading.RLock(), 0

    def _locked(self):
        """One writer at a time: a thread lock (run_T runs questions in parallel) and an flock on <ledger>.lock (several processes). Re-entrant."""
        ledger = self

        class _Ctx:
            def __enter__(_s):
                ledger._tl.acquire()
                if ledger._depth == 0:
                    ledger._fh = open(str(ledger.path) + ".lock", "a")
                    fcntl.flock(ledger._fh, fcntl.LOCK_EX)
                ledger._depth += 1

            def __exit__(_s, *a):
                ledger._depth -= 1
                if ledger._depth == 0:
                    fcntl.flock(ledger._fh, fcntl.LOCK_UN)
                    ledger._fh.close()
                ledger._tl.release()
        return _Ctx()

    def rows(self) -> list[dict]:
        out, prev = [], "0" * 64
        if self.path.exists():
            for n, line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
                if line.strip():
                    r = json.loads(line)
                    if r.get("chain") != _h({"prev": prev, "body": {k: v for k, v in r.items() if k != "chain"}}):
                        raise ValueError(f"LEDGER_CHAIN_BROKEN at row {n}")
                    prev = r["chain"]
                    out.append(r)
        return out

    def _add(self, kind: str, body: dict) -> dict:
        assert kind in KINDS
        with self._locked():
            rows = self.rows()
            body = {"kind": kind, "seq": len(rows) + 1, "at": time.time(), **body}
            row = {**body, "chain": _h({"prev": rows[-1]["chain"] if rows else "0" * 64, "body": body})}
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
        if self.mirror is not None:                                       # the local chain is the source of truth; a MangoMe failure is recorded, never raised
            try:
                self.mirror("ORG_LEARNING_" + kind, str(row["seq"]), row)
            except Exception as exc:  # noqa: BLE001
                self.mirror_errors.append(f"{kind}#{row['seq']}: {type(exc).__name__}: {str(exc)[:120]}")
        return row

    def _known(self, did: str) -> None:
        if not any(r["kind"] == "DISCOVERY" and r["id"] == did for r in self.rows()):
            raise KeyError(f"unknown discovery {did}")

    def discover(self, *, claim: str, origin_run: str, origin_task: str, proposer: str, applicability: str, evidence_ref: str, provenance: dict | None = None) -> str:
        """Record a model-asserted claim. `applicability` states when it may be reused (e.g. 'same question only'); `evidence_ref` points at the raw source record."""
        if not (claim and origin_run and applicability and evidence_ref):
            raise ValueError("claim, origin_run, applicability and evidence_ref are required")
        did = "D-" + _h([claim, origin_run, origin_task])[:16]
        with self._locked():
          if not any(r["kind"] == "DISCOVERY" and r["id"] == did for r in self.rows()):
            self._add("DISCOVERY", {"id": did, "claim": claim, "origin_run": origin_run, "origin_task": origin_task, "proposer": proposer,
                                    "applicability": applicability, "evidence_ref": evidence_ref, "provenance": provenance or {}})
        return did

    def verify(self, did: str, *, verdict: str, verifier: str, evidence_ref: str) -> None:
        """verdict SUPPORTS|CONTRADICTS from an independent verifier. A model verifying a model is rejected."""
        self._known(did)
        if verifier not in VERIFIERS:
            raise ValueError(f"verifier must be one of {sorted(VERIFIERS)}; model agreement is not verification")
        if verdict not in ("SUPPORTS", "CONTRADICTS"):
            raise ValueError("verdict must be SUPPORTS or CONTRADICTS")
        self._add("VERIFICATION", {"id": did, "verdict": verdict, "verifier": verifier, "evidence_ref": evidence_ref})

    def retrieve(self, did: str, *, run: str, task: str) -> None:
        self._known(did)
        self._add("RETRIEVAL", {"id": did, "run": run, "task": task})

    def apply(self, did: str, *, run: str, task: str, how: str) -> None:
        self._known(did)
        self._add("APPLICATION", {"id": did, "run": run, "task": task, "how": how})

    def outcome(self, did: str, *, run: str, task: str, reward: float, control_reward: float, grader: str, control_run: str) -> None:
        """Applied-vs-control result of a LATER run. The control is the same task without the stored discovery; both come from the same grader."""
        self._known(did)
        if not any(r["kind"] == "APPLICATION" and r["id"] == did and r["run"] == run and r["task"] == task for r in self.rows()):
            raise ValueError("an outcome needs a recorded APPLICATION of this discovery in that run and task")
        if grader not in VERIFIERS:
            raise ValueError(f"the outcome grader must be independent of the models: one of {sorted(VERIFIERS)}")
        if control_run == run:
            raise ValueError("the control must be a different run (same task without the stored discovery)")
        if not all(isinstance(x, (int, float)) and math.isfinite(x) and 0.0 <= x <= 1.0 for x in (reward, control_reward)):
            raise ValueError("rewards must be finite and lie in [0, 1]")
        with self._locked():
            if any(r["kind"] == "OUTCOME" and r["id"] == did and r["run"] == run and r["task"] == task for r in self.rows()):
                return                                                    # idempotent: one OUTCOME per discovery, run and task
            self._add("OUTCOME", {"id": did, "run": run, "task": task, "reward": float(reward), "control_reward": float(control_reward),
                                  "grader": grader, "control_run": control_run})

    def status(self, did: str) -> dict:
        rows = [r for r in self.rows() if r.get("id") == did]
        d = next((r for r in rows if r["kind"] == "DISCOVERY"), None)
        if d is None:
            raise KeyError(did)
        ver = [r for r in rows if r["kind"] == "VERIFICATION"]
        sup, con = [r for r in ver if r["verdict"] == "SUPPORTS"], [r for r in ver if r["verdict"] == "CONTRADICTS"]
        later = lambda r: r["run"] != d["origin_run"]                                   # reuse only counts in a run other than the one that produced it
        ret = [r for r in rows if r["kind"] == "RETRIEVAL" and later(r)]
        app = [r for r in rows if r["kind"] == "APPLICATION" and later(r)]
        out = [r for r in rows if r["kind"] == "OUTCOME" and later(r)]
        if not ver:
            state = "ASSERTED"
        elif con and not sup:
            state = "FALSIFIED"
        elif con and sup:
            state = "CONTRADICTED"
        elif out:
            gain = [o["reward"] - o["control_reward"] for o in out]
            state = "BENEFIT_OBSERVED" if sum(gain) > 0 else "HARM_OBSERVED" if sum(gain) < 0 else "NO_EFFECT_OBSERVED"
        elif app:
            state = "APPLIED"
        elif ret:
            state = "RETRIEVED"
        else:
            state = "STORED_NOT_REUSED"
        return {"id": did, "state": state, "claim": d["claim"], "applicability": d["applicability"], "verifications": len(ver),
                "retrievals": len(ret), "applications": len(app), "outcomes": len(out),
                "gain_sum": round(sum(o["reward"] - o["control_reward"] for o in out), 6) if out else None}

    def retrievable(self, task: str, run: str, task_text: str = "", min_overlap: float = 0.34) -> list[dict]:
        """Discoveries that may be shown to a LATER episode. Leak guard: no discovery is ever shown to the task it came from (otherwise the applied arm is a memorised-answer arm), and 'same question only'
        scope is never retrievable; a grading result must not enter a live reasoning context. FALSIFIED/CONTRADICTED/ASSERTED never qualify."""
        want = _terms(task_text)
        out = []
        for did in [r["id"] for r in self.rows() if r["kind"] == "DISCOVERY"]:
            rows = [r for r in self.rows() if r.get("id") == did]
            d = next(r for r in rows if r["kind"] == "DISCOVERY")
            ver = [r for r in rows if r["kind"] == "VERIFICATION"]
            if not ver or any(v["verdict"] == "CONTRADICTS" for v in ver) or d["origin_run"] == run:
                continue
            if d["origin_task"] == task or d["applicability"].lower().startswith("same question"):
                continue                                                  # never shown to the task it came from (any verifier), and task-bound scope is not transferable
            if want and len(want & _terms(d["claim"])) / max(1, len(_terms(d["claim"]))) < min_overlap:
                continue
            out.append({"id": did, "claim": d["claim"], "applicability": d["applicability"], "verifiers": sorted({v["verifier"] for v in ver})})
        return out

    def report(self) -> dict:
        ids = [r["id"] for r in self.rows() if r["kind"] == "DISCOVERY"]
        sts = [self.status(i) for i in ids]
        counts: dict[str, int] = {}
        for s in sts:
            counts[s["state"]] = counts.get(s["state"], 0) + 1
        learned = [s["id"] for s in sts if s["state"] == "BENEFIT_OBSERVED"]
        return {"discoveries": len(ids), "by_state": counts, "organizational_learning_instances": learned, "statuses": sts}


def ingest_episodes(ledger: Ledger, episodes_json: str) -> list[str]:
    """Offline seed from the reconstruction: every genuine-duo episode in which collaboration moved or conceded an answer becomes a DISCOVERY,
    verified ONLY against the dataset key. Same-lineage (Luna-only) episodes are not collaboration and are skipped. No retrieval/application is invented."""
    data = json.loads(Path(episodes_json).read_text())
    ids = []
    for e in data["episodes"]:
        if not e["valid_duo"]:
            continue
        accepted = [o for o in e["objections"] if o["state"] == "ACCEPTED"]
        first_primary = e["first_letters"].get(e["primary"]) if e["primary"] else None
        if not accepted and (e["primary"] is None or e["final_letter"] == first_primary):
            continue
        m = data["manifest"][f"{e['source'].split('(')[0]}_{e['qid']}"]
        src = f"{m['origin']}@sha256:{m['sha256'][:16]}"
        did = led_id = ledger.discover(
            claim=f"option {e['final_letter']} is the correct answer to question {e['qid']}", origin_run=e["source"], origin_task=e["qid"],
            proposer=(accepted[0]["raised_by_lineage"] if accepted else "collaboration"), applicability="same question only (multiple-choice item; no transfer to other items)",
            evidence_ref=src)
        ledger.verify(did, verdict="SUPPORTS" if e["final_correct"] else "CONTRADICTS", verifier="dataset_key", evidence_ref=f"{src}#key={e['key']}")
        ids.append(led_id)
    return ids


if __name__ == "__main__":
    import sys
    led = Ledger(sys.argv[2])
    ingest_episodes(led, sys.argv[1])
    print(json.dumps(led.report(), indent=1, sort_keys=True))
