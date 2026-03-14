# Knowledge Graph for Snapshot Review

This directory contains a lightweight, review-oriented graph generated from lockdown snapshots.

## Files

- `latest.json`: Current generated graph from `tests/snapshots/*` + `docs/recovery/recovery_registry.yaml`.

## Schema (high-level)

```json
{
  "meta": {
    "snapshot_dir": "tests/snapshots",
    "module_contract_sources": ["batch_001_003_module_contracts.json"],
    "registry_coverage_sources": ["batch_001_003_registry_coverage.json"],
    "total_modules": 150,
    "in_registry": 4,
    "syntax_error_modules": 0
  },
  "modules": {
    "src/core/error_handling.py": {
      "path": "src/core/error_handling.py",
      "sha256": "...",
      "has_syntax_error": false,
      "syntax_error": null,
      "functions": [],
      "classes": [],
      "in_registry": true,
      "registry_id": "core-error-handling-logger-shim",
      "batch": "batch_001_003"
    }
  },
  "registry_entries": {
    "core-error-handling-logger-shim": "src/core/error_handling.py"
  }
}
```

## Build the graph

```bash
python scripts/build_knowledge_graph.py \
  --snapshots-dir tests/snapshots \
  --registry docs/recovery/recovery_registry.yaml \
  --output knowledge_graph/latest.json
```

## Generate a diff summary

From local graph files:

```bash
python scripts/snapshot_diff_summary.py --old old.json --new new.json
```

From git refs (default graph path `knowledge_graph/latest.json`):

```bash
python scripts/snapshot_diff_summary.py --base HEAD~1 --head HEAD
```

Fail CI when changed module paths are outside allowed prefixes:

```bash
python scripts/snapshot_diff_summary.py \
  --old old.json --new new.json \
  --expected-prefix src/core/ \
  --fail-on-unexpected
```

## Query graph quickly

```bash
python scripts/graph_query.py --graph knowledge_graph/latest.json --list-syntax-errors
python scripts/graph_query.py --graph knowledge_graph/latest.json --registry-gaps
python scripts/graph_query.py --graph knowledge_graph/latest.json --find-module src/core/error_handling.py
```
