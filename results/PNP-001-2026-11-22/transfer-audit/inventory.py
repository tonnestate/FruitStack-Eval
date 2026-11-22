"""Mechanical evidence inventory for the transfer audit: statements, authors, reviews, families, statement/review match."""
import json, re, sys, glob
S = sys.argv[1]
DEPS = [("Q-85e487150a", s) for s in ("S0014", "S0016", "S0017")] + \
       [("Q-156fa9c912", s) for s in ("S0138", "S0125", "S0127", "S0135", "S0144", "S0145", "S0098", "S0102", "S0021", "S0024", "S0043", "S0053", "S0086")] + \
       [("Q-f0a0962f12", s) for s in ("S0002", "S0003", "S0007", "S0011")] + [("Q-0b7da33369", "S0117"), ("Q-7555dd132d", "S0014"),
        ("Q-e72cdd5423", "S0001"), ("Q-0a1653e365", "S0002"), ("Q-5f55fb62c2", "S0028"), ("Q-248eb0b818", "S0021")]
FAM = ("claude", "nemotron", "gemma", "gpt", "gemini", "qwen", "deepseek", "muse", "llama", "mistral", "kimi", "glm")
fam = lambda m: next((k for k in FAM if k in (m or "").lower()), None)
tok = lambda s: {w for w in re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", str(s).lower())} - {"lemma", "proof", "with", "that", "this", "then", "every", "from", "have", "reviewed", "correct", "statement", "claim", "claimed", "review", "step"}
out = ["| Step | Status | Author | Reviews (family, verdict, match) | Flags |", "|---|---|---|---|---|"]
details = []
for q, sid in DEPS:
    try: E = json.load(open(f"{S}/desk/proofstate/{q}.json"))
    except FileNotFoundError: out.append(f"| {q}:{sid} | MISSING | | | proof state not found |"); continue
    st = next((e for e in E if e.get("id") == sid and e.get("proved_step")), None)
    if not st: out.append(f"| {q}:{sid} | MISSING | | | step not in this question |"); continue
    revs = [e for e in E if e.get("review_of") == sid]
    disp = [e for e in E if e.get("dispute_of") == sid]
    T = tok(st["proved_step"]); cells = []; flags = []; valid = []
    for r in revs:
        R = tok(r.get("evidence")); j = len(T & R) / max(1, min(len(T), len(R)))
        cross = fam(st.get("model")) and fam(r.get("model")) and fam(st.get("model")) != fam(r.get("model"))
        m = "ok" if j >= 0.25 else "LOW"
        cells.append(f"{r.get('model')} ({'cross' if cross else 'same/unknown'}) {r.get('status')} match={m} {j:.2f}")
        if r.get("status") == "SURVIVED_REVIEW" and cross and m == "ok": valid.append(r)
        if m == "LOW": flags.append("possible misattribution")
    status = revs[-1]["status"] if revs else "CLAIMED"
    if any(r.get("status") == "REFUTED" for r in revs): flags.append("has REFUTED review")
    if disp: flags.append(f"{len(disp)} dispute(s)")
    if status == "SURVIVED_REVIEW" and not valid: flags.append("NO valid cross-family review")
    out.append(f"| {q}:{sid} | {status} | {st.get('model')} | {'<br>'.join(cells) or '-'} | {', '.join(sorted(set(flags))) or '-'} |")
    details.append(f"### {q}:{sid}\n\nAuthor `{st.get('model')}`, session `{st.get('session')}`.\n\n> {str(st['proved_step'])[:4000]}\n\n" +
                   "".join(f"- Review `{r.get('session')}` ({r.get('model')}, {r.get('status')}): {str(r.get('evidence'))[:1500]}\n" for r in revs) +
                   "".join(f"- Dispute `{d.get('session')}` ({d.get('model')}): {str(d.get('evidence'))[:800]}\n" for d in disp))
print("\n".join(out)); print("\n## Full statements and reviews\n"); print("\n".join(details))
