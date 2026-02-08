# Graph Nexus Ingest Protocol
1. Project Scanner JSON is the SSOT for structural nodes.
2. Node IDs hash: type + path + signature (sha256 hex).
3. Required node types: file, symbol, module, entrypoint.
4. Required edge types: contains, belongs_to, declares.
5. Metadata must exclude full file contents.
6. Paths normalize to forward slashes and relative when possible.
7. Deterministic ordering by node_id/edge_id before persistence.
8. Scanner output is not re-parsed for structure.
9. Graph storage uses sqlite nodes/edges tables.
