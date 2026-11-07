#!/usr/bin/env python3
"""Creates the isolated COLLAB-1 base (offline preparation, no inference): a directory laid out like the evaluation base (env.sh, runs/work.env, benchmarks link, slots/D ledger snapshot) whose MangoMe database is its OWN
COPY of the evaluation database, so no COLLAB-1 write can reach the evaluation state used by C3 and no C3 state is read. Reads the source, writes only the target; refuses to overwrite.
usage: prepare_study_base.py [--source DIR] [--target DIR] [--db NAME]"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013")
TARGET = Path("/root/fruits/research/FRUITSTACK-EVAL-004/ogi-013-collab1")
SOURCE_DB = "mangome_ogi013_eval"
STUDY_DB = "mangome_ogi013_collab1"


def mongosh(js: str) -> str:
    r = subprocess.run(["mongosh", "--quiet", "--eval", js], capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError("mongosh failed: " + r.stderr[-300:])
    return r.stdout.strip()


def counts(db: str) -> dict:
    return json.loads(mongosh(f"JSON.stringify(Object.fromEntries(db.getSiblingDB('{db}').getCollectionNames().sort().map(c=>[c,db.getSiblingDB('{db}')[c].countDocuments()])))"))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--source", default=str(SOURCE))
    p.add_argument("--target", default=str(TARGET))
    p.add_argument("--db", default=STUDY_DB)
    a = p.parse_args(argv)
    src, dst = Path(a.source), Path(a.target)
    if dst.exists():
        print(f"REFUSED: {dst} exists (never overwritten)", file=sys.stderr)
        return 2
    if a.db in json.loads(mongosh("JSON.stringify(db.getMongo().getDBNames())")):
        print(f"REFUSED: database {a.db} already exists (never overwritten)", file=sys.stderr)
        return 2
    before = counts(SOURCE_DB)
    (dst / "runs").mkdir(parents=True)
    (dst / "benchmarks").mkdir()
    (dst / "benchmarks/tau2-bench").symlink_to(src / "benchmarks/tau2-bench")
    (dst / "env.sh").write_text((src / "env.sh").read_text().replace(SOURCE_DB, a.db).replace(f"D={src}", f"D={dst}"))
    for f in ("work.env", "sim_allowlist.json"):
        if (src / "runs" / f).is_file():
            shutil.copy(src / "runs" / f, dst / "runs" / f)
    heads = {}
    for n in ("chat", "project"):
        (dst / "slots/D/ledgers").mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "-q", "--bare", str(src / f"slots/D/ledgers/{n}.git"), str(dst / f"slots/D/ledgers/{n}.git")], check=True)
        heads[n] = subprocess.run(["git", "--git-dir", str(dst / f"slots/D/ledgers/{n}.git"), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    mongosh(f"const s=db.getSiblingDB('{SOURCE_DB}'), d=db.getSiblingDB('{a.db}'); s.getCollectionNames().forEach(c=>s[c].aggregate([{{$match:{{}}}},{{$out:{{db:'{a.db}',coll:c}}}}]));")
    copied = counts(a.db)
    if copied != before or counts(SOURCE_DB) != before:
        raise RuntimeError("database copy differs from the source or the source changed")
    (dst / "STUDY_BASE.json").write_text(json.dumps({"source": str(src), "source_db": SOURCE_DB, "study_db": a.db, "ledger_heads": heads, "collection_counts": copied}, indent=1, sort_keys=True))
    print(json.dumps({"target": str(dst), "db": a.db, "ledger_heads": heads}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
