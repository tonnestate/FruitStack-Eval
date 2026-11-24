# VPS_ACTIVATION — conditional manual runbook (NOT AUTHORIZED TO EXECUTE)

> **Operational status:** Prior freeze order withdrawn. Freeze NOT active or VPS-verified. The runbook is a conditional template, not a standing order; no scheduler, queue, writer or production checkout was changed by this audit.

The earlier freeze instruction was withdrawn by the owner. This is a preparation artifact only. Before execution record renewed owner approval, actual service names, queue backend/export and restore commands, verified-writer configuration schema, current checkout and signer. Missing inputs are STOP conditions; no guessed service name, queue format or environment flag. No reset of GitHub main or deletion of evidence. The operator must adapt the backend-specific commands to the documented implementation; the repository contains research results, not production service software.

## 0. Preflight (read-only)
From an authorized VPS session, run:
```bash
date -Is
hostname
systemctl list-units --type=service --all
systemctl list-timers --all
git -C "$PROD_REPO" status --porcelain
git -C "$PROD_REPO" rev-parse HEAD
git -C "$PROD_REPO" branch --show-current
git -C "$PROD_REPO" remote -v
```
Set PROD_REPO to the verified production checkout and SCHEDULER_UNIT to the confirmed PNP scheduler (not a shared unrelated unit); identify producer/writer service and timer if present, canonical ledger, actual queue dump/count/restore commands, and the documented config flag that disables verified writes. If shared scheduler or missing flag, stop and obtain a scoped alternative; do not edit code. Record queue counts, active leases, ledger hash, original HEAD/branch and running unit states, configuration backup path. Expected before: clean checkout or preserved worktree and known service topology. Rollback: none (read-only). Sign-off: ___.

## 1. Pause dispatch and checkpoint; preserve queue
Only after recorded approval:
```bash
sudo systemctl status "$SCHEDULER_UNIT" --no-pager
sudo systemctl stop "$SCHEDULER_UNIT"
systemctl is-active "$SCHEDULER_UNIT"
```
If a timer or another producer can restart dispatch, pause the identified PNP-only timer/producer too and verify no dispatch. Checkpoint in-flight tasks using the actual scheduler drain operation, retaining pending work. Disable canonical verified writer through the verified configuration flag before accepting further results; if this cannot be done safely, hold dispatch and escalate. Expected after: no new dispatch, pending tasks retained, in-flight leases checkpointed; no canonical writes. Run the documented queue export command to a private durable dump file (record exact command and its exit status); then:
```bash
umask 077
test -s "$QUEUE_DUMP"
sha256sum "$QUEUE_DUMP" > "$QUEUE_DUMP.sha256"
sha256sum -c "$QUEUE_DUMP.sha256"
```
Record before/after counts and validate the dump using backend-specific restore validation; do not restore over live data as a test. The export command cannot be specified accurately without backend discovery. Rollback: restore original writer config and restart only units that were originally active, after queue and ledger reconciliation and owner authorization. Never drop or blindly reimport the live queue. Sign-off: ___.

## 2. Pin baseline without rewriting history
After checking that PROD_REPO is the intended checkout and local work is preserved:
```bash
BASE=d7635f9ea437c494f1c032e4faadfb673a4e90b1
git -C "$PROD_REPO" cat-file -e "$BASE^{commit}"
git -C "$PROD_REPO" status --porcelain
git -C "$PROD_REPO" rev-parse HEAD
git -C "$PROD_REPO" tag freeze-20261124 "$BASE"
git -C "$PROD_REPO" checkout --detach "$BASE"
git -C "$PROD_REPO" rev-parse HEAD
git -C "$PROD_REPO" rev-parse freeze-20261124
```
If tag exists, compare its exact target; do not force overwrite. Expected: HEAD and tag equal BASE; no remote ref rewrite. Preserve original HEAD and branch for rollback via git checkout of the recorded ref after checking worktree cleanliness. If production requires executable code not present in this results repository, do not replace its checkout: pin a separate research-evidence clone instead and document discrepancy. Branch protection, if separately authorized, requires administrator access and verification; local tag alone is not write protection. Sign-off: ___.

## 3. Staging and verified-path configuration
```bash
umask 077
mkdir -p -- "$STAGING_DIR"
test -d "$STAGING_DIR" && test -w "$STAGING_DIR"
sha256sum "$CANONICAL_LEDGER"
```
Use the actual documented configuration flag and configuration tool discovered in preflight; record exact command, prior value and changed value in private operator log. Set output destination to staging if supported and verified promotion disabled. If no documented flag exists, do not invent one; abort activation and report blocker. Verify config effective after reload only if safe and separately authorized. Negative tests: forged verified entry, direct writer, same-family reviews, unknown dependency, frozen dispatch; each must be denied; valid candidate must persist only in staging. Re-hash canonical ledger, record before/after exact state. Rollback: restore backed-up configuration and validate original writer; retain staging, never delete or auto-merge. Sign-off: ___.

## 4. Signed evidence
Prepare ACTIVATION_LOG.md in a separate audit checkout (not the detached production worktree), with timestamp, operator identity, owner approval, redacted command outputs, original/current refs, queue dump hash (not raw queue), queue counts, actual flag names/values, service states, test outcomes, residual blockers and sign-offs. Never commit secrets or personal queue contents.
```bash
git -C "$AUDIT_REPO" branch --show-current
git -C "$AUDIT_REPO" rev-parse HEAD
git -C "$AUDIT_REPO" add -- results/PNP-001-2026-11-23/reconstruction/ACTIVATION_LOG.md
git -C "$AUDIT_REPO" commit -S -m "PNP-001: record operator freeze activation evidence"
git -C "$AUDIT_REPO" verify-commit HEAD
git -C "$AUDIT_REPO" push origin audit/pnp001-freeze-20261124
```
Require the named audit branch and configured signing key; if verification fails, no signed acceptance. Until evidence is returned, status remains NOT ACTIVE / unverified. Sign-off: ___.
