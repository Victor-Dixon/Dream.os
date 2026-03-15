<!-- SSOT Domain: documentation -->

# MASTER_TASK_LOG

Last Updated: 2026-03-15
Source of Update: `docs/reports/codebase_recon_and_execution_plan_2026-03-15.md`

## THIS_WEEK (Closure-First, Max 5)

1. [ ] **CRITICAL** (200 pts): Canonical Entrypoint Decision + ADR
   - Decide and publish one primary operational entrypoint.
   - Mark all other CLIs as compatibility shims.
   - DoD: ADR merged, README + START_HERE aligned, one launch path verified.

2. [ ] **CRITICAL** (200 pts): Remove Dead CLI Imports / Broken Handler Paths
   - Remove stale `src.core.service_manager` import fallback usage.
   - Resolve missing validation-handler references in CLI command router paths.
   - DoD: import checks pass for all active CLI modules.

3. [ ] **HIGH** (150 pts): Harden Merge Gate to Fail on Real Breakage
   - Remove non-essential `continue-on-error` behavior in mandatory checks.
   - Eliminate references to missing scripts in active workflows.
   - DoD: CI fails deterministically for missing scripts/import/test failures.

4. [ ] **HIGH** (150 pts): Packaging Surface Repair
   - Fix root `package.json` validity.
   - Align `pyproject.toml` console scripts with real callable exports.
   - DoD: package metadata validates and script entrypoints resolve.

5. [ ] **HIGH** (150 pts): Replace Placeholder Smoke/Import Tests
   - Convert non-assertive placeholder tests to hard assertions.
   - Ensure failing imports break CI reliably.
   - DoD: tests fail when critical imports or runtime contracts are broken.

## INBOX

- [ ] **HIGH** (125 pts): Swarm-console execution realism
  - Replace scaffold `"tests not run"` reporting with actual command/test execution telemetry.
  - DoD: run artifacts include real command output, test results, and failure propagation.

- [ ] **MEDIUM** (75 pts): Reduce syntax-check exclusion list in technical debt workflow
  - Move from exclusion-heavy syntax validation to targeted repair.
  - DoD: excluded-file count reduced and documented with owner/date.

- [ ] **MEDIUM** (60 pts): Pytest config SSOT consolidation
  - Align active pytest configuration authority between `pytest.ini` and `pyproject.toml`.
  - DoD: no config conflict warning during CI/local runs.

## WAITING_ON

- [ ] Owner assignment for canonical entrypoint ADR
- [ ] Team agreement on merge-gate strictness policy

## PARKED / DEFERRED

- [ ] Broad `src/core` and `src/services` architecture rewrite (defer until gate reliability is restored)
- [ ] New feature expansion across additional CLI surfaces (freeze until entrypoint consolidation closes)

## COMPLETED_THIS_CYCLE

- [x] Added clinical, evidence-based repository recon report and closure-first 30-day plan.
  - Artifact: `docs/reports/codebase_recon_and_execution_plan_2026-03-15.md`
