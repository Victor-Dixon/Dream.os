# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Build a review-oriented knowledge graph from lockdown snapshots.
# SSOT: docs/recovery/recovery_registry.yaml

"""Build a consolidated knowledge graph from lockdown snapshot JSON files.

Usage:
    python scripts/build_knowledge_graph.py \
        --snapshots-dir tests/snapshots \
        --registry docs/recovery/recovery_registry.yaml \
        --output knowledge_graph/latest.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


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


def _function_signature(function_data: dict[str, Any]) -> str:
    args = function_data.get("args", 0)
    kwonly_args = function_data.get("kwonly_args", 0)
    defaults = function_data.get("defaults", 0)
    async_prefix = "async " if function_data.get("async") else ""
    return f"{async_prefix}(args={args}, kwonly={kwonly_args}, defaults={defaults})"


def _normalize_methods(class_data: dict[str, Any]) -> list[dict[str, Any]]:
    methods: list[dict[str, Any]] = []
    for method in class_data.get("methods", []):
        if not isinstance(method, dict):
            continue
        methods.append(
            {
                "name": method.get("name"),
                "signature": _function_signature(method),
                "decorators": method.get("decorators", []),
                "lineno": method.get("lineno"),
            }
        )
    return methods


def build_graph_from_snapshots(snapshots_dir: Path, registry_path: Path) -> dict[str, Any]:
    module_contract_paths = sorted(snapshots_dir.glob("*_module_contracts.json"))
    coverage_paths = sorted(snapshots_dir.glob("*_registry_coverage.json"))

    if not module_contract_paths:
        raise FileNotFoundError(f"No *_module_contracts.json files found in {snapshots_dir}")

    registry_by_path, registry_by_id = _load_registry_map(registry_path)

    modules: dict[str, dict[str, Any]] = {}
    in_registry_paths: set[str] = set()

    for coverage_path in coverage_paths:
        coverage_data = _load_json(coverage_path)
        for path in coverage_data.get("in_registry", []):
            if isinstance(path, str):
                in_registry_paths.add(path)

    for contract_path in module_contract_paths:
        batch_name = contract_path.name.replace("_module_contracts.json", "")
        module_data = _load_json(contract_path)
        if not isinstance(module_data, list):
            continue

        for module in module_data:
            if not isinstance(module, dict):
                continue
            module_path = module.get("file")
            if not isinstance(module_path, str):
                continue

            has_syntax_error = "syntax_error" in module
            registry_id = registry_by_path.get(module_path)
            in_registry = module_path in in_registry_paths or registry_id is not None

            functions = []
            classes = []
            if not has_syntax_error:
                for function in module.get("functions", []):
                    if not isinstance(function, dict):
                        continue
                    functions.append(
                        {
                            "name": function.get("name"),
                            "signature": _function_signature(function),
                            "decorators": function.get("decorators", []),
                            "lineno": function.get("lineno"),
                        }
                    )
                for class_data in module.get("classes", []):
                    if not isinstance(class_data, dict):
                        continue
                    classes.append(
                        {
                            "name": class_data.get("name"),
                            "bases": class_data.get("bases", []),
                            "decorators": class_data.get("decorators", []),
                            "methods": _normalize_methods(class_data),
                            "lineno": class_data.get("lineno"),
                        }
                    )

            modules[module_path] = {
                "path": module_path,
                "sha256": module.get("sha256"),
                "has_syntax_error": has_syntax_error,
                "syntax_error": module.get("syntax_error") if has_syntax_error else None,
                "docstring": module.get("docstring") if not has_syntax_error else False,
                "imports": module.get("imports") if not has_syntax_error else 0,
                "functions": functions,
                "classes": classes,
                "in_registry": in_registry,
                "registry_id": registry_id,
                "top_level": module.get("top_level", []) if not has_syntax_error else [],
                "batch": batch_name,
            }

    ordered_modules = {
        path: modules[path]
        for path in sorted(modules)
    }
    return {
        "meta": {
            "snapshot_dir": str(snapshots_dir),
            "module_contract_sources": [path.name for path in module_contract_paths],
            "registry_coverage_sources": [path.name for path in coverage_paths],
            "total_modules": len(ordered_modules),
            "in_registry": sum(1 for item in ordered_modules.values() if item["in_registry"]),
            "syntax_error_modules": sum(
                1 for item in ordered_modules.values() if item["has_syntax_error"]
            ),
        },
        "modules": ordered_modules,
        "registry_entries": dict(sorted(registry_by_id.items())),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build snapshot knowledge graph")
    parser.add_argument("--snapshots-dir", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    graph = build_graph_from_snapshots(args.snapshots_dir, args.registry)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(graph, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    print(f"Wrote knowledge graph: {args.output}")
    print(f"Modules: {graph['meta']['total_modules']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
