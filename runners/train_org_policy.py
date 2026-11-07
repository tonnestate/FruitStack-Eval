"""OGI-013 organisational structure policy: pre-check, train, evaluate vs baselines, gate verdict, attest.

Run: train_org_policy.py --store DIR --gate ORG_GATE_V1.json --out DIR  (venv3.12, KERAS_BACKEND=jax, PYTHONPATH incl. plum-org/src).
Nothing here activates a policy. A verdict only permits; activation is the host's separate decision.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import random
import sys
from pathlib import Path

os.environ.setdefault("KERAS_BACKEND", "jax")

from ogi013_org_learning import STRUCTURES, load_training_table  # noqa: E402
from plumme.keras_data import bootstrap_by_task, split_by_task  # noqa: E402
from plumme.keras_model import calibration  # noqa: E402

KINDS = ("READ", "WRITE", "TRANSFER", "MESSAGE")
MEMBERS = 5
EPOCHS = 200            # upper bound only: each member stops early on its out-of-bag TASKS (training data only, never the held-out tasks)
PATIENCE = 15
PERMITTED = "LEARNED_POLICY_PERMITTED_FOR_AUTHORIZED_ARM"
ATTEST_SCHEMA = "OGI013-ORG-ATTESTATION/1"
FEATURE_NAMES = ["importance", "kind_READ", "kind_WRITE", "kind_TRANSFER", "kind_MESSAGE", "step_index_scaled", "prior_alerts_scaled",
                 "n_prior_org_decisions_scaled", "n_prior_dissents_scaled", *[f"structure_{s}" for s in STRUCTURES]]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _base(features: dict) -> list[float]:
    kind = features["kind"]
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    return [float(features["importance"]), *[1.0 if kind == k else 0.0 for k in KINDS],
            float(features["step_index"]) / 20.0, float(features["prior_alerts"]) / 3.0,
            float(features["n_prior_org_decisions"]) / 20.0, float(features["n_prior_dissents"]) / 5.0]


def _x(features: dict, structure: str) -> list[float]:
    return _base(features) + [1.0 if structure == s else 0.0 for s in STRUCTURES]


def _xy(rows: list[dict]):
    import numpy as np
    X = np.array([_x(r["features"], r["structure"]) for r in rows], dtype="float32")
    y = np.array([r["reward"] for r in rows], dtype="float32")
    return X, y


def _build(n_in: int):
    import keras
    reg = keras.regularizers.l2(1e-3)
    net = keras.Sequential([keras.Input(shape=(n_in,)), keras.layers.Dense(8, activation="relu", kernel_regularizer=reg),
                            keras.layers.Dropout(0.1), keras.layers.Dense(1, activation="sigmoid")])
    net.compile(optimizer=keras.optimizers.Adam(0.01), loss="binary_crossentropy")
    return net


def _fit_ensemble(rows: list[dict], seed: int) -> list:
    """Same pattern as plumme.keras_model.MQEnsemble.fit: task-level bootstrap per member, deterministic seeds."""
    import keras
    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(r["task_ref"], []).append(r)
    ids = sorted(by)
    nets = []
    for m in range(MEMBERS):
        rng = random.Random(f"{seed}|{m}")
        sample = [r for t in (rng.choice(ids) for _ in ids) for r in by[t]]
        keras.utils.set_random_seed(int(hashlib.sha256(f"{seed}|{m}".encode()).hexdigest()[:8], 16))
        X, y = _xy(sample)
        net = _build(X.shape[1])
        # Labels are episode-level, so the effective sample size is the number of TASKS. Early stopping on the member's out-of-bag tasks (not drawn into its bootstrap) bounds
        # memorisation of per-task noise without ever looking at the held-out evaluation tasks.
        oob = [r for t in ids if t not in {r2["task_ref"] for r2 in sample} for r in by[t]]
        if oob:
            Xv, yv = _xy(oob)
            cb = keras.callbacks.EarlyStopping(monitor="val_loss", patience=PATIENCE, restore_best_weights=True)
            net.fit(X, y, epochs=EPOCHS, batch_size=len(sample), verbose=0, shuffle=False, validation_data=(Xv, yv), callbacks=[cb])
        else:
            net.fit(X, y, epochs=30, batch_size=len(sample), verbose=0, shuffle=False)
        nets.append(net)
    return nets


def _predict(nets: list, X):
    import numpy as np
    return np.stack([np.asarray(n.predict(X, verbose=0)).reshape(-1) for n in nets]).mean(0)


def _logreg(X, y, iters: int = 2000, lr: float = 0.5, l2: float = 1e-3):
    """Plain numpy logistic regression (gradient descent). The gate's third baseline."""
    import numpy as np
    X1 = np.hstack([np.ones((len(X), 1)), X])
    w = np.zeros(X1.shape[1])
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-X1 @ w))
        w -= lr * (X1.T @ (p - y) / len(y) + l2 * np.r_[0.0, w[1:]])
    return lambda Z: 1.0 / (1.0 + np.exp(-(np.hstack([np.ones((len(Z), 1)), Z]) @ w)))


