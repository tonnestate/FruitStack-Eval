"""PNP-001 reconstruction register (owner contract 2026-11-23, PNP-001-EXISTING-PROOF-RECONSTRUCTION-2026-11-23.md).
Mechanical, read-only: indexes every proof-state step and every PROOF_STEP/VERIFICATION/REFUTATION/RETRACTION ledger event.
Status is derived from recorded events only; a review counts as independent only if it is from another session AND model family.
Usage: python3 register.py <proofstate dir> <proofbook.jsonl> <out dir>"""
import json, re, sys, collections
from pathlib import Path

FAM = lambda m: re.sub(r"[-_.]?\d.*$", "", str(m or "").split("@")[0].split("/")[-1]).split("-")[0].lower()   # claude-haiku-5-5 -> claude


def main(ps_dir, book, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    nodes, edges = [], []
    for f in sorted(Path(ps_dir).glob("Q-*.json")):
        q = f.stem
        try:
            ev = json.loads(f.read_text())
        except ValueError:
            continue
        steps = {e["id"]: e for e in ev if e.get("proved_step") and e.get("id")}
        for sid, s in steps.items():
            revs = [e for e in ev if e.get("review_of") == sid]
            indep = [r for r in revs if r.get("session") != s.get("session") and FAM(r.get("model")) != FAM(s.get("model"))]
            stmt = " ".join(str(s["proved_step"]).split()).lower()
            def quotes(r):          # does the review text share a 40-char window with the statement? (misattribution check)
                t = " ".join(str(r.get("evidence") or r.get("statement_start") or "").split()).lower()
                return any(stmt[i:i + 40] in t for i in range(0, max(1, len(stmt) - 40), 20)) if len(stmt) >= 40 else stmt in t
            last = {}
            for r in revs:
                if r.get("status") in ("SURVIVED_REVIEW", "REFUTED", "DISPUTED", "FORMALLY_VERIFIED", "FORMALLY_REFUTED"):
                    if r.get("status") == "SURVIVED_REVIEW" and r not in indep:
                        continue
                    last = r
            status = last.get("status") or "CLAIMED"
            formal = [r.get("status") for r in revs if str(r.get("status", "")).startswith("FORMALLY")]
            nodes.append({"id": f"{q}:{sid}", "question": q, "step": sid, "kind": s.get("kind", "LEMMA"), "model": s.get("model"),
                          "session": s.get("session"), "status": status, "formal": formal, "closes": s.get("closes"),
                          "independent_reviews": [{"session": r.get("session"), "model": r.get("model"), "status": r.get("status"),
                                                   "quotes_statement": quotes(r)} for r in indep],
                          "same_family_reviews": len(revs) - len(indep), "statement": s["proved_step"]})
            for r in indep:
                edges.append({"from": f"{q}:{sid}", "to": r.get("session"), "type": "VERIFIED_BY" if r.get("status") == "SURVIVED_REVIEW"
                              else "REFUTED_BY" if r.get("status") == "REFUTED" else r.get("status")})
            for ref in sorted(set(re.findall(r"\b(?:repair|correction|replaces?|refin\w*) of (S\d{4})", str(s["proved_step"]), re.I))):
                edges.append({"from": f"{q}:{sid}", "to": f"{q}:{ref}", "type": "REPLACES"})
            for g in sorted(set(re.findall(r"\bG\d{4}\b", str(s.get("closes"))))):
                edges.append({"from": f"{q}:{sid}", "to": f"{q}:{g}", "type": "CLAIMS_TO_CLOSE"})
    ledger = [e for e in map(json.loads, open(book)) if e.get("kind") in ("PROOF_STEP", "VERIFICATION", "REFUTATION", "RETRACTION")]
    (out / "register-nodes.json").write_text(json.dumps(nodes, indent=1, ensure_ascii=False))
    (out / "register-edges.json").write_text(json.dumps(edges, indent=1))
    (out / "ledger-proof-events.json").write_text(json.dumps(ledger, indent=1, ensure_ascii=False))
    c = collections.Counter(n["status"] for n in nodes)
    unq = sum(1 for n in nodes if n["status"] == "SURVIVED_REVIEW" and not any(r["quotes_statement"] for r in n["independent_reviews"]
                                                                              if r["status"] == "SURVIVED_REVIEW"))
    print(json.dumps({"steps": len(nodes), "status": c, "survived_without_quoting_review": unq, "edges": len(edges),
                      "ledger_proof_events": collections.Counter(e["kind"] for e in ledger)}, default=str))


if __name__ == "__main__":
    main(*sys.argv[1:4])
