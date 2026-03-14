# Graph Nexus Ingestion Gap Report

## Executive Summary (5 bullets max)
- The current ingestion persists graph nodes/edges with deterministic IDs, but only for
  structural relationships (contains/belongs_to/declares). (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L19-L105)
- Ingestion commits nodes and edges in separate transactions, so partial writes are
  possible if one step fails. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59,
  src/dreamos_graph_nexus/store/graph_repository.py:L85-L141)
- Deletion/rename handling is absent; only upserts exist, so stale nodes/edges can
  accumulate across runs. (src/dreamos_graph_nexus/store/graph_repository.py:L85-L142,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59)
- Canonical symbol identity is implemented, but it depends on path normalization and
  optional scope/signature fields that can change across scanner formats. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L162-L175,
  src/dreamos_graph_nexus/ingest/ingest_utils.py:L51-L62,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L248-L259)
- Schema versioning exists as a table insert only; no migrations or evolution flow is
  implemented. (src/dreamos_graph_nexus/store/graph_repository.py:L61-L83)

## What exists today (with file cites)

### Confirmed
- Graph models define nodes/edges and their fields. (src/dreamos_graph_nexus/models.py:L9-L38)
- Edge types currently defined: contains, belongs_to, declares. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L24-L26)
- Edge insertion occurs only for contains (file -> symbol), belongs_to (file -> module),
  and declares (file -> entrypoint). (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L82-L105)
- File metadata persisted is limited to a fixed set including hash fields. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L28-L36,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L234-L240)
- Node IDs use sha256 of namespace + parts and symbol identity uses name/kind/scope or
  signature. (src/dreamos_graph_nexus/ingest/ingest_utils.py:L24-L62,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L248-L259)
- Schema includes nodes, edges, and schema_version tables. (src/dreamos_graph_nexus/store/graph_repository.py:L37-L69)
- CLI supports indexing and indicates incremental mode is not implemented. (src/dreamos_graph_nexus/cli.py:L20-L71)

### Inferred
- Ingestion is not atomic because node and edge upserts are committed in separate
  connections. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59,
  src/dreamos_graph_nexus/store/graph_repository.py:L85-L141)
- Cross-language normalization is minimal: symbol kinds are derived from keys and
  language is only stored at the file level. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L189-L205,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L28-L36)

### Missing (not present in code)
- Semantic edges such as imports, calls, depends_on, routes_to, inherits, overrides,
  references are not defined or emitted. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L24-L26,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L82-L105)
- Deletion or rename handling is not implemented (no delete APIs, no sweep/mark).
  (src/dreamos_graph_nexus/store/graph_repository.py:L85-L142,
  src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59)
- Migration logic beyond schema_version initialization is not implemented.
  (src/dreamos_graph_nexus/store/graph_repository.py:L61-L83)

## Gap list (prioritized, with impact)

1. **P0: Missing semantic edges (imports/calls/depends_on/routes_to/inherits/overrides/references).**
   Impact: Without these edges, graph queries are limited to structure and cannot power
   dependency analysis or impact queries. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L24-L26,
   src/dreamos_graph_nexus/ingest/from_project_scanner.py:L82-L105)

2. **P0: No deletion/rename strategy (DB can only grow).**
   Impact: Stale nodes/edges persist across runs, so the graph drifts from reality.
   (src/dreamos_graph_nexus/store/graph_repository.py:L85-L142,
   src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59)

3. **P1: Non-transactional ingest.**
   Impact: Partial writes can leave dangling edges or missing nodes if ingest fails
   between commits. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L51-L59,
   src/dreamos_graph_nexus/store/graph_repository.py:L85-L141)

4. **P1: Schema evolution is not defined beyond schema_version=1.**
   Impact: Future schema changes will require ad-hoc changes and risk breaking existing
   databases. (src/dreamos_graph_nexus/store/graph_repository.py:L61-L83)

5. **P2: Cross-language normalization contract is incomplete.**
   Impact: Symbol identity depends on scanner-specific fields and lacks language-aware
   normalization, risking ID churn across scanner versions. (src/dreamos_graph_nexus/ingest/ingest_utils.py:L51-L62,
   src/dreamos_graph_nexus/ingest/from_project_scanner.py:L189-L205)

## Proposed upgrade plan (Stage 1/2/3)

### Stage 1 (MVP to unlock relationship queries)
- **Add semantic edge ingestion** from scanner JSON (imports/calls/depends_on/routes_to/
  inherits/overrides/references) and store as edges. (GNX-001)
- **Add single-transaction ingest** path that upserts nodes+edges within one connection
  and rolls back on failure. (GNX-002)
- **Define a normalization contract** for symbol identity that includes language/kind/scope
  and add it to ingest docs. (GNX-003)

### Stage 2 (Graph correctness over time)
- **Add ingest_run tracking + mark/sweep** for deletions and soft deletes. (GNX-004)
- **Rename/move detection** using file hash metadata to link old path to new path. (GNX-005)
- **Add schema migration scaffolding** with versioned migration steps. (GNX-006)

### Stage 3 (Hardening + performance)
- **Add edge-level validation** to prevent dangling references before commit. (GNX-007)
- **Add regression tests** for semantic edges, deletions, and transactions. (GNX-008)

## Migration + backward compatibility
- Current schema_version is initialized at 1 with no migration flow. (src/dreamos_graph_nexus/store/graph_repository.py:L61-L83)
- Introducing ingest_run tracking or soft deletes should add new nullable columns or
  companion tables to avoid breaking older DBs. (Proposed: GNX-004/GNX-006)
- Adding semantic edges is backward compatible since edge_type is already a free-form
  string; existing consumers must tolerate new edge types. (src/dreamos_graph_nexus/store/graph_repository.py:L51-L57)
- Rename detection based on file hash should be optional if hash is absent to avoid
  blocking ingestion. (src/dreamos_graph_nexus/ingest/from_project_scanner.py:L28-L36)

## Test plan (what proves it works)
- **Semantic edge ingestion test**: fixture with imports/calls/etc and assert edge types.
  (Targets: GNX-001)
- **Transactional ingest test**: force an edge insert failure and assert no nodes/edges
  are persisted. (Targets: GNX-002)
- **Deletion/rename test**: ingest two runs with removed/renamed file and assert soft
  deletion or rename edge. (Targets: GNX-004/GNX-005)
- **Schema migration test**: start with version 1 DB and apply migration to version 2,
  then validate schema_version bump. (Targets: GNX-006)
