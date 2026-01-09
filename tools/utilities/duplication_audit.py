#!/usr/bin/env python3
"""
Duplication Audit Tool for Session Closures
===========================================

Helps agents identify potential duplication and audit their work before closure.

Usage:
    python tools/duplication_audit.py --agent Agent-X [--scope path/to/scope]

This tool:
1. Searches for TODO/FIXME items that might be redundant
2. Identifies potential duplicate implementations
3. Checks for incomplete work (broken imports, unfinished features)
4. Generates audit report for session closure
"""

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Set


class DuplicationAuditor:
    """Audits codebase for potential duplication and incomplete work."""

    def __init__(self, scope_path: str = "."):
        self.scope_path = Path(scope_path)
        self.findings = {
            "redundant_todos": [],
            "potential_duplicates": [],
            "incomplete_work": [],
            "broken_imports": []
        }

    def audit_todos_and_fixmes(self) -> None:
        """Find TODO/FIXME items that might be redundant."""
        todo_pattern = re.compile(r'#\s*(TODO|FIXME|XXX).*', re.IGNORECASE)

        for file_path in self.scope_path.rglob("*.py"):
            if self._should_skip_file(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for line_num, line in enumerate(lines, 1):
                    if todo_pattern.search(line):
                        self.findings["redundant_todos"].append({
                            "file": str(file_path),
                            "line": line_num,
                            "content": line.strip(),
                            "suggestion": "Review if this TODO is still needed after recent changes"
                        })
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

    def audit_duplicate_implementations(self) -> None:
        """Find potential duplicate implementations."""
        # Common patterns that might indicate duplication
        patterns = [
            (r'class.*Service.*:', 'Service classes'),
            (r'def.*_handler.*:', 'Handler functions'),
            (r'from.*import.*', 'Import statements'),
            (r'class.*Client.*:', 'Client classes'),
            (r'class.*Manager.*:', 'Manager classes'),
        ]

        implementations = {}

        for file_path in self.scope_path.rglob("*.py"):
            if self._should_skip_file(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                for pattern, category in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    for match in matches:
                        key = f"{category}:{match}"
                        if key not in implementations:
                            implementations[key] = []
                        implementations[key].append(str(file_path))

            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

        # Find duplicates
        for key, files in implementations.items():
            if len(files) > 1:
                self.findings["potential_duplicates"].append({
                    "pattern": key,
                    "files": files,
                    "suggestion": f"Multiple implementations of {key.split(':')[0]} found - check for duplication"
                })

    def audit_incomplete_work(self) -> None:
        """Find incomplete implementations."""
        incomplete_patterns = [
            (r'#\s*TODO.*implement', 'Unimplemented TODO'),
            (r'#\s*FIXME.*broken', 'Broken FIXME'),
            (r'raise\s+NotImplementedError', 'NotImplementedError'),
            (r'pass\s*#.*implement', 'Pass placeholder'),
            (r'#\s*HACK|#.*temporary', 'Temporary hacks'),
        ]

        for file_path in self.scope_path.rglob("*.py"):
            if self._should_skip_file(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                for pattern, description in incomplete_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        self.findings["incomplete_work"].append({
                            "file": str(file_path),
                            "pattern": match,
                            "description": description,
                            "suggestion": "Review and complete this implementation"
                        })
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

    def audit_broken_imports(self) -> None:
        """Find potentially broken imports."""
        import_pattern = re.compile(r'^(\s*)(from\s+[\w.]+\s+import|import\s+[\w.]+)', re.MULTILINE)

        for file_path in self.scope_path.rglob("*.py"):
            if self._should_skip_file(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                imports = import_pattern.findall(content)
                for indent, import_stmt in imports:
                    # Check for common problematic imports
                    if any(problem in import_stmt for problem in ['src.', 'agent_workspaces.', '..']):
                        if 'src.' in import_stmt and 'from src.' in import_stmt:
                            # This might be a relative import issue
                            self.findings["broken_imports"].append({
                                "file": str(file_path),
                                "import": import_stmt.strip(),
                                "issue": "Potential relative import path issue",
                                "suggestion": "Verify import path works from current execution context"
                            })
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

    def _should_skip_file(self, file_path: Path) -> bool:
        """Determine if file should be skipped in audit."""
        skip_patterns = [
            '__pycache__',
            '.git',
            'node_modules',
            '.pytest_cache',
            'venv',
            '.env',
            'dist',
            'build',
            '*.pyc',
            '*.pyo',
        ]

        return any(pattern in str(file_path) for pattern in skip_patterns)

    def run_audit(self) -> Dict:
        """Run complete duplication audit."""
        print("🔍 Running duplication audit...")

        self.audit_todos_and_fixmes()
        self.audit_duplicate_implementations()
        self.audit_incomplete_work()
        self.audit_broken_imports()

        return self.findings

    def generate_report(self) -> str:
        """Generate human-readable audit report."""
        report = ["# 🔍 Duplication Audit Report\n"]

        total_findings = sum(len(v) for v in self.findings.values())

        if total_findings == 0:
            report.append("✅ No duplication or incomplete work found!")
            return "\n".join(report)

        # Summary
        report.append("## 📊 Summary\n")
        for category, items in self.findings.items():
            if items:
                report.append(f"- **{category.replace('_', ' ').title()}**: {len(items)} findings")

        # Details
        for category, items in self.findings.items():
            if items:
                report.append(f"\n## {category.replace('_', ' ').title()}\n")
                for item in items[:10]:  # Limit to first 10 per category
                    report.append(f"### {item.get('file', 'Unknown file')}")
                    if 'line' in item:
                        report.append(f"**Line {item['line']}**: {item.get('content', '')}")
                    if 'pattern' in item:
                        report.append(f"**Pattern**: `{item['pattern']}`")
                    if 'files' in item:
                        report.append(f"**Files**: {', '.join(item['files'])}")
                    if 'import' in item:
                        report.append(f"**Import**: `{item['import']}`")
                    if 'issue' in item:
                        report.append(f"**Issue**: {item['issue']}")
                    if 'suggestion' in item:
                        report.append(f"**Suggestion**: {item['suggestion']}")
                    report.append("")

                if len(items) > 10:
                    report.append(f"*... and {len(items) - 10} more findings*\n")

        report.append("## 📝 Session Closure Note")
        report.append("Add these findings to your master task list if they represent real work that needs to be done.")
        report.append("Document in your closure: 'Duplication audit completed — [summary of findings]'")

        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Audit codebase for duplication and incomplete work")
    parser.add_argument("--agent", required=True, help="Agent identifier (e.g., Agent-4)")
    parser.add_argument("--scope", default=".", help="Scope path to audit (default: current directory)")
    parser.add_argument("--output", help="Output file for report (optional)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    print(f"🔍 Starting duplication audit for {args.agent}...")
    print(f"📂 Scope: {args.scope}")

    auditor = DuplicationAuditor(args.scope)
    findings = auditor.run_audit()

    if args.json:
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(findings, f, indent=2)
        else:
            print(json.dumps(findings, indent=2))
    else:
        report = auditor.generate_report()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"📄 Report saved to: {args.output}")
        else:
            print(report)

    total_findings = sum(len(v) for v in findings.values())
    print(f"\n🎯 Audit complete! Total findings: {total_findings}")

    if total_findings > 0:
        print("💡 Review findings above and add any real work to your master task list.")
        print("📝 For session closure: 'Duplication audit completed — [summary of findings]'")


if __name__ == "__main__":
    main()