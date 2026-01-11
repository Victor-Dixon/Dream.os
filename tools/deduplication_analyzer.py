#!/usr/bin/env python3
"""
Code Deduplication Analyzer
===========================

Analyzes the codebase for repetitive patterns and generates deduplication reports.

V2 Compliance: Analysis tool for code quality improvement
Author: Agent-3 - Infrastructure & DevOps Specialist
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict, Counter

class CodeDeduplicationAnalyzer:
    """Analyzes code for duplication patterns."""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.patterns = defaultdict(list)
        self.stats = defaultdict(int)

    def analyze_directory(self, directory: str) -> Dict:
        """Analyze a directory for code duplication patterns."""
        dir_path = self.root_path / directory
        if not dir_path.exists():
            return {"error": f"Directory {directory} not found"}

        results = {
            "directory": directory,
            "files_analyzed": 0,
            "patterns_found": {},
            "total_duplications": 0,
            "recommendations": []
        }

        # Analyze Python files
        for py_file in dir_path.rglob("*.py"):
            if self._should_analyze_file(py_file):
                file_patterns = self.analyze_file(py_file)
                if file_patterns:
                    results["files_analyzed"] += 1
                    for pattern_type, patterns in file_patterns.items():
                        if pattern_type not in results["patterns_found"]:
                            results["patterns_found"][pattern_type] = {}
                        for pattern, count in patterns.items():
                            results["patterns_found"][pattern_type][pattern] = \
                                results["patterns_found"][pattern_type].get(pattern, 0) + count
                            results["total_duplications"] += count

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single file for duplication patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"error": f"Could not read {file_path}: {e}"}

        patterns = {}

        # Logger initialization patterns
        logger_patterns = re.findall(r'self\.logger\s*=\s*logging\.getLogger\([^)]+\)', content)
        if logger_patterns:
            patterns["logger_initialization"] = dict(Counter(logger_patterns))

        # Error handling patterns
        error_patterns = re.findall(r'except\s+Exception\s+as\s+\w+:\s*\n\s*self\.logger\.error\([^)]+\)', content, re.MULTILINE)
        if error_patterns:
            patterns["error_handling"] = {"standard_error_handler": len(error_patterns)}

        # Embed creation patterns
        embed_patterns = re.findall(r'discord\.Embed\(', content)
        if embed_patterns:
            patterns["embed_creation"] = {"discord_embed": len(embed_patterns)}

        # Command logging patterns
        command_log_patterns = re.findall(r'self\.logger\.info\(f"Command\s+\'[^\']+\'\s+triggered', content)
        if command_log_patterns:
            patterns["command_logging"] = {"standard_command_log": len(command_log_patterns)}

        # Role decorator patterns
        role_patterns = re.findall(r'@commands\.has_any_role\([^)]+\)', content)
        if role_patterns:
            patterns["role_decorators"] = dict(Counter(role_patterns))

        # Import patterns
        import_patterns = re.findall(r'^import\s+\w+|from\s+\w+\s+import', content, re.MULTILINE)
        if len(import_patterns) > 10:  # Only flag if excessive
            patterns["imports"] = {"total_imports": len(import_patterns)}

        return patterns

    def _should_analyze_file(self, file_path: Path) -> bool:
        """Determine if a file should be analyzed."""
        # Skip test files, __init__.py, and very small files
        if file_path.name.startswith("test_") or file_path.name == "__init__.py":
            return False
        if file_path.stat().st_size < 1000:  # Skip files smaller than 1KB
            return False
        return True

    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate deduplication recommendations."""
        recommendations = []

        patterns = results.get("patterns_found", {})

        # Logger initialization
        if "logger_initialization" in patterns:
            total = sum(patterns["logger_initialization"].values())
            if total > 5:
                recommendations.append(f"🔧 Create logger mixin - {total} repetitive logger initializations found")

        # Error handling
        if "error_handling" in patterns:
            total = patterns["error_handling"].get("standard_error_handler", 0)
            if total > 5:
                recommendations.append(f"🔧 Create error handling decorator - {total} repetitive error handlers found")

        # Embed creation
        if "embed_creation" in patterns:
            total = patterns["embed_creation"].get("discord_embed", 0)
            if total > 10:
                recommendations.append(f"🔧 Create embed builder utility - {total} repetitive embed creations found")

        # Command logging
        if "command_logging" in patterns:
            total = patterns["command_logging"].get("standard_command_log", 0)
            if total > 5:
                recommendations.append(f"🔧 Create command logging decorator - {total} repetitive command logs found")

        # Role decorators
        if "role_decorators" in patterns:
            total_roles = sum(patterns["role_decorators"].values())
            if total_roles > 5:
                recommendations.append(f"🔧 Consolidate role decorators - {total_roles} repetitive role checks found")

        # Import patterns
        if "imports" in patterns:
            total_imports = patterns["imports"].get("total_imports", 0)
            if total_imports > 20:
                recommendations.append(f"🔧 Create import utility - {total_imports} imports in single file")

        return recommendations

    def generate_report(self, directories: List[str]) -> Dict:
        """Generate comprehensive deduplication report."""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "directories_analyzed": directories,
            "summary": {},
            "detailed_results": {},
            "overall_recommendations": []
        }

        total_duplications = 0
        total_files = 0

        for directory in directories:
            result = self.analyze_directory(directory)
            if "error" not in result:
                report["detailed_results"][directory] = result
                total_duplications += result["total_duplications"]
                total_files += result["files_analyzed"]

                # Add recommendations
                report["overall_recommendations"].extend(result["recommendations"])

        report["summary"] = {
            "total_directories": len(directories),
            "total_files_analyzed": total_files,
            "total_duplications_found": total_duplications,
            "recommendations_count": len(report["overall_recommendations"])
        }

        return report


def main():
    """Main function."""
    analyzer = CodeDeduplicationAnalyzer(".")

    # Analyze key directories with repetitive code
    directories_to_analyze = [
        "src/discord_commander/commands",
        "src/services",
        "src/core",
        "tools"
    ]

    print("🔍 Analyzing codebase for code duplication...")
    report = analyzer.generate_report(directories_to_analyze)

    # Save report
    report_file = Path("code_deduplication_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"✅ Analysis complete! Report saved to {report_file}")
    print(f"📊 Found {report['summary']['total_duplications_found']} duplication patterns")
    print(f"📝 Generated {report['summary']['recommendations_count']} recommendations")

    # Print key findings
    print("\n🔧 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(report["overall_recommendations"][:5], 1):
        print(f"{i}. {rec}")


if __name__ == "__main__":
    main()