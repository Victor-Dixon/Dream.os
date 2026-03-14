# Knowledge Graph for Snapshot Review

This directory stores lightweight, version-controlled metadata for snapshot graph generation.
The full graph is generated on demand and should not be committed when it creates large diffs.
`latest.json` is a small pointer file (not the full graph dump).

## Schema

The generated graph (local artifact) is stored in `latest.json` with:

- `metadata`: generation metadata and totals.
- `nodes`: list of typed nodes.
- `edges`: list of typed relationships.

### Node types

- `Module`
  - `path`: Python module path.
  - `sha256`: hash captured in module contract snapshot.
  - `has_syntax_error`: whether the module failed AST parsing in the snapshot.
- `Function`
  - `name`, `signature`, `decorators`, `module_path`.
- `Class`
  - `name`, `bases`, `methods`, `module_path`.
- `RegistryEntry`
  - `path` (registry ID/path).

### Edge types

- `DEFINES`: Module → Function/Class.
- `INHERITS`: Class → Class (within known class nodes).
- `IMPORTS`: Module → Module (optional; source parsing enabled with `--include-import-edges`).
- `REGISTERED`: Module → RegistryEntry.

## Generate graph

```bash
python scripts/build_knowledge_graph.py \
  --snapshots-dir tests/snapshots \
  --output knowledge_graph/latest.json
```

The command also writes a compact SSOT manifest at
`knowledge_graph/latest_manifest.json` containing snapshot hashes and graph hash.
Commit this manifest instead of committing large graph dumps.

With optional import analysis:

```bash
python scripts/build_knowledge_graph.py --include-import-edges
```

## Diff summary

Compare two graph files:

```bash
python scripts/snapshot_diff_summary.py path/to/old.json path/to/new.json
```

Or compare graph at two Git refs:

```bash
python scripts/snapshot_diff_summary.py --base-ref origin/main --head-ref HEAD
```

## Query examples

```bash
python scripts/graph_query.py --syntax-errors
python scripts/graph_query.py --missing-from-registry
python scripts/graph_query.py --dependents src/core/__init__.py
```
