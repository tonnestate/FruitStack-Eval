"""Write QA2D_LOCK.txt before the first QA-2D study call: refuses on a dirty component, a wrong id count/order, or a missing file.
usage: write_qa2d_lock.py ITEMS.jsonl IDS.txt DATASET.parquet OUT_LOCK.txt"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
COMPONENTS = {"FruitStack-Eval": ROOT, "PlumMe": ROOT.parent / "ogi013-plum-org", "CherryMe": ROOT.parent / "ogi013-cherry-org", "PeachMe": ROOT.parent / "ogi013-org-components" / "PeachMe",
              "MangoMe": ROOT.parent / "ogi013-mangome-pinned"}


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git(repo: Path, *a) -> str:
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout.strip()


def main(items, ids_path, dataset, out) -> int:
    ids = [l.strip() for l in Path(ids_path).read_text().splitlines() if l.strip()]
    rows = [json.loads(l) for l in Path(items).read_text().splitlines() if l.strip()]
    if len(ids) != 400 or [r["id"] for r in rows] != ids:
        raise SystemExit("ids/items mismatch or not 400")
    expect = sorted(ids, key=lambda i: hashlib.sha256(("OGI013-QA1|" + i).encode()).hexdigest())
    if expect != ids:
        raise SystemExit("ids are not in QA-1 hash order")
    sys.path.insert(0, str(RUNNERS))
    import ogi013_argument as ag
    import ogi013_qa1 as q1
    prompts = {"QUESTION_PROMPT": q1.QUESTION_PROMPT, "ANSWER_SUFFIX": q1.ANSWER_SUFFIX, "CRITIC_INSTRUCTIONS": ag.CRITIC_INSTRUCTIONS, "REPLY_INSTRUCTIONS": ag.REPLY_INSTRUCTIONS}
    commits = {}
    for name, repo in COMPONENTS.items():
        dirty = git(repo, "status", "--porcelain", "--untracked-files=no")
        if dirty:
            raise SystemExit(f"{name} has uncommitted changes:\n{dirty[:300]}")
        commits[name] = git(repo, "rev-parse", "HEAD")
    lines = ["QA2D_LOCK (written before the first QA-2D study call)",
             f"ids: n={len(ids)} sha256={hashlib.sha256((chr(10).join(ids) + chr(10)).encode()).hexdigest()} order=sha256('OGI013-QA1|'+id)",
             f"dataset: {Path(dataset).name} sha256={sha_file(dataset)}",
             f"prompts sha256={hashlib.sha256(json.dumps(prompts, sort_keys=True).encode()).hexdigest()} " + " ".join(f"{k}={hashlib.sha256(v.encode()).hexdigest()[:12]}" for k, v in prompts.items()),
             f"prereg sha256={sha_file(ROOT / 'evidence/ogi013-lead/OGI013_QA2D_PREREG.md')}",
             f"analyze_qa2d.py sha256={sha_file(RUNNERS / 'analyze_qa2d.py')}", f"analyze_qa1.py sha256={sha_file(RUNNERS / 'analyze_qa1.py')} (imported: paired, holm, McNemar)"]
    lines += [f"{f} sha256={sha_file(RUNNERS / f)}" for f in ("ogi013_qa2d.py", "ogi013_qa1.py", "ogi013_argument.py", "ogi013_vote.py", "ogi013_team_code.py")]
    lines += [f"commit {name}={sha}" for name, sha in commits.items()]
    lines += ["models: Luna = gpt-6-luna (Codex headless, read-only sandbox, no tools); nemotron = nemotron-3-ultra-550b@default (PlumMe, free routes, cost 0)", "run cap: 3000 invocations (PlumMe RunBudget); pause exit code 76"]
    Path(out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:5]))
