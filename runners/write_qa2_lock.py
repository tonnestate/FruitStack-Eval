#!/usr/bin/env python3
"""Writes QA2_LOCK.txt (own lock of the QA-2 replication). Refuses if analyze_qa1.py differs from the sealed QA-1 file, or if any component is -dirty.
usage: write_qa2_lock.py --data-dir DIR --s-model KEY --out QA2_LOCK.txt"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SEALED_ANALYSIS = "d5803210feba3fc40803a5b8f94c089a8e90085ff49e06223b03227a85e79d6c"
REPO = Path(__file__).resolve().parent.parent
COMPONENTS = {"FruitStack-Eval": REPO, "CherryMe": Path("/root/fruits/integration/ogi013-cherry-org"), "PlumMe": Path("/root/fruits/integration/ogi013-plum-org"),
              "PeachMe": Path("/root/fruits/integration/ogi013-peach-org"), "MangoMe": Path("/root/fruits/integration/ogi013-mangome-pinned")}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(path: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(path), *args], capture_output=True, text=True, check=True).stdout.strip()


def build(data_dir: Path, s_model: str, analysis: Path = REPO / "runners/analyze_qa1.py", prereg: Path = REPO / "evidence/ogi013-qa2/OGI013_QA2_PREREG.md", components=COMPONENTS) -> str:
    if sha(analysis) != SEALED_ANALYSIS:
        raise SystemExit("REFUSED: analyze_qa1.py differs from the sealed QA-1 file")
    info = json.loads((data_dir / "dataset_info.json").read_text())
    if not info.get("n_ok"):
        raise SystemExit(f"REFUSED: dataset has {info.get('n')} questions, expected 198")
    commits = {}
    for name, path in components.items():
        if name == "FruitStack-Eval":                                 # the lock file itself is untracked at this point; tracked files must be clean
            dirty = git(path, "status", "--porcelain", "--untracked-files=no")
            commits[name] = (git(path, "rev-parse", "HEAD"), bool(dirty))
        else:
            commits[name] = (git(path, "rev-parse", "HEAD"), git(path, "describe", "--always", "--dirty").endswith("-dirty"))
    if any(d for _, d in commits.values()):
        raise SystemExit(f"REFUSED: dirty component(s): {[n for n, (_, d) in commits.items() if d]}")
    lines = ["QA-2 LOCK (GPQA Diamond replication of the sealed QA-1 protocol)", "",
             "DATASET", f"  file: Idavidrein/gpqa gpqa_diamond.csv", f"  file sha256: {info['csv_sha256']}   ({info['n']} questions)", f"  ids sha256 (sorted record ids, newline-joined): {info['ids_sha256']}",
             "  question texts are kept outside the repository, never committed", "", f"S MODEL (selected by the QA-1 procedure at this lock time): {s_model}", "",
             "SEALED FILES (sha256)", f"  {prereg.relative_to(REPO)} : {sha(prereg)}", f"  runners/analyze_qa1.py : {sha(analysis)}  (identical to the QA-1 seal)", "", "COMMITS (none -dirty)"]
    lines += [f"  {n:<16}: {c}" for n, (c, _) in commits.items()]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, required=True)
    ap.add_argument("--s-model", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.write_text(build(a.data_dir, a.s_model))
    print(a.out)
