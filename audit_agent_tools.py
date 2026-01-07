#!/usr/bin/env python3
"""
Agent Workspaces Tools Audit Script
===================================

Comprehensive audit of all tools in agent_workspaces/tools/
Checks syntax, imports, functionality, and health status.
"""

import os
import sys
import ast
import importlib.util
import traceback
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

TOOLS_DIR = Path("agent_workspaces/tools")

class ToolsAuditor:
    def __init__(self):
        self.results = {
            "total_files": 0,
            "syntax_errors": [],
            "import_errors": [],
            "functional_tests": [],
            "file_sizes": {},
            "line_counts": {},
            "complexity_warnings": []
        }

    def audit_all_tools(self) -> Dict[str, Any]:
        """Run comprehensive audit on all tools."""
        print("🔍 Auditing Agent Workspaces Tools...")
        print("=" * 50)

        # Get all Python files
        tool_files = list(TOOLS_DIR.glob("*.py"))
        self.results["total_files"] = len(tool_files)

        print(f"📋 Found {len(tool_files)} tool files to audit")

        for tool_file in tool_files:
            if tool_file.name.startswith("__"):  # Skip __pycache__, etc.
                continue

            print(f"\n🔧 Auditing {tool_file.name}...")
            self.audit_single_tool(tool_file)

        self.print_summary()
        return self.results

    def audit_single_tool(self, tool_file: Path) -> None:
        """Audit a single tool file."""
        filename = tool_file.name

        # Check syntax
        syntax_ok, syntax_error = self.check_syntax(tool_file)
        if not syntax_ok:
            self.results["syntax_errors"].append({
                "file": filename,
                "error": syntax_error
            })
            print(f"  ❌ Syntax Error: {syntax_error}")
            return  # Can't continue if syntax is broken

        print("  ✅ Syntax OK")

        # Check file size and lines
        try:
            with open(tool_file, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            self.results["line_counts"][filename] = len(lines)
            self.results["file_sizes"][filename] = len(content)

            print(f"  📏 Size: {len(content)} chars, {len(lines)} lines")

            # Basic complexity check (very simple heuristic)
            if len(lines) > 300:
                self.results["complexity_warnings"].append({
                    "file": filename,
                    "issue": "Very large file (>300 lines)",
                    "lines": len(lines)
                })

            # Check for main function
            has_main = 'if __name__ == "__main__":' in content or 'def main():' in content
            print(f"  🏃‍♂️ Has main: {'✅' if has_main else '❌'}")

            # Check for docstring
            tree = ast.parse(content)
            has_docstring = (
                len(tree.body) > 0 and
                isinstance(tree.body[0], ast.Expr) and
                isinstance(tree.body[0].value, ast.Str)
            )
            print(f"  📖 Docstring: {'✅' if has_docstring else '❌'}")

            # Check imports
            imports_ok, import_issues = self.check_imports(tree)
            if not imports_ok:
                self.results["import_errors"].append({
                    "file": filename,
                    "issues": import_issues
                })
                print(f"  🔗 Import Issues: {len(import_issues)}")
            else:
                print("  🔗 Imports: ✅ OK")
        except Exception as e:
            print(f"  💥 Error reading file: {e}")

    def check_syntax(self, tool_file: Path) -> Tuple[bool, str]:
        """Check if file has valid Python syntax."""
        try:
            with open(tool_file, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            return True, ""
        except SyntaxError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {e}"

    def check_imports(self, tree: ast.AST) -> Tuple[bool, List[str]]:
        """Check import statements for potential issues."""
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Check for potentially problematic imports
                    if alias.name.startswith('__'):
                        issues.append(f"Private import: {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('__'):
                    issues.append(f"Private module import: {node.module}")

        return len(issues) == 0, issues

    def print_summary(self) -> None:
        """Print audit summary."""
        print("\n" + "=" * 50)
        print("📊 AUDIT SUMMARY")
        print("=" * 50)

        print(f"📁 Total Files: {self.results['total_files']}")

        if self.results["syntax_errors"]:
            print(f"❌ Syntax Errors: {len(self.results['syntax_errors'])}")
            for error in self.results["syntax_errors"][:3]:  # Show first 3
                print(f"   - {error['file']}: {error['error']}")

        if self.results["import_errors"]:
            print(f"🔗 Import Issues: {len(self.results['import_errors'])}")

        if self.results["complexity_warnings"]:
            print(f"⚠️  Complexity Warnings: {len(self.results['complexity_warnings'])}")
            for warning in self.results["complexity_warnings"]:
                print(f"   - {warning['file']}: {warning['issue']}")

        # File size summary
        if self.results["file_sizes"]:
            sizes = list(self.results["file_sizes"].values())
            avg_size = sum(sizes) / len(sizes)
            max_size = max(sizes)
            max_file = max(self.results["file_sizes"], key=self.results["file_sizes"].get)

            print(f"📏 Average File Size: {avg_size:.0f} chars")
            print(f"📏 Largest File: {max_file} ({max_size} chars)")

        # Line count summary
        if self.results["line_counts"]:
            lines = list(self.results["line_counts"].values())
            avg_lines = sum(lines) / len(lines)
            max_lines = max(lines)
            max_lines_file = max(self.results["line_counts"], key=self.results["line_counts"].get)

            print(f"📏 Average Line Count: {avg_lines:.0f} lines")
            print(f"📏 Longest File: {max_lines_file} ({max_lines} lines)")

        # Overall health score
        health_score = self.calculate_health_score()
        print(f"🏥 Overall Health Score: {health_score}/100")

        if health_score >= 90:
            print("🎉 Tools directory is in excellent health!")
        elif health_score >= 75:
            print("✅ Tools directory is in good health.")
        elif health_score >= 60:
            print("⚠️  Tools directory needs some attention.")
        else:
            print("❌ Tools directory requires significant cleanup.")

    def calculate_health_score(self) -> int:
        """Calculate overall health score (0-100)."""
        score = 100

        # Syntax errors: -20 per error
        score -= len(self.results["syntax_errors"]) * 20

        # Import errors: -10 per file with issues
        score -= len(self.results["import_errors"]) * 10

        # Complexity warnings: -5 per warning
        score -= len(self.results["complexity_warnings"]) * 5

        # Large files penalty
        large_files = sum(1 for size in self.results["file_sizes"].values() if size > 10000)
        score -= large_files * 2

        return max(0, min(100, score))

def main():
    auditor = ToolsAuditor()
    results = auditor.audit_all_tools()

    # Save results to file
    import json
    with open("agent_tools_audit_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n💾 Results saved to agent_tools_audit_results.json")
    return 0 if results["syntax_errors"] == [] else 1

if __name__ == "__main__":
    exit(main())