#!/usr/bin/env python3
"""QA-2 data preparation (GPQA Diamond, exact replication of the sealed QA-1 protocol). Needs a Hugging Face token WITH GPQA access that the owner provides (HF_TOKEN or ~/.cache/huggingface/token).
This script never accepts dataset terms and never works around the gate: without access it stops (exit 3). Question texts are written outside the repository only.
usage: prepare_qa2.py --out DIR [--csv LOCAL.csv] [--check]    --check = only test access (HEAD request), writes nothing."""
import argparse
import csv
import hashlib
import io
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

URL = "https://huggingface.co/datasets/Idavidrein/gpqa/resolve/main/gpqa_diamond.csv"
LETTERS = "ABCD"


class AccessDenied(RuntimeError):
    pass


def token() -> str | None:
    t = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    for p in (Path.home() / ".cache/huggingface/token", Path.home() / ".huggingface/token"):
        if not t and p.exists():
            t = p.read_text().strip()
    return t or None


def request(method: str, tok: str | None):
    req = urllib.request.Request(URL, method=method, headers={"Authorization": f"Bearer {tok}"} if tok else {})
    try:
        return urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403, 404):
            raise AccessDenied(f"GPQA Diamond is gated: HTTP {exc.code}. The owner must accept the dataset terms on Hugging Face and provide a token with access; nothing was accepted or bypassed.") from exc
        raise


def option_order(record_id: str) -> list:
    """Deterministic permutation of the four answer options (index 0 is the correct one) from sha256 of the record id: no random state, reproducible."""
    return sorted(range(4), key=lambda i: hashlib.sha256(f"OGI013-QA2-options|{record_id}|{i}".encode()).hexdigest())


def convert(csv_text: str) -> list:
    out = []
    for row in csv.DictReader(io.StringIO(csv_text)):
        rid = (row.get("Record ID") or "").strip()
        cands = [row["Correct Answer"].strip()] + [row[f"Incorrect Answer {i}"].strip() for i in (1, 2, 3)]
        perm = option_order(rid)
        out.append({"id": rid, "question": row["Question"].strip(), "options": [cands[i] for i in perm], "key": LETTERS[perm.index(0)], "category": row.get("High-level domain", "")})
    return sorted(out, key=lambda r: r["id"])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path)
    ap.add_argument("--csv", type=Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    try:
        if a.check:
            request("HEAD", token())
            print("GPQA access OK")
            return 0
        text = a.csv.read_text() if a.csv else request("GET", token()).read().decode()
    except AccessDenied as exc:
        print(str(exc), file=sys.stderr)
        return 3
    rows = convert(text)
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / "gpqa_diamond.csv").write_text(text)
    with (a.out / "study.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    ids = "\n".join(r["id"] for r in rows)
    info = {"n": len(rows), "csv_sha256": hashlib.sha256(text.encode()).hexdigest(), "ids_sha256": hashlib.sha256(ids.encode()).hexdigest(), "expected_n": 198, "n_ok": len(rows) == 198}
    (a.out / "dataset_info.json").write_text(json.dumps(info, indent=1))
    print(json.dumps(info))
    return 0 if info["n_ok"] else 4


if __name__ == "__main__":
    sys.exit(main())
