# Lockdown Audit: Batches 004-013

## Scope
- Batches: 004 through 013 (`batches/batch_004_paths.txt` ... `batches/batch_013_paths.txt`).
- Lockdown artifacts: module contract snapshot + SSOT registry coverage snapshot.

## Findings
- Total unique files in scope: **480**.
- Files present in SSOT (`docs/recovery/recovery_registry.yaml`): **5**.
- Files missing from SSOT: **475** (captured in snapshot).
- Files missing from disk: **0**.
- Files with syntax errors under Python AST parse: **32** (current behavior locked via snapshot).

## Notes
- The contract snapshot intentionally captures current parser outcomes for every file in scope, including non-Python files and syntax-error states.
- No automatic quarantining/deprecation move was performed in this PR.
- Snapshot failures in future changes should be treated as explicit contract drift requiring review and re-baselining.

## Snapshot Artifacts
- `tests/snapshots/batch_004_013_module_contracts.json`
- `tests/snapshots/batch_004_013_registry_coverage.json`

## Syntax-Error Files
- `src/core/auto_gas_pipeline_system.py`
- `src/core/caching/intelligent_cache.py`
- `src/core/debate_to_gas_integration.py`
- `src/core/message_queue/core/processor.py`
- `src/core/unified_service_base.py`
- `tools/development/repository-navigator/__mocks__/vscode.js`
- `tools/development/repository-navigator/coverage/lcov-report/block-navigation.js`
- `tools/development/repository-navigator/coverage/lcov-report/prettify.js`
- `tools/development/repository-navigator/coverage/lcov-report/sorter.js`
- `tools/development/repository-navigator/jest.config.js`
- `tools/development/repository-navigator/out/completionProvider.js`
- `tools/development/repository-navigator/out/extension.js`
- `tools/development/repository-navigator/out/importPathProvider.js`
- `tools/development/repository-navigator/out/metadataReader.js`
- `tools/development/repository-navigator/out/treeDataProvider.js`
- `tools/development/repository-navigator/out/types.js`
- `tools/development/repository-navigator/src/completionProvider.ts`
- `tools/development/repository-navigator/src/extension.ts`
- `tools/development/repository-navigator/src/importPathProvider.ts`
- `tools/development/repository-navigator/src/metadataReader.ts`
- `tools/development/repository-navigator/src/treeDataProvider.ts`
- `tools/development/repository-navigator/src/types.ts`
- `tools/development/repository-navigator/test/runTest.ts`
- `tools/development/repository-navigator/test/suite/e2e/workflow.e2e.test.ts`
- `tools/development/repository-navigator/test/suite/index.ts`
- `tools/development/repository-navigator/test/suite/integration/extension.integration.test.ts`
- `tools/development/repository-navigator/test/suite/unit/completionProvider.test.ts`
- `tools/development/repository-navigator/test/suite/unit/extension.test.ts`
- `tools/development/repository-navigator/test/suite/unit/importPathProvider.test.ts`
- `tools/development/repository-navigator/test/suite/unit/metadataReader.test.ts`
- `tools/development/repository-navigator/test/suite/unit/treeDataProvider.test.ts`
- `tools/github/github_manager.py`
