#!/usr/bin/env python3
"""
SSOT (Single Source of Truth) Linter
===================================

Enforces SSOT principles by checking:
- No imports of deprecated files
- Proper use of canonical paths
- Documentation references updated
- SSOT headers present where required

Integrates with CI/CD pipeline to prevent SSOT violations.

Author: Agent-4 (Captain) - SSOT Enforcement Specialist
"""

import sys
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# SSOT mappings - canonical locations for functionality
SSOT_MAPPINGS = {
    # Deploy scripts -> MCP deployment server
    "scripts/deploy_via_wordpress_admin": "mcp_servers/deployment_server",
    "tools/deploy_tradingrobotplug_plugin": "mcp_servers/deployment_server",
    "tools/deploy_tradingrobotplug_plugin_phase3": "mcp_servers/deployment_server",
    "tools/deploy_fastapi_tradingrobotplug": "mcp_servers/deployment_server",
    "tools/deploy_weareswarm_feed_system": "mcp_servers/deployment_server",
    "tools/deploy_weareswarm_font_fix": "mcp_servers/deployment_server",
    "tools/deploy_tradingrobotplug_font_fix": "mcp_servers/deployment_server",

    # WordPress management -> WP-CLI server
    "tools/wordpress_manager": "mcp_servers/wp_cli_manager_server",

    # Deployment utilities -> deployment server
    "ops/deployment/simple_wordpress_deployer": "mcp_servers/deployment_server",
}

# Files that should have SSOT headers
REQUIRES_SSOT_HEADER = {
    "src/control_plane/adapters/hostinger/*.py",  # Adapter consolidation
    "src/web/static/js/services/deployment-*.js",  # Frontend consolidation
    "scripts/site_management/sync_*.py",  # Theme sync consolidation
}

class SSOTViolation:
    """Represents an SSOT violation."""

    def __init__(self, file_path: Path, violation_type: str, message: str,
                 line_number: Optional[int] = None, suggestion: Optional[str] = None):
        self.file_path = file_path
        self.violation_type = violation_type
        self.message = message
        self.line_number = line_number
        self.suggestion = suggestion

    def __str__(self) -> str:
        location = f"{self.file_path}"
        if self.line_number:
            location += f":{self.line_number}"

        result = f"{self.violation_type}: {location}\n  {self.message}"
        if self.suggestion:
            result += f"\n  💡 {self.suggestion}"
        return result

