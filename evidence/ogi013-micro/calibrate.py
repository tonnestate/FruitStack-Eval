import json, shutil, subprocess, sys, tempfile
from pathlib import Path
R = Path("/root/fruits/research/OGI013-MICRO"); P = R / "ogi013-micro-pilot"
ref = json.load(open(P / "CALIBRATION_v2_2.json"))["micro"]
out, ok = {}, True
for t in sorted(ref):
    out[t] = {}
    for kind in ("base", "gold", "wrong"):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"; shutil.copytree(R / t / "base", ws)
            if kind != "base":
                subprocess.run(["git", "apply", "--whitespace=nowarn", str(P / t / f"{kind}.patch")], cwd=ws, check=True)
            res = Path(tmp) / "g.json"
            env = {"FSE_BASE_TREE": str(R / t / "base_tree"), "PATH": "/usr/bin:/bin"}
            subprocess.run([str(R / t / "venv38/bin/python"), str(R / t / "evaluate_v2.py"), str(ws), str(res)], capture_output=True, text=True, timeout=600, env=env)
            g = json.load(open(res))
        row = {k: g.get(k) for k in ("f2p_passed", "f2p_total", "p2p_passed", "p2p_total", "resolved", "error")}
        out[t][kind] = row
        match = row == ref[t][kind]
        ok &= match
        print(t, kind, row, "MATCH" if match else f"DIFFERS from {ref[t][kind]}")
json.dump(out, open(R / "CALIBRATION_v2_2_reproduced.json", "w"), indent=1)
print("ALL_MATCH" if ok else "MISMATCH")
