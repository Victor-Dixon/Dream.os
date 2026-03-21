<!-- SSOT Domain: documentation -->

# NEXT_UP

Last Validated: 2026-03-21 (UTC)

## You are here (phase + objective)
- **Current Phase:** Phase 1 — Audit Batch 001 (Inventory Lockdown)
- **Objective of this phase:** establish truth of what code stays vs. what is dead/quarantine, with SSOT-backed evidence.
- **Why this matters now:** without this, we cannot safely tighten gates or do architecture cleanup.

## 60-Second Human Brief
- We finished the header remediation phase. SSOT metadata checks are passing.
- We are now entering **Audit Batch 001** (behavioral truth + inventory lockdown).
- The project risk is no longer "missing headers"; it is now "unknown dead code and weak requirement mapping."

## Where we left off
- Header validator now reports zero violations on new files after SSOT header remediation on the three previously failing targets.
- Recovery registry and recovery-notes compliance checks are both passing.
- Local git branch state is already consolidated to a single branch (`work`), so there are no extra local branches to delete/merge.

## Exact next repair target
Advance from metadata compliance to behavioral SSOT lockdown (Audit Batch 001):

1. Build an explicit in-scope file inventory artifact for `src/`, `tools/`, and `scripts/`.
2. Mark each inventory entry as one of:
   - requirement-mapped and retained, or
   - quarantine/deprecate candidate with rationale.
3. Start lock-in tests for the first retained slice with requirement IDs in test names/docstrings.

## Roadmap (short and actionable)
1. **Step 1 (now):** Commit inventory artifact `docs/recovery/audit_batch_001_inventory.md`.
2. **Step 2:** Commit first requirement-mapped lock-in test + any needed snapshot/log evidence.
3. **Step 3:** Re-run SSOT checks and update this file + `MASTER_TASK_LOG.md` with pass/fail and deltas.
4. **Step 4 (after 1-3):** Start merge-gate hardening tasks only if Step 1/2 evidence exists.

## What to ask the agent next (copy/paste)
Use this exact request for the next turn:

> Execute Audit Batch 001 now. Create `docs/recovery/audit_batch_001_inventory.md` with a table of in-scope files (`src/`, `tools/`, `scripts/`) and columns: file, SSOT registry id, retain/quarantine decision, rationale, required test/snapshot proof. Then implement the first requirement-mapped lock-in test slice and update `MASTER_TASK_LOG.md` + `NEXT_UP.md` with results. Run and report: `python tools/file_header_validator.py validate`, `python tools/validation/check_recovery_registry.py`, `python tools/recovery_notes/check_compliance.py`.

If you want a tighter scoped first pass, use:

> Start Audit Batch 001 with only `src/core/managers/**` and `src/core/utilities/**`. Produce the inventory artifact and one lock-in test tied to a requirement ID. Update `MASTER_TASK_LOG.md` and `NEXT_UP.md` with exact file list covered and what remains.

## Done when
- `python tools/file_header_validator.py validate` remains at zero `violations_on_new_files`.
- Discord template imports continue to load from `src.discord_commander.templates` without fallback.
- CI-critical checks still pass:
  - `python tools/validation/check_recovery_registry.py`
  - `python tools/recovery_notes/check_compliance.py`
  - `git branch --format='%(refname:short)'` continues to show a single active local branch for execution (`work`).
- Audit Batch 001 produces a requirement-mapped inventory artifact committed to the repo (or linked runtime artifact path).

## If we do nothing else this cycle
Ship at least these two artifacts:
1. `docs/recovery/audit_batch_001_inventory.md` (human-readable inventory + decisions)
2. One lock-in test tied to a named requirement ID that demonstrably fails when behavior is broken.

## Definition of "real progress" for this phase
- Not just passing validators.
- We must leave behind:
  - a committed inventory with explicit retain/quarantine decisions,
  - requirement-linked test evidence,
  - and an updated phase status showing what moved from unknown → known.

## Inventory & Lockdown (post-header gate)

### Why this phase exists
- Header compliance confirms formatting and ownership metadata.
- Inventory & Lockdown confirms behavioral truth, and reduces drift by forcing every surviving function to map back to SSOT.

### Audit Batch 001 workflow
1. **Ghost Hunt (coverage-first pruning)**
   - Run baseline coverage during core flows and identify dead or never-hit modules.
   - For each uncovered module/function, require one of:
     - SSOT requirement mapping + lock-in test, or
     - explicit move to `deprecated/` or `quarantine/` with rationale.
2. **Regression Anchor (golden snapshots)**
   - Capture deterministic snapshots for core outputs:
     - recovery registry validation output,
     - generated file structures/manifests,
     - critical logs from core orchestration paths.
   - CI must fail on snapshot deltas until approved with a requirement-linked change note.
3. **Truth vs. Reality Reconciliation**
   - Add a reconciliation pass that compares filesystem artifacts vs. `docs/recovery/recovery_registry.yaml`.
   - Fail on extra files outside registry allowlists.
   - Fail on missing files that the registry claims exist.

### Guardrails against "slop tests"
- Each lock-in test must include an SSOT requirement ID in the test name or docstring.
- Every new/changed test in Audit Batch 001 must fail when the mapped behavior is intentionally broken.
- Coverage increases are accepted only when tied to requirement-mapped assertions (not shallow smoke-only assertions).
- PR template section required: `Requirement -> Function(s) -> Test(s) -> Snapshot(s)`.


## PR #69 Gatekeeper Stability Checkpoint

### Lock-In Protocol (merge gate)
- **Validation Log required**: every file touched across all 13 batches must have an entry in the validation log artifact.
- **Batch coverage required**: run `./scripts/validate_batch.sh` for each affected batch (001-013 where applicable), not a partial subset.
- **Proof required**: attach command logs under `runtime/validation_logs/` (example: `runtime/validation_logs/batch_001.log`).
- **No logs = no merge**.

### Process Stability enforcement
- **No out-of-scope changes**: PR #69 may only touch files assigned to its batch scope.
- If unrelated files were changed (agent "helpful refactor"), revert them before merge.
- Reviewer check: sample 3 files in diff and verify header summary matches actual logic (reject generic filler summaries).

### Registry structural integrity
- After any delete/move/quarantine operation, update `docs/recovery/recovery_registry.yaml` in the same PR.
- Run `python tools/validation/check_recovery_registry.py` after those updates.
- Fail review if code location changed but registry mapping did not.
