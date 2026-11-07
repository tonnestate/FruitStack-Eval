"""Regenerates COLLAB_TRACE.md: four scripted scenarios (no model, no network) through the real cherryme.brother rounds, collaborate() and ContributionLedger.
Run: PYTHONPATH=<CherryMe>:runners:tests:. python evidence/ogi013-collab/make_trace.py   (tests/test_ogi013_org_collab.py fails if the committed file drifts)"""
import json
from pathlib import Path

from test_ogi013_org_collab import BAD, GOOD, Workers, digest, run

CHECKS = "ISSUES: NONE\nPolicy 24h window: booking made 2h ago is inside it; HAT001 is the reservation named in the CONVERSATION."
FOUND = "ISSUES: FOUND\nThe reservation id WRONG1 is not the customer's booking; use HAT001 (see CONVERSATION)."
SCENARIOS = [
    ("A. Sound answer: one independent assessment with stated grounds", Workers(independently_confirmed=[CHECKS], challenge=[CHECKS]), GOOD),
    ("B. Flawed answer: challenged, revised, the revision examined again", Workers(independently_confirmed=[FOUND, CHECKS], challenge=[FOUND, CHECKS], revise=[json.dumps(GOOD)]), BAD),
    ("C. Unresolved disagreement: the author rejects, the specialist backs the author, the objection stays", Workers(independently_confirmed=[FOUND], challenge=[FOUND], revise=[json.dumps(BAD)], specialist=[json.dumps(BAD)]), BAD),
    ("D. Author overruled: the specialist backs the critic, its answer is reviewed once more by a new lineage",
     Workers(independently_confirmed=[FOUND, CHECKS], challenge=[FOUND, CHECKS], revise=[json.dumps(BAD) + " "], specialist=[json.dumps(GOOD)]), BAD),
]


def render() -> str:
    names = {digest(BAD): "WRONG1", digest(GOOD): "HAT001"}
    out = ["# Offline collaboration traces (scripted workers; real cherryme.brother rounds + ContributionLedger; zero model calls)", "",
           "Task: POLICY refunds only within 24h; the customer asks to cancel HAT001 booked 2h ago. WRONG1 is the wrong reservation. Agreement below is a reviewer's claim, not proof.", ""]
    for title, workers, seed in SCENARIOS:
        res, ledger = run(workers, seed_action=seed)
        out += [f"## {title}", "", "| # | ledger kind | worker (lineage) | status | excerpt |", "|---|---|---|---|---|"]
        for i, r in enumerate(ledger.rows, 1):
            out.append(f"| {i} | {r.kind} | {r.worker} ({r.identity.get('independence_key')}) | {r.epistemic_status} | {(r.answer_text or r.reason or '').splitlines()[0][:90] if (r.answer_text or r.reason) else ''} |")
        fin = names.get(digest(res.final_action), "?")
        out += ["", f"- stages called: {workers.stages()}; provider calls={res.calls}; stop={res.stop_reason}",
                f"- final action: reservation {fin}; changed={res.changed}; improved={res.improved}; validated={res.validated}; ungrounded_agreement={res.ungrounded_agreement}; final_reviewed={res.final_reviewed}"]
        for a in res.agreement:
            out.append(f"- AGREED: {a['model']} ({a['lineage']}) with {names.get(a['agreed_with'], '?')} - grounds: {a['grounds'] or '(none stated)'}")
        for o in res.overruled:
            out.append(f"- OVERRULED author: {o['author']} kept {names.get(o['author_position'], '?')}; overruled by {o['overruled_by']}")
        for u in res.unresolved:
            out.append(f"- UNRESOLVED objection by {u['critic']}: {u['objection'].splitlines()[0][:90]}")
        for a in res.attribution:
            out.append(f"- contributor: {a['role']} {a['model']} ({a['lineage']}) " + ", ".join(f"{k}={a[k]}" for k in ("found_issues", "materially_improved", "changed_action") if k in a))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    Path(__file__).with_name("COLLAB_TRACE.md").write_text(render())
