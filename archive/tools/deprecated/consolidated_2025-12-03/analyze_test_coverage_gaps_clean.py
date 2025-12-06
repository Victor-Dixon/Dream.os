#!/usr/bin/env python3
"""
Test Coverage Gap Analysis - Clean Version
===========================================

<!-- SSOT Domain: qa -->

Analyzes test coverage gaps EXCLUDING unnecessary files that should be deleted.
Only analyzes files that are actually used in the codebase.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-01
Priority: HIGH - Focus testing on files that matter
"""

import ast
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

# Import unnecessary files data
try:
    with open("agent_workspaces/Agent-5/unnecessary_files_analysis.json", "r", encoding="utf-8") as f:
        unnecessary_data = json.load(f)
    unnecessary_files = set()
    for category in ["unused", "deprecated_directory", "deletion_markers", "duplicates"]:
        for file_info in unnecessary_data.get(category, []):
            unnecessary_files.add(file_info["file_path"])
except Exception:
    unnecessary_files = set()
    print("⚠️  Warning: Could not load unnecessary files data. Analyzing all files.")


class CleanTestCoverageAnalyzer:
    """Analyzes test coverage gaps excluding unnecessary files."""

    def __init__(self, src_root: str = "src", tests_root: str = "tests"):
        """Initialize analyzer."""
        self.src_root = Path(src_root)
        self.tests_root = Path(tests_root)
        self.unnecessary_files = unnecessary_files
        self.coverage_data = defaultdict(dict)
        self.gaps = []

    def find_all_source_files(self) -> list[Path]:
        """Find all Python source files, excluding unnecessary ones."""
        source_files = []
        for path in self.src_root.rglob("*.py"):
            if "__pycache__" not in str(path) and "__init__" not in str(path):
                # Skip unnecessary files
                if str(path) in self.unnecessary_files:
                    continue
                source_files.append(path)
        return sorted(source_files)

    def find_all_test_files(self) -> list[Path]:
        """Find all test files."""
        test_files = []
        for path in self.tests_root.rglob("test_*.py"):
            if "__pycache__" not in str(path):
                test_files.append(path)
        return sorted(test_files)

    def get_test_for_source(self, source_file: Path) -> Path | None:
        """Find corresponding test file for source file."""
        relative = source_file.relative_to(self.src_root)
        test_name = f"test_{relative.stem}.py"
        
        possible_paths = [
            self.tests_root / relative.parent / test_name,
            self.tests_root / "core" / relative.name.replace(".py", f"test_{relative.name}"),
            self.tests_root / "unit" / relative.name.replace(".py", f"test_{relative.name}"),
            self.tests_root / relative.name.replace(".py", f"test_{relative.name}"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        for test_file in self.find_all_test_files():
            if relative.stem in test_file.stem or test_file.stem.replace("test_", "") == relative.stem:
                return test_file
        
        return None

    def analyze_file(self, source_file: Path) -> dict[str, Any]:
        """Analyze a single source file."""
        try:
            with open(source_file, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), str(source_file))
            
            classes = []
            functions = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    functions.append(node.name)
            
            test_file = self.get_test_for_source(source_file)
            
            return {
                "source_file": str(source_file),
                "relative_path": str(source_file.relative_to(self.src_root)),
                "test_file": str(test_file) if test_file else None,
                "has_test": test_file is not None,
                "class_count": len(classes),
                "function_count": len(functions),
                "classes": classes,
                "functions": functions,
            }
        except Exception as e:
            return {
                "source_file": str(source_file),
                "error": str(e),
                "has_test": False,
            }

    def calculate_priority(self, file_data: dict[str, Any]) -> int:
        """Calculate priority score."""
        priority = 0
        
        if not file_data.get("has_test", False):
            priority += 100
        
        priority += file_data.get("class_count", 0) * 10
        priority += file_data.get("function_count", 0) * 5
        
        path = file_data.get("relative_path", "")
        if any(kw in path for kw in ["core", "engine", "coordinator", "orchestrator"]):
            priority += 50
        
        if "services" in path:
            priority += 25
        
        return priority

    def analyze_coverage(self) -> dict[str, Any]:
        """Analyze overall test coverage (only necessary files)."""
        source_files = self.find_all_source_files()
        test_files = self.find_all_test_files()
        
        print(f"🔍 Analyzing {len(source_files)} necessary source files (unnecessary files excluded)...")
        
        analyzed = []
        for source_file in source_files:
            file_data = self.analyze_file(source_file)
            file_data["priority"] = self.calculate_priority(file_data)
            analyzed.append(file_data)
        
        analyzed.sort(key=lambda x: x.get("priority", 0), reverse=True)
        
        total_files = len(analyzed)
        files_with_tests = sum(1 for f in analyzed if f.get("has_test", False))
        coverage_percentage = (files_with_tests / total_files * 100) if total_files > 0 else 0
        
        return {
            "total_source_files": total_files,
            "total_test_files": len(test_files),
            "files_with_tests": files_with_tests,
            "files_without_tests": total_files - files_with_tests,
            "coverage_percentage": round(coverage_percentage, 2),
            "all_files": analyzed,
        }

    def generate_priority_matrix(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Generate priority matrix."""
        files = analysis["all_files"]
        
        matrix = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
        }
        
        for file_data in files:
            if not file_data.get("has_test", False):
                priority = file_data.get("priority", 0)
                if priority >= 200:
                    matrix["critical"].append(file_data)
                elif priority >= 150:
                    matrix["high"].append(file_data)
                elif priority >= 100:
                    matrix["medium"].append(file_data)
                else:
                    matrix["low"].append(file_data)
        
        return matrix

    def generate_dashboard(self, analysis: dict[str, Any], matrix: dict[str, Any]) -> dict[str, Any]:
        """Generate coverage metrics dashboard."""
        return {
            "summary": {
                "total_source_files": analysis["total_source_files"],
                "total_test_files": analysis["total_test_files"],
                "coverage_percentage": analysis["coverage_percentage"],
                "gaps_count": analysis["files_without_tests"],
                "unnecessary_files_excluded": len(self.unnecessary_files),
            },
            "priority_breakdown": {
                "critical": len(matrix["critical"]),
                "high": len(matrix["high"]),
                "medium": len(matrix["medium"]),
                "low": len(matrix["low"]),
            },
            "top_priorities": {
                "critical": matrix["critical"][:10],
                "high": matrix["high"][:10],
            },
        }


def main():
    """Main execution."""
    print("🔍 CLEAN TEST COVERAGE ANALYSIS")
    print("=" * 60)
    print("Analyzing only necessary files (excluding unnecessary/deleted files)\n")
    
    analyzer = CleanTestCoverageAnalyzer()
    analysis = analyzer.analyze_coverage()
    matrix = analyzer.generate_priority_matrix(analysis)
    dashboard = analyzer.generate_dashboard(analysis, matrix)
    
    print("\n" + "=" * 60)
    print("📊 CLEAN TEST COVERAGE SUMMARY")
    print("=" * 60)
    print(f"Necessary Source Files: {dashboard['summary']['total_source_files']}")
    print(f"Files With Tests: {analysis['files_with_tests']}")
    print(f"Files Without Tests: {analysis['files_without_tests']}")
    print(f"Coverage: {dashboard['summary']['coverage_percentage']}%")
    print(f"\nUnnecessary Files Excluded: {dashboard['summary']['unnecessary_files_excluded']}")
    print(f"\nPriority Breakdown:")
    print(f"  Critical: {dashboard['priority_breakdown']['critical']} files")
    print(f"  High: {dashboard['priority_breakdown']['high']} files")
    print(f"  Medium: {dashboard['priority_breakdown']['medium']} files")
    print(f"  Low: {dashboard['priority_breakdown']['low']} files")
    
    # Save results
    output_dir = Path("agent_workspaces/Agent-5")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "test_coverage_dashboard_clean.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    
    print(f"\n✅ Clean analysis saved to: {output_file}")
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()


