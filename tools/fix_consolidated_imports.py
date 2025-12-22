#!/usr/bin/env python3
"""
Fix Consolidated Imports
=========================

<!-- SSOT Domain: fixes -->

Resolves import conflicts from tool consolidation activities.
Scans for broken imports, identifies correct paths, and fixes them.

V2 Compliance: < 300 lines, single responsibility
Author: Agent-8 (SSOT & System Integration Specialist)
"""

import ast
import json
import logging
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ImportFixer:
    """Fixes import conflicts from tool consolidation."""

    def __init__(self, root_dir: Path, dry_run: bool = False):
        """Initialize fixer with root directory."""
        self.root_dir = Path(root_dir)
        self.dry_run = dry_run
        self.broken_imports: List[Dict] = []
        self.fixed_imports: List[Dict] = []
        self.module_map: Dict[str, Path] = {}

    def build_module_map(self) -> None:
        """Build map of module names to file paths."""
        logger.info("Building module path map...")
        for py_file in self.root_dir.rglob("*.py"):
            if any(
                exclude in str(py_file)
                for exclude in ["__pycache__", ".venv", "venv", ".git"]
            ):
                continue
            try:
                rel_path = py_file.relative_to(self.root_dir)
                module_parts = str(rel_path).replace("\\", "/").replace(".py", "").split("/")
                # Create multiple possible import paths
                for i in range(len(module_parts)):
                    module_name = ".".join(module_parts[i:])
                    if module_name and module_name not in self.module_map:
                        self.module_map[module_name] = py_file
            except Exception as e:
                logger.debug(f"Error mapping {py_file}: {e}")

    def find_broken_imports(self) -> None:
        """Find broken imports by attempting to parse files."""
        logger.info("Scanning for broken imports...")
        python_files = list(self.root_dir.rglob("*.py"))
        logger.info(f"Scanning {len(python_files)} Python files")

        for file_path in python_files:
            if any(
                exclude in str(file_path)
                for exclude in [
                    "__pycache__",
                    ".venv",
                    "venv",
                    ".git",
                    "migrations",
                    "temp_repos",
                ]
            ):
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                tree = ast.parse(content, filename=str(file_path))
                self._check_imports_in_tree(file_path, tree, content)
            except SyntaxError as e:
                # Syntax errors might indicate import issues
                logger.debug(f"Syntax error in {file_path}: {e}")
            except Exception as e:
                logger.debug(f"Error parsing {file_path}: {e}")

    def _check_imports_in_tree(
        self, file_path: Path, tree: ast.AST, content: str
    ) -> None:
        """Check imports in AST tree."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._check_import(file_path, alias.name, None, content)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self._check_import(file_path, node.module, node.level, content)

    def _check_import(
        self, file_path: Path, import_name: str, level: Optional[int], content: str
    ) -> None:
        """Check if import is broken and find fix."""
        # Skip standard library and known good imports
        if import_name.split(".")[0] in [
            "sys",
            "os",
            "json",
            "logging",
            "pathlib",
            "typing",
            "datetime",
            "collections",
            "re",
            "subprocess",
            "ast",
        ]:
            return

        # Check if module exists in our map
        if import_name not in self.module_map:
            # Try to find alternative path
            alternative = self._find_alternative_import(import_name)
            if alternative:
                self.broken_imports.append(
                    {
                        "file": str(file_path.relative_to(self.root_dir)),
                        "import": import_name,
                        "level": level,
                        "suggested_fix": alternative,
                    }
                )

    def _find_alternative_import(self, import_name: str) -> Optional[str]:
        """Find alternative import path for broken import."""
        # Try partial matches
        parts = import_name.split(".")
        for i in range(len(parts), 0, -1):
            partial = ".".join(parts[:i])
            if partial in self.module_map:
                remaining = ".".join(parts[i:])
                if remaining:
                    return f"{partial}.{remaining}"
                return partial
        return None

    def fix_imports(self) -> None:
        """Fix broken imports in files."""
        logger.info(f"Fixing {len(self.broken_imports)} broken imports...")

        for issue in self.broken_imports:
            file_path = self.root_dir / issue["file"]
            if not file_path.exists():
                continue

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                old_import = issue["import"]
                new_import = issue["suggested_fix"]

                # Replace import statements
                patterns = [
                    (rf"from\s+{re.escape(old_import)}\s+import", f"from {new_import} import"),
                    (rf"import\s+{re.escape(old_import)}\b", f"import {new_import}"),
                ]

                modified = False
                for pattern, replacement in patterns:
                    if re.search(pattern, content):
                        content = re.sub(pattern, replacement, content)
                        modified = True

                if modified and not self.dry_run:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    self.fixed_imports.append(
                        {
                            "file": issue["file"],
                            "old_import": old_import,
                            "new_import": new_import,
                        }
                    )
                    logger.info(f"✅ Fixed import in {issue['file']}")
                elif modified:
                    logger.info(f"🔍 Would fix import in {issue['file']} (dry-run)")

            except Exception as e:
                logger.error(f"❌ Failed to fix {issue['file']}: {e}")

    def validate_fixes(self) -> bool:
        """Validate that fixes work by checking syntax."""
        logger.info("Validating fixes...")
        all_valid = True

        for fix in self.fixed_imports:
            file_path = self.root_dir / fix["file"]
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                logger.warning(f"⚠️ Syntax error in {fix['file']}: {e}")
                all_valid = False
            except Exception as e:
                logger.warning(f"⚠️ Error validating {fix['file']}: {e}")
                all_valid = False

        return all_valid

    def generate_report(self, output_file: Path) -> None:
        """Generate fix report."""
        logger.info(f"Generating report: {output_file}")

        report = {
            "timestamp": datetime.now().isoformat(),
            "dry_run": self.dry_run,
            "summary": {
                "broken_imports_found": len(self.broken_imports),
                "imports_fixed": len(self.fixed_imports),
            },
            "broken_imports": self.broken_imports,
            "fixed_imports": self.fixed_imports,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Generate markdown report
        md_report = output_file.with_suffix(".md")
        with open(md_report, "w", encoding="utf-8") as f:
            f.write("# Consolidated Imports Fix Report\n\n")
            f.write(f"**Generated**: {report['timestamp']}\n")
            f.write(f"**Dry Run**: {report['dry_run']}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- **Broken Imports Found**: {report['summary']['broken_imports_found']}\n")
            f.write(f"- **Imports Fixed**: {report['summary']['imports_fixed']}\n\n")

            if self.fixed_imports:
                f.write("## Fixed Imports\n\n")
                for fix in self.fixed_imports:
                    f.write(f"- **{fix['file']}**\n")
                    f.write(f"  - Old: `{fix['old_import']}`\n")
                    f.write(f"  - New: `{fix['new_import']}`\n\n")

        logger.info(f"✅ Report generated: {output_file}")

    def run_fix(self) -> int:
        """Run complete fix process."""
        logger.info("Starting consolidated imports fix...")
        try:
            self.build_module_map()
            self.find_broken_imports()
            self.fix_imports()

            if self.fixed_imports:
                is_valid = self.validate_fixes()
                if not is_valid:
                    logger.warning("⚠️ Some fixes may have introduced errors")

            report_file = self.root_dir / "reports" / "consolidated_imports_fix_report.json"
            report_file.parent.mkdir(parents=True, exist_ok=True)
            self.generate_report(report_file)

            if self.fixed_imports:
                logger.info(f"✅ Fixed {len(self.fixed_imports)} imports")
                return 0
            else:
                logger.info("✅ No import fixes needed")
                return 0

        except Exception as e:
            logger.error(f"❌ Fix process failed: {e}")
            return 1


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Fix consolidated imports")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be fixed without making changes"
    )
    args = parser.parse_args()

    root_dir = Path(__file__).parent.parent
    fixer = ImportFixer(root_dir, dry_run=args.dry_run)
    return fixer.run_fix()


if __name__ == "__main__":
    sys.exit(main())


