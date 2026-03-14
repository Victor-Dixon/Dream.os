import json
from pathlib import Path

from scripts.build_knowledge_graph import GraphPaths, build_graph
from scripts.snapshot_diff_summary import generate_markdown


def test_build_graph_includes_known_module_and_registry_link(tmp_path: Path):
    output_path = tmp_path / "graph.json"
    graph = build_graph(
        GraphPaths(
            snapshots_dir=Path("tests/snapshots"),
            output_file=output_path,
            repo_root=Path("."),
        )
    )

    module = next(node for node in graph["nodes"] if node["id"] == "module:src/core/__init__.py")
    assert module["type"] == "Module"
    assert module["has_syntax_error"] is False

    registered_edges = [edge for edge in graph["edges"] if edge["type"] == "REGISTERED"]
    assert any(edge["source"] == "module:src/core/config_ssot.py" for edge in registered_edges)


def test_generate_markdown_detects_function_changes():
    old_graph = {
        "nodes": [
            {"id": "module:pkg/a.py", "type": "Module", "sha256": "1", "has_syntax_error": False},
            {
                "id": "function:pkg/a.py::foo",
                "type": "Function",
                "name": "foo",
                "signature": "(args=1, kwonly=0, defaults=0, async=False)",
            },
        ],
        "edges": [{"source": "module:pkg/a.py", "target": "function:pkg/a.py::foo", "type": "DEFINES"}],
    }
    new_graph = {
        "nodes": [
            {"id": "module:pkg/a.py", "type": "Module", "sha256": "2", "has_syntax_error": False},
            {
                "id": "function:pkg/a.py::foo",
                "type": "Function",
                "name": "foo",
                "signature": "(args=2, kwonly=0, defaults=0, async=False)",
            },
            {
                "id": "function:pkg/a.py::bar",
                "type": "Function",
                "name": "bar",
                "signature": "(args=0, kwonly=0, defaults=0, async=False)",
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
