#!/usr/bin/env python3
"""
Test Coverage Prioritizer - Productivity Tool
=============================================

Helps prioritize which files need test coverage next based on:
- File importance (core infrastructure, services, etc.)
- Current test coverage status
- Usage patterns (actively used code)
- Complexity metrics
- Dependencies

Usage:
    python tools/test_coverage_prioritizer.py
    python tools/test_coverage_prioritizer.py --output report.md
    python tools/test_coverage_prioritizer.py --focus core

Author: Agent-2 (Architecture & Design Specialist)
V2 Compliant: <400 lines
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import argparse


class TestCoveragePrioritizer:
    """Prioritizes files for test coverage based on multiple factors."""

    def __init__(self, src_dir: Path = Path("src")):
        """Initialize prioritizer."""
        self.src_dir = src_dir
        self.priority_weights = {
            "core_infrastructure": 10,
            "services": 8,
            "repositories": 7,
            "utils": 5,
            "discord_commander": 4,
            "other": 3
        }

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize file by path."""
        path_str = str(file_path)
        if "core" in path_str:
            return "core_infrastructure"
        elif "services" in path_str:
            return "services"
        elif "repositories" in path_str:
            return "repositories"
        elif "utils" in path_str:
            return "utils"
        elif "discord_commander" in path_str:
            return "discord_commander"
        else:
            return "other"

    def _count_complexity(self, file_path: Path) -> int:
        """Count complexity metrics (functions, classes, lines)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            
            functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
            classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
            lines = len(content.splitlines())
            
            return {
                'functions': functions,
                'classes': classes,
                'lines': lines,
                'complexity_score': functions * 2 + classes * 3 + (lines // 10)
            }
        except Exception:
            return {
                'functions': 0,
                'classes': 0,
                'lines': 0,
                'complexity_score': 0
            }

    def _check_has_tests(self, file_path: Path) -> bool:
        """Check if file has corresponding test file."""
        file_stem = file_path.stem
        test_patterns = [
            f"test_{file_stem}.py",
            f"test_{file_path.parent.name}_{file_stem}.py",
        ]
        
        tests_dir = Path("tests")
        if not tests_dir.exists():
            return False
        
        for pattern in test_patterns:
            if list(tests_dir.rglob(pattern)):
                return True
        
        return False

    def _check_usage(self, file_path: Path, all_files: List[Path]) -> int:
        """Check how many files import/use this file."""
        try:
            relative_path = file_path.relative_to(Path.cwd())
            module_parts = relative_path.with_suffix('').parts
            module_path = '.'.join(module_parts)
        except ValueError:
            return 0
        
        usage_count = 0
        for other_file in all_files:
            if other_file == file_path:
                continue
            
            try:
                content = other_file.read_text(encoding='utf-8')
                if f"from {module_path}" in content or f"import {module_path}" in content:
                    usage_count += 1
            except Exception:
                continue
        
        return usage_count

    def prioritize_files(self, focus: Optional[str] = None) -> List[Dict]:
        """Prioritize files for test coverage."""
        python_files = list(self.src_dir.rglob("*.py"))
        
        # Filter out test files and __init__ files
        source_files = [
            f for f in python_files
            if "test_" not in f.name and f.name != "__init__.py"
        ]
        
        if focus:
            source_files = [f for f in source_files if focus in str(f)]
        
        prioritized = []
        
        for file_path in source_files:
            category = self._categorize_file(file_path)
            complexity = self._count_complexity(file_path)
            has_tests = self._check_has_tests(file_path)
            usage_count = self._check_usage(file_path, source_files)
            
            if has_tests:
                continue  # Skip files that already have tests
            
            # Calculate priority score
            category_weight = self.priority_weights.get(category, 3)
            complexity_weight = min(complexity['complexity_score'] / 10, 5)
            usage_weight = min(usage_count / 5, 5)
            
            priority_score = (
                category_weight * 3 +
                complexity_weight * 2 +
                usage_weight * 2
            )
            
            try:
                file_str = str(file_path.relative_to(Path.cwd()))
            except ValueError:
                file_str = str(file_path)
            
            prioritized.append({
                'file': file_str,
                'category': category,
                'priority_score': round(priority_score, 2),
                'complexity': complexity,
                'usage_count': usage_count,
                'has_tests': has_tests
            })
        
        # Sort by priority score (highest first)
        prioritized.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return prioritized

    def generate_report(self, prioritized: List[Dict], output_file: Optional[Path] = None) -> str:
        """Generate markdown report."""
        report = "# Test Coverage Prioritization Report\n\n"
        report += f"**Generated**: {Path.cwd()}\n"
        report += f"**Files Prioritized**: {len(prioritized)}\n\n"
        report += "---\n\n"
        
        # Group by category
        by_category = defaultdict(list)
        for item in prioritized:
            by_category[item['category']].append(item)
        
        for category in sorted(by_category.keys(), 
                               key=lambda c: self.priority_weights.get(c, 0), 
                               reverse=True):
            items = by_category[category]
            report += f"## {category.replace('_', ' ').title()}\n\n"
            report += f"**Files**: {len(items)}\n\n"
            
            # Top 10 for each category
            for item in items[:10]:
                report += f"### {item['file']}\n"
                report += f"- **Priority Score**: {item['priority_score']}\n"
                report += f"- **Complexity**: {item['complexity']['functions']} functions, "
                report += f"{item['complexity']['classes']} classes, "
                report += f"{item['complexity']['lines']} lines\n"
                report += f"- **Usage**: {item['usage_count']} files import this\n"
                report += f"- **Status**: {'✅ Has tests' if item['has_tests'] else '❌ No tests'}\n\n"
            
            if len(items) > 10:
                report += f"\n... and {len(items) - 10} more files\n\n"
            
            report += "---\n\n"
        
        # Top 20 overall
        report += "## Top 20 Priority Files\n\n"
        for i, item in enumerate(prioritized[:20], 1):
            report += f"{i}. **{item['file']}** (Score: {item['priority_score']}, "
            report += f"Category: {item['category']}, Usage: {item['usage_count']})\n"
        
        if output_file:
            output_file.write_text(report, encoding='utf-8')
            print(f"✅ Report saved to: {output_file}")
        
        return report


def main():
    """Main execution."""
    parser = argparse.ArgumentParser(description="Prioritize files for test coverage")
    parser.add_argument("--output", "-o", type=Path, help="Output report file")
    parser.add_argument("--focus", "-f", help="Focus on specific path (e.g., 'core', 'services')")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    print("🔍 Test Coverage Prioritizer")
    print("=" * 60)
    print()
    
    prioritizer = TestCoveragePrioritizer()
    prioritized = prioritizer.prioritize_files(focus=args.focus)
    
    print(f"📊 Found {len(prioritized)} files needing test coverage\n")
    
    if args.json:
        output = json.dumps(prioritized, indent=2)
        if args.output:
            args.output.write_text(output, encoding='utf-8')
        else:
            print(output)
    else:
        report = prioritizer.generate_report(prioritized, args.output)
        if not args.output:
            print(report)
    
    print("\n✅ Prioritization complete!")


if __name__ == "__main__":
    main()

