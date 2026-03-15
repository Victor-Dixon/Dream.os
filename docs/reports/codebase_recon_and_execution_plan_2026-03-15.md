# Codebase Recon and Closure-First Execution Plan (2026-03-15)

## Executive Summary
This repository is currently a **hybrid tooling lab + partial product surface**, not a cohesive shippable product. The runtime has at least two overlapping control planes (`main.py` service launcher vs `apps/api` swarm-console API) plus multiple CLIs (`main.py`, `python -m src.cli`, `agent-cellphone` package script), with inconsistent ownership and behavior. The primary launcher path works for basic argument parsing but contains dead imports and unreachable handlers that indicate drift in command architecture. CI is present but not a reliable merge gate: multiple jobs are explicitly non-blocking, one workflow references missing scripts, and test suites include placeholder assertions that do not enforce runtime correctness. Packaging metadata is materially inconsistent (invalid root `package.json`; Python script entrypoints reference non-existent module-level functions), indicating release-surface fragility. Documentation is extensive but overstates operational reliability relative to current implementation details (stubs, fallbacks, soft-fail CI paths). The `src/core` and `src/services` trees remain large and abstraction-heavy, with many `pass`/stub regions and adapter layers that are not clearly exercised. The highest-leverage path is to **freeze expansion and close runtime/CI integrity gaps first**: one canonical entrypoint, one canonical test gate, and one canonical packaging contract. Until that closure lane is complete, adding new systems will continue to increase architecture drift and operational risk.

## Codebase Map

| Area | Observed Purpose | Status |
|---|---|---|
| `main.py` + `src/cli/argument_parser.py` + `src/services/service_manager.py` | Legacy-but-active service launcher and process control path | active (drifted) |
| `src/cli/__main__.py` | Separate “unified CLI” domain router (`services`/`core`) | experimental/parallel |
| `src/agent_cellphone/cli.py` + `pyproject.toml` scripts | Packaged CLI surface for `agent-cellphone` commands | active surface, implementation mostly static/demo |
| `apps/api/` + `apps/ui/` + `scripts/run_swarm_console_*.sh` | Swarm-console scaffold (repo selection, runs, patch export) | experimental (scaffold) |
| `src/core/` | Large utility/orchestration hub with many subdomains and abstractions | active but high-debt |
| `src/services/` | Business/service layer with messaging, coordination, analytics, traders | active but high-debt |
| `src/discord_commander/` | Discord integration subsystem | active |
| `src/trading_robot/` | TSLA/report/trading workflows and supporting services | active |
| `.github/workflows/*.yml` | Multiple CI/quality/debt/recovery gates | active but inconsistent/partially soft |
| `archive/`, `root_cleanup_archive_*`, numerous docs archives | historical migrations and retained legacy artifacts | legacy/archive |

## Real Architecture
The real runtime architecture is not single-lane. `main.py` is still the practical operations entrypoint for service lifecycle actions (`--start`, `--status`, `--stop`) by delegating to `src/cli/argument_parser.py` and `src/services/service_manager.py`. In parallel, `src/cli/__main__.py` defines a separate domain-based CLI routing model (`services`, `core`) and deprecation shims in `src/core/cli/__main__.py` and `src/services/cli/__main__.py` redirect toward it. A third public interface exists via packaging scripts in `pyproject.toml`, mapped to `src/agent_cellphone/cli.py`. 

Separately, `apps/api/main.py` exposes a FastAPI control-plane scaffold for run records and patch export, while `apps/ui` is a static frontend that calls that API. This API path is currently evidence-oriented and scaffolded (stores files under `runtime/`), not integrated into the `main.py` service orchestration path.

**Main entrypoints and control flow found in code:**
1. `python main.py ...` → parse args (`src/cli/argument_parser.py`) → run handler/service manager (`src/services/service_manager.py`).
2. `python -m src.cli ...` → independent domain CLI dispatch (`src/cli/__main__.py`).
3. `python -m uvicorn apps.api.main:app ...` via `scripts/run_swarm_console_api.sh`.
4. `python -m http.server 5173` in `apps/ui` via `scripts/run_swarm_console_ui.sh`.
5. Packaging console scripts in `pyproject.toml` targeting `agent_cellphone.cli`.

## Critical Findings
1. **CLI architecture drift and dead import surfaces.** `main.py` imports `src.core.service_manager` and a non-existent validation handler in a try/except fallback block, while its active code path uses `src.services.service_manager`; this masks broken references instead of removing them. `src/cli/commands/command_router.py` also imports the same missing validation handler and currently fails module import. 
2. **Packaging contract mismatch.** `pyproject.toml` defines console scripts (`agent-cellphone-monitor`, `agent-cellphone-status`, etc.) pointing to module-level functions that do not exist in `src/agent_cellphone/cli.py` (they are class methods, not module exports). 
3. **Node/package metadata is broken at root.** `package.json` has trailing-comma invalid JSON, suggesting non-functional Node package tooling at repo root.
4. **CI gates are permissive and inconsistent.** `ci-cd.yml` uses broad `continue-on-error` and explicit “skip/echo warning” patterns for checks; `technical-debt-checks.yml` references missing `systems/technical_debt/weekly_debt_report.py`, and excludes a long list of Python files from syntax checks rather than forcing repair.
5. **Test contract weakness.** `tests/test_basic.py` is a placeholder always-true test, and `tests/test_import_validation.py` returns booleans instead of asserting, so import failures may not fail CI.
6. **Scaffold API not yet execution-real.** `apps/api/main.py` records run metadata but sets `test_output = "tests not run"` and static summary text, indicating non-executing task pipeline.
7. **Docs-to-implementation drift.** README reliability statements and architecture claims imply high operational certainty while implementation contains stub/fallback/deprecated pathways and soft CI behavior.