def _logloss(p, y):
    import numpy as np
    p = np.clip(np.asarray(p, dtype="float64"), 1e-6, 1 - 1e-6)
    y = np.asarray(y, dtype="float64")
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def _evaluate(train: list[dict], test: list[dict], gate: dict) -> tuple[list, float | None, dict, dict]:
    """Fit on train tasks (conformal calibration on disjoint tasks), score the held-out tasks. Returns nets, conformal q, evaluation, checks."""
    import numpy as np
    fit_rows, cal_rows, cal_split = split_by_task(train, seed=gate["split_seed"] + 1, holdout_fraction=0.25)
    if len(cal_rows) < 10:
        fit_rows = train
    nets = _fit_ensemble(fit_rows, gate["split_seed"])
    q = None
    if len(cal_rows) >= 10:
        Xc, yc = _xy(cal_rows)
        res = np.sort(np.abs(_predict(nets, Xc) - yc))
        cov = gate["conformal_coverage"]
        q = float(res[min(len(res) - 1, math.ceil(cov * (len(res) + 1)) - 1)])
    Xtr, ytr = _xy(train)
    Xte, yte = _xy(test)
    p_keras = _predict(nets, Xte)
    s_tr = np.array([STRUCTURES.index(r["structure"]) for r in train])
    s_te = np.array([STRUCTURES.index(r["structure"]) for r in test])
    global_mean = float(ytr.mean())
    struct_means = np.array([ytr[s_tr == i].mean() if (s_tr == i).any() else global_mean for i in range(len(STRUCTURES))])
    preds = {"global_mean": np.full(len(test), global_mean), "structure_mean": struct_means[s_te],
             "logistic": _logreg(Xtr, ytr)(Xte)}
    losses = {k: _logloss(v, yte) for k, v in preds.items()}
    best = min(losses, key=lambda k: float(losses[k].mean()))
    lk = _logloss(p_keras, yte)
    gain_rows = [dict(r, _i=i) for i, r in enumerate(test)]
    lb = losses[best]

    def gain(sample: list[dict]):
        idx = [r["_i"] for r in sample]
        return float(lb[idx].mean() - lk[idx].mean())
    lo, hi = bootstrap_by_task(gain_rows, gain, n=gate["bootstrap_resamples"], seed=gate["split_seed"])
    ece = calibration([float(p) for p in p_keras], [float(v) for v in yte])["ece"]
    coverage = None
    if q is not None:
        coverage = float((np.abs(yte - p_keras) <= q).mean())
    ev = {"calibration_split": cal_split, "conformal_half_width": q, "conformal_coverage_observed": coverage,
          "test": {"rows": len(test), "keras_logloss": float(lk.mean()),
                   "baseline_logloss": {k: float(v.mean()) for k, v in losses.items()}, "best_baseline": best,
                   "logloss_gain_over_best_baseline": {"point": gain(gain_rows), "ci95": [lo, hi]}, "ece": ece}}
    checks = {"logloss_gain_point_positive": ev["test"]["logloss_gain_over_best_baseline"]["point"] > 0,
              "logloss_gain_ci_low_above_threshold": lo is not None and lo > gate["min_logloss_gain_ci_low"],
              "ece_within_max": ece <= gate["max_ece"]}
    return nets, q, ev, checks


def _versions() -> dict:
    """Recorded in every attestation. A refusal (INSUFFICIENT_EVIDENCE) needs no Keras, so a host without it records None instead of crashing before the refusal is written."""
    from importlib.metadata import PackageNotFoundError, version
    import plumme

    def installed(name: str) -> str | None:
        try:
            return version(name)
        except PackageNotFoundError:
            return None

    try:
        import keras
        kv, backend = keras.__version__, keras.backend.backend()
    except ImportError:
        kv = backend = None
    return {"python": platform.python_version(), "keras": kv, "backend": backend, "numpy": installed("numpy"), "plumme": getattr(plumme, "__version__", None)}


def _finish(out: Path, gate: dict, verdict: str, checks: dict, counts: dict, data_sha: str, split: dict | None,
            ev: dict | None, reason: str, weights: dict | None) -> dict:
    att = {"schema": ATTEST_SCHEMA, "gate_version": gate["version"], "verdict": verdict, "reason": reason, "checks": checks,
           "failed_checks": sorted(k for k, v in checks.items() if not v), "thresholds": gate, "counts": counts,
           "data_sha256": data_sha, "split": split, "evaluation": ev, "weights": weights, "versions": _versions(),
           "activation": "NOT_ACTIVATED: host decision required"}
    (out / "attestation.json").write_text(json.dumps(att, indent=1, sort_keys=True), encoding="utf-8")
    return att


