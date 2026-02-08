"""SQLite-backed repository for graph nodes and edges."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from src.infrastructure.persistence.database_connection import DatabaseConnection
from src.infrastructure.persistence.persistence_models import PersistenceConfig

from ..models import GraphEdge, GraphNode


class GraphRepository:
    """Repository for persisting graph nodes and edges."""

    def __init__(self, db_path: Path, db_connection: DatabaseConnection | None = None):
        self.db_path = Path(db_path)
        self.db = db_connection or DatabaseConnection(
            PersistenceConfig(db_path=str(self.db_path))
        )

    def initialize_schema(self) -> None:
        """Ensure schema exists."""
        schema_queries = [
            """
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                node_type TEXT NOT NULL,
                name TEXT NOT NULL,
                path TEXT,
                signature TEXT,
                metadata_json TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS edges (
                edge_id TEXT PRIMARY KEY,
                edge_type TEXT NOT NULL,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                FOREIGN KEY(source_id) REFERENCES nodes(node_id),
                FOREIGN KEY(target_id) REFERENCES nodes(node_id)
            )
            """,
            "CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(node_type)",
            "CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type)",
        ]
        self.db.create_tables(schema_queries)

    def upsert_nodes(self, nodes: Iterable[GraphNode]) -> int:
        """Insert or update graph nodes."""
        node_rows = [
            (
                node.node_id,
                node.node_type,
                node.name,
                node.path,
                node.signature,
                json.dumps(node.metadata, sort_keys=True),
            )
            for node in nodes
        ]
        if not node_rows:
            return 0
        with self.db.get_connection() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO nodes (
                    node_id, node_type, name, path, signature, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                node_rows,
            )
            conn.commit()
        return len(node_rows)

    def upsert_edges(self, edges: Iterable[GraphEdge]) -> int:
        """Insert or update graph edges."""
        edge_rows = [
            (
                edge.edge_id,
                edge.edge_type,
                edge.source_id,
                edge.target_id,
                json.dumps(edge.metadata, sort_keys=True),
            )
            for edge in edges
        ]
        if not edge_rows:
            return 0
        with self.db.get_connection() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO edges (
                    edge_id, edge_type, source_id, target_id, metadata_json
                ) VALUES (?, ?, ?, ?, ?)
                """,
                edge_rows,
            )
            conn.commit()
        return len(edge_rows)
