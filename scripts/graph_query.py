# Header-Variant: line
# Owner: Dream.os Platform
# Purpose: Query the generated knowledge graph.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-graph-query

"""Simple query interface for knowledge_graph/latest.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _node_map(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {n["id"]: n for n in graph.get("nodes", []) if "id" in n}


def _syntax_errors(graph: dict[str, Any]) -> list[str]:
    out = []
    for node in graph.get("nodes", []):
        if node.get("type") == "Module" and node.get("has_syntax_error"):
            out.append(node.get("path", node.get("id", "<unknown>")))
    return sorted(out)


def _missing_from_registry(graph: dict[str, Any]) -> list[str]:
    nodes = _node_map(graph)
    registered: set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") != "REGISTERED":
            continue
        mod = nodes.get(edge.get("source"))
        if mod and mod.get("type") == "Module" and mod.get("path"):
            registered.add(mod["path"])
    modules = sorted(
        node.get("path")
        for node in graph.get("nodes", [])
        if node.get("type") == "Module" and node.get("path")
    )
    return [m for m in modules if m not in registered]


def _dependents(graph: dict[str, Any], module_path: str) -> list[str]:
    nodes = _node_map(graph)
    target_id = f"module:{module_path}"
    if target_id not in nodes:
        return []
    return sorted(
        nodes[edge.get("source", "")].get("path", "")
        for edge in graph.get("edges", [])
        if edge.get("type") == "IMPORTS"
        and edge.get("target") == target_id
        and nodes.get(edge.get("source", ""), {}).get("type") == "Module"
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query knowledge graph")
    parser.add_argument("--graph", type=Path, default=Path("knowledge_graph/latest.json"))
    parser.add_argument("--syntax-errors", action="store_true")
    parser.add_argument("--missing-from-registry", action="store_true")
    parser.add_argument("--dependents", type=str)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    graph = _load_graph(args.graph)

    if args.syntax_errors:
        print("\n".join(_syntax_errors(graph)))
    if args.missing_from_registry:
        print("\n".join(_missing_from_registry(graph)))
    if args.dependents:
        print("\n".join(_dependents(graph, args.dependents)))

    if not (args.syntax_errors or args.missing_from_registry or args.dependents):
        print("No query provided. Use --help.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
