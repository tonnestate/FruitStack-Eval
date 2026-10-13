import sys
from pathlib import Path

from fruitstack_eval import stack
from test_git_tools import commit_file, run

ROOT = Path(__file__).resolve().parent.parent


def checkout(tmp_path):
    upstream = tmp_path / "up"
    upstream.mkdir()
    run(upstream, "init", "-q", "-b", "main")
    commit_file(upstream, "src/x.py", "a = 1\n", "init")
    run(tmp_path, "clone", "-q", str(upstream), "clone")
    return upstream, tmp_path / "clone"


def test_stack_passes_only_on_canonical_clean_checkouts(tmp_path, monkeypatch):
    upstream, clone = checkout(tmp_path)
    meta = {"plumme": {"installed": True, "version": "0.1.11", "editable": True, "url": f"file://{clone / 'src'}"},
            "peachme": {"installed": False},
            "mangome": {"installed": True, "version": "0.3", "vcs_commit": "abc"}}
    monkeypatch.setattr(stack, "probe_distributions", lambda python, dists: meta)
    comps = [stack.Component("plumme", dist="plumme"), stack.Component("peachme", dist="peachme"),
             stack.Component("mangome", dist="mangome", required=False),
             stack.Component("omniroute", units=("avcos-omniroute.service",)),
             stack.Component("cogc", paths=(str(tmp_path / "missing" / "SKILL.md"),), required=False)]
    result = stack.check(comps, "python", units_probe=lambda unit: False)
    by = {c["name"]: c for c in result["components"]}
    assert by["plumme"]["ok"] and by["plumme"]["checks"]["checkout"]["head"] == by["plumme"]["checks"]["checkout"]["origin_main"]
    assert not by["peachme"]["ok"] and "not installed" in by["peachme"]["problems"][0]
    assert by["mangome"]["ok"]
    assert not by["omniroute"]["ok"] and not by["cogc"]["ok"]
    assert sorted(result["blocking"]) == ["omniroute", "peachme"] and not result["passed"]

    (clone / "src" / "x.py").write_text("a = 2\n")                              # hand-patched source
    commit_file(upstream, "src/y.py", "b = 1\n", "newer main")
    patched = stack.check(comps[:1], "python", fetch=True)
    problems = patched["components"][0]["problems"]
    assert any("local changes" in p for p in problems) and any("!= origin/main" in p for p in problems)


def test_real_metadata_probe_reads_without_importing(tmp_path):
    meta = stack.probe_distributions(sys.executable, ["pytest", "surely-not-installed-dist"])
    assert meta["pytest"]["installed"] and meta["surely-not-installed-dist"] == {"installed": False}


def test_default_stack_config_lists_the_whole_fruitstack():
    names = {c.name: c for c in stack.load(ROOT / "config" / "stack.toml")}
    assert {"plumme", "peachme", "cherryme", "appleme", "pomelome", "cogc", "omniroute"} <= set(names)
    assert all(names[n].required for n in ("plumme", "peachme", "cherryme", "appleme", "pomelome"))