def run(store: str | Path, gate_path: str | Path, out: str | Path) -> dict:
    gate = json.loads(Path(gate_path).read_text(encoding="utf-8"))
    if gate.get("version") != "ORG-GATE/1":
        raise ValueError("unsupported gate version")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    table = load_training_table(store)
    elig = [r for r in table if r["eligible_for_training"] and r.get("reward") is not None]
    payload = [{"task_ref": r["task_ref"], "structure": r["structure"], "features": r["features"], "reward": r["reward"]} for r in elig]
    data_sha = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    per = {s: sum(1 for r in elig if r["structure"] == s) for s in STRUCTURES}
    tasks = {r["task_ref"] for r in elig}
    counts = {"decision_rows": len(table), "eligible_rows": len(elig), "eligible_tasks": len(tasks), "per_structure_rows": per}
    checks = {"min_rows": len(elig) >= gate["min_rows"], "min_tasks": len(tasks) >= gate["min_tasks"],
              "min_rows_per_structure": all(c >= gate["min_rows_per_structure"] for c in per.values())}
    if not all(checks.values()):
        return _finish(out, gate, "INSUFFICIENT_EVIDENCE", checks, counts, data_sha, None, None,
                       "pre-training minimums not met; no weights trained", None)
    train, test, split = split_by_task(elig, seed=gate["split_seed"], holdout_fraction=gate["holdout_fraction"])
    counts.update({"train_rows": len(train), "test_rows": len(test), "test_tasks": split["test_tasks"]})
    checks["min_test_tasks"] = split["test_tasks"] >= gate["min_test_tasks"]
    if not checks["min_test_tasks"]:
        return _finish(out, gate, "INSUFFICIENT_EVIDENCE", checks, counts, data_sha, split, None,
                       "too few held-out tasks; no weights trained", None)
    nets, q, ev, eval_checks = _evaluate(train, test, gate)
    checks.update(eval_checks)
    verdict = PERMITTED if all(checks.values()) else "NOT_BETTER_THAN_BASELINE_OR_MISCALIBRATED"
    weights = _save_weights(out, nets, q, elig)
    return _finish(out, gate, verdict, checks, counts, data_sha, split, ev,
                   "gate evaluated on held-out tasks; activation is a separate host decision", weights)


def _save_weights(out: Path, nets: list, q: float | None, elig: list[dict]) -> dict:
    imp = [float(r["features"]["importance"]) for r in elig]
    stp = [float(r["features"]["step_index"]) for r in elig]
    meta = {"schema": "OGI013-ORG-WEIGHTS/1", "feature_names": FEATURE_NAMES, "structures": list(STRUCTURES), "kinds": list(KINDS),
            "conformal_half_width": q, "support": {"importance": [min(imp), max(imp)], "step_index": [min(stp), max(stp)]},
            "members": []}
    files = {}
    for i, net in enumerate(nets):
        name = f"weights_member_{i}.keras"
        net.save(out / name)
        files[name] = _sha(out / name)
        meta["members"].append(name)
    (out / "weights.json").write_text(json.dumps(meta, indent=1, sort_keys=True), encoding="utf-8")
    files["weights.json"] = _sha(out / "weights.json")
    return {"files": files, "sha256": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()}


class OrgPolicy:
    """Advisory structure recommender. Abstains (None) unless the attestation permits AND every weight file matches its hash
    AND the features fall inside the training support. Never activates anything itself."""

    def __init__(self, weights_dir):
        self.dir = Path(weights_dir)
        p = self.dir / "attestation.json"
        self._att = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
        self._nets = None
        self._meta = None
        self.permitted = self._verify()

    @property
    def attestation(self) -> dict | None:
        return self._att

    def _verify(self) -> bool:
        att = self._att
        if not att or att.get("verdict") != PERMITTED or not att.get("weights"):
            return False
        files = att["weights"]["files"]
        return all((self.dir / n).exists() and _sha(self.dir / n) == d for n, d in files.items())

    def recommend(self, features: dict) -> str | None:
        if not self.permitted:
            return None
        if self._meta is None:
            self._meta = json.loads((self.dir / "weights.json").read_text(encoding="utf-8"))
        sup = self._meta["support"]
        if features["kind"] not in self._meta["kinds"] or not (sup["importance"][0] <= float(features["importance"]) <= sup["importance"][1]) \
                or not (sup["step_index"][0] <= float(features["step_index"]) <= sup["step_index"][1]):
            return None
        if self._nets is None:
            import keras
            self._nets = [keras.saving.load_model(self.dir / n, compile=False) for n in self._meta["members"]]
        import numpy as np
        X = np.array([_x(features, s) for s in STRUCTURES], dtype="float32")
        score = _predict(self._nets, X)
        return STRUCTURES[int(np.argmax(score))]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--store", required=True)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    att = run(a.store, a.gate, a.out)
    print(json.dumps({"verdict": att["verdict"], "failed_checks": att["failed_checks"], "out": a.out,
                      "activation": "NOT_ACTIVATED"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
