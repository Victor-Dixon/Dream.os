# Header-Variant: full
# Owner: Dream.os Platform
# Purpose: Query helper for knowledge graph inspection.
# SSOT: docs/recovery/recovery_registry.yaml

"""Run ad-hoc queries against a generated knowledge graph.

Usage examples:
    python scripts/graph_query.py --graph knowledge_graph/latest.json --list-syntax-errors
    python scripts/graph_query.py --graph knowledge_graph/latest.json --find-module src/core/error_handling.py
    python scripts/graph_query.py --graph knowledge_graph/latest.json --registry-gaps
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_graph(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Query knowledge graph")
    parser.add_argument("--graph", type=Path, required=True)
    parser.add_argument("--list-syntax-errors", action="store_true")
    parser.add_argument("--find-module", help="Exact module path")
    parser.add_argument("--registry-gaps", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    graph = _load_graph(args.graph)
    modules = graph.get("modules", {})

    if args.list_syntax_errors:
        paths = sorted(path for path, data in modules.items() if data.get("has_syntax_error"))
        print("\n".join(paths) if paths else "No syntax errors detected.")

    if args.find_module:
        module = modules.get(args.find_module)
        if module is None:
            print(f"Module not found: {args.find_module}")
            return 1
        print(json.dumps(module, indent=2))

    if args.registry_gaps:
        gaps = sorted(path for path, data in modules.items() if not data.get("in_registry"))
        print("\n".join(gaps) if gaps else "No registry gaps detected.")

    if not (args.list_syntax_errors or args.find_module or args.registry_gaps):
        print("No query option selected. Use --help.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
