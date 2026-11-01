"""QA-2D v2 closure report generator (existing evidence only; no provider call). EXPLORATORY and DESCRIPTIVE: the preregistered 400-question confirmatory study did not complete.
usage: qa2d_v2_closure.py RESULTS.jsonl OUT_DIR   (RESULTS = runs/qa2d_v2/out/run/results.jsonl)"""
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

from analyze_qa1 import clopper_pearson, paired

ARMS = ("T", "E", "SL", "SN")
PAIRS = (("T", "SL"), ("T", "E"), ("T", "SN"), ("E", "SL"), ("E", "SN"), ("SN", "SL"))


def load(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def cause(r) -> str:
    d = str(r.get("infra_detail"))
    if "REASONING_LEAKED_AS_CONTENT" in d:
        return "call made; output unusable (reasoning leaked as content, finish_reason=length)"
    if "NOT_PERFORMED" in d and re.search(r"HTTP 502", d):
        return "no provider call; route cooling down after upstream timeout (HTTP 502)"
    if "NOT_PERFORMED" in d and re.search(r"HTTP 429", d):
        return "no provider call; route rate-limited / on cooldown (HTTP 429)"
    return "other: " + d[:80]


def ci(k, n):
    lo, hi = clopper_pearson(k, n) if n else (0, 1)
    return f"{k}/{n} = {100 * k / n:.1f}% [{100 * lo:.1f}, {100 * hi:.1f}]" if n else "-"


def pair_table(rows, qids, a, b):
    x = [bool(rows[(q, a)]["correct"]) for q in qids]
    y = [bool(rows[(q, b)]["correct"]) for q in qids]
    both = sum(1 for u, v in zip(x, y) if u and v)
    only_a = sum(1 for u, v in zip(x, y) if u and not v)
    only_b = sum(1 for u, v in zip(x, y) if v and not u)
    neither = sum(1 for u, v in zip(x, y) if not u and not v)
    p = paired(x, y)
    return (f"| {a} vs {b} | {both} | {only_a} | {only_b} | {neither} | {100 * p['diff']:+.1f} pts [{100 * p['ci_low']:+.1f}, {100 * p['ci_high']:+.1f}] | {p['p']:.4f} |")


def main(results, out_dir) -> int:
    rows_l = load(results)
    rows = {(r["qid"], r["arm"]): r for r in rows_l}
    assert len(rows) == len(rows_l), "duplicate (qid, arm)"
    new = [r for r in rows_l if not r.get("reused_from")]
    qids = sorted({r["qid"] for r in new})
    assert all((q, a) in rows for q in qids for a in ARMS), "a question lacks an arm"
    L = ["# QA-2D v2 closure report (exploratory, descriptive; study closed as infrastructure-infeasible)", "",
         "**Conclusion.** QA-2D v2 could not complete its preregistered confirmatory study because the available Nemotron supply exceeded the infrastructure-failure threshold. "
         "The collected observations do not establish whether organized cooperation is superior to the controls.", "",
         "## Scope and history",
         f"- {len(rows_l)} result rows: {len(rows_l) - len(new)} reused QA-1 Luna rows (SL) + {len(new)} new T/E/SN rows over {len(qids)} of the 400 preregistered questions. The planned 400-question confirmatory "
         "analysis (H1L, H1c with Holm) was **not** performed; nothing below is a confirmatory result.",
         "- History: superseded v1 run (246 rows, archived, not used) -> Amendment A1 -> lock v2 (`f88e7d7`, source `dde6307`) -> 40 rows -> stopped for truth reconciliation (sync/local-truth fast-forwarded to `ab6cabe`) -> "
         "retrospective provenance addendum (written after the first 40 rows) -> resumed -> automatic pause at question 6264 (`INFRA_SHARE_ABOVE_10PCT:E`) -> closed by decision.",
         "- The 16 questions observed in v1 are inside the first 53 questions of the same hash order and are described in Amendment A1.", ""]
    # reconciliation
    bad = [r for r in new if r["status"] != "OK"]
    by_arm = collections.Counter(r["arm"] for r in bad)
    L += ["## Infrastructure failures (reconciled against the row files and the printed run logs)",
          f"Total {len(bad)} = " + " + ".join(f"{a} {by_arm[a]}" for a in ('T', 'E', 'SN')) + ". By cause:", "", "| cause | T | E | SN | total |", "|---|---|---|---|---|"]
    causes = collections.defaultdict(collections.Counter)
    for r in bad:
        causes[cause(r)][r["arm"]] += 1
    for c, cnt in sorted(causes.items()):
        L.append(f"| {c} | {cnt['T']} | {cnt['E']} | {cnt['SN']} | {sum(cnt.values())} |")
    L += [f"| **total** | {by_arm['T']} | {by_arm['E']} | {by_arm['SN']} | {len(bad)} |", "",
          "Failure shares (new rows, 95% exact CI): " + "; ".join(f"{a} {ci(by_arm[a], len(qids))}" for a in ('T', 'E', 'SN')) + ".",
          "A protocol-defined infrastructure failure is counted as incorrect in the primary table; it is **not** a model reasoning error.", ""]
    # arm outcomes
    L += [f"## Arm outcomes, all {len(qids)} questions (primary view: infrastructure failures counted as incorrect)", "",
          "| arm | correct (95% exact CI) | model-wrong (row OK, answer wrong) | infra-failed (counted wrong) | correct among OK rows |", "|---|---|---|---|---|"]
    for a in ARMS:
        rs = [rows[(q, a)] for q in qids]
        ok = [r for r in rs if r["status"] == "OK"]
        c = sum(bool(r["correct"]) for r in rs)
        L.append(f"| {a} | {ci(c, len(rs))} | {sum(1 for r in ok if not r['correct'])} | {len(rs) - len(ok)} | {ci(sum(bool(r['correct']) for r in ok), len(ok))} |")
    L += ["", "Asymmetric exposure: T, E and SN depend on the free nemotron route and carry its infrastructure failures; SL (Luna) has none because its 198 rows are reused QA-1 rows. The primary view therefore "
          "penalises the nemotron-dependent arms for supply failures, which are not reasoning errors."]
    pt = "| pair | both correct | first only | second only | neither | paired difference [exact conditional CI] | exact McNemar p |\n|---|---|---|---|---|---|---|"
    L += ["", "## Paired contingency tables, primary view (EXPLORATORY; no multiplicity control; not the preregistered Holm family)", "", pt]
    L += [pair_table(rows, qids, a, b) for a, b in PAIRS]
    clean = [q for q in qids if all(rows[(q, a)]["status"] == "OK" for a in ARMS)]
    L += ["", f"## Sensitivity: questions with no infrastructure failure in any arm (n = {len(clean)} of {len(qids)}) — labelled SENSITIVITY ANALYSIS", "",
          "This subset is selected on infrastructure success, which depends on the supply and on call counts (T and E make more nemotron calls on harder, disagreeing questions). It is **not** unbiased evidence "
          "of superiority and does not replace the primary view.", "", "| arm | correct (95% exact CI) |", "|---|---|"]
    L += [f"| {a} | {ci(sum(bool(rows[(q, a)]['correct']) for q in clean), len(clean))} |" for a in ARMS]
    L += ["", pt] + [pair_table(rows, clean, a, b) for a, b in PAIRS]
    # T trace
    t_ok = [rows[(q, "T")] for q in qids if rows[(q, "T")]["status"] == "OK"]
    L += ["", "## T arm descriptive trace (OK rows)",
          f"- T OK rows {len(t_ok)}; first answers agreed {sum(1 for r in t_ok if r.get('stop') == 'AGREED_FIRST')}; exchanges {sum(1 for r in t_ok if r.get('stop') != 'AGREED_FIRST')}; "
          f"stops {dict(collections.Counter(r.get('stop') for r in t_ok))}.", ""]
    # resources
    L += ["## Resource consumption (new rows only; failed rows record no tokens, so these are lower bounds)", "", "| arm | rows | tokens | calls | arm seconds |", "|---|---|---|---|---|"]
    for a in ("T", "E", "SN"):
        rs = [r for r in new if r["arm"] == a]
        L.append(f"| {a} | {len(rs)} | {sum(r.get('tokens') or 0 for r in rs)} | {sum(r.get('calls') or 0 for r in rs)} | {round(sum(r.get('seconds') or 0 for r in rs))} |")
    L += [f"| total | {len(new)} | {sum(r.get('tokens') or 0 for r in new)} | {sum(r.get('calls') or 0 for r in new)} | {round(sum(r.get('seconds') or 0 for r in new))} |", ""]
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    Path(out_dir, "closure_report.md").write_text("\n".join(L) + "\n")
    Path(out_dir, "closure_numbers.json").write_text(json.dumps({"rows": len(rows_l), "new_rows": len(new), "questions": len(qids), "infra": dict(by_arm), "infra_total": len(bad),
                                                               "causes": {c: dict(v) for c, v in causes.items()}, "clean_questions": len(clean)}, indent=1))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:3]))
