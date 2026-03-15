"""Tests for snapshot knowledge graph tooling."""

from __future__ import annotations

import json
from pathlib import Path

from scripts.build_knowledge_graph import GraphPaths, build_graph, write_manifest
from scripts.snapshot_diff_summary import generate_markdown


ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS_DIR = ROOT / "tests" / "snapshots"
REGISTRY_PATH = ROOT / "docs" / "recovery" / "recovery_registry.yaml"


def test_build_graph_includes_known_module_and_registry_link(tmp_path: Path) -> None:
    output_path = tmp_path / "graph.json"
    manifest_path = tmp_path / "manifest.json"

    paths = GraphPaths(
        snapshots_dir=SNAPSHOTS_DIR,
        output_file=output_path,
        repo_root=ROOT,
        registry_file=REGISTRY_PATH,
        manifest_file=manifest_path,
    )

    graph = build_graph(paths)
    write_manifest(graph, paths)

    module = next(node for node in graph["nodes"] if node["id"] == "module:src/core/__init__.py")
    assert module["type"] == "Module"
    assert module["has_syntax_error"] is False

    registered_edges = [edge for edge in graph["edges"] if edge["type"] == "REGISTERED"]
    assert any(edge["source"] == "module:src/core/config_ssot.py" for edge in registered_edges)

    assert manifest_path.exists()

    first_manifest = manifest_path.read_text(encoding="utf-8")
    write_manifest(graph, paths)
    second_manifest = manifest_path.read_text(encoding="utf-8")
    assert first_manifest == second_manifest


def test_generate_markdown_detects_function_changes() -> None:
    old_graph = {
        "nodes": [
            {
                "id": "module:pkg/a.py",
                "type": "Module",
                "path": "pkg/a.py",
                "sha256": "1",
                "has_syntax_error": False,
            },
            {
                "id": "function:pkg/a.py::foo",
                "type": "Function",
                "name": "foo",
                "module_path": "pkg/a.py",
                "signature": "(args=1, kwonly=0, defaults=0)",
            },
        ],
        "edges": [
            {"source": "module:pkg/a.py", "target": "function:pkg/a.py::foo", "type": "DEFINES"}
        ],
    }
    new_graph = {
        "nodes": [
            {
                "id": "module:pkg/a.py",
                "type": "Module",
                "path": "pkg/a.py",
                "sha256": "2",
                "has_syntax_error": False,
            },
            {
                "id": "function:pkg/a.py::foo",
                "type": "Function",
                "name": "foo",
                "module_path": "pkg/a.py",
                "signature": "(args=2, kwonly=0, defaults=0)",
            },
            {
                "id": "function:pkg/a.py::bar",
                "type": "Function",
                "name": "bar",
                "module_path": "pkg/a.py",
                "signature": "(args=0, kwonly=0, defaults=0)",
            },
        ],
        "edges": [
            {"source": "module:pkg/a.py", "target": "function:pkg/a.py::foo", "type": "DEFINES"},
            {"source": "module:pkg/a.py", "target": "function:pkg/a.py::bar", "type": "DEFINES"},
        ],
    }

    report = generate_markdown(old_graph, new_graph)
    assert "Added functions" in report
    assert "Signature changes" in report


def test_latest_graph_file_parses() -> None:
    path = ROOT / "knowledge_graph" / "latest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "metadata" in data
    assert "nodes" in data
    assert "edges" in data