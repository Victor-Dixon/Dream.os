# Header-Variant: line
# Owner: Dream.os Platform
# Purpose: Build a versioned knowledge graph from lockdown snapshots.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-build-knowledge-graph

"""Build a knowledge graph from snapshot and registry artifacts.

Usage:
  python scripts/build_knowledge_graph.py \
      --repo-root . \
      --output knowledge_graph/latest.json
"""

from __future__ import annotations

import argparse
import ast
import glob
import json
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


@dataclass
class GraphData:
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    warnings: list[str]


def _module_snapshot_paths(repo_root: Path) -> list[Path]:
    pattern = str(repo_root / "tests/snapshots/batch_*_module_contracts.json")
    return sorted(Path(p) for p in glob.glob(pattern))


def _coverage_snapshot_paths(repo_root: Path) -> list[Path]:
    pattern = str(repo_root / "tests/snapshots/batch_*_registry_coverage.json")
    return sorted(Path(p) for p in glob.glob(pattern))


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_registry_entries(repo_root: Path) -> list[dict[str, Any]]:
    registry_path = repo_root / "docs/recovery/recovery_registry.yaml"
    if not registry_path.exists():
        return []
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
    files = data.get("files", [])
    return [item for item in files if isinstance(item, dict)]


def _method_names(class_contract: dict[str, Any]) -> list[str]:
    methods = class_contract.get("methods", [])
    return [m.get("name", "<unknown>") for m in methods if isinstance(m, dict)]


def _func_signature(function_contract: dict[str, Any]) -> str:
    return (
        f"args={function_contract.get('args', 0)},"
        f"kwonly={function_contract.get('kwonly_args', 0)},"
        f"defaults={function_contract.get('defaults', 0)},"
        f"async={bool(function_contract.get('async', False))}"
    )


def _module_imports(repo_root: Path, module_rel: str) -> list[str]:
    file_path = repo_root / module_rel
    if not file_path.exists() or file_path.suffix != ".py":
        return []
    try:
        parsed = ast.parse(file_path.read_text(encoding="utf-8"))
    except SyntaxError:
        return []

    imports: list[str] = []
    for node in parsed.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level > 0:
                imports.append(f".{module}")
            else:
                imports.append(module)
    return sorted(set(filter(None, imports)))


