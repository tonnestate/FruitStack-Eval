import os
import subprocess
from pathlib import Path

import pytest

from fruitstack_eval import attribution, lite, protected

ROOT = Path(__file__).resolve().parent.parent


def run(repo, *args, author="Owner <owner@example.org>"):
    name, email = author[:-1].split(" <")
    env = {**os.environ, "GIT_AUTHOR_NAME": name, "GIT_AUTHOR_EMAIL": email, "GIT_COMMITTER_NAME": name,
           "GIT_COMMITTER_EMAIL": email, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True,
                          env=env).stdout.strip()


def commit_file(repo, path, content, message, author="Owner <owner@example.org>"):
    target = Path(repo) / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    run(repo, "add", path, author=author)
    run(repo, "commit", "-q", "-m", message, author=author)
    return run(repo, "rev-parse", "HEAD")


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "plumme"
    path.mkdir()
    run(path, "init", "-q", "-b", "main")
    commit_file(path, "src/plumme/market.py", "a = 1\nb = 2\n", "human start")
    return path


def test_attribution_by_trailer_branch_and_unattributed(repo):
    commit_file(repo, "src/plumme/policy.py", "x = 1\n", "feat: policy\n\nCo-Authored-By: Claude Opus <noreply@anthropic.com>")
    run(repo, "checkout", "-q", "-b", "web/chatgpt")
    commit_file(repo, "src/plumme/extra.py", "y = 1\nz = 2\nw = 3\n", "feat: extra")
    run(repo, "checkout", "-q", "main")
    run(repo, "merge", "-q", "--no-ff", "web/chatgpt", "-m", "Merge pull request #1 from tonnestate/web/chatgpt")
    rules = attribution.load_rules(ROOT / "config" / "attribution.toml")
    result = attribution.report(repo, rules)
    assert result["lines_by_builder"] == {"CHATGPT": 3, "CLAUDE": 1, "UNATTRIBUTED": 2}
    assert result["critical_lines_by_builder"] == {"CLAUDE": 1, "UNATTRIBUTED": 2}
    assert result["share_by_builder"]["CHATGPT"] == 0.5
    assert result["shallow"] is False
    assert "SOME_LINES_UNATTRIBUTED" in result["warnings"]


def test_builder_trailer_and_explicit_range(repo):
    base = run(repo, "rev-parse", "HEAD")
    run(repo, "checkout", "-q", "-b", "web/chatgpt")
    commit_file(repo, "src/plumme/a.py", "a = 1\n", "feat: unmarked proposal commit", author="TonnEstate <t@example.org>")
    commit_file(repo, "src/plumme/b.py", "b = 1\nc = 2\n", "feat: marked\n\nFruitStack-Builder: luna")
    rules = attribution.load_rules(ROOT / "config" / "attribution.toml")
    without = attribution.report(repo, rules)
    assert without["lines_by_builder"] == {"LUNA": 2, "UNATTRIBUTED": 3}
    with_range = attribution.report(repo, rules, ranges=[attribution.parse_range(f"{base}..HEAD=chatgpt")])
    assert with_range["lines_by_builder"] == {"CHATGPT": 1, "LUNA": 2, "UNATTRIBUTED": 2}
    with pytest.raises(ValueError):
        attribution.parse_range("no-builder")


def test_protected_paths_block_system_commits(repo):
    manifest = protected.load_manifest(ROOT / "config" / "protected_paths.toml")
    base = run(repo, "rev-parse", "HEAD")
    commit_file(repo, "src/plumme/scheduler.py", "s = 1\n", "feat: scheduler\n\nFruitStack-Origin: system")
    clean = protected.check(repo, "plumme", base, "HEAD", manifest)
    assert clean["passed"] and clean["violations"] == [] and clean["commits_checked"] == 1
    commit_file(repo, "src/plumme/budget.py", "limit = 0\n", "fix: budget by builder")
    commit_file(repo, "src/plumme/market.py", "a = 9\n", "self-improve\n\nFruitStack-Origin: system")
    result = protected.check(repo, "plumme", base, "HEAD", manifest)
    assert not result["passed"]
    assert [v["files"] for v in result["violations"]] == [["src/plumme/market.py"]]
    assert [r["files"] for r in result["host_review_required"]] == [["src/plumme/budget.py"]]
    with pytest.raises(ValueError):
        protected.check(repo, "unknown-repo", base, "HEAD", manifest)


def test_lite_pin_check(tmp_path, repo):
    head = run(repo, "rev-parse", "HEAD")
    manifest_path = tmp_path / "lite.toml"
    manifest_path.write_text(
        f'[[component]]\nname = "plumme"\ncommit = "{head[:12]}"\n\n'
        '[[component]]\nname = "cherryme"\ncommit = "UNPINNED"\n', encoding="utf-8")
    components = lite.load_manifest(manifest_path)
    result = lite.check(components, repo.parent)
    statuses = {c["name"]: c["status"] for c in result["components"]}
    assert statuses == {"plumme": "PINNED_OK", "cherryme": "UNPINNED"}
    assert result["ready"] is False


def test_shipped_configs_load():
    assert "plumme" in protected.load_manifest(ROOT / "config" / "protected_paths.toml")
    assert attribution.load_rules(ROOT / "config" / "attribution.toml").version == "FSE-ATTRIBUTION/1"
    names = [c["name"] for c in lite.load_manifest(ROOT / "lite" / "manifest.toml")]
    assert names[0] == "plumme" and "fruitstack-eval" in names
