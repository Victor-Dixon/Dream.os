#!/usr/bin/env python3
"""
Tool Tagging Analyzer
====================

Analyzes tools directory for proper tagging and discoverability.

Usage:
    python tools/tag_analyzer.py                    # Analyze all tools
    python tools/tag_analyzer.py --directory docs  # Analyze specific directory
    python tools/tag_analyzer.py --report-only     # Generate report only

Features:
- Scans files for proper tagging (purpose, author, date, usage)
- Identifies files missing critical tags
- Generates tagging improvement recommendations
- Creates comprehensive reports for SSOT coordination
- Supports multiple file types and directories

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-28
Purpose: Improve agent discoverability and tool documentation
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TagAnalysis:
    """Analysis result for a single file."""
    file_path: Path
    file_type: str
    has_purpose: bool
    has_author: bool
    has_created_date: bool
    has_usage: bool
    has_description: bool
    score: int  # Out of 5
    recommendations: List[str]


class ToolTaggingAnalyzer:
    """Analyzes files for proper tagging and discoverability."""

    def __init__(self, target_dir: Optional[Path] = None):
        """Initialize the analyzer."""
        self.target_dir = target_dir or Path("tools")
        self.supported_extensions = ['.py', '.md', '.sh', '.js', '.ts', '.json', '.yaml', '.yml']

        # Tag patterns to look for
        self.tag_patterns = {
            'purpose': ['purpose', 'goal', 'objective', 'what this does'],
            'author': ['author', 'created by', '@author', 'by:'],
            'created_date': ['created', 'date', 'written on', 'last updated'],
            'usage': ['usage', 'example', 'how to use', 'command'],
            'description': ['description', 'overview', 'summary']
        }

    def analyze_file(self, file_path: Path) -> TagAnalysis:
        """Analyze a single file for tagging."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(3000).lower()  # First 3000 chars, lowercase for matching

            file_type = file_path.suffix
            recommendations = []

            # Check for each tag type
            has_purpose = any(pattern in content for pattern in self.tag_patterns['purpose'])
            has_author = any(pattern in content for pattern in self.tag_patterns['author'])
            has_created_date = any(pattern in content for pattern in self.tag_patterns['created_date'])
            has_usage = any(pattern in content for pattern in self.tag_patterns['usage'])
            has_description = any(pattern in content for pattern in self.tag_patterns['description'])

            # Calculate score (0-5)
            score = sum([has_purpose, has_author, has_created_date, has_usage, has_description])

            # Generate recommendations
            if not has_purpose:
                recommendations.append("Add purpose/goal section explaining what this tool does")
            if not has_author:
                recommendations.append("Add author attribution (who created/maintains this)")
            if not has_created_date:
                recommendations.append("Add creation/last updated date")
            if not has_usage:
                recommendations.append("Add usage examples or command-line help")
            if not has_description:
                recommendations.append("Add brief description/overview at the top")

            return TagAnalysis(
                file_path=file_path,
                file_type=file_type,
                has_purpose=has_purpose,
                has_author=has_author,
                has_created_date=has_created_date,
                has_usage=has_usage,
                has_description=has_description,
                score=score,
                recommendations=recommendations
            )

        except Exception as e:
            return TagAnalysis(
                file_path=file_path,
                file_type=file_path.suffix,
                has_purpose=False,
                has_author=False,
                has_created_date=False,
                has_usage=False,
                has_description=False,
                score=0,
                recommendations=[f"Error analyzing file: {str(e)}"]
            )

    def analyze_directory(self) -> List[TagAnalysis]:
        """Analyze all supported files in the target directory."""
        results = []

        if not self.target_dir.exists():
            print(f"Directory {self.target_dir} does not exist")
            return results

        for file_path in self.target_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                analysis = self.analyze_file(file_path)
                results.append(analysis)

        return results

    def generate_report(self, results: List[TagAnalysis]) -> str:
        """Generate comprehensive tagging analysis report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate statistics
        total_files = len(results)
        if total_files == 0:
            return f"# Tag Analysis Report\n**Generated:** {timestamp}\n\nNo files found to analyze."

        scores = [r.score for r in results]
        avg_score = sum(scores) / total_files

        perfect_files = sum(1 for r in results if r.score == 5)
        needs_work = sum(1 for r in results if r.score < 3)

        # Group by score
        score_distribution = {}
        for i in range(6):
            score_distribution[i] = sum(1 for r in results if r.score == i)

        report = f"""# Tool Tagging Analysis Report
