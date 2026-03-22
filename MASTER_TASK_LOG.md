<!-- SSOT Domain: documentation -->

# MASTER_TASK_LOG

Last Updated: 2026-03-21
Source of Update: validation snapshot from
- `python tools/file_header_validator.py validate`
- `python tools/validation/check_recovery_registry.py`
- `python tools/recovery_notes/check_compliance.py`

## HUMAN STATUS (READ THIS FIRST)

### Program phase tracker (authoritative)
| Phase | Name | Status | Evidence | Exit Criteria |
|---|---|---|---|---|
| 0 | Branch + metadata stabilization | ✅ Complete | Header validator=0 violations on new files; registry/compliance checks passing | All SSOT metadata checks green |
| 1 | Audit Batch 001 - inventory lockdown | 🟡 In Progress (starting now) | Next-up plan defined; no inventory artifact committed yet | `docs/recovery/audit_batch_001_inventory.md` committed + first lock-in test merged |
| 2 | Runtime gate hardening | ⏳ Not Started | Awaiting Phase 1 artifacts | CI fails deterministically on real breakage |
| 3 | Entrypoint consolidation + packaging cleanup | ⏳ Not Started | Pending owner/policy decisions | ADR + packaging/script entrypoints aligned |

### Where the project stands right now
- ✅ SSOT metadata gates are green:
  - Header validator: `violation_count: 0`
  - Recovery registry check: pass
  - Recovery-notes compliance check: pass
- ✅ Local branch cleanup is complete for active execution (`work` only).
- ⚠️ Core delivery work is still open; we have not yet started Audit Batch 001 execution artifacts.

### What is blocked vs unblocked
- **Unblocked now**: Audit Batch 001 inventory + requirement mapping + first lock-in tests.
- **Blocked / waiting**:
  - canonical entrypoint owner decision (ADR owner not assigned),
  - merge-gate strictness policy agreement.

### The single most important next move
Start **Audit Batch 001** and commit a human-readable inventory artifact that labels each in-scope file as:
1) requirement-mapped (retain), or 2) quarantine/deprecate candidate (with reason).

### Current stance in one sentence
We are **past remediation** and now in **proof-building mode**: produce inventory evidence + requirement-mapped tests before any broader refactors.

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

- [x] Fixed CI-reported pytest breakages in messaging + discord paths (2026-03-21).
  - Restored D2A policy completeness by injecting `Preferred Reply Format` into rendered D2A output.
  - Aligned Discord service config/devlog reads with test contract (`open(...)` path handling).
  - Removed dependency on missing `src.discord_agent_communication` in messaging controller by using canonical `Agent-1..Agent-8` pattern validation.
  - Evidence commands run:
    - `PYENV_VERSION=3.11.14 python -m pytest tests/core/test_messaging_templates.py::test_d2a_defaults_include_policies -v --tb=short` (pass)
    - broader Discord test targets are pending local dependency parity (`requests`, async plugins) but are expected to execute in CI runner environment.

- [x] Closed the highest-priority SSOT drift by remediating all header violations on newly added files (2026-03-21).
  - `python tools/file_header_validator.py validate` → `violation_count: 0` and `violations_on_new_files: []`.
  - Updated header blocks for:
    - `src/core/managers/core_onboarding_manager.py`
    - `src/core/utilities/validation_utilities.py`
    - `tools/recovery_notes/check_compliance.py`
  - Added missing SSOT registry entries for:
    - `core-onboarding-manager`
    - `validation-utilities-compat`

- [x] Revalidated SSOT control checks after header and registry updates (2026-03-21).
  - `python tools/validation/check_recovery_registry.py` → pass.
  - `python tools/recovery_notes/check_compliance.py` → pass.

- [x] Verified branch consolidation baseline for local repository state.
  - Local branch inventory contains only one branch: `work`.
  - No extra local branches available to delete or merge.

- [x] Published shared local/cloud agent SSOT runbook for autonomous header remediation closure.
  - Artifact: `docs/recovery/autonomous_header_remediation_ssot.md`

- [x] Completed SSOT header remediation for batch 004 (50 files) and revalidated batch with zero header violations.
  - Artifacts: `batches/batch_004.json`, `scripts/validate_batch.sh`, `docs/recovery/header_batch_validation_2026-03-15.md`
- [x] Added clinical, evidence-based repository recon report and closure-first 30-day plan.
  - Artifact: `docs/reports/codebase_recon_and_execution_plan_2026-03-15.md`