## Shipping Blockers
1. **Canonical entrypoint not settled (architecture blocker).** Competing launcher/control paths (`main.py`, `src.cli`, packaged CLI, swarm-console API) create ownership ambiguity.
2. **Merge gate lacks hard guarantees (process/CI blocker).** Non-blocking checks + missing referenced scripts reduce confidence in green pipelines.
3. **Broken distribution interface (code/release blocker).** Invalid `package.json` and miswired console scripts can break installation/runtime entry commands.
4. **Silent failure patterns (code quality blocker).** try/except fallbacks around missing imports and placeholder tests hide regressions.
5. **Scaffolded run execution path (scope blocker).** The swarm-console API is currently record-keeping oriented, not actually running validation/test execution.

## What To Kill / Freeze / Defer
- **Kill:** root Node package surface unless actively required; if retained, repair JSON and define actual scripts/dependencies.
- **Freeze:** new CLI surfaces until one canonical operational interface is chosen (recommend: keep `main.py` operational lane first, treat others as adapters).
- **Freeze:** new workflow additions in `.github/workflows/archive` and non-critical “meta-quality” jobs until existing gates are hardened.
- **Defer:** broad architecture re-org of `src/core`/`src/services`; first enforce import/test/CI integrity, then prune abstractions.
- **Defer:** feature expansion in swarm-console API/UI until task execution is real (test run + command execution + robust error model).

## What To Build Next
**Primary lane: Runtime and merge-gate closure (single lane only).**

1. **Entrypoint consolidation contract** (owner + ADR): choose canonical runtime interface, mark others as compatibility shims.
2. **Remove dead imports and fix broken handlers**: eliminate `src.core.service_manager` and missing validation-handler references from active paths.
3. **Repair release interfaces**: fix `pyproject` console scripts and root `package.json` validity.
4. **Harden CI to fail on real regressions**: remove or narrow `continue-on-error`; eliminate references to missing scripts; reduce syntax-check exclusion list.
5. **Replace placeholder tests with assertive checks**: convert smoke/import tests into hard assertions that fail on import/runtime breakage.
6. **Upgrade swarm-console from scaffold to executor**: replace static `test_output`/summary with actual command+test execution telemetry.

**Why this order:** each step reduces false-green signals and converges to a trustworthy shipping baseline before deeper refactors.

## 30-Day Execution Plan
### Week 1 — Control-surface closure
- Decide and document canonical operational entrypoint.
- Remove dead CLI imports and non-resolving handler references.
- Exit criterion: one documented command surface that boots and reports status reliably.

### Week 2 — Gate reliability closure
- Harden CI workflows: fail on missing scripts, remove silent skip patterns for mandatory checks.
- Align `pytest` config source (single config authority) and enforce assertive smoke/import tests.
- Exit criterion: PR pipeline failure accurately reflects breakage.

### Week 3 — Packaging and distribution closure
- Fix console script exports and package metadata contracts.
- Validate install + command invocation path in clean env.
- Exit criterion: packaged CLI commands resolve and execute deterministically.

### Week 4 — Execution-path closure
- Promote swarm-console API from scaffold to real task execution/evidence pipeline.
- Add minimum integration tests covering run creation, test execution capture, and failure propagation.
- Exit criterion: end-to-end run includes real command/test results and fails loudly on errors.

## Evidence Appendix
- `README.md` — Reliability and architecture claims; main entrypoint narrative; V2 standards framing. 
- `docs/START_HERE.md` — Onboarding path still centered on `main.py` service lifecycle. 
- `main.py` — Active launcher flow plus dead/missing import fallback and command dispatch behavior. 
- `src/cli/argument_parser.py` — Real command normalization contract for `main.py`.
- `src/cli/__main__.py` — Separate unified CLI path, parallel to `main.py`.
- `src/core/cli/__main__.py` and `src/services/cli/__main__.py` — Deprecated shims redirecting to unified CLI.
- `src/cli/commands/command_router.py` — Import dependency on missing validation handler.
- `src/services/service_manager.py` — Runtime lifecycle manager; placeholder foreground run notes and Windows-specific stop handling.
- `src/agent_cellphone/cli.py` — Hardcoded/demo CLI outputs and method-based command implementations.
- `pyproject.toml` — Console script mapping and packaging metadata.
- `package.json` — Invalid JSON structure at root.
- `apps/api/main.py` — Scaffolded run recording flow (`tests not run`, static summary).
- `apps/api/README.md`, `apps/ui/README.md`, `scripts/run_swarm_console_api.sh`, `scripts/run_swarm_console_ui.sh` — swarm-console runtime and operation model.
- `.github/workflows/ci-cd.yml` — Soft-fail quality/test behavior and optional-check patterns.
- `.github/workflows/technical-debt-checks.yml` — Missing-script reference and large syntax-check exclusion list.
- `tests/test_basic.py`, `tests/test_import_validation.py` — Placeholder/non-assertive baseline tests.
