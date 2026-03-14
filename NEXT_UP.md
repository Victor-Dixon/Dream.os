<!-- SSOT Domain: documentation -->

# NEXT_UP

## Exact next repair target
Reduce file-header compliance drift by fixing validator-reported violations on newly added files first:

1. `src/core/managers/core_onboarding_manager.py` (`HDR001`)
2. `src/core/utilities/validation_utilities.py` (`HDR001`, `HDR004`)
3. `tools/recovery_notes/check_compliance.py` (`HDR001`, `HDR004`)

## Done when
- `python tools/file_header_validator.py validate` shows zero `violations_on_new_files`.
- Discord template imports continue to load from `src.discord_commander.templates` without fallback.
- CI-critical checks still pass:
  - `python tools/validation/check_recovery_registry.py`
  - `python tools/recovery_notes/check_compliance.py`

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
