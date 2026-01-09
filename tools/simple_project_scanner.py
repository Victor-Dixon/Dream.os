#!/usr/bin/env python3
"""
Simple Project Scanner - Mock Implementation
===========================================

Provides basic project analysis for Thea integration testing.

Features:
- Scans Python files for basic metrics
- Provides sample data for Thea guidance
- Lightweight and fast

Usage:
    python tools/simple_project_scanner.py [project_path]
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

class SimpleProjectScanner:
    """Simple project scanner for Thea testing."""

    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root or os.getcwd())

    def scan_project(self) -> Dict[str, Any]:
        """Scan the project and return analysis."""
        print(f"🔍 Simple scanner analyzing: {self.project_root}")

        # Basic file counting
        python_files = list(self.project_root.rglob("*.py"))
        total_files = len(python_files)

        # Count lines and functions (simple approach)
        total_lines = 0
        total_functions = 0
        total_classes = 0

        for py_file in python_files[:50]:  # Limit to 50 files for speed
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    total_lines += lines

                    # Simple counting
                    total_functions += content.count('def ')
                    total_classes += content.count('class ')

            except Exception:
                continue

        # Create mock analysis data
        analysis = {
            "project_info": {
                "name": self.project_root.name,
                "path": str(self.project_root),
                "type": "python_application"
            },
            "tech_stack": {
                "primary_language": "python",
                "languages": ["python"],
                "frameworks": ["unknown"],
                "tools": ["unknown"]
            },
            "code_metrics": {
                "total_files": total_files,
                "total_lines": total_lines,
                "total_functions": total_functions,
                "total_classes": total_classes,
                "avg_lines_per_file": total_lines / max(total_files, 1)
            },
            "issues": [
                "Consider adding type hints for better code maintainability",
                "Large functions detected - consider breaking them down",
                "Missing comprehensive test coverage",
                "Consider adding API documentation"
            ],
            "scan_metadata": {
                "scanner_version": "simple_v1.0",
                "scan_timestamp": "2026-01-09T02:59:00Z",
                "files_analyzed": min(len(python_files), 50)
            }
        }

        # Save to project_analysis.json for compatibility
        output_file = self.project_root / "project_analysis.json"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"💾 Analysis saved to: {output_file}")
        except Exception as e:
            print(f"⚠️ Could not save analysis: {e}")

        return analysis

def main():
    """CLI interface."""
    import sys

    project_path = sys.argv[1] if len(sys.argv) > 1 else None

    scanner = SimpleProjectScanner(project_path)
    results = scanner.scan_project()

    print("✅ Project scan complete!")
    print(f"📊 Files analyzed: {results['code_metrics']['total_files']}")
    print(f"📝 Total lines: {results['code_metrics']['total_lines']}")
    print(f"🔧 Functions: {results['code_metrics']['total_functions']}")
    print(f"🏗️ Classes: {results['code_metrics']['total_classes']}")

if __name__ == "__main__":
    main()