"""Import analysis for the audit harness (SSOT)."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict


def analyze_imports(project_root: Path, timestamp: str, root: str, output_file: str) -> Dict[str, Any]:
    """Analyze import relationships."""
    print("🔗 Analyzing import relationships...")

    analysis: Dict[str, Any] = {
        "timestamp": timestamp,
        "command": f"python tools/audit_harness.py imports --root {root} --out {output_file}",
        "root": root,
        "import_graph": {},
        "orphan_modules": [],
    }

    root_path = project_root / root
    if not root_path.exists():
        print(f"⚠️ Root {root} does not exist")
        return analysis

    all_files = list(root_path.rglob("*.py"))

    imports_from = defaultdict(set)
    imported_by = defaultdict(set)

    for py_file in all_files:
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as handle:
                content = handle.read()

            file_path = str(py_file.relative_to(project_root))

            for match in re.finditer(r"^from\s+([\w.]+)\s+import", content, re.MULTILINE):
                imported_module = match.group(1)
                imports_from[file_path].add(imported_module)
                imported_by[imported_module].add(file_path)

            for match in re.finditer(r"^import\s+([\w.]+)", content, re.MULTILINE):
                imported_module = match.group(1)
                imports_from[file_path].add(imported_module)
                imported_by[imported_module].add(file_path)

        except OSError as exc:
            print(f"⚠️ Error analyzing imports in {py_file}: {exc}")

    analysis["import_graph"] = {
        "imports_from": dict(imports_from),
        "imported_by": dict(imported_by),
    }

    all_modules = set()
    for py_file in all_files:
        module_path = str(py_file.relative_to(project_root))
        module_name = module_path.replace(".py", "").replace("/", ".")
        all_modules.add(module_name)

    orphan_modules = []
    for module in all_modules:
        if module not in imported_by and not module.endswith(".__init__"):
            if not any(m.startswith(module + ".") for m in imported_by):
                orphan_modules.append(module)

    analysis["orphan_modules"] = sorted(orphan_modules)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Import Analysis - Generated {timestamp}\n")
        handle.write(f"# Command: {analysis['command']}\n")
        handle.write(f"# Root: {root}\n\n")

        handle.write("## Orphan Modules (not imported anywhere)\n")
        for module in analysis["orphan_modules"][:20]:
            handle.write(f"- {module}\n")
        handle.write(f"\nTotal orphans: {len(analysis['orphan_modules'])}\n\n")

        handle.write("## Import Graph Summary\n")
        handle.write(f"- Modules analyzed: {len(all_modules)}\n")
        handle.write(
            f"- Import relationships: {sum(len(rels) for rels in imports_from.values())}\n"
        )
        handle.write(f"- Modules with imports: {len([m for m in imports_from.values() if m])}\n")

    print(f"✅ Import analysis saved to {output_file}")
    print(f"   Orphan modules: {len(analysis['orphan_modules'])}")

    return analysis
