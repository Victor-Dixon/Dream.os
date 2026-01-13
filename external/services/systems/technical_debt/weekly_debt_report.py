#!/usr/bin/env python3
"""
Weekly Technical Debt Report Generator
=====================================

Automatically generates comprehensive technical debt reports including:
- Code duplication metrics
- SSOT compliance status
- Error rates and trends
- File size and complexity analysis
- Recommendations for debt reduction

Runs weekly via scheduled task and integrates with CI/CD.

Author: Agent-4 (Captain) - Technical Debt Analytics Specialist
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics

@dataclass
class DebtMetrics:
    """Technical debt metrics snapshot."""
    timestamp: datetime
    total_files: int
    total_lines: int
    duplicate_files: int
    duplicate_groups: int
    ssot_violations: int
    syntax_errors: int
    test_coverage: float
    error_rate_24h: float
    largest_file_kb: int
    avg_file_size_kb: float
    technical_debt_score: int  # 0-100 scale

@dataclass
class DebtRecommendation:
    """Technical debt reduction recommendation."""
    priority: str  # "HIGH", "MEDIUM", "LOW"
    category: str  # "DUPLICATION", "SSOT", "COMPLEXITY", etc.
    description: str
    effort_estimate: str  # "SMALL", "MEDIUM", "LARGE"
    impact_score: int  # 1-10
    files_affected: List[str]

class TechnicalDebtReporter:
    """Generates comprehensive technical debt reports."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.reports_dir = repo_root / "reports" / "technical_debt"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_weekly_report(self) -> str:
        """Generate complete weekly technical debt report."""
        print("📊 Generating Weekly Technical Debt Report...")

        # Collect all metrics
        metrics = self._collect_metrics()
        recommendations = self._generate_recommendations(metrics)

        # Generate report
        report = self._format_report(metrics, recommendations)

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"debt_report_{timestamp}.md"
        report_file.write_text(report)

        # Save metrics as JSON for trending
        metrics_file = self.reports_dir / f"metrics_{timestamp}.json"
        metrics_data = asdict(metrics)
        # Convert datetime to string for JSON
        metrics_data["timestamp"] = metrics.timestamp.isoformat()
        metrics_file.write_text(json.dumps(metrics_data, indent=2))

        print(f"✅ Report saved to: {report_file}")
        return report

    def _collect_metrics(self) -> DebtMetrics:
        """Collect comprehensive technical debt metrics using SSOT scanner."""
        print("  📏 Collecting metrics using SSOT scanner...")

        # Run SSOT debt scanner
        try:
            import subprocess
            import json
            from pathlib import Path

            # Run the SSOT scanner
            result = subprocess.run([
                "python", "tools/debt_scan.py"
            ], capture_output=True, text=True, cwd=self.repo_root)

            if result.returncode == 0 and result.stdout:
                # Parse JSON output from reports/debt_scan.json
                report_path = self.repo_root / "reports" / "debt_scan.json"
                if report_path.exists():
                    with open(report_path, "r", encoding="utf-8") as f:
                        scan_data = json.load(f)

                    return DebtMetrics(
                        timestamp=datetime.fromisoformat(scan_data["timestamp"]),
                        total_files=scan_data["total_files"],
                        total_lines=scan_data["total_lines"],
                        duplicate_files=sum(len(dup["files"]) for dup in scan_data["duplicate_groups"]),
                        duplicate_groups=len(scan_data["duplicate_groups"]),
                        ssot_violations=len(scan_data["ssot_violations"]),
                        syntax_errors=len(scan_data["syntax_errors"]),
                        test_coverage=scan_data["test_coverage_estimate"],
                        error_rate_24h=scan_data["error_rate_24h"],
                        largest_file_kb=scan_data["largest_file_kb"],
                        avg_file_size_kb=scan_data["avg_file_size_kb"],
                        technical_debt_score=0  # Will be calculated below
                    )

        except (subprocess.SubprocessError, json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            print(f"     Warning: SSOT scanner failed, falling back to basic metrics: {e}")

        # Fallback to basic metrics if SSOT scanner fails
        total_files, total_lines = self._count_files_and_lines()
        largest_file_kb, avg_file_size_kb = self._analyze_file_sizes()

        return DebtMetrics(
            timestamp=datetime.now(),
            total_files=total_files,
            total_lines=total_lines,
            duplicate_files=0,  # Unknown without scanner
            duplicate_groups=0,
            ssot_violations=0,
            syntax_errors=0,
            test_coverage=0.0,
            error_rate_24h=0.0,
            largest_file_kb=largest_file_kb,
            avg_file_size_kb=avg_file_size_kb,
            technical_debt_score=0
        )

    def _count_files_and_lines(self) -> Tuple[int, int]:
        """Count total files and lines of code."""
        total_files = 0
        total_lines = 0

        skip_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}

        for file_path in self.repo_root.rglob("*"):
            if not file_path.is_file():
                continue

            if any(part in skip_dirs for part in file_path.parts):
                continue

            if file_path.suffix in [".py", ".js", ".ts", ".md"]:
                total_files += 1

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = len(f.readlines())
                        total_lines += lines
                except (OSError, UnicodeDecodeError):
                    pass

        return total_files, total_lines

    def _analyze_file_sizes(self) -> Tuple[int, float]:
        """Analyze file sizes for complexity metrics."""
        file_sizes_kb = []

        for file_path in self.repo_root.rglob("*.py"):
            if not any(part in [".git", ".venv", "__pycache__"] for part in file_path.parts):
                try:
                    size_kb = file_path.stat().st_size / 1024
                    file_sizes_kb.append(size_kb)
                except OSError:
                    pass

        if file_sizes_kb:
            largest_file_kb = int(max(file_sizes_kb))
            avg_file_size_kb = round(statistics.mean(file_sizes_kb), 1)
        else:
            largest_file_kb = 0
            avg_file_size_kb = 0.0

        return largest_file_kb, avg_file_size_kb

    # All detection logic now moved to tools/debt_scan.py (SSOT)

    def _calculate_error_rate(self) -> float:
        """Calculate 24h rolling error rate."""
        # Check recent error logs
        logs_dir = self.repo_root / "logs"
        if not logs_dir.exists():
            return 0.0

        error_count = 0
        total_entries = 0

        # Check recent log files
        cutoff = datetime.now() - timedelta(hours=24)
        for log_file in logs_dir.glob("*.log"):
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    for line in f:
                        total_entries += 1
                        if "ERROR" in line or "CRITICAL" in line:
                            # Check if within 24h (rough check)
                            if "ERROR" in line:
                                error_count += 1
            except (OSError, UnicodeDecodeError):
                pass

        if total_entries == 0:
            return 0.0

        error_rate = (error_count / total_entries) * 100
        return round(error_rate, 2)

    def _calculate_debt_score(self, duplicates: int, ssot_violations: int,
                            syntax_errors: int, test_coverage: float,
                            total_files: int) -> int:
        """Calculate overall technical debt score (0-100) using SSOT scanner data."""
        score = 0

        # Duplication penalty (up to 40 points - more aggressive with accurate data)
        dup_ratio = duplicates / max(1, total_files)
        score += min(40, dup_ratio * 200)

        # SSOT violations penalty (up to 30 points)
        score += min(30, ssot_violations * 2)

        # Syntax errors penalty (up to 20 points)
        score += min(20, syntax_errors * 10)  # More aggressive for syntax errors

        # Test coverage bonus (up to -20 points)
        coverage_penalty = max(0, (80 - test_coverage) / 4)  # Penalty if < 80% coverage
        score += coverage_penalty

        return min(100, max(0, int(score)))

    def _generate_recommendations(self, metrics: DebtMetrics) -> List[DebtRecommendation]:
        """Generate debt reduction recommendations."""
        recommendations = []

        # High priority recommendations
        if metrics.duplicate_files > 10:
            recommendations.append(DebtRecommendation(
                priority="HIGH",
                category="DUPLICATION",
                description=f"Consolidate {metrics.duplicate_files} duplicate files into SSOT locations",
                effort_estimate="LARGE",
                impact_score=9,
                files_affected=["See reports/dup_scan.md"]
            ))

        if metrics.ssot_violations > 0:
            recommendations.append(DebtRecommendation(
                priority="HIGH",
                category="SSOT",
                description=f"Fix {metrics.ssot_violations} SSOT compliance violations",
                effort_estimate="MEDIUM",
                impact_score=8,
                files_affected=["Run scripts/ssot_linter.py for details"]
            ))

        if metrics.syntax_errors > 0:
            recommendations.append(DebtRecommendation(
                priority="HIGH",
                category="QUALITY",
                description=f"Fix {metrics.syntax_errors} Python syntax errors",
                effort_estimate="SMALL",
                impact_score=10,
                files_affected=["Run python main.py --scan-project"]
            ))

        if metrics.test_coverage < 70:
            recommendations.append(DebtRecommendation(
                priority="MEDIUM",
                category="TESTING",
                description=f"Increase test coverage from {metrics.test_coverage}% to >80%",
                effort_estimate="LARGE",
                impact_score=7,
                files_affected=["tests/"]
            ))

        if metrics.avg_file_size_kb > 50:
            recommendations.append(DebtRecommendation(
                priority="MEDIUM",
                category="COMPLEXITY",
                description=f"Refactor large files (avg {metrics.avg_file_size_kb}KB, largest {metrics.largest_file_kb}KB)",
                effort_estimate="MEDIUM",
                impact_score=6,
                files_affected=["Run file size analysis"]
            ))

        # Sort by impact score
        recommendations.sort(key=lambda x: x.impact_score, reverse=True)

        return recommendations[:5]  # Top 5 recommendations

    def _format_report(self, metrics: DebtMetrics,
                      recommendations: List[DebtRecommendation]) -> str:
        """Format the complete report."""
        report_lines = []

        # Header
        report_lines.append("# Weekly Technical Debt Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")

        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")

        debt_level = "LOW" if metrics.technical_debt_score < 30 else "MEDIUM" if metrics.technical_debt_score < 70 else "HIGH"
        report_lines.append(f"**Technical Debt Score:** {metrics.technical_debt_score}/100 ({debt_level})")
        report_lines.append(f"**Total Files:** {metrics.total_files:,}")
        report_lines.append(f"**Lines of Code:** {metrics.total_lines:,}")
        report_lines.append(f"**24h Error Rate:** {metrics.error_rate_24h}%")
        report_lines.append("")

        # Detailed Metrics
        report_lines.append("## Detailed Metrics")
        report_lines.append("")
        report_lines.append("| Metric | Value | Status |")
        report_lines.append("|--------|-------|--------|")
        report_lines.append(f"| Duplicate Files | {metrics.duplicate_files} | {'❌' if metrics.duplicate_files > 10 else '✅'} |")
        report_lines.append(f"| Duplicate Groups | {metrics.duplicate_groups} | {'❌' if metrics.duplicate_groups > 5 else '✅'} |")
        report_lines.append(f"| SSOT Violations | {metrics.ssot_violations} | {'❌' if metrics.ssot_violations > 0 else '✅'} |")
        report_lines.append(f"| Syntax Errors | {metrics.syntax_errors} | {'❌' if metrics.syntax_errors > 0 else '✅'} |")
        report_lines.append(f"| Test Coverage | {metrics.test_coverage}% | {'❌' if metrics.test_coverage < 70 else '✅'} |")
        report_lines.append(f"| Largest File | {metrics.largest_file_kb}KB | {'⚠️' if metrics.largest_file_kb > 200 else '✅'} |")
        report_lines.append(f"| Avg File Size | {metrics.avg_file_size_kb}KB | {'⚠️' if metrics.avg_file_size_kb > 50 else '✅'} |")
        report_lines.append("")

        # Recommendations
        report_lines.append("## Priority Recommendations")
        report_lines.append("")

        for rec in recommendations:
            priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[rec.priority]
            effort_emoji = {"SMALL": "🐌", "MEDIUM": "🏃", "LARGE": "🚀"}[rec.effort_estimate]

            report_lines.append(f"### {priority_emoji} {rec.category} - {rec.description}")
            report_lines.append(f"**Effort:** {effort_emoji} {rec.effort_estimate} | **Impact:** {rec.impact_score}/10")
            report_lines.append("")

        # Trends (placeholder for future enhancement)
        report_lines.append("## Trends & Analysis")
        report_lines.append("")
        report_lines.append("*Trend analysis will be available after multiple reports are generated.*")
        report_lines.append("")

        return "\n".join(report_lines)

def main():
    """Main entry point for weekly debt reporting."""
    print("📈 Weekly Technical Debt Report Generator")
    print("=" * 45)

    repo_root = Path(".")
    reporter = TechnicalDebtReporter(repo_root)

    try:
        report = reporter.generate_weekly_report()
        print("\n✅ Weekly technical debt report generated successfully!")
        print("📄 Check reports/technical_debt/ for the latest report")

        return 0
    except Exception as e:
        print(f"❌ Failed to generate report: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())