"""Tests for knowledge graph build and diff tooling."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)


def test_build_knowledge_graph_smoke(tmp_path: Path) -> None:
    output = tmp_path / "graph.json"
    _run(
        [
            "python",
            "scripts/build_knowledge_graph.py",
            "--repo-root",
            ".",
            "--output",
            str(output),
        ]
    )
    graph = json.loads(output.read_text(encoding="utf-8"))
    assert "nodes" in graph and "edges" in graph
    assert any(node.get("type") == "Module" for node in graph["nodes"])
    assert any(node.get("type") == "RegistryEntry" for node in graph["nodes"])


def test_snapshot_diff_summary_smoke(tmp_path: Path) -> None:
    old_graph = tmp_path / "old.json"
    new_graph = tmp_path / "new.json"
    report = tmp_path / "report.md"

    _run(["python", "scripts/build_knowledge_graph.py", "--repo-root", ".", "--output", str(old_graph)])
    _run(
        [
            "python",
            "scripts/build_knowledge_graph.py",
            "--repo-root",
            ".",
            "--output",
            str(new_graph),
            "--include-imports",
        ]
    )
    _run(
        [
            "python",
            "scripts/snapshot_diff_summary.py",
            "--old-graph",
            str(old_graph),
            "--new-graph",
            str(new_graph),
            "--output",
            str(report),
        ]
    )
    text = report.read_text(encoding="utf-8")
    assert "## Snapshot Graph Diff Summary" in text
    assert "### Overview" in text
