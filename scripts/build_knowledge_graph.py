#!/usr/bin/env python3
"""Build a lightweight knowledge graph from snapshot artifacts."""

from __future__ import annotations

import argparse
import ast
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class GraphPaths:
    snapshots_dir: Path
    output_file: Path
    repo_root: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshots-dir",
        default="tests/snapshots",
        help="Directory containing batch snapshot JSON files.",
    )
    parser.add_argument(
        "--output",
        default="knowledge_graph/latest.json",
        help="Destination path for generated knowledge graph JSON.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root for optional import analysis.",
    )
    parser.add_argument(
        "--include-import-edges",
        action="store_true",
        help="Best-effort import edge extraction by parsing source files.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _signature_from_snapshot(function: Dict[str, Any]) -> str:
    return (
        f"(args={function.get('args', 0)}, kwonly={function.get('kwonly_args', 0)}, "
        f"defaults={function.get('defaults', 0)}, async={bool(function.get('async', False))})"
    )


def _module_node(module_path: str, sha256: str, syntax_error: bool) -> Dict[str, Any]:
    return {
        "id": f"module:{module_path}",
        "type": "Module",
        "path": module_path,
        "sha256": sha256,
        "has_syntax_error": syntax_error,
    }


def _function_node(module_path: str, function: Dict[str, Any]) -> Dict[str, Any]:
    function_name = function["name"]
    return {
        "id": f"function:{module_path}::{function_name}",
        "type": "Function",
        "name": function_name,
        "module_path": module_path,
        "signature": _signature_from_snapshot(function),
        "decorators": function.get("decorators", []),
    }


def _class_node(module_path: str, class_data: Dict[str, Any]) -> Dict[str, Any]:
    class_name = class_data["name"]
    return {
        "id": f"class:{module_path}::{class_name}",
        "type": "Class",
        "name": class_name,
        "module_path": module_path,
        "bases": class_data.get("bases", []),
        "methods": class_data.get("methods", []),
    }


def _registry_node(registry_path: str) -> Dict[str, Any]:
    return {
        "id": f"registry:{registry_path}",
        "type": "RegistryEntry",
        "path": registry_path,
    }


def _find_snapshot_files(snapshots_dir: Path) -> Tuple[List[Path], List[Path]]:
    module_contracts = sorted(snapshots_dir.glob("batch_*_module_contracts.json"))
    registry_coverage = sorted(snapshots_dir.glob("batch_*_registry_coverage.json"))
    return module_contracts, registry_coverage


def _load_contract_entries(paths: Iterable[Path]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    for path in paths:
        data = _load_json(path)
        if not isinstance(data, list):
            print(f"[WARN] Contract snapshot is not a list: {path}")
            continue
        entries.extend(item for item in data if isinstance(item, dict))
    return entries


def _load_registry_coverage(paths: Iterable[Path]) -> Tuple[Set[str], Set[str]]:
    in_registry: Set[str] = set()
    missing_from_registry: Set[str] = set()
    for path in paths:
        data = _load_json(path)
        if not isinstance(data, dict):
            print(f"[WARN] Registry snapshot is not a mapping: {path}")
            continue
        in_registry.update(data.get("in_registry", []))
        missing_from_registry.update(data.get("missing_from_registry", []))
    return in_registry, missing_from_registry


def _module_imports_from_source(repo_root: Path, module_paths: Set[str]) -> List[Tuple[str, str]]:
    imports_edges: List[Tuple[str, str]] = []
    module_by_stem = {
        path.replace("/", ".").removesuffix(".py"): path for path in module_paths if path.endswith(".py")
    }
    for module_path in sorted(module_paths):
        source_path = repo_root / module_path
        if not source_path.exists() or not module_path.endswith(".py"):
            continue
        try:
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        imports: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)
        for imported in imports:
            for segment_count in range(len(imported.split(".")), 0, -1):
                candidate = ".".join(imported.split(".")[:segment_count])
                target = module_by_stem.get(candidate)
                if target and target != module_path:
                    imports_edges.append((module_path, target))
                    break
    return sorted(set(imports_edges))


def build_graph(paths: GraphPaths, include_import_edges: bool = False) -> Dict[str, Any]:
    contracts_files, registry_files = _find_snapshot_files(paths.snapshots_dir)
    contract_entries = _load_contract_entries(contracts_files)
    in_registry, missing_from_registry = _load_registry_coverage(registry_files)

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Set[Tuple[str, str, str]] = set()
    module_paths: Set[str] = set()

    for entry in contract_entries:
        module_path = entry.get("file")
        sha256 = entry.get("sha256", "")
        if not module_path:
            print(f"[WARN] Skipping entry without file field: {entry}")
            continue
        module_paths.add(module_path)

        module_id = f"module:{module_path}"
        has_syntax_error = bool(entry.get("syntax_error"))
        nodes[module_id] = _module_node(module_path, sha256, has_syntax_error)

        if has_syntax_error:
            continue

        for function in entry.get("functions", []):
            if "name" not in function:
                print(f"[WARN] Function missing name in {module_path}: {function}")
                continue
            fn_node = _function_node(module_path, function)
            nodes[fn_node["id"]] = fn_node
            edges.add((module_id, fn_node["id"], "DEFINES"))

        classes_in_module = entry.get("classes", [])
        class_ids: Dict[str, str] = {}
        for class_data in classes_in_module:
            if "name" not in class_data:
                print(f"[WARN] Class missing name in {module_path}: {class_data}")
                continue
            cls_node = _class_node(module_path, class_data)
            nodes[cls_node["id"]] = cls_node
            class_ids[class_data["name"]] = cls_node["id"]
            edges.add((module_id, cls_node["id"], "DEFINES"))

        for class_data in classes_in_module:
            source_id = class_ids.get(class_data.get("name"))
            if not source_id:
                continue
            for base in class_data.get("bases", []):
                target_id = class_ids.get(base)
                if target_id:
                    edges.add((source_id, target_id, "INHERITS"))

    for registry_path in sorted(in_registry):
        reg_node = _registry_node(registry_path)
        nodes[reg_node["id"]] = reg_node
        module_id = f"module:{registry_path}"
        if module_id in nodes:
            edges.add((module_id, reg_node["id"], "REGISTERED"))
        else:
            print(f"[WARN] Registry entry has no matching module contract: {registry_path}")

    for missing in sorted(missing_from_registry):
        if f"module:{missing}" not in nodes:
            print(f"[WARN] Missing-from-registry path not found in contracts: {missing}")

    if include_import_edges:
        for source, target in _module_imports_from_source(paths.repo_root, module_paths):
            edges.add((f"module:{source}", f"module:{target}", "IMPORTS"))

    graph = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": "1.0.0",
            "source_snapshots": {
                "module_contracts": [str(p) for p in contracts_files],
                "registry_coverage": [str(p) for p in registry_files],
            },
            "totals": {
                "nodes": len(nodes),
                "edges": len(edges),
                "modules": len([n for n in nodes.values() if n["type"] == "Module"]),
                "functions": len([n for n in nodes.values() if n["type"] == "Function"]),
                "classes": len([n for n in nodes.values() if n["type"] == "Class"]),
                "registry_entries": len([n for n in nodes.values() if n["type"] == "RegistryEntry"]),
            },
        },
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [
            {"source": source, "target": target, "type": edge_type}
            for source, target, edge_type in sorted(edges)
        ],
    }
    return graph


def main() -> None:
    args = parse_args()
    paths = GraphPaths(
        snapshots_dir=Path(args.snapshots_dir),
        output_file=Path(args.output),
        repo_root=Path(args.repo_root),
    )
    graph = build_graph(paths, include_import_edges=args.include_import_edges)
    paths.output_file.parent.mkdir(parents=True, exist_ok=True)
    paths.output_file.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote graph with {len(graph['nodes'])} nodes to {paths.output_file}")


if __name__ == "__main__":
    main()
