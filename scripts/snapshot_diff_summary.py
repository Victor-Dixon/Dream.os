# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Summarize knowledge graph diffs for snapshot-heavy pull requests.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-snapshot-diff-summary

"""Generate Markdown summaries from knowledge graph diffs.

Usage:
    python scripts/snapshot_diff_summary.py --old old.json --new new.json
    python scripts/snapshot_diff_summary.py --base HEAD~1 --head HEAD
    python scripts/snapshot_diff_summary.py --old old.json --new new.json --output knowledge_graph/diff_summary.md
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_graph_from_git(commitish: str, graph_path: str) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{commitish}:{graph_path}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _index_nodes(graph: dict[str, Any], node_type: str) -> dict[str, dict[str, Any]]:
    return {
        node["id"]: node
        for node in graph.get("nodes", [])
        if isinstance(node, dict) and node.get("type") == node_type and "id" in node
    }


def _module_children(graph: dict[str, Any], child_prefix: str) -> dict[str, set[str]]:
    modules = _index_nodes(graph, "Module")
    children = {
        node["id"]: node
        for node in graph.get("nodes", [])
        if isinstance(node, dict)
        and isinstance(node.get("id"), str)
        and node["id"].startswith(child_prefix)
    }

    result: dict[str, set[str]] = defaultdict(set)
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("type") != "DEFINES":
            continue
        source = edge.get("source")
        target = edge.get("target")
        if source in modules and target in children:
            result[source].add(target)
    return result


def _registered_modules(graph: dict[str, Any]) -> set[str]:
    registered: set[str] = set()
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        source = edge.get("source")
        if edge.get("type") == "REGISTERED" and isinstance(source, str) and source.startswith("module:"):
            registered.add(source.removeprefix("module:"))
    return registered


def _imports(graph: dict[str, Any]) -> set[tuple[str, str]]:
    imports: set[tuple[str, str]] = set()
    for edge in graph.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if edge.get("type") != "IMPORTS":
            continue
        source = edge.get("source")
        target = edge.get("target")
        if isinstance(source, str) and isinstance(target, str):
            imports.add((source, target))
    return imports


def _module_name(module_id: str) -> str:
    return module_id.removeprefix("module:")


def _entity_name(entity_id: str) -> str:
    return entity_id.split("::", 1)[1] if "::" in entity_id else entity_id


def _signature_lookup(graph: dict[str, Any], prefix: str) -> dict[str, str]:
    return {
        node["id"]: node.get("signature", "")
        for node in graph.get("nodes", [])
        if isinstance(node, dict)
        and isinstance(node.get("id"), str)
        and node["id"].startswith(prefix)
    }


def generate_markdown(
    old_graph: dict[str, Any],
    new_graph: dict[str, Any],
    expected_prefixes: list[str] | None = None,
) -> str:
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

    entity_changes: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
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

    unexpected: list[str] = []
    if expected_prefixes:
        changed_paths = [_module_name(module_id) for module_id in changed_modules]
        added_paths = [_module_name(module_id) for module_id in added_modules]
        removed_paths = [_module_name(module_id) for module_id in removed_modules]
        for path in changed_paths + added_paths + removed_paths:
            if not any(path.startswith(prefix) for prefix in expected_prefixes):
                unexpected.append(path)

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
                    if key == "signature_changes":
                        rendered = ", ".join(values)
                    else:
                        rendered = ", ".join(f"`{value}`" for value in values)
                    lines.append(f"  - {label}: {rendered}")
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

    lines.extend(["", "## Unexpected changes"])
    if unexpected:
        lines.append(
            "- Changes outside expected prefixes detected: "
            + ", ".join(f"`{path}`" for path in sorted(set(unexpected)))
        )
    else:
        lines.append("- No unexpected module path changes detected.")

    return "\n".join(lines) + "\n"


def summarize_diff(
    old_graph: dict[str, Any],
    new_graph: dict[str, Any],
    expected_prefixes: list[str] | None = None,
) -> tuple[str, bool]:
    summary = generate_markdown(
        old_graph=old_graph,
        new_graph=new_graph,
        expected_prefixes=expected_prefixes,
    )

    old_modules = _index_nodes(old_graph, "Module")
    new_modules = _index_nodes(new_graph, "Module")
    old_ids = {_module_name(module_id) for module_id in old_modules}
    new_ids = {_module_name(module_id) for module_id in new_modules}

    changed_paths = sorted(
        _module_name(module_id)
        for module_id in (set(old_modules) & set(new_modules))
        if old_modules[module_id].get("sha256") != new_modules[module_id].get("sha256")
        or old_modules[module_id].get("has_syntax_error") != new_modules[module_id].get("has_syntax_error")
    )
    added_paths = sorted(new_ids - old_ids)
    removed_paths = sorted(old_ids - new_ids)

    unexpected = False
    if expected_prefixes:
        for path in changed_paths + added_paths + removed_paths:
            if not any(path.startswith(prefix) for prefix in expected_prefixes):
                unexpected = True
                break

    return summary, unexpected


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize snapshot graph differences")
    parser.add_argument("--old", type=Path, help="Path to old graph JSON")
    parser.add_argument("--new", type=Path, help="Path to new graph JSON")
    parser.add_argument("--base", help="Git commit/ref for old graph at knowledge_graph/latest.json")
    parser.add_argument("--head", help="Git commit/ref for new graph at knowledge_graph/latest.json")
    parser.add_argument(
        "--graph-path",
        default="knowledge_graph/latest.json",
        help="Graph path used with --base/--head mode",
    )
    parser.add_argument(
        "--expected-prefix",
        action="append",
        default=[],
        help="Expected changed module prefix (repeatable)",
    )
    parser.add_argument("--fail-on-unexpected", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write Markdown summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()

    if args.old and args.new:
        old_graph = _load_graph(args.old)
        new_graph = _load_graph(args.new)
    elif args.base and args.head:
        old_graph = _load_graph_from_git(args.base, args.graph_path)
        new_graph = _load_graph_from_git(args.head, args.graph_path)
    else:
        raise SystemExit("Provide either --old/--new or --base/--head")

    summary, has_unexpected = summarize_diff(
        old_graph=old_graph,
        new_graph=new_graph,
        expected_prefixes=args.expected_prefix,
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(summary, encoding="utf-8")
        print(f"Wrote summary: {args.output}")
    else:
        print(summary)

    if args.fail_on_unexpected and has_unexpected:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())