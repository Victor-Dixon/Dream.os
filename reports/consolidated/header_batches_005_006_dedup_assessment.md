# Header Compliance + Dedup Assessment (Batches 005 & 006)

## Scope
- Files reviewed: 100
- Inputs: `batches/batch_005_paths.txt`, `batches/batch_006_paths.txt`, file headers, and `docs/recovery/recovery_registry.yaml`.

## Header Compliance Outcome
- Added standardized header blocks to all files in batches 005 and 006:
  - `Header-Variant: full`
  - `Owner: @dreamos/platform`
  - `Purpose: <module> module.`
  - `SSOT` and `@registry` pointers

## Duplicate Logic Candidates (Header + Structure Signals)
- **src/core/message_queue/core/processor.py** ↔ **src/core/message_queue_processor/core/processor.py**: parallel processor implementations. Recommendation: consolidate into one SSOT implementation and make the other a thin compatibility wrapper before removal.
- **src/core/service_base.py** ↔ **src/core/unified_service_base.py**: competing base service abstractions. Recommendation: consolidate into one SSOT implementation and make the other a thin compatibility wrapper before removal.
- **src/core/managers/monitoring/metric_manager.py** ↔ **src/core/managers/monitoring/metrics_manager.py**: singular/plural monitoring metric manager split. Recommendation: consolidate into one SSOT implementation and make the other a thin compatibility wrapper before removal.
- **tools/utilities/registry.py** ↔ **tools/utilities/project_inventory_catalog.py**: overlapping inventory and registry responsibilities. Recommendation: consolidate into one SSOT implementation and make the other a thin compatibility wrapper before removal.

## Duplicate Filename Groups (likely overlap)
- `__init__.py`:
  - `src/core/intelligent_context/unified_intelligent_context/__init__.py`
  - `src/core/managers/__init__.py`
  - `src/core/managers/adapters/__init__.py`
  - `src/core/managers/domains/__init__.py`
  - `src/core/managers/execution/__init__.py`
  - `src/core/managers/monitoring/__init__.py`
- `processor.py`:
  - `src/core/message_queue/core/processor.py`
  - `src/core/message_queue_processor/core/processor.py`

## Unnecessary File Candidates (post-consolidation)
- Candidate removals should only happen **after** call-site migration + tests:
  - `src/core/message_queue_processor/core/processor.py` (likely removable if superseded by pair primary file)
  - `src/core/unified_service_base.py` (likely removable if superseded by pair primary file)
  - `src/core/managers/monitoring/metrics_manager.py` (likely removable if superseded by pair primary file)
  - `tools/utilities/project_inventory_catalog.py` (likely removable if superseded by pair primary file)

## Structural Placement Recommendations
- Keep runtime orchestration SSOT under `src/core/` and reserve `tools/` for operator scripts only.
- For manager stack, converge monitoring responsibilities to one metrics manager module under `src/core/managers/monitoring/`.
- For queue processing, keep one canonical processor path (`src/core/message_queue/core/processor.py`) and deprecate alias path(s).
- For inventory/registry scripts, keep one catalog SSOT in `tools/utilities/project_inventory_catalog.py` and convert `tools/utilities/registry.py` into compatibility facade or retire it.

## Next SSOT Actions
1. Mark secondary files with deprecation header comments and migration targets.
2. Update imports/call-sites to canonical modules.
3. Remove legacy-retired files after one release cycle and validation sweep.
