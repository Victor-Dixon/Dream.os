# Lockdown Audit: Batches 001-003

- Scope: `batches/batch_001_paths.txt`, `batches/batch_002_paths.txt`, `batches/batch_003_paths.txt`.
- Total files audited: **150**.
- Files present in recovery registry: **1**.
- Files missing from recovery registry: **149** (captured in snapshot).
- Files with syntax errors: **3** (current behavior locked via snapshot).
- Dead code quarantine: no files moved to `deprecated/` in this pass; static AST/caller certainty was insufficient for safe automated quarantine.

## Syntax-error modules (locked as-is)
- `src/core/engines/validation_core_engine.py`
- `src/core/error_handling.py`
- `src/core/gas_pipeline/core/__init__.py`

## Registry gaps (needs follow-up)
See `tests/snapshots/batch_001_003_registry_coverage.json` for full list.
