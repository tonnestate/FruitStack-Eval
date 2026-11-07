"""QA-2D v2 closure analysis. Deterministic; reads only the preserved rows under ../inputs; writes ../QA2D_V2_CLOSURE_REPORT.md and closure_numbers.json.
No hypothesis test, no p-value, no winner: counts, exact Clopper-Pearson 95% intervals and 2x2 tables only. usage: python3 closure_analysis.py   (from this directory)"""
import collections
import json
import re
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ARMS = ("SL", "SN", "T", "E")
PAIRS = (("T", "SL"), ("T", "E"), ("T", "SN"), ("E", "SL"), ("E", "SN"), ("SN", "SL"))
CONCLUSION = ("QA-2D v2 could not complete its preregistered confirmatory study because the available Nemotron supply exceeded the infrastructure-failure threshold. "
              "The collected observations do not establish whether organized cooperation is superior to the controls.")


def load(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def cp(k, n, a=0.05):
    """Exact Clopper-Pearson interval by bisection on the binomial tail (deterministic)."""
    if n == 0:
        return (0.0, 1.0)
    def cdf(x, p):
        return sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(0, x + 1))
    lo, hi = 0.0, 1.0
    if k > 0:
        l, h = 0.0, k / n
        for _ in range(80):
            m = (l + h) / 2
            if 1 - cdf(k - 1, m) > a / 2:
                h = m
            else:
                l = m
        lo = h
    if k < n:
        l, h = k / n, 1.0
        for _ in range(80):
            m = (l + h) / 2
            if cdf(k, m) > a / 2:
                l = m
            else:
                h = m
        hi = l
    return lo, hi


def fmt(k, n):
    lo, hi = cp(k, n)
    return f"{k}/{n} = {100 * k / n:.1f}% [{100 * lo:.1f}, {100 * hi:.1f}]" if n else "0/0"


def cause(r):
    d = str(r.get("infra_detail"))
    if "REASONING_LEAKED_AS_CONTENT" in d:
        return "C3 call made; output unusable (REASONING_LEAKED_AS_CONTENT at the length cap)"
    if "NOT_PERFORMED" in d and "HTTP 502" in d:
        return "C2 no provider call; refusal during cooldown after an upstream timeout (HTTP 502)"
    if "NOT_PERFORMED" in d and "HTTP 429" in d:
        return "C1 no provider call; HTTP 429 no capacity / rate-limited route"
    return "C0 other: " + d[:60]


def table2(a, b, rows, qs):
    x = [bool(rows[(q, a)]["correct"]) for q in qs]
    y = [bool(rows[(q, b)]["correct"]) for q in qs]
    return (f"| {a} vs {b} | {len(qs)} | {sum(1 for u, v in zip(x, y) if u and v)} | {sum(1 for u, v in zip(x, y) if u and not v)} | "
            f"{sum(1 for u, v in zip(x, y) if v and not u)} | {sum(1 for u, v in zip(x, y) if not u and not v)} |")


TH = "| pair (A vs B) | n | both correct | A only | B only | neither |\n|---|---|---|---|---|---|"


def arm_rows(rows, qs, title):
    out = [f"| arm | correct / {len(qs)} (95% exact CI) | rows OK | model-wrong (OK row, wrong answer) | infra-failed (protocol: counted wrong) |", "|---|---|---|---|---|"]
    for a in ARMS:
        rs = [rows[(q, a)] for q in qs]
        ok = [r for r in rs if r["status"] == "OK"]
        out.append(f"| {a} | {fmt(sum(bool(r['correct']) for r in rs), len(rs))} | {len(ok)} | {sum(1 for r in ok if not r['correct'])} | {len(rs) - len(ok)} |")
    return out