class SSOTLinter:
    """SSOT compliance checker."""

    def __init__(self):
        self.violations: List[SSOTViolation] = []

    def check_file(self, file_path: Path) -> None:
        """Check a single file for SSOT violations."""
        if file_path.suffix == ".py":
            self._check_python_file(file_path)
        elif file_path.suffix in [".md", ".txt"]:
            self._check_documentation_file(file_path)
        elif file_path.suffix == ".js":
            self._check_javascript_file(file_path)

    def _check_python_file(self, file_path: Path) -> None:
        """Check Python file for SSOT violations."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for deprecated imports
            self._check_deprecated_imports(file_path, content)

            # Check for SSOT header requirements
            self._check_ssot_header_requirement(file_path, content)

            # Parse AST for import analysis
            try:
                tree = ast.parse(content)
                self._analyze_python_imports(file_path, tree)
            except SyntaxError:
                # File has syntax errors - already caught by other checks
                pass

        except (OSError, UnicodeDecodeError) as e:
            self.violations.append(SSOTViolation(
                file_path, "FILE_ERROR",
                f"Could not read file: {e}"
            ))

    def _check_deprecated_imports(self, file_path: Path, content: str) -> None:
        """Check for imports of deprecated modules."""
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            line = line.strip()

            # Check import statements
            if line.startswith(('import ', 'from ')):
                for deprecated, canonical in SSOT_MAPPINGS.items():
                    if deprecated in line:
                        # Extract the actual import path
                        if 'from ' in line:
                            imported_module = line.split('from ')[1].split(' import ')[0].strip()
                        else:
                            imported_module = line.split('import ')[1].split(' as ')[0].strip()

                        if deprecated in imported_module:
                            self.violations.append(SSOTViolation(
                                file_path, "DEPRECATED_IMPORT",
                                f"Importing deprecated module: {imported_module}",
                                i,
                                f"Use: from {canonical} import ..."
                            ))

    def _check_ssot_header_requirement(self, file_path: Path, content: str) -> None:
        """Check if file requires SSOT header and has it."""
        file_str = str(file_path)

        for pattern in REQUIRES_SSOT_HEADER:
            if "*" in pattern:
                # Convert glob pattern to regex
                regex_pattern = pattern.replace("*", ".*")
                if re.match(regex_pattern, file_str):
                    if "⚠️ DEPRECATED" not in content:
                        self.violations.append(SSOTViolation(
                            file_path, "MISSING_SSOT_HEADER",
                            f"File matches SSOT consolidation pattern but lacks deprecation header",
                            suggestion="Add proper SSOT deprecation header"
                        ))
                    break

    def _analyze_python_imports(self, file_path: Path, tree: ast.AST) -> None:
        """Analyze Python AST for import patterns."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    self._check_import_violation(file_path, module_name, node.lineno)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    module_name = node.module
                    self._check_import_violation(file_path, module_name, node.lineno)

    def _check_import_violation(self, file_path: Path, module_name: str, line_number: int) -> None:
        """Check if import violates SSOT rules."""
        for deprecated, canonical in SSOT_MAPPINGS.items():
            if module_name.startswith(deprecated) or deprecated in module_name:
                self.violations.append(SSOTViolation(
                    file_path, "SSOT_VIOLATION",
                    f"Importing from deprecated module: {module_name}",
                    line_number,
                    f"Import from canonical location: {canonical}"
                ))

    def _check_documentation_file(self, file_path: Path) -> None:
        """Check documentation files for outdated references."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                for deprecated in SSOT_MAPPINGS.keys():
                    # Look for file path references in docs
                    if f"`{deprecated}" in line or f"{deprecated}`" in line:
                        if "deprecated" not in line.lower() and "replacement" not in line.lower():
                            self.violations.append(SSOTViolation(
                                file_path, "OUTDATED_DOC_REFERENCE",
                                f"Documentation references deprecated path: {deprecated}",
                                i,
                                f"Update to reference canonical path: {SSOT_MAPPINGS[deprecated]}"
                            ))

        except (OSError, UnicodeDecodeError):
            pass  # Skip files that can't be read

    def _check_javascript_file(self, file_path: Path) -> None:
        """Check JavaScript files for SSOT compliance."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for SSOT header requirements
            file_str = str(file_path)
            for pattern in REQUIRES_SSOT_HEADER:
                if "*" in pattern and "js" in pattern:
                    regex_pattern = pattern.replace("*", ".*")
                    if re.match(regex_pattern, file_str):
                        if "DEPRECATED" not in content:
                            self.violations.append(SSOTViolation(
                                file_path, "MISSING_SSOT_HEADER",
                                "JavaScript file in consolidation scope lacks deprecation header",
                                suggestion="Add SSOT deprecation comment"
                            ))
                        break

        except (OSError, UnicodeDecodeError):
            pass

    def scan_repository(self, root_path: Path) -> None:
        """Scan entire repository for SSOT violations."""
        print("🔍 Scanning repository for SSOT violations...")

        skip_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules", "logs"}

        file_count = 0
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip certain directories
            if any(part in skip_dirs for part in file_path.parts):
                continue

            # Only check relevant file types
            if file_path.suffix.lower() not in [".py", ".md", ".txt", ".js", ".ts"]:
                continue

            file_count += 1
            if file_count % 200 == 0:
                print(f"  Checked {file_count} files...")

            self.check_file(file_path)

        print(f"✅ Scanned {file_count} files")

def main() -> int:
    """Main SSOT linting function."""
    print("🎯 SSOT Linter Check")
    print("=" * 30)

    repo_root = Path(".")
    linter = SSOTLinter()

    linter.scan_repository(repo_root)

    if linter.violations:
        print(f"❌ FAILED: Found {len(linter.violations)} SSOT violations!")
        print()

        # Group violations by type
        violations_by_type = {}
        for violation in linter.violations:
            violations_by_type.setdefault(violation.violation_type, []).append(violation)

        for violation_type, violations in violations_by_type.items():
            print(f"🚫 {violation_type}: {len(violations)} violations")
            # Show first 3 examples
            for violation in violations[:3]:
                print(f"   {violation}")
            if len(violations) > 3:
                print(f"   ... and {len(violations) - 3} more")
            print()

        print("💡 To resolve:")
        print("   1. Update imports to use canonical SSOT locations")
        print("   2. Add SSOT deprecation headers where required")
        print("   3. Update documentation references")
        print("   4. See docs/SSOT_MAP.md for guidance")

        return 1
    else:
        print("✅ PASSED: No SSOT violations found!")
        print("   All imports use canonical locations")
        print("   All required SSOT headers present")
        print("   Documentation references updated")

        return 0

if __name__ == "__main__":
    sys.exit(main())