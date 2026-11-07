#!/usr/bin/env python3
"""Regression fixture for the FruitStack host entrypoint (runners/fs_runtime.py): config/fs_runtime/offline_fixture.toml in mode offline-fixture.

Scripted provider texts behind the public PlumMe adapter interface; every other component is the real code path. Not evidence of capability or organizational gain.
Operational runs use fs_runtime.py --mode operational directly.
Usage: fs_fullstack_e2e.py OUT_DIR
"""
import sys
from pathlib import Path

from fs_runtime import main

CONFIG = Path(__file__).resolve().parents[1] / "config" / "fs_runtime" / "offline_fixture.toml"

if __name__ == "__main__":
    sys.exit(main(["--config", str(CONFIG), sys.argv[1], "--mode", "offline-fixture"]))
