"""Offline re-classification of the stored objections and replies of a chain hunt with classify_argument (no model calls).
usage: reclassify_chain_hunt.py RUN_DIR   (RUN_DIR holds results.jsonl and exchange/<qid>.json). Stored texts are capped (objections 1500, replies 400 characters)."""
import json
import sys
from pathlib import Path

import ogi013_argument as ag
from ogi013_qa1 import chain_class, chain_stages

run = Path(sys.argv[1])
for line in (run / "results.jsonl").read_text().splitlines():
    row = json.loads(line)
    f = run / "exchange" / f"{row['qid']}.json"
    if not f.exists():
        print(f"{row['qid']}: no exchange ({row.get('infra_detail', '')[:70]})")
        continue
    ex = json.loads(f.read_text())
    pos_lin = (row.get("lineages") or {}).get("positions", {})
    obj_rows, indep_grounded, ev_replies, ev_withdrawn = [], 0, 0, 0
    for o in ex["objections"]:
        g = ag.classify_argument(o["text"], "")
        grounded_o = g["kind"] in ("command", "quote")
        indep = bool(o.get("lineage")) and o["lineage"] != pos_lin.get(o["target"])
        indep_grounded += int(grounded_o and indep)
        reps = []
        for r in o.get("replies", []):
            gr = ag.classify_argument(r.get("text", ""), "")
            ok = gr["kind"] in ("command", "quote")
            if indep:
                ev_replies += int(ok)
                ev_withdrawn += int(ok and r.get("action") == "withdraw")
            reps.append(f"{r['role']}:{r['action']}={'GROUNDED' if ok else gr['argument']['reason']}")
        obj_rows.append(f"{o['id']}({o.get('lineage')}->{o['target']}) {'GROUNDED' if grounded_o else g['argument']['reason']}" + (f" | replies {reps}" if reps else ""))
    new = {**row, "independent_grounded_objections": indep_grounded, "evidenced_replies": ev_replies, "evidenced_withdrawn": ev_withdrawn}
    st = chain_stages(new)
    print(f"{row['qid']}: now reaches {st['reached']} (was {chain_stages(row)['reached']}) complete={st['complete']} class={chain_class(new) if st['complete'] else None}")
    for t in obj_rows:
        print("    ", t)
