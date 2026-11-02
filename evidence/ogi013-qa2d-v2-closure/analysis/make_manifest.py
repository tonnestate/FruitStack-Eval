"""Write ../closure_manifest.json: sha256 of every preserved item (in-repo and host-local), exact SHAs, receipts/gateway accounting. Host-local paths are read when present."""
import collections, datetime, hashlib, json, platform, sqlite3, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent; E = HERE.parent; ROOT = E.parent.parent
R = Path("/root/fruits/research/OGI013-QA1/runs"); D = Path("/root/fruits/research/OGI013-QA1/data")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else "MISSING"  # noqa: E731
git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).stdout.strip()  # noqa: E731
rec, ids = collections.defaultdict(lambda: [0, 0]), []
for l in open("/root/.plumme/receipts.jsonl"):
    if '"started_at"' not in l:
        continue
    try:
        r = json.loads(l)
    except ValueError:
        continue
    s = str(r.get("started_at"))[:19]
    for name, (a, b) in {"first process": ("2026-10-31T22:53:39", "2026-10-31T23:10:30"), "resumed process": ("2026-10-31T23:20:56", "2026-11-01T00:31:30")}.items():
        if a <= s <= b and r.get("model") == "nemotron-3-ultra-550b":
            rec[name][0 if r.get("success") else 1] += 1
            ids.append(str(r.get("receipt_id")))
ev = ROOT / "evidence/ogi013-lead"
m = {"status": "CLOSED_INFRASTRUCTURE_INFEASIBLE", "generated_utc": datetime.datetime.utcnow().strftime("%FT%TZ"), "python": platform.python_version(),
     "sha256": {"inputs/results.jsonl (357 rows)": sha(E / "inputs/results.jsonl"), "inputs/results_at_first_stop.jsonl (238 rows)": sha(E / "inputs/results_at_first_stop.jsonl"),
                "inputs/invocations.json": sha(E / "inputs/invocations.json"), "inputs/gateway_nemotron_requests_v2_windows.csv": sha(E / "inputs/gateway_nemotron_requests_v2_windows.csv"),
                "inputs/qa1_T_rows.jsonl": sha(E / "inputs/qa1_T_rows.jsonl"), "QA2D_LOCK.txt (lock v2, f88e7d7)": sha(ev / "QA2D_LOCK.txt"), "QA2D_LOCK_v1_SUPERSEDED.txt": sha(ev / "QA2D_LOCK_v1_SUPERSEDED.txt"),
                "QA2D_AMENDMENT_A1.md": sha(ev / "QA2D_AMENDMENT_A1.md"), "QA2D_LOCK_v2_PROVENANCE_ADDENDUM_1.md (b62e853)": sha(ev / "QA2D_LOCK_v2_PROVENANCE_ADDENDUM_1.md"),
                "v1 archived results (246 rows, host-local)": sha(R / "qa2d/out_superseded_prelock_1/run/results.jsonl"), "v2 live results file (host-local)": sha(R / "qa2d_v2/out/run/results.jsonl"),
                "items file (qa2d_items.jsonl, host-local, not published)": sha(D / "qa2d_items.jsonl"), "ids list": sha(D / "qa2d_ids.txt"), "analysis/closure_analysis.py": sha(HERE / "closure_analysis.py"),
                "QA2D_V2_CLOSURE_REPORT.md": sha(E / "QA2D_V2_CLOSURE_REPORT.md")},
     "receipts_nemotron (success, failed)": dict(rec), "receipt_ids_sha256": hashlib.sha256("\n".join(sorted(ids)).encode()).hexdigest(),
     "shas": {"FruitStack-Eval source locked": "dde6307bde0e2aac808a36bbf0b9be35a1bcbfea", "lock v2": "f88e7d7f38190ec66c875e40dd0c2f8fefd9fef2", "lock v1": "6c20e7a", "provenance addendum": "b62e853",
              "head at manifest generation": git("rev-parse", "HEAD"), "PlumMe": "a81546c17325514e52f36e86eb66c2da60ee1aaa", "CherryMe": "c9055391a7879b77f709b275671c3fab828c8bbb", "PeachMe": "efa9bab63ea11cfccc1457aa5f36cf8c65764720",
              "MangoMe": "835d8bef5119fc8266ed8a18f2bd99e105f4bea9", "OrangeMe": "953e725", "PomeloMe": "348975e", "AppleMe": "c2ee35a",
              "GitHub main": "ab6cabe5c99b79d449250d12aed5614cf3b5288a", "GitHub sync/local-truth": "ab6cabe5c99b79d449250d12aed5614cf3b5288a (from 313a015a89c356d9382dae4ba1b7f52d464c1f4a)"},
     "regenerate": "cd evidence/ogi013-qa2d-v2-closure/analysis && python3 closure_analysis.py   (stdlib only; reads ../inputs)",
     "not_published": "question texts, model outputs (exchange/*.json), the global PlumMe receipts file, client ip / user-agent / key ids of the gateway log"}
(E / "closure_manifest.json").write_text(json.dumps(m, indent=1))
print(json.dumps({"receipts": m["receipts_nemotron (success, failed)"]}))
