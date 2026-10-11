"""Command line interface: `fse <command>`. All results are printed as JSON.

Exit codes: 0 success, 1 a check failed, 2 invalid input.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import ablation, attribution, compare, costaudit, drift, interventions, lite, ope, power, protected, tasks
from .decision_log import load_views

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


def _jsonl(path: str) -> list[dict]:
    rows = []
    for lineno, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON ({exc.msg})") from exc
    return rows


def _emit(data) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))


def _default(name: str) -> str | None:
    candidate = CONFIG_DIR / name
    return str(candidate) if candidate.exists() else None


def _ope_config(args) -> ope.OPEConfig:
    return ope.OPEConfig(clip=args.clip, min_support=args.min_support, min_ess=args.min_ess,
                         family_key=args.family_key, family=args.family, bootstrap=args.bootstrap, seed=args.seed)


def cmd_power(args) -> int:
    if args.design == "paired":
        n = power.paired_noninferiority_n(args.margin, args.discordance, alpha=args.alpha, power=args.power,
                                          true_difference=args.true_difference)
        _emit({"design": "paired", "tasks": n})
    else:
        n = power.unpaired_noninferiority_n(args.margin, args.reference_rate, alpha=args.alpha, power=args.power,
                                            true_difference=args.true_difference)
        _emit({"design": "unpaired", "tasks_per_arm": n})
    return 0


def cmd_ope(args) -> int:
    views, warnings = load_views(Path(args.log))
    config = _ope_config(args)
    if args.action == "evaluate":
        result = ope.evaluate(views.values(), ope.TargetPolicy.from_dict(json.loads(args.target)), config).to_dict()
        result["log_warnings"] = warnings
        _emit(result)
        return 0
    candidate = ope.evaluate(views.values(), ope.TargetPolicy.from_dict(json.loads(args.candidate)), config)
    incumbent = ope.evaluate(views.values(), ope.TargetPolicy.from_dict(json.loads(args.incumbent)), config)
    review = ope.promotion_review(candidate, incumbent, config)
    _emit({"review": review, "candidate": candidate.to_dict(), "incumbent": incumbent.to_dict(),
           "log_warnings": warnings})
    return 0


def cmd_costaudit(args) -> int:
    views, warnings = load_views(Path(args.log))
    result = costaudit.audit(views.values(), args.allow or costaudit.DEFAULT_ALLOWED).to_dict()
    result["log_warnings"] = warnings
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_drift(args) -> int:
    views, warnings = load_views(Path(args.log))
    result = drift.detect(views.values())
    result["log_warnings"] = warnings
    _emit(result)
    return 0


def cmd_interventions(args) -> int:
    if args.action == "add":
        item = interventions.Intervention(actor=args.actor, kind=args.kind, action=args.intervention,
                                          minutes=args.minutes, phase=args.phase, refs=tuple(args.ref or ()),
                                          note=args.note)
        interventions.append(Path(args.log), item)
        _emit(item.to_dict())
        return 0
    items, warnings = interventions.load(Path(args.log))
    summary = interventions.summarize(items, args.verified_tasks)
    summary["log_warnings"] = warnings
    _emit(summary)
    return 0


def cmd_tasks(args) -> int:
    rows = _jsonl(args.tasks)
    if args.action == "validate":
        problems = tasks.validate(rows)
        _emit({"tasks": len(rows), "problems": problems})
        return 1 if problems else 0
    if args.action == "commit":
        manifest, salts = tasks.commit(rows)
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        fd = os.open(args.salts, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(salts, indent=2) + "\n")
        _emit({"tasks": len(manifest["tasks"]), "digest": manifest["digest"], "manifest": args.manifest,
               "salts": args.salts})
        return 0
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    salts = json.loads(Path(args.salts).read_text(encoding="utf-8"))
    problems = tasks.verify(manifest, rows, salts)
    _emit({"tasks": len(manifest.get("tasks", [])), "problems": problems})
    return 1 if problems else 0


def cmd_compare(args) -> int:
    scored, excluded = compare.score_rows(_jsonl(args.results), args.success_threshold)
    result = {
        "arms": compare.summarize_arms(scored),
        "excluded": excluded,
        "h4": compare.paired_noninferiority(scored, args.new, args.reference, args.margin, alpha=args.alpha,
                                            bootstrap=args.bootstrap, seed=args.seed),
    }
    _emit(result)
    return 0


def cmd_ablation(args) -> int:
    scored, excluded = compare.score_rows(_jsonl(args.results), args.success_threshold)
    result = ablation.analyze(scored, ablation.load_configs(Path(args.configs)), metric=args.metric,
                              bootstrap=args.bootstrap, alpha=args.alpha, seed=args.seed)
    result["excluded"] = excluded
    _emit(result)
    return 0


def cmd_attribution(args) -> int:
    rules_path = args.rules or _default("attribution.toml")
    if rules_path is None:
        raise ValueError("no attribution rules found; pass --rules")
    ranges = [attribution.parse_range(text) for text in (args.range or [])]
    _emit(attribution.report(Path(args.repo), attribution.load_rules(Path(rules_path)), args.rev, ranges))
    return 0


def cmd_protected(args) -> int:
    manifest_path = args.manifest or _default("protected_paths.toml")
    if manifest_path is None:
        raise ValueError("no protected-path manifest found; pass --manifest")
    result = protected.check(Path(args.repo), args.name, args.base, args.head,
                             protected.load_manifest(Path(manifest_path)))
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_lite(args) -> int:
    result = lite.check(lite.load_manifest(Path(args.manifest)), Path(args.workspace))
    _emit(result)
    return 0 if result["ready"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fse", description="FruitStack-Eval research instrumentation")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("power", help="sample sizes for the H4 non-inferiority test")
    p.add_argument("design", choices=["paired", "unpaired"])
    p.add_argument("--margin", type=float, required=True)
    p.add_argument("--discordance", type=float, default=0.2)
    p.add_argument("--reference-rate", type=float, default=0.7)
    p.add_argument("--alpha", type=float, default=0.025)
    p.add_argument("--power", type=float, default=0.80)
    p.add_argument("--true-difference", type=float, default=0.0)
    p.set_defaults(func=cmd_power)

    p = sub.add_parser("ope", help="independent off-policy evaluation of a DecisionLog export")
    p.add_argument("action", choices=["evaluate", "review"])
    p.add_argument("--log", required=True)
    p.add_argument("--target", default='{"selector": "deterministic"}')
    p.add_argument("--candidate", default='{"selector": "deterministic"}')
    p.add_argument("--incumbent", default='{"selector": "deterministic"}')
    p.add_argument("--family")
    p.add_argument("--family-key", default="task_family")
    p.add_argument("--clip", type=float, default=10.0)
    p.add_argument("--min-support", type=int, default=30)
    p.add_argument("--min-ess", type=float, default=100.0)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261011)
    p.set_defaults(func=cmd_ope)

    p = sub.add_parser("costaudit", help="verify that only free offers were chosen and nothing was billed")
    p.add_argument("--log", required=True)
    p.add_argument("--allow", action="append", help="allowed cost class (repeatable)")
    p.set_defaults(func=cmd_costaudit)

    p = sub.add_parser("drift", help="model drift epochs from per-call fingerprints")
    p.add_argument("--log", required=True)
    p.set_defaults(func=cmd_drift)

    p = sub.add_parser("interventions", help="typed human-intervention log")
    p.add_argument("action", choices=["add", "summary"])
    p.add_argument("--log", required=True)
    p.add_argument("--actor")
    p.add_argument("--kind", choices=sorted(interventions.KINDS))
    p.add_argument("--intervention", help="action name, e.g. PROMOTE_POLICY or HINT")
    p.add_argument("--minutes", type=float)
    p.add_argument("--phase", choices=sorted(interventions.PHASES))
    p.add_argument("--ref", action="append")
    p.add_argument("--note")
    p.add_argument("--verified-tasks", type=int)
    p.set_defaults(func=cmd_interventions)

    p = sub.add_parser("tasks", help="task registry with committed references")
    p.add_argument("action", choices=["validate", "commit", "verify"])
    p.add_argument("--tasks", required=True)
    p.add_argument("--manifest")
    p.add_argument("--salts")
    p.set_defaults(func=cmd_tasks)

    p = sub.add_parser("compare", help="replay results and test H4 (paired non-inferiority)")
    p.add_argument("--results", required=True)
    p.add_argument("--new", required=True)
    p.add_argument("--reference", required=True)
    p.add_argument("--margin", type=float, required=True)
    p.add_argument("--alpha", type=float, default=0.025)
    p.add_argument("--success-threshold", type=float, default=1.0)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261011)
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser("ablation", help="which organizational component causes which gain (LOO and Shapley)")
    p.add_argument("--results", required=True)
    p.add_argument("--configs", required=True, help="TOML with an [arms] table: arm = [components switched on]")
    p.add_argument("--metric", choices=list(ablation.METRICS), default="utility")
    p.add_argument("--success-threshold", type=float, default=1.0)
    p.add_argument("--alpha", type=float, default=0.05)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261011)
    p.set_defaults(func=cmd_ablation)

    p = sub.add_parser("attribution", help="who wrote the code as it stands (git blame)")
    p.add_argument("--repo", required=True)
    p.add_argument("--rev", default="HEAD")
    p.add_argument("--rules")
    p.add_argument("--range", action="append", help="base..head=BUILDER, e.g. origin/main..origin/web/chatgpt=CHATGPT")
    p.set_defaults(func=cmd_attribution)

    p = sub.add_parser("protected", help="check commits against protected paths")
    p.add_argument("--repo", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--head", default="HEAD")
    p.add_argument("--manifest")
    p.set_defaults(func=cmd_protected)

    p = sub.add_parser("lite", help="check FruitStack-Lite pins")
    p.add_argument("action", choices=["check"])
    p.add_argument("--manifest", required=True)
    p.add_argument("--workspace", required=True)
    p.set_defaults(func=cmd_lite)
    return parser


def _required(args, names: list[str]) -> None:
    missing = [name for name in names if getattr(args, name) is None]
    if missing:
        raise ValueError("missing required options: " + ", ".join("--" + m.replace("_", "-") for m in missing))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "interventions" and args.action == "add":
            _required(args, ["actor", "kind", "intervention", "minutes", "phase"])
        if args.command == "tasks" and args.action in ("commit", "verify"):
            _required(args, ["manifest", "salts"])
        return args.func(args)
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
