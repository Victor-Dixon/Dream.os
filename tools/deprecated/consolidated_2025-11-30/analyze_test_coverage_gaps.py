#!/usr/bin/env python3
"""
Test Coverage Gap Analysis Tool
================================

Analyzes test coverage gaps across the codebase and generates priority matrix.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
"""

import ast
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any


class TestCoverageAnalyzer:
    """Analyzes test coverage gaps."""

    def __init__(self, src_root: str = "src", tests_root: str = "tests"):
        """Initialize analyzer."""
        self.src_root = Path(src_root)
        self.tests_root = Path(tests_root)
        self.coverage_data = defaultdict(dict)
        self.gaps = []

    def find_all_source_files(self) -> list[Path]:
        """Find all Python source files."""
        source_files = []
        for path in self.src_root.rglob("*.py"):
            if "__pycache__" not in str(path) and "__init__" not in str(path):
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
        # Convert src/core/analytics/engine.py -> tests/core/test_analytics_engine.py
        relative = source_file.relative_to(self.src_root)
        test_name = f"test_{relative.stem}.py"
        
        # Try different locations
        possible_paths = [
            self.tests_root / relative.parent / test_name,
            self.tests_root / "core" / relative.name.replace(".py", f"test_{relative.name}"),
            self.tests_root / "unit" / relative.name.replace(".py", f"test_{relative.name}"),
            self.tests_root / relative.name.replace(".py", f"test_{relative.name}"),
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Also check if there's a test file with similar name anywhere
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
        """Calculate priority score (higher = more urgent)."""
        priority = 0
        
        # Missing test = high priority
        if not file_data.get("has_test", False):
            priority += 100
        
        # More classes/functions = higher priority
        priority += file_data.get("class_count", 0) * 10
        priority += file_data.get("function_count", 0) * 5
        
        # Core/infrastructure files = higher priority
        path = file_data.get("relative_path", "")
        if any(kw in path for kw in ["core", "engine", "coordinator", "orchestrator"]):
            priority += 50
        
        # Services = medium priority
        if "services" in path:
            priority += 25
        
        return priority

    def analyze_coverage(self) -> dict[str, Any]:
        """Analyze overall test coverage."""
        source_files = self.find_all_source_files()
        test_files = self.find_all_test_files()
        
        analyzed = []
        for source_file in source_files:
            file_data = self.analyze_file(source_file)
            file_data["priority"] = self.calculate_priority(file_data)
            analyzed.append(file_data)
        
        # Sort by priority
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
            "high_priority_gaps": [f for f in analyzed if f.get("priority", 0) >= 150 and not f.get("has_test", False)][:20],
            "all_files": analyzed,
        }

    def generate_priority_matrix(self, analysis: dict[str, Any]) -> dict[str, Any]:
        """Generate priority matrix for test coverage."""
        files = analysis["all_files"]
        
        matrix = {
            "critical": [],  # Priority >= 200
            "high": [],      # Priority 150-199
            "medium": [],    # Priority 100-149
            "low": [],       # Priority < 100
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
            "coverage_by_category": self._categorize_coverage(analysis["all_files"]),
        }

    def _categorize_coverage(self, files: list[dict[str, Any]]) -> dict[str, Any]:
        """Categorize coverage by file type."""
        categories = defaultdict(lambda: {"total": 0, "with_tests": 0})
        
        for file_data in files:
            path = file_data.get("relative_path", "")
            
            if "core" in path:
                category = "core"
            elif "services" in path:
                category = "services"
            elif "analytics" in path:
                category = "analytics"
            elif "utils" in path:
                category = "utils"
            else:
                category = "other"
            
            categories[category]["total"] += 1
            if file_data.get("has_test", False):
                categories[category]["with_tests"] += 1
        
        # Calculate percentages
        result = {}
        for cat, data in categories.items():
            result[cat] = {
                "total": data["total"],
                "with_tests": data["with_tests"],
                "percentage": round(data["with_tests"] / data["total"] * 100, 2) if data["total"] > 0 else 0,
            }
        
        return result


def main():
    """Main execution."""
    analyzer = TestCoverageAnalyzer()
    
    print("🔍 Analyzing test coverage gaps...")
    analysis = analyzer.analyze_coverage()
    
    print("📊 Generating priority matrix...")
    matrix = analyzer.generate_priority_matrix(analysis)
    
    print("📈 Creating coverage dashboard...")
    dashboard = analyzer.generate_dashboard(analysis, matrix)
    
    # Save results
    output_dir = Path("agent_workspaces/Agent-5")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save full analysis
    with open(output_dir / "test_coverage_analysis.json", "w") as f:
        json.dump(analysis, f, indent=2)
    
    # Save priority matrix
    with open(output_dir / "test_coverage_priority_matrix.json", "w") as f:
        json.dump(matrix, f, indent=2)
    
    # Save dashboard
    with open(output_dir / "test_coverage_dashboard.json", "w") as f:
        json.dump(dashboard, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST COVERAGE ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Source Files: {analysis['total_source_files']}")
    print(f"Files With Tests: {analysis['files_with_tests']}")
    print(f"Files Without Tests: {analysis['files_without_tests']}")
    print(f"Coverage: {analysis['coverage_percentage']}%")
    print(f"\nPriority Breakdown:")
    print(f"  Critical: {len(matrix['critical'])} files")
    print(f"  High: {len(matrix['high'])} files")
    print(f"  Medium: {len(matrix['medium'])} files")
    print(f"  Low: {len(matrix['low'])} files")
    print("\n✅ Analysis complete! Files saved to agent_workspaces/Agent-5/")


if __name__ == "__main__":
    main()

