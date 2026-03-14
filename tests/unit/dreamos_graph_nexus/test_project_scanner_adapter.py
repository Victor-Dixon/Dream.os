"""Tests for Project Scanner adapter ingestion."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from src.dreamos_graph_nexus.ingest.from_project_scanner import ProjectScannerAdapter
from src.dreamos_graph_nexus.store.graph_repository import GraphRepository

FIXTURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "graph_nexus"
    / "scanner_fixture.json"
)


def test_scanner_fixture_ingest(tmp_path: Path) -> None:
    """Ensure scanner fixture produces expected nodes and edges."""
    db_path = tmp_path / "graph.sqlite"
    repository = GraphRepository(db_path)
    adapter = ProjectScannerAdapter(project_root=tmp_path)

    result = adapter.ingest(FIXTURE_PATH, repository)
    assert result.node_count == 7
    assert result.edge_count == 5

    with sqlite3.connect(db_path) as conn:
        node_rows = conn.execute(
            "SELECT node_type, COUNT(*) FROM nodes GROUP BY node_type"
        ).fetchall()
        edge_rows = conn.execute(
            "SELECT edge_type, COUNT(*) FROM edges GROUP BY edge_type"
        ).fetchall()

    node_counts = {row[0]: row[1] for row in node_rows}
    edge_counts = {row[0]: row[1] for row in edge_rows}

    assert node_counts.get("file") == 2
    assert node_counts.get("symbol") == 3
    assert node_counts.get("module") == 1
    assert node_counts.get("entrypoint") == 1

    assert edge_counts.get("contains") == 3
    assert edge_counts.get("belongs_to") == 1
    assert edge_counts.get("declares") == 1
