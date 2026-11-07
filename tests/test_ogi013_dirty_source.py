import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "runners"))
import ogi013_host_bootstrap as hb  # noqa: E402


def test_git_describe_marks_a_tracked_modification_dirty(tmp_path):
    run = lambda *a: subprocess.run(["git", "-C", str(tmp_path), "-c", "user.email=a@b", "-c", "user.name=t", *a], check=True, capture_output=True)
    run("init", "-q")
    (tmp_path / "f.py").write_text("x = 1\n")
    run("add", "-A")
    run("commit", "-qm", "c")
    assert not hb.git_describe(tmp_path).endswith("-dirty")
    (tmp_path / "f.py").write_text("x = 2\n")
    assert hb.git_describe(tmp_path).endswith("-dirty")
