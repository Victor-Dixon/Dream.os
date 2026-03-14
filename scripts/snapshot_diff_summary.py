#!/usr/bin/env python3
"""Generate markdown summary between two knowledge graph snapshots."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_graph", nargs="?", help="Path to old graph JSON")
    parser.add_argument("new_graph", nargs="?", help="Path to new graph JSON")
    parser.add_argument("--base-ref", help="Git base reference (e.g. origin/main)")
    parser.add_argument("--head-ref", default="HEAD", help="Git head reference")
    parser.add_argument(
        "--graph-path",
        default="knowledge_graph/latest.json",
        help="Graph path within git refs for ref-based comparison.",
    )
    return parser.parse_args()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_graph_from_git(ref: str, graph_path: str) -> Dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{ref}:{graph_path}"],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(result.stdout)


def _index_nodes(graph: Dict[str, Any], node_type: str) -> Dict[str, Dict[str, Any]]:
    return {node["id"]: node for node in graph.get("nodes", []) if node.get("type") == node_type}


def _module_children(graph: Dict[str, Any], child_type_prefix: str) -> Dict[str, Set[str]]:
    module_nodes = _index_nodes(graph, "Module")
    child_nodes = {node["id"]: node for node in graph.get("nodes", []) if node["id"].startswith(child_type_prefix)}
    result: Dict[str, Set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        if edge.get("type") != "DEFINES":
            continue
        source = edge.get("source")
        target = edge.get("target")
        if source in module_nodes and target in child_nodes:
            result[source].add(target)
    return result


def _registered_modules(graph: Dict[str, Any]) -> Set[str]:
    registered: Set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") == "REGISTERED" and edge.get("source", "").startswith("module:"):
            registered.add(edge["source"].replace("module:", "", 1))
    return registered


def _imports(graph: Dict[str, Any]) -> Set[Tuple[str, str]]:
    imports: Set[Tuple[str, str]] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") == "IMPORTS":
            imports.add((edge.get("source", ""), edge.get("target", "")))
    return imports


def _module_name(module_id: str) -> str:
    return module_id.replace("module:", "", 1)


def _entity_name(entity_id: str) -> str:
    return entity_id.split("::", 1)[1] if "::" in entity_id else entity_id


def _signature_lookup(graph: Dict[str, Any], prefix: str) -> Dict[str, str]:
    return {
        node["id"]: node.get("signature", "")
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("id", "").startswith(prefix)
    }


def generate_markdown(old_graph: Dict[str, Any], new_graph: Dict[str, Any]) -> str:
    old_modules = _index_nodes(old_graph, "Module")
    new_modules = _index_nodes(new_graph, "Module")

    old_ids = set(old_modules)
    new_ids = set(new_modules)
    added_modules = sorted(new_ids - old_ids)
    removed_modules = sorted(old_ids - new_ids)
    common_modules = sorted(old_ids & new_ids)

    changed_modules = [
        module_id
        for module_id in common_modules
        if old_modules[module_id].get("sha256") != new_modules[module_id].get("sha256")
        or old_modules[module_id].get("has_syntax_error") != new_modules[module_id].get("has_syntax_error")
    ]

    fixed_syntax = [
        module_id
        for module_id in common_modules
        if old_modules[module_id].get("has_syntax_error") and not new_modules[module_id].get("has_syntax_error")
    ]
    introduced_syntax = [
        module_id
        for module_id in common_modules
        if not old_modules[module_id].get("has_syntax_error") and new_modules[module_id].get("has_syntax_error")
    ]

    old_functions = _module_children(old_graph, "function:")
    new_functions = _module_children(new_graph, "function:")
    old_classes = _module_children(old_graph, "class:")
    new_classes = _module_children(new_graph, "class:")

    old_signatures = _signature_lookup(old_graph, "function:")
    new_signatures = _signature_lookup(new_graph, "function:")

    entity_changes: Dict[str, Dict[str, List[str]]] = defaultdict(lambda: defaultdict(list))
    for module_id in common_modules:
        added_fns = sorted(new_functions.get(module_id, set()) - old_functions.get(module_id, set()))
        removed_fns = sorted(old_functions.get(module_id, set()) - new_functions.get(module_id, set()))
        added_cls = sorted(new_classes.get(module_id, set()) - old_classes.get(module_id, set()))
        removed_cls = sorted(old_classes.get(module_id, set()) - new_classes.get(module_id, set()))
        if added_fns:
            entity_changes[module_id]["added_functions"] = [_entity_name(v) for v in added_fns]
        if removed_fns:
            entity_changes[module_id]["removed_functions"] = [_entity_name(v) for v in removed_fns]
        if added_cls:
            entity_changes[module_id]["added_classes"] = [_entity_name(v) for v in added_cls]
        if removed_cls:
            entity_changes[module_id]["removed_classes"] = [_entity_name(v) for v in removed_cls]

        shared_fns = old_functions.get(module_id, set()) & new_functions.get(module_id, set())
        for fn_id in sorted(shared_fns):
            if old_signatures.get(fn_id) != new_signatures.get(fn_id):
                entity_changes[module_id]["signature_changes"].append(
                    f"{_entity_name(fn_id)}: `{old_signatures.get(fn_id, '')}` → `{new_signatures.get(fn_id, '')}`"
                )

    old_registered = _registered_modules(old_graph)
    new_registered = _registered_modules(new_graph)
    registry_added = sorted(new_registered - old_registered)
    registry_removed = sorted(old_registered - new_registered)

    old_imports = _imports(old_graph)
    new_imports = _imports(new_graph)
    import_added = sorted(new_imports - old_imports)
    import_removed = sorted(old_imports - new_imports)

    lines = ["# Snapshot Diff Summary", "", "## Summary"]
    lines.append(f"- Modules changed: **{len(changed_modules)}**")
    lines.append(f"- Modules added: **{len(added_modules)}**")
    lines.append(f"- Modules removed: **{len(removed_modules)}**")

    lines.extend(["", "## Syntax error changes"])
    if fixed_syntax:
        lines.append("- Fixed syntax errors:")
        lines.extend([f"  - `{_module_name(mid)}`" for mid in fixed_syntax])
    if introduced_syntax:
        lines.append("- New syntax errors:")
        lines.extend([f"  - `{_module_name(mid)}`" for mid in introduced_syntax])
    if not fixed_syntax and not introduced_syntax:
        lines.append("- No syntax error state changes.")

    lines.extend(["", "## Function/class changes"])
    if entity_changes:
        for module_id in sorted(entity_changes):
            lines.append(f"- `{_module_name(module_id)}`")
            for key, label in [
                ("added_functions", "Added functions"),
                ("removed_functions", "Removed functions"),
                ("added_classes", "Added classes"),
                ("removed_classes", "Removed classes"),
                ("signature_changes", "Signature changes"),
            ]:
                values = entity_changes[module_id].get(key, [])
                if values:
                    lines.append(f"  - {label}: {', '.join(f'`{value}`' for value in values)}")
    else:
        lines.append("- No function/class contract changes.")

    lines.extend(["", "## Registry coverage changes"])
    if registry_added or registry_removed:
        if registry_added:
            lines.append("- Added to registry:")
            lines.extend([f"  - `{path}`" for path in registry_added])
        if registry_removed:
            lines.append("- Removed from registry:")
            lines.extend([f"  - `{path}`" for path in registry_removed])
    else:
        lines.append("- No registry coverage changes.")

    lines.extend(["", "## Import changes"])
    if import_added or import_removed:
        if import_added:
            lines.append("- New imports:")
            lines.extend([f"  - `{_module_name(src)} -> {_module_name(dst)}`" for src, dst in import_added])
        if import_removed:
            lines.append("- Removed imports:")
            lines.extend([f"  - `{_module_name(src)} -> {_module_name(dst)}`" for src, dst in import_removed])
    else:
        lines.append("- No import graph changes (or import edges unavailable).")

    if added_modules:
        lines.extend(["", "## Added modules"])
        lines.extend([f"- `{_module_name(module_id)}`" for module_id in added_modules])
    if removed_modules:
        lines.extend(["", "## Removed modules"])
        lines.extend([f"- `{_module_name(module_id)}`" for module_id in removed_modules])

    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    if args.old_graph and args.new_graph:
        old_graph = _load_json(Path(args.old_graph))
        new_graph = _load_json(Path(args.new_graph))
    elif args.base_ref:
        old_graph = _load_graph_from_git(args.base_ref, args.graph_path)
        new_graph = _load_graph_from_git(args.head_ref, args.graph_path)
    else:
        raise SystemExit("Provide either <old_graph> <new_graph> or --base-ref <ref>.")

    print(generate_markdown(old_graph, new_graph))


if __name__ == "__main__":
    main()
