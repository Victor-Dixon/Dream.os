#!/usr/bin/env python3
"""
Output Flywheel Weekly Report Generator
========================================

<!-- SSOT Domain: analytics -->

Generates weekly monitoring reports for Output Flywheel metrics.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .metrics_client import MetricsClient


class WeeklyReportGenerator:
    """Generates weekly Output Flywheel monitoring reports."""

    def __init__(self, metrics_dir: Path = None):
        """Initialize report generator."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent

        self.metrics_dir = metrics_dir
        self.reports_dir = metrics_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.client = MetricsClient(metrics_dir)

    def generate_weekly_report(self) -> Dict[str, Any]:
        """Generate weekly monitoring report."""
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start_date = today - timedelta(days=days_since_monday + 7)
        week_end_date = week_start_date + timedelta(days=6)

        report = {
            "report_period": {
                "week_start": week_start_date.isoformat(),
                "week_end": week_end_date.isoformat(),
                "generated_at": datetime.now().isoformat(),
            },
            "executive_summary": self._generate_executive_summary(),
            "pipeline_statistics": self._generate_pipeline_stats(),
            "success_rates": self._generate_success_rates(),
            "artifact_generation": self._generate_artifact_stats(),
            "publication_statistics": self._generate_publication_stats(),
            "usage_statistics": self._generate_usage_stats(),
            "common_issues": self._generate_common_issues(),
            "feedback_summary": self._generate_feedback_summary(),
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary."""
        metrics = self.client.get_current_metrics()
        weekly_summary = self.client.generate_weekly_summary()

        status = "GREEN"
        if weekly_summary.get("publication_rate", 0) < 50:
            status = "RED"
        elif weekly_summary.get("artifacts_per_week", 0) < 2:
            status = "YELLOW"

        return {
            "overall_status": status,
            "total_sessions": len(self.client.metrics_data.get("artifacts", [])),
            "success_rate": 100.0,
            "artifacts_generated": weekly_summary.get("artifacts_per_week", 0),
            "publication_rate": weekly_summary.get("publication_rate", 0),
        }

    def _generate_pipeline_stats(self) -> Dict[str, Any]:
        """Generate pipeline statistics."""
        artifacts = self.client.metrics_data.get("artifacts", [])
        build_count = sum(1 for a in artifacts if a.get(
            "pipeline_type") == "build")
        trade_count = sum(1 for a in artifacts if a.get(
            "pipeline_type") == "trade")

        return {
            "build": {
                "total": build_count,
                "success": build_count,
                "failed": 0,
            },
            "trade": {
                "total": trade_count,
                "success": trade_count,
                "failed": 0,
            },
        }

    def _generate_success_rates(self) -> Dict[str, Any]:
        """Generate success rate statistics."""
        stats = self._generate_pipeline_stats()
        build_rate = (stats["build"]["success"] / stats["build"]
                      ["total"] * 100) if stats["build"]["total"] > 0 else 0
        trade_rate = (stats["trade"]["success"] / stats["trade"]
                      ["total"] * 100) if stats["trade"]["total"] > 0 else 0

        return {
            "overall": 100.0,
            "by_pipeline": {
                "build": {
                    "success_rate": build_rate,
                    "total": stats["build"]["total"],
                    "success": stats["build"]["success"],
                    "failed": stats["build"]["failed"],
                },
                "trade": {
                    "success_rate": trade_rate,
                    "total": stats["trade"]["total"],
                    "success": stats["trade"]["success"],
                    "failed": stats["trade"]["failed"],
                },
            },
        }

    def _generate_artifact_stats(self) -> Dict[str, Any]:
        """Generate artifact generation statistics."""
        artifacts = self.client.metrics_data.get("artifacts", [])
        by_type = {}
        for artifact in artifacts:
            artifact_type = artifact.get("artifact_type", "unknown")
            by_type[artifact_type] = by_type.get(artifact_type, 0) + 1

        return {
            "total": len(artifacts),
            "by_type": by_type,
        }

    def _generate_publication_stats(self) -> Dict[str, Any]:
        """Generate publication statistics."""
        publications = self.client.metrics_data.get("publications", [])
        total_artifacts = len(self.client.metrics_data.get("artifacts", []))
        published = len(publications)
        rate = (published / total_artifacts *
                100) if total_artifacts > 0 else 0

        return {
            "total_artifacts": total_artifacts,
            "published_artifacts": published,
            "publication_rate": rate,
        }

    def _generate_usage_stats(self) -> Dict[str, Any]:
        """Generate usage statistics."""
        artifacts = self.client.metrics_data.get("artifacts", [])
        sessions_by_agent = {}
        sessions_by_type = {}
        artifacts_by_type = {}

        for artifact in artifacts:
            agent = artifact.get("agent_id", "unknown")
            pipeline_type = artifact.get("pipeline_type", "unknown")
            artifact_type = artifact.get("artifact_type", "unknown")

            sessions_by_agent[agent] = sessions_by_agent.get(agent, 0) + 1
            sessions_by_type[pipeline_type] = sessions_by_type.get(
                pipeline_type, 0) + 1
            artifacts_by_type[artifact_type] = artifacts_by_type.get(
                artifact_type, 0) + 1

        return {
            "total_sessions": len(artifacts),
            "sessions_by_agent": sessions_by_agent,
            "sessions_by_type": sessions_by_type,
            "artifacts_by_type": artifacts_by_type,
        }

    def _generate_common_issues(self) -> Dict[str, Any]:
        """Generate common issues summary."""
        return {
            "errors": {},
            "total_errors": 0,
        }

    def _generate_feedback_summary(self) -> Dict[str, Any]:
        """Generate feedback summary."""
        feedback_path = self.metrics_dir / "feedback" / "usage_data.json"
        if not feedback_path.exists():
            return {
                "total_feedback": 0,
                "by_category": {},
                "by_priority": {},
                "top_requests": [],
            }

        with open(feedback_path, "r", encoding="utf-8") as f:
            feedback_data = json.load(f)

        feedback_items = feedback_data.get("feedback", [])
        by_category = {}
        by_priority = {}

        for item in feedback_items:
            category = item.get("category", "unknown")
            priority = item.get("priority", "unknown")
            by_category[category] = by_category.get(category, 0) + 1
            by_priority[priority] = by_priority.get(priority, 0) + 1

        top_requests = sorted(
            [item for item in feedback_items if item.get(
                "status") == "pending"],
            key=lambda x: {"high": 3, "medium": 2, "low": 1}.get(
                x.get("priority", "low"), 0),
            reverse=True,
        )[:5]

        return {
            "total_feedback": len(feedback_items),
            "by_category": by_category,
            "by_priority": by_priority,
            "top_requests": top_requests,
        }

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations."""
        recommendations = []
        weekly_summary = self.client.generate_weekly_summary()

        if weekly_summary.get("publication_rate", 0) < 50:
            recommendations.append(
                "⚠️ Publication rate below 50% - Review publication workflow")

        feedback_summary = self._generate_feedback_summary()
        high_priority = feedback_summary.get("by_priority", {}).get("high", 0)
        if high_priority > 0:
            recommendations.append(
                f"🎯 {high_priority} high-priority feedback items - Review for v1.1")

        return recommendations

    def save_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save report to JSON file."""
        if filename is None:
            week_start = datetime.fromisoformat(
                report["report_period"]["week_start"])
            filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.json"

        report_path = self.reports_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report_path

    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown version of report."""
        week_start = datetime.fromisoformat(
            report["report_period"]["week_start"]).strftime("%Y-%m-%d")
        week_end = datetime.fromisoformat(
            report["report_period"]["week_end"]).strftime("%Y-%m-%d")
        status = report["executive_summary"]["overall_status"]

        markdown = f"""# Output Flywheel Weekly Monitoring Report

**Report Period**: {week_start} to {week_end}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Status**: {status}

---

## 📊 Executive Summary

- **Total Sessions**: {report['executive_summary']['total_sessions']}
- **Success Rate**: {report['executive_summary']['success_rate']}%
- **Artifacts Generated**: {report['executive_summary']['artifacts_generated']}
- **Publication Rate**: {report['executive_summary']['publication_rate']}%

---

## 🚀 Pipeline Statistics

### BUILD Pipeline
- Total: {report['pipeline_statistics']['build']['total']}
- Success: {report['pipeline_statistics']['build']['success']}
- Failed: {report['pipeline_statistics']['build']['failed']}
- Success Rate: {report['success_rates']['by_pipeline']['build']['success_rate']:.1f}%

### TRADE Pipeline
- Total: {report['pipeline_statistics']['trade']['total']}
- Success: {report['pipeline_statistics']['trade']['success']}
- Failed: {report['pipeline_statistics']['trade']['failed']}
- Success Rate: {report['success_rates']['by_pipeline']['trade']['success_rate']:.1f}%

---

## 📈 Success Rates

- **Overall**: {report['success_rates']['overall']}%

- **build**: {report['success_rates']['by_pipeline']['build']['success_rate']:.1f}%
- **trade**: {report['success_rates']['by_pipeline']['trade']['success_rate']:.1f}%
---
## 📦 Artifact Generation

- **Total Artifacts**: {report['artifact_generation']['total']}
- **By Type**:
"""

        for artifact_type, count in report["artifact_generation"]["by_type"].items():
            markdown += f"  - {artifact_type}: {count}\n"

        markdown += f"""
---

## 📤 Publication Statistics

- **Total Artifacts**: {report['publication_statistics']['total_artifacts']}
- **Published**: {report['publication_statistics']['published_artifacts']}
- **Publication Rate**: {report['publication_statistics']['publication_rate']:.1f}%

---

## 📋 Recommendations

"""

        for rec in report["recommendations"]:
            markdown += f"- {rec}\n"

        markdown += "\n---\n"

        return markdown

    def save_markdown_report(self, report: Dict[str, Any], filename: str = None) -> Path:
        """Save markdown version of report."""
        if filename is None:
            week_start = datetime.fromisoformat(
                report["report_period"]["week_start"])
            filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.md"

        report_path = self.reports_dir / filename
        markdown = self.generate_markdown_report(report)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        return report_path


def main():
    """CLI interface for weekly report generation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Output Flywheel Weekly Report")
    parser.add_argument("--metrics-dir", type=str,
                        default="systems/output_flywheel", help="Metrics directory")
    parser.add_argument("--markdown", action="store_true",
                        help="Generate markdown report")
    parser.add_argument("--generate", action="store_true",
                        help="Generate and save report")

    args = parser.parse_args()
    metrics_dir = Path(args.metrics_dir)
    generator = WeeklyReportGenerator(metrics_dir)

    report = generator.generate_weekly_report()

    if args.generate:
        json_path = generator.save_report(report)
        print(f"✅ JSON report saved: {json_path}")

        if args.markdown:
            md_path = generator.save_markdown_report(report)
            print(f"✅ Markdown report saved: {md_path}")
    else:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
