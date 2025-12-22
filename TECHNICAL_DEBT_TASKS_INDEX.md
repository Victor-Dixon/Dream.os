# Technical Debt Tasks Index

**Purpose:** Single place to see all technical-debt plans, reports, and task sources.

---

## 1. Master Plans & High-Level Strategy

- `docs/technical_debt/TECHNICAL_DEBT_REDUCTION_MASTER_PLAN.md`  
  High-level duplicate-file debt plan (categories A/B/C/D, execution strategy, metrics).

- `docs/analysis/messaging_template_texts_growth_analysis.md` (if present)  
  Context for the large messaging templates exception and future refactor plan.

- `docs/V2_COMPLIANCE_EXCEPTIONS.md`  
  Approved V2 size exceptions and remaining violations.

---

## 2. Current Analysis & Dashboards

- `docs/technical_debt/TECHNICAL_DEBT_ANALYSIS.json`  
  Latest consolidated technical-debt scan (markers, duplicates, consolidation opportunities).

- `docs/technical_debt/TECHNICAL_DEBT_ANALYSIS_REPORT.md`  
  Human-readable summary of markers by type/priority and top consolidation opportunities.

- *(Planned)* `docs/v2_compliance/V2_SIZE_DASHBOARD.md`  
  Weekly V2 size audit results (to be implemented).

- `docs/technical_debt/TECHNICAL_DEBT_DASHBOARD.md`  
  Weekly captain view: budget, cadence, key metrics, and current-cycle priorities.

---

## 3. Duplicate Files – Execution Artifacts

- `docs/technical_debt/DUPLICATE_ANALYSIS_REPORT.md` (if present)  
  Detailed grouping of duplicates discovered in earlier scans.

- `docs/technical_debt/DUPLICATE_RESOLUTION_LOG.md` (if present)  
  Log of which duplicates were deleted/merged, with before/after metrics.

- Tools:
  - `tools/technical_debt_analyzer.py`
  - `tools/enhanced_duplicate_detector.py`
  - `tools/compare_duplicate_files.py`
  - `tools/execute_duplicate_resolution.py`

---

## 4. V2 Compliance & Size Violations

- `docs/V2_COMPLIANCE_EXCEPTIONS.md`  
  Canonical list of files allowed to exceed normal V2 limits.

- `temp_v2_violations_report.txt`  
  Snapshot of remaining V2 violations and their sizes.

- *(Referenced)* `COMPREHENSIVE_V2_VIOLATION_REPORT_2025-12-14.md`  
  Detailed report for Critical/Major violations (500–1000+ lines).

- Tools:
  - `mcp_servers/v2_compliance_server.py`
  - `tools/` (V2 utilities, if present)

---

## 5. Task Sources & Assignment Docs

- `MASTER_TASK_LOG.md`  
  Central INBOX where technical-debt tasks are captured (see tech-debt section).

- `DELEGATION_BOARD.md`  
  Ownership mapping (Victor vs Swarm vs Family) for many of these tasks.

- `agent_workspaces/`  
  Per-agent workspaces where some technical-debt tasks and experiments live:
  - `agent_workspaces/Agent-2/…` – architecture/refactor work
  - `agent_workspaces/Agent-3/…` – testing/QA work

- `SWARM_TASK_PACKETS.md`  
  Swarm-ready directives derived from these technical-debt items (to be expanded).

---

## 6. How to Use This Index

1. **Start here** to locate the relevant *plan* and *report* for any technical-debt effort.  
2. Use `MASTER_TASK_LOG.md` to see which items are currently in the INBOX / THIS WEEK.  
3. Use `DELEGATION_BOARD.md` + `agent_workspaces/` to see **who** is supposed to execute.  
4. When adding new technical-debt docs or tools, **link them here** under the right section.


