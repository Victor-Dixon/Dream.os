# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Summarize knowledge graph diffs for snapshot-heavy pull requests.
# SSOT: docs/recovery/recovery_registry.yaml

"""Generate Markdown summaries from knowledge graph diffs.

Usage:
    python scripts/snapshot_diff_summary.py --old old.json --new new.json
    python scripts/snapshot_diff_summary.py --base HEAD~1 --head HEAD
"""

from __future__ import annotations

import argparse
import json
import subprocess
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


def _names(items: list[dict[str, Any]]) -> set[str]:
    return {item.get("name") for item in items if isinstance(item, dict) and item.get("name")}


def _function_map(module: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for fn in module.get("functions", []):
        if isinstance(fn, dict) and fn.get("name"):
            output[fn["name"]] = fn.get("signature", "")
    return output


def _class_map(module: dict[str, Any]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for cls in module.get("classes", []):
        if isinstance(cls, dict) and cls.get("name"):
            output[cls["name"]] = cls
    return output


def summarize_diff(
    old_graph: dict[str, Any],
    new_graph: dict[str, Any],
    expected_prefixes: list[str] | None = None,
) -> tuple[str, bool]:
    old_modules = old_graph.get("modules", {})
    new_modules = new_graph.get("modules", {})

    old_paths = set(old_modules)
    new_paths = set(new_modules)
    added_paths = sorted(new_paths - old_paths)
    removed_paths = sorted(old_paths - new_paths)
    shared_paths = sorted(old_paths & new_paths)

    changed_paths: list[str] = []
    syntax_fixed: list[str] = []
    syntax_regressed: list[str] = []
    function_class_changes: dict[str, list[str]] = {}
    registry_changes: list[str] = []

    for path in shared_paths:
        old_module = old_modules[path]
        new_module = new_modules[path]
        if old_module == new_module:
            continue
        changed_paths.append(path)

        old_error = bool(old_module.get("has_syntax_error"))
        new_error = bool(new_module.get("has_syntax_error"))
        if old_error and not new_error:
            syntax_fixed.append(path)
        elif not old_error and new_error:
            syntax_regressed.append(path)

        module_lines: list[str] = []
        old_fn = _function_map(old_module)
        new_fn = _function_map(new_module)
        fn_added = sorted(set(new_fn) - set(old_fn))
        fn_removed = sorted(set(old_fn) - set(new_fn))
        fn_sig_changed = sorted(name for name in set(old_fn) & set(new_fn) if old_fn[name] != new_fn[name])

        old_cls = _class_map(old_module)
        new_cls = _class_map(new_module)
        cls_added = sorted(set(new_cls) - set(old_cls))
        cls_removed = sorted(set(old_cls) - set(new_cls))

        if fn_added:
            module_lines.append(f"functions added: {', '.join(f'`{name}`' for name in fn_added)}")
        if fn_removed:
            module_lines.append(f"functions removed: {', '.join(f'`{name}`' for name in fn_removed)}")
        if fn_sig_changed:
            details = ", ".join(
                f"`{name}` ({old_fn[name]} → {new_fn[name]})" for name in fn_sig_changed
            )
            module_lines.append(f"function signatures changed: {details}")
        if cls_added:
            module_lines.append(f"classes added: {', '.join(f'`{name}`' for name in cls_added)}")
        if cls_removed:
            module_lines.append(f"classes removed: {', '.join(f'`{name}`' for name in cls_removed)}")

        for class_name in sorted(set(old_cls) & set(new_cls)):
            old_methods = _names(old_cls[class_name].get("methods", []))
            new_methods = _names(new_cls[class_name].get("methods", []))
            if old_methods != new_methods:
                added_methods = sorted(new_methods - old_methods)
                removed_methods = sorted(old_methods - new_methods)
                if added_methods:
                    module_lines.append(
                        f"class `{class_name}` methods added: "
                        + ", ".join(f"`{name}`" for name in added_methods)
                    )
                if removed_methods:
                    module_lines.append(
                        f"class `{class_name}` methods removed: "
                        + ", ".join(f"`{name}`" for name in removed_methods)
                    )

        old_registry = (old_module.get("in_registry"), old_module.get("registry_id"))
        new_registry = (new_module.get("in_registry"), new_module.get("registry_id"))
        if old_registry != new_registry:
            registry_changes.append(
                f"`{path}`: in_registry `{old_registry[0]}` → `{new_registry[0]}`, "
                f"id `{old_registry[1]}` → `{new_registry[1]}`"
            )

        if module_lines:
            function_class_changes[path] = module_lines

    old_registry_entries = old_graph.get("registry_entries", {})
    new_registry_entries = new_graph.get("registry_entries", {})
    added_registry_ids = sorted(set(new_registry_entries) - set(old_registry_entries))
    removed_registry_ids = sorted(set(old_registry_entries) - set(new_registry_entries))
    changed_registry_ids = sorted(
        rid
        for rid in set(old_registry_entries) & set(new_registry_entries)
        if old_registry_entries[rid] != new_registry_entries[rid]
    )

    unexpected: list[str] = []
    if expected_prefixes:
        for path in changed_paths + added_paths + removed_paths:
            if not any(path.startswith(prefix) for prefix in expected_prefixes):
                unexpected.append(path)

    lines = ["# Snapshot Diff Summary", ""]
    lines.append("## Overall")
    lines.append(f"- **Old modules**: {len(old_paths)}")
    lines.append(f"- **New modules**: {len(new_paths)}")
    lines.append(f"- **Changed modules**: {len(changed_paths)}")
    lines.append(f"- **Added modules**: {len(added_paths)}")
    lines.append(f"- **Removed modules**: {len(removed_paths)}")

    lines.append("")
    lines.append("## Syntax error state changes")
    if syntax_fixed:
        lines.append("- **Fixed (error → valid)**: " + ", ".join(f"`{path}`" for path in syntax_fixed))
    if syntax_regressed:
        lines.append("- **Regressed (valid → error)**: " + ", ".join(f"`{path}`" for path in syntax_regressed))
    if not syntax_fixed and not syntax_regressed:
        lines.append("- No syntax error state changes detected.")

    lines.append("")
    lines.append("## Function/Class changes")
    if function_class_changes:
        for path in sorted(function_class_changes):
            lines.append(f"- `{path}`")
            for detail in function_class_changes[path]:
                lines.append(f"  - {detail}")
    else:
        lines.append("- No function/class deltas detected.")

    lines.append("")
    lines.append("## Registry coverage changes")
    if registry_changes:
        lines.extend(f"- {item}" for item in registry_changes)
    else:
        lines.append("- No per-module registry coverage changes detected.")

    if added_registry_ids:
        lines.append(
            "- Registry IDs added: "
            + ", ".join(f"`{rid}` → `{new_registry_entries[rid]}`" for rid in added_registry_ids)
        )
    if removed_registry_ids:
        lines.append(
            "- Registry IDs removed: "
            + ", ".join(f"`{rid}`" for rid in removed_registry_ids)
        )
    if changed_registry_ids:
        lines.append(
            "- Registry IDs remapped: "
            + ", ".join(
                f"`{rid}` (`{old_registry_entries[rid]}` → `{new_registry_entries[rid]}`)"
                for rid in changed_registry_ids
            )
        )

    lines.append("")
    lines.append("## Unexpected changes")
    if unexpected:
        lines.append(
            "- ⚠️ Changes outside expected prefixes detected: "
            + ", ".join(f"`{path}`" for path in sorted(set(unexpected)))
        )
    else:
        lines.append("- No unexpected module path changes detected.")

    return "\n".join(lines) + "\n", bool(unexpected)


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
    print(summary)

    if args.fail_on_unexpected and has_unexpected:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
