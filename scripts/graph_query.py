# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Query helper for knowledge graph inspection.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-graph-query

"""Run ad-hoc queries against a generated knowledge graph.

Usage examples:
    python scripts/graph_query.py --graph knowledge_graph/latest.json --list-syntax-errors
    python scripts/graph_query.py --graph knowledge_graph/latest.json --find-module src/core/error_handling.py
    python scripts/graph_query.py --graph knowledge_graph/latest.json --registry-gaps
    python scripts/graph_query.py --graph knowledge_graph/latest.json --dependents src/core/error_handling.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query knowledge graph")
    parser.add_argument(
        "--graph",
        type=Path,
        default=Path("knowledge_graph/latest.json"),
        help="Path to generated knowledge graph JSON.",
    )
    parser.add_argument("--list-syntax-errors", action="store_true")
    parser.add_argument("--find-module", help="Exact module path")
    parser.add_argument("--registry-gaps", action="store_true")
    parser.add_argument("--dependents", help="Show modules importing this module path")
    return parser.parse_args()


def _module_nodes(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        node["id"]: node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("type") == "Module" and "id" in node
    }


def _module_node_by_path(graph: dict[str, Any], module_path: str) -> dict[str, Any] | None:
    target_id = f"module:{module_path}"
    return _module_nodes(graph).get(target_id)


def _registered_module_ids(graph: dict[str, Any]) -> set[str]:
    registered: set[str] = set()
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("type") == "REGISTERED" and isinstance(edge.get("source"), str):
            registered.add(edge["source"])
    return registered


def _query_syntax_errors(graph: dict[str, Any]) -> list[str]:
    modules = _module_nodes(graph)
    return sorted(
        node["path"]
        for node in modules.values()
        if isinstance(node.get("path"), str) and node.get("has_syntax_error")
    )


def _query_registry_gaps(graph: dict[str, Any]) -> list[str]:
    modules = _module_nodes(graph)
    registered = _registered_module_ids(graph)
    return sorted(
        node["path"]
        for module_id, node in modules.items()
        if module_id not in registered
        and isinstance(node.get("path"), str)
        and node["path"].endswith(".py")
    )


def _query_dependents(graph: dict[str, Any], module_path: str) -> list[str]:
    target_id = f"module:{module_path}"
    dependents: set[str] = set()

    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("type") != "IMPORTS":
            continue
        if edge.get("target") != target_id:
            continue

        source = edge.get("source")
        if isinstance(source, str) and source.startswith("module:"):
            dependents.add(source.removeprefix("module:"))

    return sorted(dependents)


def main() -> int:
    args = _parse_args()
    graph = _load_graph(args.graph)

    did_query = False

    if args.list_syntax_errors:
        did_query = True
        paths = _query_syntax_errors(graph)
        print("\n".join(paths) if paths else "No syntax errors detected.")

    if args.find_module:
        did_query = True
        module = _module_node_by_path(graph, args.find_module)
        if module is None:
            print(f"Module not found: {args.find_module}")
            return 1
        print(json.dumps(module, indent=2))

    if args.registry_gaps:
        did_query = True
        gaps = _query_registry_gaps(graph)
        print("\n".join(gaps) if gaps else "No registry gaps detected.")

    if args.dependents:
        did_query = True
        dependents = _query_dependents(graph, args.dependents)
        print("\n".join(dependents) if dependents else "No dependents found.")

    if not did_query:
        print("No query option selected. Use --help.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())