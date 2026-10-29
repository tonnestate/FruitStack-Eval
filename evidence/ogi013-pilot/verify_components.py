#!/usr/bin/env python3
"""Read-only: do the seven FruitStack components (and the pinned tau2 tree) resolve from the canonical checkouts under the CURRENT environment? This is the bootstrap's own test
(runners/ogi013_host_bootstrap.py: is_component_from_checkout / is_module_from_source) without its remedy: the bootstrap would `pip install -e` into the SHARED host venv, which the pilot must not
do. Exit 0 = nothing would be installed. usage: verify_components.py COMPONENTS_ROOT TAU2_CHECKOUT   (run with the pilot's PYTHONPATH and the host python)"""
import json
import sys
from importlib.util import find_spec
from pathlib import Path

COMPONENTS = {"mangome": "MangoMe", "orangeme": "OrangeMe", "peachme": "PeachMe", "pomelome": "PomeloMe", "plumme": "PlumMe", "cherryme": "CherryMe", "appleme": "AppleMe"}


def resolve(module: str, checkout: Path) -> dict:
    spec = find_spec(module)
    origin = str(Path(spec.origin).resolve()) if spec and spec.origin else None
    return {"module": module, "origin": origin, "canonical": bool(origin) and Path(origin).is_relative_to(checkout.resolve())}


def main(argv) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, tau2 = Path(argv[1]), Path(argv[2])
    rows = [resolve(m, root / repo) for m, repo in COMPONENTS.items()] + [resolve("tau2", tau2)]
    print(json.dumps({"all_canonical": all(r["canonical"] for r in rows), "modules": rows}))
    return 0 if all(r["canonical"] for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
