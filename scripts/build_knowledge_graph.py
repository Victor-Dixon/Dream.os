# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Build a review-oriented knowledge graph from lockdown snapshots.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-build-knowledge-graph

"""Build a consolidated knowledge graph from lockdown snapshot JSON files.

Usage:
    python scripts/build_knowledge_graph.py \
        --snapshots-dir tests/snapshots \
        --registry docs/recovery/recovery_registry.yaml \
        --output knowledge_graph/latest.json

Or:

    python scripts/build_knowledge_graph.py \
        --repo-root . \
        --output knowledge_graph/latest.json \
        --include-import-edges
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import yaml


@dataclass(frozen=True)
class GraphPaths:
    snapshots_dir: Path
    output_file: Path
    repo_root: Path
    registry_file: Optional[Path] = None
    manifest_file: Optional[Path] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshots-dir",
        type=Path,
        default=Path("tests/snapshots"),
        help="Directory containing batch snapshot JSON files.",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path("docs/recovery/recovery_registry.yaml"),
        help="Recovery registry YAML used to map files to registry IDs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("knowledge_graph/latest.local.json"),
        help="Destination path for generated knowledge graph JSON.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root for optional import analysis.",
    )
    parser.add_argument(
        "--manifest-out",
        type=Path,
        default=Path("knowledge_graph/latest_manifest.json"),
        help="Optional compact manifest path with input hashes and graph hash.",
    )
    parser.add_argument(
        "--include-import-edges",
        action="store_true",
        help="Best-effort import edge extraction by parsing source files.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry_map(registry_path: Path) -> tuple[dict[str, str], dict[str, str]]:
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    entries = data.get("files", [])
    if not isinstance(entries, list):
        raise ValueError("Recovery registry must define a top-level 'files' list")

    by_path: dict[str, str] = {}
    by_id: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        file_path = entry.get("file")
        entry_id = entry.get("id")
        if isinstance(file_path, str) and isinstance(entry_id, str):
            by_path[file_path] = entry_id
            by_id[entry_id] = file_path
    return by_path, by_id


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _signature_from_snapshot(function: Dict[str, Any]) -> str:
    async_prefix = "async " if function.get("async", False) else ""
    return (
        f"{async_prefix}(args={function.get('args', 0)}, "
        f"kwonly={function.get('kwonly_args', 0)}, "
        f"defaults={function.get('defaults', 0)})"
    )


def _module_node(
    module_path: str,
    sha256: str,
    syntax_error: bool,
    registry_id: Optional[str],
    in_registry: bool,
    batch_name: Optional[str],
) -> Dict[str, Any]:
    return {
        "id": f"module:{module_path}",
        "type": "Module",
        "path": module_path,
        "sha256": sha256,
        "has_syntax_error": syntax_error,
        "registry_id": registry_id,
        "in_registry": in_registry,
        "batch": batch_name,
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
        "lineno": function.get("lineno"),
    }


def _class_node(module_path: str, class_data: Dict[str, Any]) -> Dict[str, Any]:
    class_name = class_data["name"]
    return {
        "id": f"class:{module_path}::{class_name}",
        "type": "Class",
        "name": class_name,
        "module_path": module_path,
        "bases": class_data.get("bases", []),
        "decorators": class_data.get("decorators", []),
        "methods": class_data.get("methods", []),
        "lineno": class_data.get("lineno"),
    }


def _registry_node(registry_id: str, registry_path: str) -> Dict[str, Any]:
    return {
        "id": f"registry:{registry_id}",
        "type": "RegistryEntry",
        "registry_id": registry_id,
        "path": registry_path,
    }


def _find_snapshot_files(snapshots_dir: Path) -> Tuple[List[Path], List[Path]]:
    module_contracts = sorted(snapshots_dir.glob("batch_*_module_contracts.json"))
    registry_coverage = sorted(snapshots_dir.glob("batch_*_registry_coverage.json"))
    return module_contracts, registry_coverage


def _load_contract_entries(paths: Iterable[Path]) -> List[Tuple[str, Dict[str, Any]]]:
    entries: List[Tuple[str, Dict[str, Any]]] = []
    for path in paths:
        data = _load_json(path)
        if not isinstance(data, list):
            print(f"[WARN] Contract snapshot is not a list: {path}")
            continue
        batch_name = path.name.replace("_module_contracts.json", "")
        entries.extend((batch_name, item) for item in data if isinstance(item, dict))
    return entries


def _load_registry_coverage(paths: Iterable[Path]) -> Tuple[Set[str], Set[str]]:
    in_registry: Set[str] = set()
    missing_from_registry: Set[str] = set()
    for path in paths:
        data = _load_json(path)
        if not isinstance(data, dict):
            print(f"[WARN] Registry snapshot is not a mapping: {path}")
            continue
        in_registry.update(p for p in data.get("in_registry", []) if isinstance(p, str))
        missing_from_registry.update(
            p for p in data.get("missing_from_registry", []) if isinstance(p, str)
        )
    return in_registry, missing_from_registry


def _module_imports_from_source(repo_root: Path, module_paths: Set[str]) -> List[Tuple[str, str]]:
    imports_edges: List[Tuple[str, str]] = []
    module_by_stem = {
        path.replace("/", ".").removesuffix(".py"): path
        for path in module_paths
        if path.endswith(".py")
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
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module)

        for imported in imports:
            imported_parts = imported.split(".")
            for segment_count in range(len(imported_parts), 0, -1):
                candidate = ".".join(imported_parts[:segment_count])
                target = module_by_stem.get(candidate)
                if target and target != module_path:
                    imports_edges.append((module_path, target))
                    break

    return sorted(set(imports_edges))


def build_graph(paths: GraphPaths, include_import_edges: bool = False) -> Dict[str, Any]:
    contracts_files, registry_files = _find_snapshot_files(paths.snapshots_dir)
    contract_entries = _load_contract_entries(contracts_files)
    in_registry_paths, missing_from_registry = _load_registry_coverage(registry_files)

    registry_by_path: dict[str, str] = {}
    registry_by_id: dict[str, str] = {}
    if paths.registry_file and paths.registry_file.exists():
        registry_by_path, registry_by_id = _load_registry_map(paths.registry_file)

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Set[Tuple[str, str, str]] = set()
    module_paths: Set[str] = set()

    for batch_name, entry in contract_entries:
        module_path = entry.get("file")
        sha256 = entry.get("sha256", "")
        if not module_path:
            print(f"[WARN] Skipping entry without file field: {entry}")
            continue

        module_paths.add(module_path)
        has_syntax_error = bool(entry.get("syntax_error"))
        registry_id = registry_by_path.get(module_path)
        in_registry = module_path in in_registry_paths or registry_id is not None

        module_id = f"module:{module_path}"
        nodes[module_id] = _module_node(
            module_path=module_path,
            sha256=sha256,
            syntax_error=has_syntax_error,
            registry_id=registry_id,
            in_registry=in_registry,
            batch_name=batch_name,
        )

        if has_syntax_error:
            continue

        for function in entry.get("functions", []):
            if not isinstance(function, dict) or "name" not in function:
                print(f"[WARN] Function missing name in {module_path}: {function}")
                continue
            fn_node = _function_node(module_path, function)
            nodes[fn_node["id"]] = fn_node
            edges.add((module_id, fn_node["id"], "DEFINES"))

        classes_in_module = [c for c in entry.get("classes", []) if isinstance(c, dict)]
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

    for registry_id, registry_path in sorted(registry_by_id.items()):
        reg_node = _registry_node(registry_id, registry_path)
        nodes[reg_node["id"]] = reg_node
        module_id = f"module:{registry_path}"
        if module_id in nodes:
            edges.add((module_id, reg_node["id"], "REGISTERED"))

    for missing in sorted(missing_from_registry):
        if f"module:{missing}" not in nodes:
            print(f"[WARN] Missing-from-registry path not found in contracts: {missing}")

    if include_import_edges:
        for source, target in _module_imports_from_source(paths.repo_root, module_paths):
            edges.add((f"module:{source}", f"module:{target}", "IMPORTS"))

    graph = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "schema_version": "1.1.0",
            "source_snapshots": {
                "module_contracts": [str(p) for p in contracts_files],
                "registry_coverage": [str(p) for p in registry_files],
                "registry": str(paths.registry_file) if paths.registry_file else None,
            },
            "totals": {
                "nodes": len(nodes),
                "edges": len(edges),
                "modules": len([n for n in nodes.values() if n["type"] == "Module"]),
                "functions": len([n for n in nodes.values() if n["type"] == "Function"]),
                "classes": len([n for n in nodes.values() if n["type"] == "Class"]),
                "registry_entries": len(
                    [n for n in nodes.values() if n["type"] == "RegistryEntry"]
                ),
            },
        },
        "nodes": sorted(nodes.values(), key=lambda item: item["id"]),
        "edges": [
            {"source": source, "target": target, "type": edge_type}
            for source, target, edge_type in sorted(edges)
        ],
    }
    return graph


def _stable_graph_hash(graph: Dict[str, Any]) -> str:
    canonical = {
        "metadata": {
            "schema_version": graph.get("metadata", {}).get("schema_version", "1.0.0"),
            "source_snapshots": graph.get("metadata", {}).get("source_snapshots", {}),
            "totals": graph.get("metadata", {}).get("totals", {}),
        },
        "nodes": graph.get("nodes", []),
        "edges": graph.get("edges", []),
    }
    graph_bytes = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(graph_bytes).hexdigest()


def write_manifest(graph: Dict[str, Any], paths: GraphPaths) -> None:
    if not paths.manifest_file:
        return

    contracts_files, registry_files = _find_snapshot_files(paths.snapshots_dir)
    input_paths = sorted([*contracts_files, *registry_files])
    if paths.registry_file and paths.registry_file.exists():
        input_paths.append(paths.registry_file)

    manifest = {
        "schema_version": graph.get("metadata", {}).get("schema_version", "1.0.0"),
        "graph_sha256": _stable_graph_hash(graph),
        "snapshot_sha256": {str(path): _sha256_file(path) for path in input_paths},
        "totals": graph.get("metadata", {}).get("totals", {}),
    }
    paths.manifest_file.parent.mkdir(parents=True, exist_ok=True)
    paths.manifest_file.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    paths = GraphPaths(
        snapshots_dir=args.snapshots_dir,
        output_file=args.output,
        repo_root=args.repo_root,
        registry_file=args.registry,
        manifest_file=args.manifest_out,
    )
    graph = build_graph(paths, include_import_edges=args.include_import_edges)
    paths.output_file.parent.mkdir(parents=True, exist_ok=True)
    paths.output_file.write_text(json.dumps(graph, indent=2) + "\n", encoding="utf-8")
    write_manifest(graph, paths)
    print(f"Wrote graph with {len(graph['nodes'])} nodes to {paths.output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())