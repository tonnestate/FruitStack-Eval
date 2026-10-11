# FruitStack-Eval — Agent Governance

This repository is the independent evaluator of the FruitStack research protocol. It is part of the FruitStack governance scope and follows the same truth model as the product repositories, with three stricter rules.

## Source of truth

The accepted steady state is:

ACTIVE VPS PRODUCTION = LOCAL CANONICAL SOURCE = GitHub `main` = GitHub `sync/local-truth`

If they unexpectedly disagree, stop and report the divergence. Do not invent an automatic merge, rebase, reset or force-push.

Until `main` exists for the first time, web agents push only to their own web branch; a truth writer creates `main` from an accepted proposal.

## Who may write truth

Luna and Claude Code are local truth writers. ChatGPT and Claude Web are proposal-only agents and use at most one reusable branch each:

- `web/chatgpt`
- `web/claude`

Before a web agent modifies its branch it verifies `origin/main == origin/sync/local-truth` once both exist. If they differ: `STOP: TRUTH_NOT_NORMALIZED`.

## Evaluator independence (stricter than the product repositories)

1. **No system-authored changes.** A commit carrying `FruitStack-Origin: system` may never change this repository. The whole repository is a protected path (`config/protected_paths.toml`).
2. **No imports from the system under test.** The evaluator reads exported logs and git history only. It never imports PlumMe, CherryMe or any other product package.
3. **Builder identity on every commit.** Every commit carries the trailer `FruitStack-Builder: <owner|chatgpt|claude|luna>`, so build-time attribution (protocol threat 4) stays measurable.

## README governance

`README.md` must describe the currently accepted behavior. Any accepted change to behavior, configuration, file formats or interpretation rules updates `README.md` in the same change, or the completing agent reports `README: NO CHANGE REQUIRED` with a reason.

## Pre-registration discipline

Thresholds, sample sizes, rubric versions and task-set digests that a deposited protocol references are frozen. Changing them after a deposit requires a new rubric or schema version and a new deposit; old versions stay readable.

## Definition of done

1. All tests pass on Python 3.11 to 3.13.
2. README is updated when required.
3. No force-push; no branch outside the allowed model.
4. Local HEAD = `origin/main` = `origin/sync/local-truth` for accepted work.
