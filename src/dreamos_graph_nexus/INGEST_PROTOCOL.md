# Graph Nexus Ingest Protocol
1. Project Scanner JSON is the SSOT for structural nodes.
2. Node IDs hash: type + path + canonical identity (sha256 hex).
3. Required node types: file, symbol, module, entrypoint.
4. Required edge types: contains, belongs_to, declares.
5. File metadata stored: language, size, hash, sha256, md5, mtime, line_count, loc.
6. Metadata must exclude full file contents.
7. Paths normalize to forward slashes and relative when possible.
8. Deterministic ordering by node_id/edge_id before persistence.
9. Scanner output is not re-parsed for structure.
10. Graph storage uses sqlite nodes/edges tables with schema_version.
