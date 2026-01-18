"""Dead code analysis for the audit harness (SSOT)."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict


def find_dead_code(project_root: Path, timestamp: str, root: str, output_file: str) -> Dict[str, Any]:
    """Find potential dead code candidates."""
    print("💀 Analyzing potential dead code...")

    analysis: Dict[str, Any] = {
        "timestamp": timestamp,
        "command": f"python tools/audit_harness.py dead --root {root} --out {output_file}",
        "root": root,
        "candidates": [],
    }

    root_path = project_root / root
    if not root_path.exists():
        print(f"⚠️ Root {root} does not exist")
        return analysis

    all_files = list(root_path.rglob("*.py"))

    defined_symbols = defaultdict(set)
    imported_symbols = defaultdict(set)

    for py_file in all_files:
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as handle:
                content = handle.read()

            for match in re.finditer(r"^(?:class|def)\s+(\w+)", content, re.MULTILINE):
                symbol = match.group(1)
                defined_symbols[symbol].add(str(py_file.relative_to(project_root)))

            for match in re.finditer(
                r"^(?:from\s+\w+\s+import|import)\s+(.+)$",
                content,
                re.MULTILINE,
            ):
                imports = match.group(1)
                for symbol in re.findall(r"\b\w+\b", imports):
                    if len(symbol) > 2:
                        imported_symbols[symbol].add(str(py_file.relative_to(project_root)))

        except OSError as exc:
            print(f"⚠️ Error analyzing {py_file}: {exc}")

    candidates = []
    for symbol, definition_files in defined_symbols.items():
        if symbol not in imported_symbols and symbol not in {"__init__", "__main__", "main"}:
            for def_file in definition_files:
                candidates.append(
                    {
                        "symbol": symbol,
                        "file": def_file,
                        "reason": "not imported anywhere in codebase",
                    }
                )

    file_imports = defaultdict(set)
    for py_file in all_files:
        file_name = py_file.stem
        if file_name in imported_symbols:
            file_imports[file_name] = imported_symbols[file_name]

    for py_file in all_files:
        file_name = py_file.stem
        if file_name not in file_imports and file_name not in {"__init__", "__main__"}:
            candidates.append(
                {
                    "symbol": f"module:{file_name}",
                    "file": str(py_file.relative_to(project_root)),
                    "reason": "module never imported",
                }
            )

    analysis["candidates"] = candidates[:50]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Dead Code Candidates - Generated {timestamp}\n")
        handle.write(f"# Command: {analysis['command']}\n")
        handle.write(f"# Root: {root}\n")
        handle.write(f"# Candidates found: {len(candidates)}\n\n")

        for i, candidate in enumerate(analysis["candidates"], 1):
            handle.write(f"{i}. {candidate['file']}:{candidate['symbol']}\n")
            handle.write(f"   Reason: {candidate['reason']}\n\n")

    print(f"✅ Dead code analysis saved to {output_file}")
    print(f"   Candidates found: {len(candidates)}")

    return analysis
