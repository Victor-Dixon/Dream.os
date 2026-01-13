#!/usr/bin/env python3
"""
Dependency Analyzer for Tools Consolidation
==========================================

Analyzes all tools for import dependencies, external libraries, and consolidation opportunities.
Part of Phase 1: Analysis & Mapping for tools consolidation initiative.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import os
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict, Counter
import json

class ToolsDependencyAnalyzer:
    """Analyzes dependencies and usage patterns across all tools."""

    def __init__(self, tools_dir: str = "tools"):
        self.tools_dir = Path(tools_dir)
        self.tools: Dict[str, Dict] = {}
        self.dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.reverse_dependencies: Dict[str, Set[str]] = defaultdict(set)
        self.external_libs: Dict[str, Set[str]] = defaultdict(set)
        self.import_patterns: Dict[str, List[str]] = defaultdict(list)

    def analyze_tool(self, tool_path: Path) -> Dict:
        """Analyze a single tool file for dependencies."""
        tool_name = tool_path.stem
        tool_info = {
            "name": tool_name,
            "path": str(tool_path),
            "size": tool_path.stat().st_size,
            "imports": set(),
            "external_imports": set(),
            "internal_imports": set(),
            "functions": [],
            "classes": [],
            "complexity_score": 0
        }

        try:
            with open(tool_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse AST for imports and structure
            tree = ast.parse(content, filename=str(tool_path))

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_name = alias.name
                        tool_info["imports"].add(import_name)
                        if self._is_external_import(import_name):
                            tool_info["external_imports"].add(import_name)
                        else:
                            tool_info["internal_imports"].add(import_name)

                elif isinstance(node, ast.ImportFrom):
                    module_name = node.module or ""
                    for alias in node.names:
                        import_name = f"{module_name}.{alias.name}" if module_name else alias.name
                        tool_info["imports"].add(import_name)
                        if self._is_external_import(import_name):
                            tool_info["external_imports"].add(import_name)
                        else:
                            tool_info["internal_imports"].add(import_name)

                # Extract functions and classes
                elif isinstance(node, ast.FunctionDef):
                    tool_info["functions"].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    tool_info["classes"].append(node.name)

            # Calculate complexity score (lines + functions + classes)
            lines = len(content.split('\n'))
            tool_info["complexity_score"] = lines + len(tool_info["functions"]) + len(tool_info["classes"])

            # Store import patterns for analysis
            self.import_patterns[tool_name] = list(tool_info["imports"])

        except Exception as e:
            tool_info["error"] = str(e)

        return tool_info

    def _is_external_import(self, import_name: str) -> bool:
        """Determine if an import is external (non-standard library)."""
        # Common external libraries that indicate consolidation opportunities
        external_indicators = {
            'requests', 'pyautogui', 'discord', 'dotenv', 'pathlib',
            'json', 'os', 'sys', 'subprocess', 'psutil', 'ast',
            'logging', 'argparse', 'typing', 'collections'
        }

        # Check if it's a known external library
        base_import = import_name.split('.')[0]
        return base_import in external_indicators or '.' in import_name

    def analyze_all_tools(self) -> Dict:
        """Analyze all tools in the tools directory."""
        print("🔍 ANALYZING TOOLS DEPENDENCIES")
        print("=" * 50)

        tool_files = list(self.tools_dir.glob("*.py"))
        tool_files.extend(self.tools_dir.glob("metrics/*.py"))

        for tool_file in tool_files:
            if tool_file.name.startswith('__'):
                continue  # Skip __pycache__

            print(f"📄 Analyzing: {tool_file.name}")
            tool_info = self.analyze_tool(tool_file)
            self.tools[tool_info["name"]] = tool_info

            # Build dependency graphs
            for dep in tool_info["imports"]:
                self.dependencies[tool_info["name"]].add(dep)
                # Note: Reverse dependencies would need module analysis

        print(f"✅ Analyzed {len(self.tools)} tools")
        return self.generate_analysis_report()

    def generate_analysis_report(self) -> Dict:
        """Generate comprehensive dependency analysis report."""
        report = {
            "summary": {
                "total_tools": len(self.tools),
                "total_dependencies": sum(len(deps) for deps in self.dependencies.values()),
                "unique_external_libs": len(set.union(*[set() for tool in self.tools.values() if "external_imports" in tool])),
                "average_complexity": sum(tool.get("complexity_score", 0) for tool in self.tools.values()) / len(self.tools)
            },
            "tools": self.tools,
            "dependency_clusters": self._identify_dependency_clusters(),
            "consolidation_opportunities": self._identify_consolidation_opportunities(),
            "migration_priorities": self._calculate_migration_priorities()
        }

        return report

    def _identify_dependency_clusters(self) -> Dict:
        """Identify clusters of tools with similar dependencies."""
        clusters = defaultdict(list)

        # Group tools by their primary external dependencies
        for tool_name, tool_info in self.tools.items():
            external_deps = tool_info.get("external_imports", set())
            if external_deps:
                # Use the most common external dep as cluster key
                primary_dep = max(external_deps, key=lambda x: len(x)) if external_deps else "misc"
                clusters[primary_dep].append(tool_name)

        return dict(clusters)

    def _identify_consolidation_opportunities(self) -> List[Dict]:
        """Identify tools that can be consolidated based on dependencies."""
        opportunities = []

        # Find tools with overlapping dependencies
        tool_deps = {name: info.get("external_imports", set())
                    for name, info in self.tools.items()}

        # Look for tools with similar dependency patterns
        for tool1, deps1 in tool_deps.items():
            for tool2, deps2 in tool_deps.items():
                if tool1 != tool2:
                    overlap = len(deps1.intersection(deps2))
                    if overlap >= 2:  # Significant overlap
                        similarity = overlap / max(len(deps1), len(deps2))
                        if similarity > 0.5:
                            opportunities.append({
                                "tool1": tool1,
                                "tool2": tool2,
                                "shared_deps": list(deps1.intersection(deps2)),
                                "similarity_score": round(similarity, 2),
                                "consolidation_potential": "HIGH" if similarity > 0.8 else "MEDIUM"
                            })

        # Remove duplicates
        seen = set()
        unique_opportunities = []
        for opp in opportunities:
            key = tuple(sorted([opp["tool1"], opp["tool2"]]))
            if key not in seen:
                seen.add(key)
                unique_opportunities.append(opp)

        return unique_opportunities

    def _calculate_migration_priorities(self) -> List[Dict]:
        """Calculate migration priorities based on complexity and dependencies."""
        priorities = []

        for tool_name, tool_info in self.tools.items():
            complexity = tool_info.get("complexity_score", 0)
            dep_count = len(tool_info.get("external_imports", set()))

            # Calculate priority score (lower = higher priority)
            priority_score = (complexity * 0.4) + (dep_count * 0.6)

            priorities.append({
                "tool": tool_name,
                "complexity_score": complexity,
                "dependency_count": dep_count,
                "priority_score": round(priority_score, 1),
                "migration_order": "HIGH" if priority_score < 100 else "MEDIUM" if priority_score < 200 else "LOW"
            })

        # Sort by priority (lowest score first)
        priorities.sort(key=lambda x: x["priority_score"])
        return priorities

    def save_report(self, report: Dict, output_file: str = "tools_dependency_analysis.json"):
        """Save the analysis report to JSON file."""
        # Convert sets to lists for JSON serialization
        json_report = self._make_json_serializable(report)

        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            json.dump(json_report, f, indent=2)
        print(f"💾 Report saved to: {output_path}")

    def _make_json_serializable(self, obj):
        """Convert sets to lists and handle other non-JSON-serializable types."""
        if isinstance(obj, dict):
            return {key: self._make_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_json_serializable(item) for item in obj]
        elif isinstance(obj, set):
            return list(obj)
        else:
            return obj

def main():
    analyzer = ToolsDependencyAnalyzer()
    report = analyzer.analyze_all_tools()

    print(f"\n📊 DEPENDENCY ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Total Tools: {report['summary']['total_tools']}")
    print(f"Total Dependencies: {report['summary']['total_dependencies']}")
    print(f"Unique External Libraries: {report['summary']['unique_external_libs']}")
    print(f"Average Complexity: {report['summary']['average_complexity']:.1f}")

    print(f"\n🔗 CONSOLIDATION OPPORTUNITIES:")
    opportunities = report.get('consolidation_opportunities', [])
    if opportunities:
        for opp in opportunities[:5]:  # Show top 5
            print(f"  • {opp['tool1']} ↔ {opp['tool2']} ({opp['consolidation_potential']})")
    else:
        print("  No significant consolidation opportunities found")

    analyzer.save_report(report)

if __name__ == "__main__":
    main()