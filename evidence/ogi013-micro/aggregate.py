"""Micro pilot aggregation: grade every snapshot with evaluate_v2 v2.2, then table (task x arm), CHAIN.md, tokens per arm."""
import json, os, subprocess, sys
from pathlib import Path
R = Path("/root/fruits/research/OGI013-MICRO"); PD = Path("/root/fruits/integration/ogi013-collab-proof"); H = "/root/fruits/integration/ogi013-hostpython-org/bin/python"
TASKS = ["micro__intervals-1", "micro__duration-1", "micro__lru-1"]
rows, per_arm_tokens, chain_runs = {}, {"T": 0, "S": 0, "L": 0}, []
for t in TASKS:
    for arm in "TSL":
        base = R / "runs" / t / arm
        run = base if arm == "L" else base / "run"
        rj = run / "run.json"
        if not rj.exists():
            rows[(t, arm)] = {"status": "INFRA_FAILED" if (R / "runs" / t / f"{arm}.INFRA_FAILED").exists() else "NOT_RUN"}
            continue
        r = json.load(open(rj))
        env = {**os.environ, "TASK_DIR": str(R / t), "FSE_BASE_TREE": str(R / t / "base_tree")}
        if not (run / "grades.json").exists():
            subprocess.run([H, str(PD / "runners/ogi013_grade_snapshots.py"), str(run)], env=env, capture_output=True, text=True, timeout=1800)
        g = json.load(open(run / "grades.json")) if (run / "grades.json").exists() else {}
        final = g.get("RELEASED.diff") or g.get("L_final.diff")
        if arm == "L":
            tokens, secs = r["usage"]["input"] + r["usage"]["output"], r["seconds"]
        else:
            tokens, secs = r["stats"]["tokens_in"] + r["stats"]["tokens_out"] if r.get("stats") else None, r.get("seconds")
        if tokens:
            per_arm_tokens[arm] += tokens
        rows[(t, arm)] = {"status": r["status"], "release": (r.get("release") or {}).get("class"), "resolved": (final or {}).get("resolved"), "f2p": f"{(final or {}).get('f2p_passed')}/{(final or {}).get('f2p_total')}" if final else "-",
                          "p2p": f"{(final or {}).get('p2p_passed')}/{(final or {}).get('p2p_total')}" if final else "-", "tokens": tokens, "seconds": secs, "snapshots": {k: f"{v['f2p_passed']}/{v['f2p_total']}" for k, v in g.items()}}
        if arm == "T":
            chain_runs.append((t, run))
print("| task | arm | status / class | resolved | F2P | P2P | tokens | wall s |\n|---|---|---|---|---|---|---|---|")
for (t, arm), v in rows.items():
    print(f"| {t} | {arm} | {v['status']}{' / ' + v['release'] if v.get('release') else ''} | {v.get('resolved', '-')} | {v.get('f2p', '-')} | {v.get('p2p', '-')} | {v.get('tokens', '-')} | {v.get('seconds', '-')} |")
print("\nTokens per arm (prompt+completion; L = raw Codex input incl. cached + output):", per_arm_tokens)
print("\nSnapshots:", {f"{t}/{a}": v.get("snapshots") for (t, a), v in rows.items() if v.get("snapshots")})
with open(R / "CHAIN.md", "w") as fh:
    p = subprocess.run([H, str(PD / "runners/ogi013_chain.py"), *[str(r) for _, r in chain_runs]], capture_output=True, text=True)
    fh.write(p.stdout + p.stderr[-800:])
json.dump({f"{t}/{a}": v for (t, a), v in rows.items()}, open(R / "pilot_table.json", "w"), indent=1, default=str)
