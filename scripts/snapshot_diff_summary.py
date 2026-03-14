# Header-Variant: line
# Owner: Dream.os Platform
# Purpose: Summarize knowledge graph changes for snapshot updates.
# SSOT: docs/recovery/recovery_registry.yaml
# @registry docs/recovery/recovery_registry.yaml#unregistered-scripts-snapshot-diff-summary

"""Generate a Markdown diff summary between two knowledge graph snapshots.

Usage:
  python scripts/snapshot_diff_summary.py --old-graph path --new-graph path
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _by_type(nodes: list[dict[str, Any]], node_type: str) -> dict[str, dict[str, Any]]:
    return {n["id"]: n for n in nodes if n.get("type") == node_type and "id" in n}


def _module_index(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    modules = _by_type(graph.get("nodes", []), "Module")
    return {node["path"]: node for node in modules.values() if "path" in node}


def _defines_map(graph: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = defaultdict(set)
    nodes = {n.get("id"): n for n in graph.get("nodes", []) if "id" in n}
    for edge in graph.get("edges", []):
        if edge.get("type") != "DEFINES":
            continue
        src = edge.get("source")
        tgt = edge.get("target")
        src_node = nodes.get(src)
        tgt_node = nodes.get(tgt)
        if not src_node or not tgt_node or src_node.get("type") != "Module":
            continue
        path = src_node.get("path")
        if not path:
            continue
        label = f"{tgt_node.get('type')}:{tgt_node.get('name', tgt)}"
        out[path].add(label)
    return out


def _function_sigs(graph: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for node in graph.get("nodes", []):
        if node.get("type") != "Function":
            continue
        module = node.get("module")
        name = node.get("name")
        signature = node.get("signature")
        if module and name:
            out[f"{module}:{name}"] = str(signature)
    return out


def _registered_paths(graph: dict[str, Any]) -> set[str]:
    nodes = {n.get("id"): n for n in graph.get("nodes", []) if "id" in n}
    out: set[str] = set()
    for edge in graph.get("edges", []):
        if edge.get("type") != "REGISTERED":
            continue
        mod = nodes.get(edge.get("source"))
        if mod and mod.get("type") == "Module" and mod.get("path"):
            out.add(mod["path"])
    return out


def _import_edges(graph: dict[str, Any]) -> set[tuple[str, str]]:
    return {
        (edge.get("source", ""), edge.get("target", ""))
        for edge in graph.get("edges", [])
        if edge.get("type") == "IMPORTS"
    }


def generate_report(old_graph: dict[str, Any], new_graph: dict[str, Any]) -> str:
    old_modules = _module_index(old_graph)
    new_modules = _module_index(new_graph)

    added_modules = sorted(set(new_modules) - set(old_modules))
    removed_modules = sorted(set(old_modules) - set(new_modules))
    common_modules = sorted(set(old_modules) & set(new_modules))

    changed_modules = []
    syntax_fixed = []
    syntax_regressed = []

    for path in common_modules:
        old = old_modules[path]
        new = new_modules[path]
        if old.get("sha256") != new.get("sha256"):
            changed_modules.append(path)
        old_err = bool(old.get("has_syntax_error"))
        new_err = bool(new.get("has_syntax_error"))
        if old_err and not new_err:
            syntax_fixed.append(path)
        if not old_err and new_err:
            syntax_regressed.append(path)

    old_defines = _defines_map(old_graph)
    new_defines = _defines_map(new_graph)
    old_sigs = _function_sigs(old_graph)
    new_sigs = _function_sigs(new_graph)

    structure_changes: list[str] = []
    for path in common_modules:
        old_items = old_defines.get(path, set())
        new_items = new_defines.get(path, set())
        add_items = sorted(new_items - old_items)
        rem_items = sorted(old_items - new_items)

        sig_changes = []
        for key, old_sig in old_sigs.items():
            if not key.startswith(f"{path}:"):
                continue
            new_sig = new_sigs.get(key)
            if new_sig is not None and new_sig != old_sig:
                fn_name = key.split(":", 1)[1]
                sig_changes.append(f"{fn_name}: `{old_sig}` → `{new_sig}`")

        if add_items or rem_items or sig_changes:
            section = [f"- `{path}`"]
            if add_items:
                section.append(f"  - Added: {', '.join(add_items)}")
            if rem_items:
                section.append(f"  - Removed: {', '.join(rem_items)}")
            for sig in sig_changes:
                section.append(f"  - Signature changed: {sig}")
            structure_changes.extend(section)

    old_reg = _registered_paths(old_graph)
    new_reg = _registered_paths(new_graph)
    reg_added = sorted(new_reg - old_reg)
    reg_removed = sorted(old_reg - new_reg)

    old_imports = _import_edges(old_graph)
    new_imports = _import_edges(new_graph)
    imports_added = sorted(new_imports - old_imports)
    imports_removed = sorted(old_imports - new_imports)

    lines = [
        "## Snapshot Graph Diff Summary",
        "",
        "### Overview",
        f"- Modules changed (sha): **{len(changed_modules)}**",
        f"- Modules added: **{len(added_modules)}**",
        f"- Modules removed: **{len(removed_modules)}**",
    ]

    if added_modules:
        lines += ["", "### Added Modules", *[f"- `{m}`" for m in added_modules]]
    if removed_modules:
        lines += ["", "### Removed Modules", *[f"- `{m}`" for m in removed_modules]]

    lines += ["", "### Syntax Error Changes"]
    if syntax_fixed:
        lines += ["- Fixed (error → valid):", *[f"  - `{m}`" for m in syntax_fixed]]
    if syntax_regressed:
        lines += ["- Regressed (valid → error):", *[f"  - `{m}`" for m in syntax_regressed]]
    if not syntax_fixed and not syntax_regressed:
        lines.append("- No syntax error status changes detected.")

    lines += ["", "### Function/Class Contract Changes"]
    if structure_changes:
        lines.extend(structure_changes)
    else:
        lines.append("- No function/class contract changes detected.")

    lines += ["", "### Registry Coverage Changes"]
    if reg_added:
        lines += ["- Added to registry:", *[f"  - `{m}`" for m in reg_added]]
    if reg_removed:
        lines += ["- Removed from registry:", *[f"  - `{m}`" for m in reg_removed]]
    if not reg_added and not reg_removed:
        lines.append("- No registry coverage changes detected.")

    lines += ["", "### Import Graph Changes"]
    if imports_added or imports_removed:
        lines.append(f"- Imports added: **{len(imports_added)}**, removed: **{len(imports_removed)}**")
    else:
        lines.append("- Import edges unavailable or unchanged.")

    return "\n".join(lines) + "\n"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize snapshot graph diffs")
    parser.add_argument("--old-graph", type=Path, required=True)
    parser.add_argument("--new-graph", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("knowledge_graph/diff_summary.md"))
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    old_graph = _load_graph(args.old_graph)
    new_graph = _load_graph(args.new_graph)
    report = generate_report(old_graph, new_graph)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"✅ Wrote summary: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