def _python_files_by_module_name(repo_root: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for py_path in repo_root.glob("src/**/*.py"):
        rel = py_path.relative_to(repo_root).as_posix()
        mod_name = rel.removesuffix(".py").replace("/", ".")
        mapping[mod_name] = rel
    return mapping


def build_graph(repo_root: Path, include_imports: bool = False) -> GraphData:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    warnings: list[str] = []

    module_files = _module_snapshot_paths(repo_root)
    coverage_files = _coverage_snapshot_paths(repo_root)
    if not module_files:
        warnings.append("No module contract snapshots found under tests/snapshots")

    modules: dict[str, dict[str, Any]] = {}
    for path in module_files:
        data = _load_json(path)
        if not isinstance(data, list):
            warnings.append(f"Skipping malformed module snapshot: {path}")
            continue
        for item in data:
            if not isinstance(item, dict) or "file" not in item:
                continue
            rel = item["file"]
            prev = modules.get(rel)
            if prev and prev.get("sha256") != item.get("sha256"):
                warnings.append(f"Conflicting snapshot rows for {rel}; using last from {path.name}")
            modules[rel] = item

    in_registry_from_coverage: set[str] = set()
    for path in coverage_files:
        data = _load_json(path)
        if not isinstance(data, dict):
            warnings.append(f"Skipping malformed coverage snapshot: {path}")
            continue
        for rel in data.get("in_registry", []):
            if isinstance(rel, str):
                in_registry_from_coverage.add(rel)

    registry_entries = _load_registry_entries(repo_root)
    registry_by_path: dict[str, dict[str, Any]] = {}
    for entry in registry_entries:
        file_path = entry.get("file")
        if isinstance(file_path, str):
            registry_by_path[file_path] = entry
            nodes.append(
                {
                    "id": f"registry:{entry.get('id', file_path)}",
                    "type": "RegistryEntry",
                    "registry_id": entry.get("id"),
                    "path": file_path,
                }
            )

    class_nodes_by_name: dict[str, list[str]] = defaultdict(list)
    py_module_map = _python_files_by_module_name(repo_root) if include_imports else {}

    for rel, contract in sorted(modules.items()):
        mod_id = f"module:{rel}"
        has_syntax_error = "syntax_error" in contract
        nodes.append(
            {
                "id": mod_id,
                "type": "Module",
                "path": rel,
                "sha256": contract.get("sha256"),
                "has_syntax_error": has_syntax_error,
            }
        )

        reg = registry_by_path.get(rel)
        if reg:
            edges.append(
                {
                    "type": "REGISTERED",
                    "source": mod_id,
                    "target": f"registry:{reg.get('id', rel)}",
                }
            )
        elif rel in in_registry_from_coverage:
            warnings.append(f"Coverage marks '{rel}' in registry but no registry entry was found")

        if has_syntax_error:
            continue

        for fn in contract.get("functions", []):
            if not isinstance(fn, dict):
                continue
            fn_name = fn.get("name", "<unknown>")
            fn_id = f"function:{rel}:{fn_name}"
            nodes.append(
                {
                    "id": fn_id,
                    "type": "Function",
                    "module": rel,
                    "name": fn_name,
                    "signature": _func_signature(fn),
                    "decorators": fn.get("decorators", []),
                }
            )
            edges.append({"type": "DEFINES", "source": mod_id, "target": fn_id})

        for cls in contract.get("classes", []):
            if not isinstance(cls, dict):
                continue
            cls_name = cls.get("name", "<unknown>")
            cls_id = f"class:{rel}:{cls_name}"
            nodes.append(
                {
                    "id": cls_id,
                    "type": "Class",
                    "module": rel,
                    "name": cls_name,
                    "bases": cls.get("bases", []),
                    "methods": _method_names(cls),
                }
            )
            class_nodes_by_name[cls_name].append(cls_id)
            edges.append({"type": "DEFINES", "source": mod_id, "target": cls_id})

    for rel, contract in sorted(modules.items()):
        if "syntax_error" in contract:
            continue
        for cls in contract.get("classes", []):
            if not isinstance(cls, dict):
                continue
            cls_id = f"class:{rel}:{cls.get('name', '<unknown>')}"
            for base in cls.get("bases", []):
                if not isinstance(base, str):
                    continue
                candidates = class_nodes_by_name.get(base, [])
                if len(candidates) == 1:
                    edges.append({"type": "INHERITS", "source": cls_id, "target": candidates[0]})

    if include_imports:
        for rel in sorted(modules):
            mod_id = f"module:{rel}"
            for imported in _module_imports(repo_root, rel):
                target_rel = py_module_map.get(imported)
                if target_rel:
                    edges.append(
                        {
                            "type": "IMPORTS",
                            "source": mod_id,
                            "target": f"module:{target_rel}",
                            "import": imported,
                        }
                    )

    return GraphData(nodes=nodes, edges=edges, warnings=warnings)


def write_graph(repo_root: Path, output: Path, include_imports: bool = False) -> Path:
    graph = build_graph(repo_root=repo_root, include_imports=include_imports)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(repo_root),
        "schema_version": "1",
        "nodes": graph.nodes,
        "edges": graph.edges,
        "warnings": graph.warnings,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output


def _git_commit(repo_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return proc.stdout.strip()
    except Exception:
        return "unknown"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build knowledge graph from snapshots")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("knowledge_graph/latest.json"))
    parser.add_argument("--include-imports", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    output = write_graph(
        repo_root=args.repo_root.resolve(),
        output=args.output,
        include_imports=args.include_imports,
    )
    print(f"✅ Wrote knowledge graph: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