def main():
    final = load(ROOT / "inputs" / "results.jsonl")
    first = load(ROOT / "inputs" / "results_at_first_stop.jsonl")
    qa1_t = load(ROOT / "inputs" / "qa1_T_rows.jsonl")
    rows = {(r["qid"], r["arm"]): r for r in final}
    assert len(rows) == len(final) == 357
    new = [r for r in final if not r.get("reused_from")]
    qs = sorted({r["qid"] for r in new})
    assert len(qs) == 53 and all((q, a) in rows for q in qs for a in ARMS)
    sl_unpaired = sum(1 for r in final if r["arm"] == "SL" and r["qid"] not in set(qs))
    first_keys = {(r["qid"], r["arm"]) for r in first}
    proc1 = [r for r in new if (r["qid"], r["arm"]) in first_keys]
    proc2 = [r for r in new if (r["qid"], r["arm"]) not in first_keys]
    L = [f"# QA-2D v2 closure report", "", f"**Conclusion (verbatim).** {CONCLUSION}", "",
         "Status: CLOSED_INFRASTRUCTURE_INFEASIBLE. Everything below is exploratory and descriptive, produced from the preserved rows by `analysis/closure_analysis.py` (deterministic; no p-values, no hypothesis tests, no winner). "
         "The planned 400-question confirmatory analysis (H1L, H1c) was not performed.", "",
         "## 1. Preserved evidence and rows",
         f"- {len(final)} rows = {len(final) - len(new)} reused QA-1 Luna rows (SL) + {len(new)} new rows (T, E, SN: 53 each) over {len(qs)} questions. {sl_unpaired} of the {len(final) - len(new)} SL rows are not paired with any other arm and are excluded from every comparison (preserved).",
         "- Preserved read-only with sha256 in `closure_manifest.json`: lock v2, Amendment A1, provenance addendum (`b62e853`), all rows, `invocations.json`, the gateway request extract, the PlumMe receipt-window id hash, the superseded v1 lock and archived rows.", "",
         "## 2. Infrastructure failures, reconciled row by row",
         "**Erratum.** The earlier report text said \"34 failures\" in its cause summary. That figure was an addition error. The row-level recount below is the correct total: **36** = T 13 + E 12 + SN 11, equal to the cause total 15 + 11 + 10.", ""]
    bad = [r for r in new if r["status"] != "OK"]
    causes = sorted({cause(r) for r in bad})
    L += ["| cause | T | E | SN | total |", "|---|---|---|---|---|"]
    for c in causes:
        L.append(f"| {c} | " + " | ".join(str(sum(1 for r in bad if cause(r) == c and r['arm'] == a)) for a in ('T', 'E', 'SN')) + f" | {sum(1 for r in bad if cause(r) == c)} |")
    L += [f"| **total** | {sum(1 for r in bad if r['arm'] == 'T')} | {sum(1 for r in bad if r['arm'] == 'E')} | {sum(1 for r in bad if r['arm'] == 'SN')} | {len(bad)} |", "",
          "By process (first process 22:53:39Z-23:10:12Z; resumed process 23:20:56Z-00:31:18Z) and cumulative, infra-failed / new rows:", "", "| arm | first process | resumed process | cumulative |", "|---|---|---|---|"]
    for a in ("T", "E", "SN"):
        f = lambda rs: f"{sum(1 for r in rs if r['arm'] == a and r['status'] != 'OK')}/{sum(1 for r in rs if r['arm'] == a)}"  # noqa: E731
        L.append(f"| {a} | {f(proc1)} | {f(proc2)} | {f(new)} |")
    L += ["", "", ""]
    import csv
    g = list(csv.reader(open(ROOT / "inputs" / "gateway_nemotron_requests_v2_windows.csv")))[1:]
    L[-2] = f"Gateway cross-check (`inputs/gateway_nemotron_requests_v2_windows.csv`): {len(g)} nemotron requests, {sum(1 for x in g if x[3] == 'error')} errors, {sum(1 for x in g if 'aborted' in x[4])} of them 60 s aborts."
    L += ["A protocol-defined infrastructure failure is counted as incorrect in the primary view. It is not a model reasoning error.", "",
          f"## 3. Primary outcomes, all {len(qs)} questions (infrastructure failures counted as wrong)", ""] + arm_rows(rows, qs, "primary")
    L += ["", "Disclosed asymmetry: SL rows were reused (zero infrastructure exposure). T and E need several successful nemotron calls per question and SN needs one; T and E are structurally more exposed to the supply failures than SN, and all three more than SL.",
          "", "### Paired 2x2 tables, primary view (counts only; no test, no p-value)", "", TH] + [table2(a, b, rows, qs) for a, b in PAIRS]
    t_ok = [r for r in new if r["arm"] == "T" and r["status"] == "OK"]
    L += ["", "### T arm trace (OK rows)", f"- {len(t_ok)} OK T rows; first answers agreed {sum(1 for r in t_ok if r.get('stop') == 'AGREED_FIRST')}; reached an exchange {sum(1 for r in t_ok if r.get('stop') != 'AGREED_FIRST')}; stops {dict(collections.Counter(r.get('stop') for r in t_ok))}.", "",
          "## 4. Resources (new rows; failed rows record no tokens, so tokens/calls are lower bounds)", "", "| arm | rows | tokens | calls | arm seconds |", "|---|---|---|---|---|"]
    for a in ("T", "E", "SN"):
        rs = [r for r in new if r["arm"] == a]
        L.append(f"| {a} | {len(rs)} | {sum(r.get('tokens') or 0 for r in rs)} | {sum(r.get('calls') or 0 for r in rs)} | {round(sum(r.get('seconds') or 0 for r in rs))} |")
    inv = json.loads((ROOT / "inputs" / "invocations.json").read_text())["used"]
    L += [f"| total | {len(new)} | {sum(r.get('tokens') or 0 for r in new)} | {sum(r.get('calls') or 0 for r in new)} | {round(sum(r.get('seconds') or 0 for r in new))} |", "",
          f"Provider attempts (`invocations.json`): {inv} of 3,000. Wall time of the two processes: 16 min 33 s + 70 min 22 s = 86 min 55 s. Receipt counts are in `closure_manifest.json`.", "",
          "## 5. Stop reason", "`INFRA_SHARE_ABOVE_10PCT:E` at 00:31:18Z (2026-11-01) after question 6264 (40 questions in the resumed process): the preregistered pause rule. No restart. Closed by decision as infrastructure-infeasible.", "",
          "## 6. Sensitivity analysis (separate; labelled)", "",
          "**Selected by an outcome-related exclusion; not unbiased; does not replace the primary outcomes; no superiority interpretation.** Whether a row is infrastructure-failed depends on the supply and on how many nemotron calls a question needs.", ""]
    clean = [q for q in qs if all(rows[(q, a)]["status"] == "OK" for a in ARMS)]
    L += [f"### 6a. All four arms OK (n = {len(clean)} of {len(qs)})", ""] + arm_rows(rows, clean, "6a") + ["", TH] + [table2(a, b, rows, clean) for a, b in PAIRS]
    L += ["", "### 6b. Pairwise complete cases (both rows OK for that pair)", "", "| pair (A vs B) | n | A correct (95% exact CI) | B correct (95% exact CI) | both | A only | B only | neither |", "|---|---|---|---|---|---|---|---|"]
    for a, b in PAIRS:
        pq = [q for q in qs if rows[(q, a)]["status"] == "OK" and rows[(q, b)]["status"] == "OK"]
        x = [bool(rows[(q, a)]["correct"]) for q in pq]
        y = [bool(rows[(q, b)]["correct"]) for q in pq]
        L.append(f"| {a} vs {b} | {len(pq)} | {fmt(sum(x), len(pq))} | {fmt(sum(y), len(pq))} | {sum(1 for u, v in zip(x, y) if u and v)} | {sum(1 for u, v in zip(x, y) if u and not v)} | "
                 f"{sum(1 for u, v in zip(x, y) if v and not u)} | {sum(1 for u, v in zip(x, y) if not u and not v)} |")
    # 6b planning
    def dis(pairs):
        return sum(1 for a, b in pairs if a != b), len(pairs)
    tp = [(r["first_by_pos"].get("S1"), r["first_by_pos"].get("S2")) for r in t_ok]
    sl_sn = [(rows[(q, "SL")]["letter"], rows[(q, "SN")]["letter"]) for q in qs if rows[(q, "SL")]["status"] == "OK" and rows[(q, "SN")]["status"] == "OK"]
    q1 = [tuple((r.get("first_letters") or {}).values()) for r in qa1_t if r["status"] == "OK"]
    q1 = [p for p in q1 if len(p) >= 2 and all(p)]
    L += ["", "## 7. Disagreement rate (planning estimate, not a result)", "", "| source | n | first answers differ | rate (95% exact CI) | expected exchange cases at 400 questions (same rate and CI) |", "|---|---|---|---|---|"]
    for name, (k, n) in (("QA-2D v2 T OK rows: Luna vs nemotron first answers (both exist)", dis(tp)), ("QA-2D v2: SL vs SN single-call letters, both rows OK (same prompt)", dis(sl_sn)),
                         ("QA-1 original T OK rows with two first answers (none: all 6 OK T rows had a single first answer; no Luna-vs-nemotron pairs exist in QA-1)", dis(q1))):
        lo, hi = cp(k, n)
        L.append(f"| {name} | {n} | {k} | {fmt(k, n)} | {400 * k / n:.0f} [{400 * lo:.0f}, {400 * hi:.0f}] |" if n else f"| {name} | 0 | - | - | - |")
    L += ["", "Sources: `inputs/results.jsonl` (T `first_by_pos`, SL/SN letters) and `inputs/qa1_T_rows.jsonl` (QA-1 original study rows). QA-1 contains no Luna-vs-nemotron pairs, so its row is a different pair of models and only indicates scale.",
          "Limits: small n; one model with a high failure share; the 53 questions are the first in a hash order; rows that failed infrastructure checks are missing from the T-based rate. This is not a power claim for H1/H1c and not a recommendation for a v3.", "",
          "## 8. Scientific history", "", "| time (UTC) | event | SHA / reference |", "|---|---|---|",
          "| 2026-10-31 21:57:04Z-22:24Z | v1 run under lock v1 (started before the correction order; stopped by PIDs); 246 rows (198 SL + 48 new over 16 questions), archived and not used | lock v1 `6c20e7a` (22:57+01:00 commit), source `84ed28f` |",
          "| 2026-10-31 (v1 rows) | the 16 observed questions: 12 OK T rows, 11 agreed, 1 exchange; they inform no later decision | Amendment A1 |",
          "| 2026-10-31 22:45:36Z | Amendment A1 (post-lock runner changes listed; independence from the 16 questions argued) | `dde6307` |",
          "| 2026-10-31 22:53:37Z | lock v2 | `f88e7d7`, source `dde6307` |",
          "| 2026-10-31 22:53:39Z-23:10:12Z | v2 first process: 40 new rows over 14 questions; stopped by PIDs for truth reconciliation | `invocations.json` used 73 |",
          "| 2026-10-31 ~23:15Z-23:19Z | truth reconciliation: GitHub sync/local-truth fast-forwarded 313a015a -> ab6cabe5; canonical local main and sync/local-truth fast-forwarded (9 uncommitted items byte-identical) | main == sync/local-truth == `ab6cabe5` |",
          "| 2026-10-31 23:20:46Z | provenance addendum, written after 40 rows existed; executed bytes not captured at launch | `b62e853` |",
          "| 2026-10-31 23:20:56Z-2026-11-01 00:31:18Z | v2 resumed process: +119 rows (resumed run total 159 new rows over 53 questions); automatic pause `INFRA_SHARE_ABOVE_10PCT:E` | used 309 |",
          "| 2026-11-01 | closed as infrastructure-infeasible (this report) | head at generation: see `closure_manifest.json` |", "",
          f"**Conclusion (verbatim).** {CONCLUSION}"]
    (ROOT / "QA2D_V2_CLOSURE_REPORT.md").write_text("\n".join(L) + "\n")
    numbers = {"rows": len(final), "new_rows": len(new), "questions": len(qs), "infra_total": len(bad), "infra_by_arm": dict(collections.Counter(r["arm"] for r in bad)),
               "infra_by_cause": dict(collections.Counter(cause(r) for r in bad)), "clean_questions_all_four": len(clean), "sl_unpaired": sl_unpaired}
    (HERE / "closure_numbers.json").write_text(json.dumps(numbers, indent=1, sort_keys=True))
    print(json.dumps(numbers, sort_keys=True))


if __name__ == "__main__":
    main()
