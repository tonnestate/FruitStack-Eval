"""Command line interface: `fse <command>`. All results are printed as JSON.

Exit codes: 0 success, 1 a check failed, 2 invalid input.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import (ablation, attribution, blind, calibration, compare, costaudit, deposit, drift, independence, inquiry,
               integrity, interventions, lite, logcheck, ope, pilot, power, protected, replay, seal, stack, tasks)
from . import ogi13
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


def cmd_ogi13(args) -> int:
    """Read exported host observations: no model inference, repo imports or writes."""
    result = ogi13.compare_paired(_jsonl(args.observations))
    result["observation_file"] = str(args.observations)
    result["complete_pairs_only"] = not (
        result["unmatched_tasks"] or result["confounded_tasks"] or
        result["missing_usage_tasks"] or result["incomplete_grade_tasks"]
    )
    _emit(result)
    if result["paired_tasks"] == 0:
        return 1
    if args.require_complete and not result["complete_pairs_only"]:
        return 1
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


def _write_jsonl(path: str, rows: list[dict]) -> None:
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows),
                          encoding="utf-8")


def cmd_integrity(args) -> int:
    requirements = integrity.load_requirements(Path(args.requirements or _default("g1_requirements.toml")))
    result = integrity.check(requirements, Path(args.clones), remote=args.remote, fetch=args.fetch)
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_calib(args) -> int:
    if args.action == "generate":
        rows = calibration.generate(args.n, args.seed)
        _write_jsonl(args.out, rows)
        _emit({"tasks": len(rows), "seed": args.seed, "digest": calibration.task_set_digest(rows), "out": args.out})
        return 0
    _required(args, ["tasks", "results"])
    task_rows = _jsonl(args.tasks)
    scored, warnings = calibration.score(task_rows, _jsonl(args.results))
    if args.out:
        _write_jsonl(args.out, scored)
    _emit({"task_set_digest": calibration.task_set_digest(task_rows), "rows": len(scored),
           "executed": sum(1 for r in scored if r["executed"]), "correct": sum(1 for r in scored if r["correct"]),
           "warnings": warnings, "out": args.out})
    return 0


def cmd_independence(args) -> int:
    thresholds = independence.Thresholds.load(Path(args.thresholds or _default("g2_thresholds.toml")))
    result = independence.analyze(_jsonl(args.scored), thresholds)
    _emit(result)
    return 0 if result["passed"] else 1


def _log_spec(text: str) -> tuple[str, tuple[Path, str]]:
    name, _, rest = text.partition("=")
    path, _, kind = rest.rpartition(":")
    if not name or not path or kind not in seal.LOG_KINDS:
        raise ValueError(f"--log must be NAME=PATH:KIND with KIND in {seal.LOG_KINDS}, got {text!r}")
    return name, (Path(path), kind)


def cmd_seal(args) -> int:
    if args.action == "create":
        logs = dict(_log_spec(t) for t in args.log or [])
        manifest, rows = seal.seal(logs)
        out, rows_path = seal.write(manifest, rows, Path(args.seal))
        _emit({"digest": manifest["digest"], "logs": {k: v["rows"] for k, v in manifest["logs"].items()},
               "seal": str(out), "rows": str(rows_path)})
        return 0
    manifest, rows = seal.read(Path(args.seal))
    result = seal.verify(manifest, rows, allow_retention=not args.strict)
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_logcheck(args) -> int:
    views, warnings = load_views(Path(args.log))
    seal_result = None
    if args.seal:
        manifest, rows = seal.read(Path(args.seal))
        seal_result = seal.verify(manifest, rows)
    result = logcheck.check(views.values(), warnings, interventions_path=Path(args.interventions) if args.interventions else None,
                            seal_result=seal_result, expect_cost_policy=args.expect_cost_policy,
                            require_feedback=args.require_feedback)
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_inquiry(args) -> int:
    task_rows = [t for t in _jsonl(args.tasks) if t.get("family") == "INQUIRY"]
    if args.action == "validate":
        problems, verdicts, key_types, subfamilies = [], {}, {}, {}
        for t in task_rows:
            try:
                ref = inquiry.parse_reference(t["reference"])
            except (ValueError, KeyError, TypeError) as exc:
                problems.append(f"{t.get('task_id')}: {exc}")
                continue
            if inquiry.FORMAT not in t.get("prompt", ""):
                problems.append(f"{t.get('task_id')}: prompt lacks the FSE-INQUIRY/1 answer format")
            verdicts[ref["verdict"]] = verdicts.get(ref["verdict"], 0) + 1
            key_types[ref["key_type"]] = key_types.get(ref["key_type"], 0) + 1
            subfamilies[t.get("subfamily")] = subfamilies.get(t.get("subfamily"), 0) + 1
        problems.extend(tasks.validate(task_rows) if task_rows else ["no INQUIRY tasks"])
        _emit({"tasks": len(task_rows), "verdicts": verdicts, "key_types": key_types, "subfamilies": subfamilies,
               "problems": problems})
        return 1 if problems else 0
    _required(args, ["results", "out"])
    by_id = {t["task_id"]: t for t in task_rows}
    graded, summary = [], {}
    for row in _jsonl(args.results):
        task = by_id.get(row.get("task_id"))
        if task is None:
            raise ValueError(f"result for unknown inquiry task {row.get('task_id')}")
        ev = inquiry.evidence(task["reference"], row.get("output"))
        graded.append({"task_id": row["task_id"], "arm": row["arm"], "family": "INQUIRY", "subfamily": task["subfamily"],
                       "evidence": ev, "quota_units": row.get("quota_units"), "cost_eur": row.get("cost_eur"),
                       "wall_seconds": row.get("wall_seconds"), "run_status": row.get("status")})
        s = summary.setdefault(row["arm"], {"items": 0, "grade_1": 0, "grade_0.5": 0, "grade_0": 0, "abstained": 0,
                                            "NO_ANSWER": 0, "NO_STRUCTURED_ANSWER": 0, "INCOMPLETE": 0})
        s["INCOMPLETE"] += int(row.get("status") == "INCOMPLETE")
        s["items"] += 1
        s[f"grade_{ev['grade']:g}"] += 1
        s["abstained"] += int(ev["abstained"])
        if ev["parse_status"] in ("NO_ANSWER", "NO_STRUCTURED_ANSWER"):
            s[ev["parse_status"]] += 1
    _write_jsonl(args.out, graded)
    _emit({"grader": inquiry.GRADER, "rows": len(graded), "by_arm": summary, "out": args.out})
    return 0


def cmd_blind(args) -> int:
    if args.action == "export":
        _required(args, ["tasks", "results", "seed", "sheet", "key", "manifest"])
        sheet, key, manifest = blind.export(_jsonl(args.results), _jsonl(args.tasks), seed=args.seed, sample=args.sample)
        _write_jsonl(args.sheet, sheet)
        fd = os.open(args.key, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(blind._canonical(key))
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _emit({k: manifest[k] for k in ("items", "tasks", "arms", "redactions", "key_sha256", "sheet_sha256")})
        return 0
    _required(args, ["manifest", "key", "sheet", "grader", "out"])
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    key_rows = [json.loads(l) for l in Path(args.key).read_text(encoding="utf-8").splitlines() if l.strip()]
    result = blind.ingest(manifest, key_rows, _jsonl(args.sheet), grader=args.grader)
    _write_jsonl(args.out, result["labels"])
    out = {"labels": len(result["labels"]), "voided_tasks": result["voided_tasks"], "out": args.out}
    if args.deterministic:
        det = {(r["task_id"], r["arm"]): r["evidence"]["grade"] for r in _jsonl(args.deterministic)}
        out["agreement_with_deterministic"] = blind.agreement(result["labels"], det)
    _emit(out)
    return 0


def cmd_pilot(args) -> int:
    _emit(pilot.analyze(_jsonl(args.graded), reference_arm=args.reference_arm, bootstrap=args.bootstrap,
                        seed=args.seed, success_threshold=args.success_threshold))
    return 0


def cmd_replay(args) -> int:
    result = replay.run(Path(args.evidence), main)
    _emit(result)
    return 0 if result["passed"] else 1


def _files(specs: list[str] | None) -> dict[str, Path]:
    out = {}
    for spec in specs or []:
        label, _, path = spec.partition("=")
        if not label or not path:
            raise ValueError(f"--file must be LABEL=PATH, got {spec!r}")
        out[label] = Path(path)
    return out


def cmd_deposit(args) -> int:
    if args.action == "build":
        _required(args, ["out"])
        manifest = deposit.build(_files(args.file))
        Path(args.out).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        _emit({"digest": manifest["digest"], "items": len(manifest["items"]), "out": args.out,
               "next": "deposit the manifest and the files, then record the DOI in the manifest's doi field"})
        return 0
    _required(args, ["manifest"])
    result = deposit.verify(json.loads(Path(args.manifest).read_text(encoding="utf-8")), _files(args.file))
    _emit(result)
    return 0 if result["passed"] else 1


def cmd_stack(args) -> int:
    result = stack.check(stack.load(Path(args.config or _default("stack.toml"))), args.python, fetch=args.fetch)
    _emit(result)
    return 0 if result["passed"] else 1


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

    p = sub.add_parser("ogi13", help="OGI-013 independent fixed/adaptive organisational efficiency comparison")
    p.add_argument("action", choices=("compare",))
    p.add_argument("--observations", required=True,
                   help="JSONL exported from host benchmark run, never self-graded by workers")
    p.add_argument("--require-complete", action="store_true",
                   help="fail on unmatched, resource-confounded, ungraded or missing-usage task pairs")
    p.set_defaults(func=cmd_ogi13)

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

    p = sub.add_parser("integrity", help="gate G1: main == sync/local-truth and required states merged")
    p.add_argument("--clones", required=True, help="directory with one git clone per repository name")
    p.add_argument("--requirements", help="TOML (default config/g1_requirements.toml)")
    p.add_argument("--remote", default="origin")
    p.add_argument("--fetch", action="store_true", help="fetch all branches before checking")
    p.set_defaults(func=cmd_integrity)

    p = sub.add_parser("calib", help="gate G2: calibration tasks with exact answers")
    p.add_argument("action", choices=["generate", "score"])
    p.add_argument("--n", type=int, default=60)
    p.add_argument("--seed", type=int, default=20261011)
    p.add_argument("--tasks")
    p.add_argument("--results")
    p.add_argument("--out")
    p.set_defaults(func=cmd_calib)

    p = sub.add_parser("independence", help="gate G2: reliability and error correlation per provider group")
    p.add_argument("--scored", required=True, help="output of `fse calib score`")
    p.add_argument("--thresholds", help="TOML (default config/g2_thresholds.toml)")
    p.set_defaults(func=cmd_independence)

    p = sub.add_parser("seal", help="gate G5: revision-evident seal of append-only logs")
    p.add_argument("action", choices=["create", "verify"])
    p.add_argument("--seal", required=True, help="seal file (rows go to <seal>.rows.json)")
    p.add_argument("--log", action="append", help="NAME=PATH:KIND, KIND decisionlog or jsonl (create)")
    p.add_argument("--strict", action="store_true", help="treat dropped (rotated-out) rows as a failure")
    p.set_defaults(func=cmd_seal)

    p = sub.add_parser("logcheck", help="gate G5: completeness of decision, intervention and seal records")
    p.add_argument("--log", required=True, help="PlumMe DecisionLog")
    p.add_argument("--interventions", help="typed intervention log")
    p.add_argument("--seal", help="seal created by `fse seal create`")
    p.add_argument("--expect-cost-policy", help="e.g. FREE_ONLY for free arms")
    p.add_argument("--require-feedback", action="store_true", help="require verified feedback rows")
    p.set_defaults(func=cmd_logcheck)

    p = sub.add_parser("inquiry", help="gate G4: validate inquiry references and grade answers deterministically")
    p.add_argument("action", choices=["validate", "grade"])
    p.add_argument("--tasks", required=True)
    p.add_argument("--results", help="JSON lines with task_id, arm, output, quota_units, cost_eur, wall_seconds")
    p.add_argument("--out")
    p.set_defaults(func=cmd_inquiry)

    p = sub.add_parser("blind", help="gate G4: blinded human grading packets")
    p.add_argument("action", choices=["export", "ingest"])
    p.add_argument("--tasks")
    p.add_argument("--results")
    p.add_argument("--seed", type=int)
    p.add_argument("--sample", type=float, default=1.0, help="share of tasks to include (whole tasks, all arms)")
    p.add_argument("--sheet", help="grading sheet (export: written; ingest: the graded sheet)")
    p.add_argument("--key", help="blind key, kept by the operator (mode 0600)")
    p.add_argument("--manifest", help="manifest with key and sheet hashes; commit before grading")
    p.add_argument("--grader")
    p.add_argument("--out")
    p.add_argument("--deterministic", help="output of `fse inquiry grade` for an agreement check")
    p.set_defaults(func=cmd_blind)

    p = sub.add_parser("pilot", help="phase 3: descriptive pilot estimates and a sample-size proposal (no tests)")
    p.add_argument("action", choices=["analyze"])
    p.add_argument("--graded", required=True, help="output of `fse inquiry grade` (or blind labels joined to results)")
    p.add_argument("--reference-arm", default="F1")
    p.add_argument("--success-threshold", type=float, default=1.0)
    p.add_argument("--bootstrap", type=int, default=2000)
    p.add_argument("--seed", type=int, default=20261011)
    p.set_defaults(func=cmd_pilot)

    p = sub.add_parser("replay", help="gate G6: recompute committed reports from raw logs (replay.toml)")
    p.add_argument("--evidence", required=True)
    p.set_defaults(func=cmd_replay)

    p = sub.add_parser("deposit", help="gate G7: deposit manifest of protocol, tasks, thresholds and freeze")
    p.add_argument("action", choices=["build", "verify"])
    p.add_argument("--file", action="append", help="LABEL=PATH; labels protocol, task_manifest, g2_thresholds, "
                                                   "pilot_procedure, freeze (plus any extra)")
    p.add_argument("--out")
    p.add_argument("--manifest")
    p.set_defaults(func=cmd_deposit)

    p = sub.add_parser("stack", help="preflight: the whole FruitStack installed from canonical checkouts (run before any eval)")
    p.add_argument("--python", required=True, help="host interpreter, e.g. /opt/fruitstack/venv-host/bin/python")
    p.add_argument("--config", help="TOML (default config/stack.toml)")
    p.add_argument("--fetch", action="store_true", help="fetch origin in each checkout first")
    p.set_defaults(func=cmd_stack)
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
        if args.command == "calib" and args.action == "generate":
            _required(args, ["out"])
        if args.command == "tasks" and args.action in ("commit", "verify"):
            _required(args, ["manifest", "salts"])
        return args.func(args)
    except (ValueError, KeyError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
