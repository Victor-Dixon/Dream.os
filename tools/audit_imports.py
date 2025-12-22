#!/usr/bin/env python3
"""
Import Dependency Auditor
=========================

<!-- SSOT Domain: validation -->

Comprehensive import dependency analysis tool that:
- Detects circular dependencies
- Validates importlinter contracts
- Checks SSOT boundary compliance
- Generates detailed reports

V2 Compliance: < 300 lines, single responsibility
Author: Agent-8 (SSOT & System Integration Specialist)
"""

import ast
import json
import logging
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImportAuditor:
    """Audits import dependencies across the codebase."""

    def __init__(self, root_dir: Path):
        """Initialize auditor with root directory."""
        self.root_dir = Path(root_dir)
        self.imports_map: Dict[str, Set[str]] = defaultdict(set)
        self.circular_deps: List[List[str]] = []
        self.importlinter_violations: List[Dict] = []
        self.ssot_violations: List[Dict] = []

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the codebase."""
        python_files = []
        for path in self.root_dir.rglob("*.py"):
            # Skip common exclusions
            if any(
                exclude in str(path)
                for exclude in [
                    "__pycache__",
                    ".venv",
                    "venv",
                    "node_modules",
                    ".git",
                    "migrations",
                ]
            ):
                continue
            python_files.append(path)
        return python_files

    def extract_imports(self, file_path: Path) -> Set[str]:
        """Extract import statements from a Python file."""
        imports = set()
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])
        except Exception as e:
            logger.warning(f"Failed to parse {file_path}: {e}")
        return imports

    def build_import_graph(self) -> None:
        """Build import dependency graph."""
        logger.info("Building import dependency graph...")
        python_files = self.find_python_files()
        logger.info(f"Found {len(python_files)} Python files")

        for file_path in python_files:
            rel_path = str(file_path.relative_to(self.root_dir))
            module_name = rel_path.replace("/", ".").replace("\\", ".").replace(
                ".py", ""
            )
            imports = self.extract_imports(file_path)
            self.imports_map[module_name] = imports

    def detect_circular_dependencies(self) -> None:
        """Detect circular dependencies using DFS."""
        logger.info("Detecting circular dependencies...")

        def dfs(
            node: str,
            path: List[str],
            visited: Set[str],
            rec_stack: Set[str],
        ) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.imports_map.get(node, set()):
                # Check if neighbor is in current path (circular)
                if neighbor in rec_stack and neighbor in self.imports_map:
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in self.circular_deps:
                        self.circular_deps.append(cycle)
                elif neighbor not in visited and neighbor in self.imports_map:
                    dfs(neighbor, path.copy(), visited, rec_stack)

            rec_stack.remove(node)

        visited = set()
        for module in self.imports_map:
            if module not in visited:
                dfs(module, [], visited, set())

    def check_importlinter(self) -> None:
        """Check importlinter contracts if available."""
        logger.info("Checking importlinter contracts...")
        importlinter_config = self.root_dir / "importlinter.ini"

        if not importlinter_config.exists():
            logger.warning("importlinter.ini not found, skipping contract checks")
            return

        try:
            result = subprocess.run(
                ["importlinter", "--config", str(importlinter_config)],
                capture_output=True,
                text=True,
                cwd=self.root_dir,
            )
            if result.returncode != 0:
                # Parse violations from output
                for line in result.stdout.split("\n"):
                    if "violates" in line.lower() or "broken" in line.lower():
                        self.importlinter_violations.append({"message": line})
        except FileNotFoundError:
            logger.warning("importlinter not installed, skipping contract checks")
        except Exception as e:
            logger.error(f"Error running importlinter: {e}")

    def check_ssot_boundaries(self) -> None:
        """Check SSOT boundary violations in import patterns."""
        logger.info("Checking SSOT boundary compliance...")

        # SSOT boundary rules from architecture
        forbidden_patterns = [
            ("src.utils", "src.services"),  # Utils cannot import services
            ("src.utils", "src.core"),  # Utils cannot import core
        ]

        for module, imports in self.imports_map.items():
            for import_name in imports:
                for forbidden_source, forbidden_target in forbidden_patterns:
                    if (
                        module.startswith(forbidden_source)
                        and import_name.startswith(forbidden_target)
                    ):
                        self.ssot_violations.append(
                            {
                                "module": module,
                                "import": import_name,
                                "violation": f"{forbidden_source} cannot import from {forbidden_target}",
                            }
                        )

    def generate_report(self, output_file: Path) -> None:
        """Generate comprehensive audit report."""
        logger.info(f"Generating report: {output_file}")

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_modules": len(self.imports_map),
                "circular_dependencies": len(self.circular_deps),
                "importlinter_violations": len(self.importlinter_violations),
                "ssot_violations": len(self.ssot_violations),
            },
            "circular_dependencies": [
                " -> ".join(cycle) for cycle in self.circular_deps
            ],
            "importlinter_violations": self.importlinter_violations,
            "ssot_violations": self.ssot_violations,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Also generate markdown report
        md_report = output_file.with_suffix(".md")
        self._generate_markdown_report(md_report, report)

        logger.info(f"✅ Report generated: {output_file}")
        logger.info(f"✅ Markdown report: {md_report}")

    def _generate_markdown_report(self, output_file: Path, report: Dict) -> None:
        """Generate markdown format report."""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("# Import Dependency Audit Report\n\n")
            f.write(f"**Generated**: {report['timestamp']}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Total Modules Analyzed**: {report['summary']['total_modules']}\n")
            f.write(
                f"- **Circular Dependencies**: {report['summary']['circular_dependencies']}\n"
            )
            f.write(
                f"- **Importlinter Violations**: {report['summary']['importlinter_violations']}\n"
            )
            f.write(
                f"- **SSOT Violations**: {report['summary']['ssot_violations']}\n\n"
            )

            if report["circular_dependencies"]:
                f.write("## Circular Dependencies\n\n")
                for cycle in report["circular_dependencies"]:
                    f.write(f"- `{cycle}`\n")
                f.write("\n")

            if report["ssot_violations"]:
                f.write("## SSOT Boundary Violations\n\n")
                for violation in report["ssot_violations"]:
                    f.write(
                        f"- **{violation['module']}** imports **{violation['import']}**\n"
                    )
                    f.write(f"  - Violation: {violation['violation']}\n\n")

    def run_audit(self) -> int:
        """Run complete audit process."""
        logger.info("Starting import dependency audit...")
        try:
            self.build_import_graph()
            self.detect_circular_dependencies()
            self.check_importlinter()
            self.check_ssot_boundaries()

            report_file = self.root_dir / "reports" / "import_audit_report.json"
            report_file.parent.mkdir(parents=True, exist_ok=True)
            self.generate_report(report_file)

            # Return exit code based on findings
            if (
                self.circular_deps
                or self.importlinter_violations
                or self.ssot_violations
            ):
                logger.warning("⚠️ Import issues found - see report for details")
                return 1
            else:
                logger.info("✅ No import issues found")
                return 0
        except Exception as e:
            logger.error(f"❌ Audit failed: {e}")
            return 1


def main() -> int:
    """Main entry point."""
    root_dir = Path(__file__).parent.parent
    auditor = ImportAuditor(root_dir)
    return auditor.run_audit()


if __name__ == "__main__":
    sys.exit(main())


