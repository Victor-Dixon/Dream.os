#!/usr/bin/env python3
"""
Consolidate CLI Entry Points
============================

Analyzes and consolidates duplicate CLI entry points across the codebase.
Merges duplicate command-line interfaces and standardizes tool access patterns.

V2 Compliance: <300 lines, single responsibility
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-21
"""

import argparse
import ast
import json
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


class CLIAnalyzer:
    """Analyzes CLI entry points in the codebase."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.cli_files: List[Path] = []
        self.cli_patterns: Dict[str, List[Path]] = defaultdict(list)

    def find_cli_files(self) -> List[Path]:
        """Find all CLI entry point files."""
        cli_files = []

        # Find files with CLI patterns
        patterns = [
            "**/cli.py",
            "**/cli_*.py",
            "**/*_cli.py",
            "**/__main__.py",  # Python module entry points
        ]

        for pattern in patterns:
            for file_path in self.root_dir.rglob(pattern):
                # Skip test files and temp directories
                if any(
                    skip in str(file_path)
                    for skip in ["test_", "__pycache__", "temp_", ".git"]
                ):
                    continue

                # Check if it's actually a CLI file
                if self._is_cli_file(file_path):
                    cli_files.append(file_path)

        self.cli_files = sorted(set(cli_files))
        return self.cli_files

    def _is_cli_file(self, file_path: Path) -> bool:
        """Check if a file is a CLI entry point."""
        try:
            content = file_path.read_text(encoding="utf-8")
            # Check for CLI indicators
            has_main = 'if __name__ == "__main__"' in content
            has_argparse = "argparse" in content or "ArgumentParser" in content
            has_click = "click" in content or "@click" in content
            has_typer = "typer" in content

            # Must have main block and some CLI framework
            return has_main and (has_argparse or has_click or has_typer)
        except Exception:
            return False

    def analyze_cli_structure(self) -> Dict:
        """Analyze CLI structure and identify duplicates."""
        analysis = {
            "total_clis": len(self.cli_files),
            "by_location": defaultdict(list),
            "by_domain": defaultdict(list),
            "duplicates": [],
            "consolidation_opportunities": [],
        }

        for cli_file in self.cli_files:
            rel_path = str(cli_file.relative_to(self.root_dir))
            domain = self._extract_domain(cli_file)
            analysis["by_location"][str(cli_file.parent)].append(rel_path)
            analysis["by_domain"][domain].append(rel_path)

        # Find duplicate patterns
        analysis["duplicates"] = self._find_duplicates()
        analysis["consolidation_opportunities"] = self._find_consolidation_opportunities()

        return analysis

    def _extract_domain(self, file_path: Path) -> str:
        """Extract domain from file path."""
        parts = file_path.parts
        if "services" in parts:
            return "services"
        elif "core" in parts:
            return "core"
        elif "workflows" in parts:
            return "workflows"
        elif "orchestrators" in parts:
            return "orchestrators"
        elif "vision" in parts:
            return "vision"
        else:
            return "other"

    def _find_duplicates(self) -> List[Dict]:
        """Find duplicate CLI entry points."""
        duplicates = []

        # Check for similar __main__.py files in cli directories
        cli_main_files = [
            f for f in self.cli_files if f.name == "__main__.py" and "cli" in str(f)
        ]

        if len(cli_main_files) > 1:
            # Compare structure
            structures = {}
            for file_path in cli_main_files:
                try:
                    content = file_path.read_text(encoding="utf-8")
                    # Extract key patterns
                    structure = {
                        "has_argparse": "argparse" in content,
                        "has_subparsers": "add_subparsers" in content,
                        "line_count": len(content.splitlines()),
                    }
                    structures[str(file_path)] = structure
                except Exception:
                    continue

            # Find similar structures
            for file1, struct1 in structures.items():
                for file2, struct2 in structures.items():
                    if file1 < file2 and self._structures_similar(struct1, struct2):
                        duplicates.append(
                            {
                                "file1": file1,
                                "file2": file2,
                                "similarity": "high",
                                "reason": "Similar structure and purpose",
                            }
                        )

        return duplicates

    def _structures_similar(self, struct1: Dict, struct2: Dict) -> bool:
        """Check if two CLI structures are similar."""
        if struct1["has_argparse"] != struct2["has_argparse"]:
            return False
        if struct1["has_subparsers"] != struct2["has_subparsers"]:
            return False
        # Similar line count (within 20%)
        line_diff = abs(struct1["line_count"] - struct2["line_count"])
        avg_lines = (struct1["line_count"] + struct2["line_count"]) / 2
        return line_diff < (avg_lines * 0.2)

    def _find_consolidation_opportunities(self) -> List[Dict]:
        """Find opportunities to consolidate CLIs."""
        opportunities = []

        # Check for services/cli and core/cli
        services_cli = self.root_dir / "src" / "services" / "cli" / "__main__.py"
        core_cli = self.root_dir / "core" / "cli" / "__main__.py"

        if services_cli.exists() and core_cli.exists():
            opportunities.append(
                {
                    "type": "merge_similar_entry_points",
                    "files": [str(services_cli), str(core_cli)],
                    "recommendation": "Merge into unified src/cli/__main__.py",
                    "priority": "high",
                }
            )

        return opportunities

    def generate_report(self, analysis: Dict) -> str:
        """Generate analysis report."""
        report = []
        report.append("=" * 70)
        report.append("CLI ENTRY POINTS CONSOLIDATION ANALYSIS")
        report.append("=" * 70)
        report.append("")

        report.append(f"Total CLI Files Found: {analysis['total_clis']}")
        report.append("")

        # Group by domain
        report.append("CLI Files by Domain:")
        for domain, files in sorted(analysis["by_domain"].items()):
            report.append(f"  {domain}: {len(files)} files")
            for file_path in files[:5]:  # Show first 5
                report.append(f"    - {file_path}")
            if len(files) > 5:
                report.append(f"    ... and {len(files) - 5} more")
        report.append("")

        # Duplicates
        if analysis["duplicates"]:
            report.append("Duplicate CLI Entry Points Found:")
            for dup in analysis["duplicates"]:
                report.append(f"  - {dup['file1']}")
                report.append(f"    {dup['file2']}")
                report.append(f"    Reason: {dup['reason']}")
            report.append("")

        # Consolidation opportunities
        if analysis["consolidation_opportunities"]:
            report.append("Consolidation Opportunities:")
            for opp in analysis["consolidation_opportunities"]:
                report.append(f"  Type: {opp['type']}")
                report.append(f"  Files: {', '.join(opp['files'])}")
                report.append(f"  Recommendation: {opp['recommendation']}")
                report.append(f"  Priority: {opp['priority']}")
                report.append("")

        return "\n".join(report)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Consolidate CLI entry points and standardize access patterns"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze CLI structure (dry run)"
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute consolidation (requires --analyze first)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="cli_consolidation_report.txt",
        help="Output file for analysis report",
    )

    args = parser.parse_args()

    if not args.analyze and not args.execute:
        parser.print_help()
        return 1

    analyzer = CLIAnalyzer()
    print("🔍 Finding CLI entry points...")
    cli_files = analyzer.find_cli_files()
    print(f"✅ Found {len(cli_files)} CLI files")

    print("📊 Analyzing CLI structure...")
    analysis = analyzer.analyze_cli_structure()

    # Generate report
    report = analyzer.generate_report(analysis)
    print("\n" + report)

    # Save report
    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")
    print(f"\n✅ Report saved to {output_path}")

    if args.execute:
        print("\n🚀 Executing consolidation...")
        # TODO: Implement actual consolidation logic
        print("⚠️  Consolidation execution not yet implemented")
        print("   Review the analysis report and implement consolidation manually")

    return 0


if __name__ == "__main__":
    exit(main())