**Generated:** {timestamp}
**Directory:** {self.target_dir}
**Files Analyzed:** {total_files}

## Executive Summary
- **Average Tag Score:** {avg_score:.1f}/5.0
- **Perfect Files (5/5):** {score_distribution[5]} ({score_distribution[5]/total_files*100:.1f}%)
- **Needs Work (<3/5):** {sum(score_distribution[i] for i in range(3))} ({sum(score_distribution[i] for i in range(3))/total_files*100:.1f}%)

## Score Distribution

"""

        for score in range(5, -1, -1):
            count = score_distribution[score]
            percentage = count / total_files * 100
            bar = "█" * int(percentage / 5)  # Scale to 20 chars max
            report += f"**{score}/5:** {count} files ({percentage:.1f}%) {bar}\n"

        report += "\n## Files Needing Attention\n\n"

        # Sort by score (worst first)
        sorted_results = sorted(results, key=lambda x: x.score)

        for result in sorted_results:
            if result.score < 4:  # Only show files that need work
                relative_path = result.file_path.relative_to(self.target_dir.parent)
                report += f"### {relative_path} (Score: {result.score}/5)\n"
                report += f"**Type:** {result.file_type}\n"

                # Show what's missing
                missing = []
                if not result.has_purpose: missing.append("Purpose")
                if not result.has_author: missing.append("Author")
                if not result.has_created_date: missing.append("Date")
                if not result.has_usage: missing.append("Usage")
                if not result.has_description: missing.append("Description")

                if missing:
                    report += f"**Missing:** {', '.join(missing)}\n"

                if result.recommendations:
                    report += "**Recommendations:**\n"
                    for rec in result.recommendations:
                        report += f"- {rec}\n"

                report += "\n"

        # Top recommendations
        report += "## Top Recommendations\n\n"

        # Count most common issues
        all_recommendations = []
        for result in results:
            all_recommendations.extend(result.recommendations)

        rec_count = {}
        for rec in all_recommendations:
            rec_count[rec] = rec_count.get(rec, 0) + 1

        sorted_recs = sorted(rec_count.items(), key=lambda x: x[1], reverse=True)

        for rec, count in sorted_recs[:5]:
            report += f"- **{rec}** ({count} files)\n"

        report += "\n## Next Steps\n\n"
        report += "1. **High Priority:** Fix files with score < 3\n"
        report += "2. **Medium Priority:** Add missing purpose/description to files with score 3-4\n"
        report += "3. **Low Priority:** Add usage examples to remaining files\n"
        report += "4. **Re-run this analyzer** after improvements to track progress\n"
        report += "\n## SSOT Integration\n\n"
        report += "This analysis supports SSOT coordination by improving discoverability. "
        report += "Well-tagged tools are easier for agents to find and use correctly.\n"

        return report

    def save_report(self, report: str, output_file: Optional[str] = None) -> Path:
        """Save report to file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reports/tag_analysis_report_{timestamp}.md"

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze files for proper tagging and discoverability"
    )
    parser.add_argument(
        "--directory",
        help="Directory to analyze (default: tools)"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report only (no console output)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: auto-generated)"
    )

    args = parser.parse_args()

    target_dir = Path(args.directory) if args.directory else Path("tools")
    analyzer = ToolTaggingAnalyzer(target_dir)

    # Run analysis
    results = analyzer.analyze_directory()

    if not args.report_only:
        # Console output
        total_files = len(results)
        if total_files == 0:
            print("No files found to analyze")
            return

        scores = [r.score for r in results]
        avg_score = sum(scores) / total_files
        perfect_files = sum(1 for r in results if r.score == 5)
        needs_work = sum(1 for r in results if r.score < 3)

        print("Tag Analysis Summary:")
        print(f"  Directory: {target_dir}")
        print(f"  Files analyzed: {total_files}")
        print(f"  Average score: {avg_score:.1f}/5.0")
        print(f"  Perfect files: {perfect_files}")
        print(f"  Needs work: {needs_work}")

        # Show worst 5 files
        sorted_results = sorted(results, key=lambda x: x.score)
        print("\nFiles needing most attention:")
        for result in sorted_results[:5]:
            relative_path = result.file_path.relative_to(target_dir.parent)
            print(f"  {result.score}/5: {relative_path}")

    # Generate and save report
    report = analyzer.generate_report(results)
    report_path = analyzer.save_report(report, args.output)

    if not args.report_only:
        print(f"\nReport saved: {report_path}")


if __name__ == "__main__":
    main()
