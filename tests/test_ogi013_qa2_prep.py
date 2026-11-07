"""QA-2 preparation tests: synthetic CSV only (no GPQA content), no network."""
import csv
import io
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import prepare_qa2 as pq  # noqa: E402


def synth(n=5):
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Record ID", "Question", "Correct Answer", "Incorrect Answer 1", "Incorrect Answer 2", "Incorrect Answer 3", "High-level domain"])
    for i in range(n):
        w.writerow([f"rec{i:03d}", f"synthetic question {i}?", f"right{i}", f"w1_{i}", f"w2_{i}", f"w3_{i}", "Physics"])
    return buf.getvalue()


def test_convert_is_deterministic_has_four_options_and_a_correct_key():
    a, b = pq.convert(synth()), pq.convert(synth())
    assert a == b and len(a) == 5
    for r in a:
        assert len(r["options"]) == 4 and r["options"][pq.LETTERS.index(r["key"])].startswith("right")
    assert len({r["key"] for r in pq.convert(synth(60))}) == 4                                 # the key letters are spread over A-D


def test_without_access_the_script_stops_and_never_accepts_terms(tmp_path, monkeypatch):
    import urllib.error
    def deny(req, timeout=0):
        raise urllib.error.HTTPError(req.full_url, 403, "gated", {}, None)
    monkeypatch.setattr(pq.urllib.request, "urlopen", deny)
    assert pq.main(["--out", str(tmp_path), "--check"]) == 3
    assert pq.main(["--out", str(tmp_path)]) == 3 and not (tmp_path / "study.jsonl").exists()


def test_prepare_from_a_local_csv_writes_hashes_and_flags_a_wrong_count(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text(synth(5))
    assert pq.main(["--out", str(tmp_path / "o"), "--csv", str(f)]) == 4                    # 5 != 198: not a full GPQA Diamond
    assert (tmp_path / "o" / "study.jsonl").exists() and '"n_ok": false' in (tmp_path / "o" / "dataset_info.json").read_text()


def test_lock_writer_refuses_a_modified_analysis_script_and_a_wrong_question_count(tmp_path):
    import json
    import write_qa2_lock as wl
    evil = tmp_path / "analyze.py"
    evil.write_text("# not the sealed file")
    d = tmp_path / "d"
    d.mkdir()
    (d / "dataset_info.json").write_text(json.dumps({"n": 198, "n_ok": True, "csv_sha256": "a", "ids_sha256": "b"}))
    with pytest.raises(SystemExit, match="differs from the sealed"):
        wl.build(d, "m", analysis=evil)
    real = Path(wl.REPO / "runners/analyze_qa1.py")
    assert wl.sha(real) == wl.SEALED_ANALYSIS                                                    # the sealed QA-1 file is the one in the repository
    (d / "dataset_info.json").write_text(json.dumps({"n": 5, "n_ok": False}))
    with pytest.raises(SystemExit, match="expected 198"):
        wl.build(d, "m")
