#!/usr/bin/env python3
"""Ad-hoc query utility for Dream.os knowledge graph."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Set


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", default="knowledge_graph/latest.json", help="Path to graph JSON.")
    parser.add_argument("--dependents", help="Show modules importing this module path.")
    parser.add_argument("--missing-from-registry", action="store_true", help="Show unregistered modules.")
    parser.add_argument("--syntax-errors", action="store_true", help="Show modules with syntax errors.")
    return parser.parse_args()


def _load_graph(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _module_nodes(graph: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    modules = {}
    for node in graph.get("nodes", []):
        if node.get("type") == "Module":
            modules[node["id"]] = node
    return modules


def _registered_module_ids(graph: Dict[str, Any]) -> Set[str]:
    registered: Set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") == "REGISTERED":
            registered.add(edge.get("source"))
    return registered


def query_dependents(graph: Dict[str, Any], module_path: str) -> List[str]:
    target_id = f"module:{module_path}"
    dependents: Set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") == "IMPORTS" and edge.get("target") == target_id:
            dependents.add(edge.get("source", "").replace("module:", "", 1))
    return sorted(v for v in dependents if v)


def query_missing_from_registry(graph: Dict[str, Any]) -> List[str]:
    modules = _module_nodes(graph)
    registered = _registered_module_ids(graph)
    return sorted(
        node["path"]
        for module_id, node in modules.items()
        if module_id not in registered and node.get("path", "").endswith(".py")
    )


def query_syntax_errors(graph: Dict[str, Any]) -> List[str]:
    modules = _module_nodes(graph)
    return sorted(node["path"] for node in modules.values() if node.get("has_syntax_error"))


def main() -> None:
    args = parse_args()
    graph = _load_graph(Path(args.graph))

    if args.dependents:
        for module in query_dependents(graph, args.dependents):
            print(module)
    if args.missing_from_registry:
        for module in query_missing_from_registry(graph):
            print(module)
    if args.syntax_errors:
        for module in query_syntax_errors(graph):
            print(module)

    if not any([args.dependents, args.missing_from_registry, args.syntax_errors]):
        print("No query selected. Use --help for options.")


if __name__ == "__main__":
    main()
