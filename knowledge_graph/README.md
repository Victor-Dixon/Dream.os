# Knowledge Graph Snapshot Integration

This directory contains a versioned knowledge graph derived from lockdown snapshots.

## Schema (node + edge JSON)

Top-level file: `knowledge_graph/latest.json`

- `nodes` contain:
  - `Module`: `path`, `sha256`, `has_syntax_error`
  - `Function`: `module`, `name`, `signature`, `decorators`
  - `Class`: `module`, `name`, `bases`, `methods`
  - `RegistryEntry`: `registry_id`, `path`
- `edges` contain:
  - `DEFINES`: `Module -> Function|Class`
  - `INHERITS`: `Class -> Class` (best-effort by base name)
  - `IMPORTS`: `Module -> Module` (optional, when built with `--include-imports`)
  - `REGISTERED`: `Module -> RegistryEntry`

## Build graph

```bash
python scripts/build_knowledge_graph.py --repo-root . --output knowledge_graph/latest.json --include-imports
```

## Diff summary

```bash
python scripts/snapshot_diff_summary.py \
  --old-graph knowledge_graph/base.json \
  --new-graph knowledge_graph/latest.json \
  --output knowledge_graph/diff_summary.md
```

## Query examples

```bash
python scripts/graph_query.py --syntax-errors
python scripts/graph_query.py --missing-from-registry
python scripts/graph_query.py --dependents src/core/error_handling.py
```
