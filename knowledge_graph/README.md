````md
# Knowledge Graph for Snapshot Review

This directory stores lightweight, review-oriented metadata for snapshot graph generation.

The full graph is generated on demand and should not be committed when it creates large diffs. Commit the compact SSOT-facing artifact instead of large generated dumps.

## Files

- `latest.json`: current generated graph from `tests/snapshots/*` and `docs/recovery/recovery_registry.yaml`
- `latest_manifest.json`: compact manifest containing snapshot hashes and graph hash for review/SSOT tracking
- `latest.local.json`: optional local-only generated graph artifact for ad hoc inspection

## Schema

The generated graph is stored with:

- `metadata`: generation metadata and totals
- `nodes`: list of typed nodes
- `edges`: list of typed relationships

### Node types

- `Module`
  - `path`: Python module path
  - `sha256`: hash captured in module contract snapshot
  - `has_syntax_error`: whether the module failed AST parsing in the snapshot
- `Function`
  - `name`, `signature`, `decorators`, `module_path`
- `Class`
  - `name`, `bases`, `methods`, `module_path`
- `RegistryEntry`
  - `path`: registry ID or mapped path

### Edge types

- `DEFINES`: Module → Function/Class
- `INHERITS`: Class → Class
- `IMPORTS`: Module → Module (optional; enabled with `--include-import-edges`)
- `REGISTERED`: Module → RegistryEntry

## Build the graph

```bash
python scripts/build_knowledge_graph.py \
  --snapshots-dir tests/snapshots \
  --registry docs/recovery/recovery_registry.yaml \
  --output knowledge_graph/latest.local.json
````

The command also writes a compact manifest at `knowledge_graph/latest_manifest.json`.

To generate the canonical checked-in graph instead:

```bash
python scripts/build_knowledge_graph.py \
  --snapshots-dir tests/snapshots \
  --registry docs/recovery/recovery_registry.yaml \
  --output knowledge_graph/latest.json
```

With optional import analysis:

```bash
python scripts/build_knowledge_graph.py \
  --snapshots-dir tests/snapshots \
  --registry docs/recovery/recovery_registry.yaml \
  --output knowledge_graph/latest.local.json \
  --include-import-edges
```

## Generate a diff summary

From local graph files:

```bash
python scripts/snapshot_diff_summary.py --old old.json --new new.json
```

From git refs:

```bash
python scripts/snapshot_diff_summary.py --base HEAD~1 --head HEAD
```

Fail CI when changed module paths are outside allowed prefixes:

```bash
python scripts/snapshot_diff_summary.py \
  --old old.json \
  --new new.json \
  --expected-prefix src/core/ \
  --fail-on-unexpected
```

## Query graph quickly

```bash
python scripts/graph_query.py --graph knowledge_graph/latest.json --list-syntax-errors
python scripts/graph_query.py --graph knowledge_graph/latest.json --registry-gaps
python scripts/graph_query.py --graph knowledge_graph/latest.json --find-module src/core/error_handling.py
```

```

## Notes

- This keeps the **registry-aware build path** from `main`.
- It preserves the **lightweight/local-artifact guidance** from the Codex branch.
- It removes the outdated schema block that conflicted with the node/edge model.

If you want, I can also give you the **git-ready final README diff** next.
```
