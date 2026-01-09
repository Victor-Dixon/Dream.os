#!/usr/bin/env python3
"""
Output Flywheel Weekly Report Generator
=======================================

<!-- SSOT Domain: analytics -->

Generates weekly progress reports for Output Flywheel metrics and usage.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-05
Priority: MEDIUM
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

from .metrics_client import MetricsClient


class WeeklyReportGenerator:
    """Generates weekly Output Flywheel reports."""

    def __init__(self, metrics_client: Optional[MetricsClient] = None):
        """Initialize report generator."""
        self.metrics_client = metrics_client or MetricsClient()
        self.reports_dir = Path(__file__).parent / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_weekly_report(
        self,
        week_start: Optional[datetime] = None,
        output_format: str = "markdown",
    ) -> Dict[str, Any]:
        """
        Generate weekly report for Output Flywheel metrics.

        Args:
            week_start: Start of week (defaults to Monday of current week)
            output_format: Output format ('markdown' or 'json')

        Returns:
            Report data dictionary
        """
        if week_start is None:
            # Get Monday of current week
            today = datetime.now()
            days_since_monday = today.weekday()
            week_start = today - timedelta(days=days_since_monday)
            week_start = week_start.replace(
                hour=0, minute=0, second=0, microsecond=0)

        week_end = week_start + timedelta(days=7)

        # Get metrics for the week
        metrics = self.metrics_client.get_metrics_summary(
            start_date=week_start,
            end_date=week_end,
        )

        # Generate report data
        report_data = {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "generated_at": datetime.now().isoformat(),
            "metrics": metrics,
            "summary": {
                "artifacts_generated": metrics.get("artifacts_count", 0),
                "repos_updated": metrics.get("repos_updated", 0),
                "publication_rate": metrics.get("publication_rate", 0.0),
                "success_rate": metrics.get("success_rate", 0.0),
            },
        }

        # Save report
        if output_format == "markdown":
            self._save_markdown_report(report_data, week_start)
        else:
            self._save_json_report(report_data, week_start)

        return report_data

    def _save_markdown_report(self, report_data: Dict[str, Any], week_start: datetime) -> None:
        """Save report as markdown."""
        filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.md"
        filepath = self.reports_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Output Flywheel Weekly Report\n\n")
            f.write(
                f"**Week**: {week_start.strftime('%Y-%m-%d')} to {(week_start + timedelta(days=7)).strftime('%Y-%m-%d')}\n\n")
            f.write(f"**Generated**: {report_data['generated_at']}\n\n")
            f.write("## Summary\n\n")
            f.write(
                f"- **Artifacts Generated**: {report_data['summary']['artifacts_generated']}\n")
            f.write(
                f"- **Repos Updated**: {report_data['summary']['repos_updated']}\n")
            f.write(
                f"- **Publication Rate**: {report_data['summary']['publication_rate']:.1%}\n")
            f.write(
                f"- **Success Rate**: {report_data['summary']['success_rate']:.1%}\n\n")
            f.write("## Metrics\n\n")
            f.write("```json\n")
            f.write(json.dumps(report_data['metrics'], indent=2))
            f.write("\n```\n")

    def _save_json_report(self, report_data: Dict[str, Any], week_start: datetime) -> None:
        """Save report as JSON."""
        filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.json"
        filepath = self.reports_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)


if __name__ == "__main__":
    generator = WeeklyReportGenerator()
    report = generator.generate_weekly_report()
    print(f"✅ Weekly report generated: {report['generated_at']}")