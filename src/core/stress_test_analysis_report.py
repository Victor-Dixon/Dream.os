#!/usr/bin/env python3
<!-- SSOT Domain: core -->
"""
Stress Test Analysis Report Generator
======================================

Generate comprehensive analysis reports from stress test metrics:
- Metrics analysis summary
- Bottleneck identification
- Optimization recommendations
- Performance insights
- Dashboard visualization data

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .stress_test_metrics_analyzer import StressTestMetricsAnalyzer

logger = logging.getLogger(__name__)


class StressTestAnalysisReport:
    """Generate comprehensive stress test analysis reports."""

    def __init__(self, dashboard_data: Optional[dict[str, Any]] = None):
        """Initialize analysis report generator."""
        self.analyzer = StressTestMetricsAnalyzer(dashboard_data)
        self.logger = logger

    def generate_full_report(self, output_dir: Optional[Path] = None) -> dict[str, Any]:
        """Generate full analysis report."""
        try:
            output_dir = output_dir or Path("stress_test_analysis_results")
            output_dir.mkdir(exist_ok=True)

            # Generate all analysis components
            report = {
                "report_metadata": {
                    "generated_at": datetime.now().isoformat(),
                    "analyzer_version": "1.0.0",
                    "report_type": "full_analysis",
                },
                "executive_summary": self._generate_executive_summary(),
                "latency_analysis": self.analyzer.analyze_latency_patterns(),
                "bottleneck_analysis": {
                    "bottlenecks": self.analyzer.identify_bottlenecks(),
                    "severity_breakdown": self._calculate_severity_breakdown(),
                },
                "optimization_opportunities": self.analyzer.generate_optimization_opportunities(),
                "performance_recommendations": self.analyzer.generate_performance_recommendations(),
                "dashboard_visualization": self.analyzer.generate_dashboard_visualization_data(),
                "key_findings": self._generate_key_findings(),
                "action_items": self._generate_action_items(),
            }

            # Save report to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = output_dir / f"stress_test_analysis_report_{timestamp}.json"
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2)

            # Generate markdown summary
            markdown_file = output_dir / f"stress_test_analysis_summary_{timestamp}.md"
            self._generate_markdown_summary(report, markdown_file)

            self.logger.info(f"Analysis report generated: {report_file}")
            self.logger.info(f"Summary report generated: {markdown_file}")

            return report
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return {}

    def _generate_executive_summary(self) -> dict[str, Any]:
        """Generate executive summary."""
        bottlenecks = self.analyzer.identify_bottlenecks()
        overall = self.analyzer.dashboard_data.get("overall_metrics", {})

        high_severity = sum(1 for b in bottlenecks if b["severity"] == "high")
        medium_severity = sum(1 for b in bottlenecks if b["severity"] == "medium")

        latency = overall.get("latency_percentiles", {})
        throughput = overall.get("throughput_msg_per_sec", 0)
        failure_rate = overall.get("failure_rate_percent", 0)

        summary = {
            "test_performance": {
                "overall_status": (
                    "needs_attention" if high_severity > 0 else "acceptable"
                    if medium_severity > 0 else "good"
                ),
                "p99_latency_ms": latency.get("p99", 0),
                "throughput_msg_per_sec": throughput,
                "failure_rate_percent": failure_rate,
            },
            "critical_issues": high_severity,
            "optimization_opportunities": len(
                self.analyzer.generate_optimization_opportunities()
            ),
            "top_priority": (
                bottlenecks[0]["description"]
                if bottlenecks and bottlenecks[0]["severity"] == "high"
                else "No critical issues identified"
            ),
        }

        return summary

    def _calculate_severity_breakdown(self) -> dict[str, Any]:
        """Calculate severity breakdown of bottlenecks."""
        bottlenecks = self.analyzer.identify_bottlenecks()

        breakdown = {
            "high": {"count": 0, "bottlenecks": []},
            "medium": {"count": 0, "bottlenecks": []},
            "low": {"count": 0, "bottlenecks": []},
        }

        for bottleneck in bottlenecks:
            severity = bottleneck.get("severity", "low")
            breakdown[severity]["count"] += 1
            breakdown[severity]["bottlenecks"].append(bottleneck)

        return breakdown

    def _generate_key_findings(self) -> list[dict[str, Any]]:
        """Generate key findings."""
        findings = []
        bottlenecks = self.analyzer.identify_bottlenecks()
        overall = self.analyzer.dashboard_data.get("overall_metrics", {})

        # High latency finding
        latency = overall.get("latency_percentiles", {})
        if latency.get("p99", 0) > 500:
            findings.append({
                "category": "latency",
                "severity": "high" if latency.get("p99", 0) > 1000 else "medium",
                "finding": f"Tail latency (p99: {latency.get('p99', 0):.2f}ms) exceeds optimal thresholds",
                "impact": "User experience degradation, potential timeout issues",
            })

        # Throughput finding
        throughput = overall.get("throughput_msg_per_sec", 0)
        if throughput < 50:
            findings.append({
                "category": "throughput",
                "severity": "high" if throughput < 20 else "medium",
                "finding": f"Throughput ({throughput:.2f} msg/sec) below expected capacity",
                "impact": "System may struggle under high load",
            })

        # Failure rate finding
        failure_rate = overall.get("failure_rate_percent", 0)
        if failure_rate > 1.0:
            findings.append({
                "category": "reliability",
                "severity": "high" if failure_rate > 5.0 else "medium",
                "finding": f"Failure rate ({failure_rate:.2f}%) exceeds acceptable threshold",
                "impact": "Data loss, retry overhead, user trust issues",
            })

        return findings

    def _generate_action_items(self) -> list[dict[str, Any]]:
        """Generate prioritized action items."""
        action_items = []
        bottlenecks = self.analyzer.identify_bottlenecks()
        opportunities = self.analyzer.generate_optimization_opportunities()

        # Add high-priority actions from bottlenecks
        for bottleneck in bottlenecks:
            if bottleneck["severity"] == "high":
                action_items.append({
                    "priority": "urgent",
                    "category": bottleneck["type"],
                    "action": f"Address {bottleneck['type']} bottleneck",
                    "description": bottleneck["description"],
                    "estimated_effort": "2-4 hours",
                    "expected_impact": "Significant performance improvement",
                })

        # Add optimization opportunities
        for opp in opportunities:
            if opp["priority"] == "high":
                action_items.append({
                    "priority": "high",
                    "category": opp["category"],
                    "action": opp["recommendation"],
                    "description": "; ".join(opp["actions"][:2]),
                    "estimated_effort": "4-8 hours",
                    "expected_impact": opp.get("expected_impact", "Performance improvement"),
                })

        return sorted(action_items, key=lambda x: {"urgent": 0, "high": 1, "medium": 2}[x["priority"]])

    def _generate_markdown_summary(self, report: dict[str, Any], output_file: Path) -> None:
        """Generate markdown summary report."""
        try:
            summary = report.get("executive_summary", {})
            bottlenecks = report.get("bottleneck_analysis", {}).get("bottlenecks", [])
            findings = report.get("key_findings", [])
            actions = report.get("action_items", [])

            markdown_content = f"""# Stress Test Analysis Report

**Generated**: {report.get('report_metadata', {}).get('generated_at', 'N/A')}

---

## Executive Summary

**Overall Status**: {summary.get('test_performance', {}).get('overall_status', 'N/A').upper()}

**Key Metrics:**
- P99 Latency: {summary.get('test_performance', {}).get('p99_latency_ms', 0):.2f} ms
- Throughput: {summary.get('test_performance', {}).get('throughput_msg_per_sec', 0):.2f} msg/sec
- Failure Rate: {summary.get('test_performance', {}).get('failure_rate_percent', 0):.2f}%

**Critical Issues**: {summary.get('critical_issues', 0)}

**Top Priority**: {summary.get('top_priority', 'N/A')}

---

## Key Findings

"""

            for finding in findings:
                markdown_content += f"""
### {finding.get('category', 'Unknown').upper()}

- **Finding**: {finding.get('finding', 'N/A')}
- **Severity**: {finding.get('severity', 'N/A').upper()}
- **Impact**: {finding.get('impact', 'N/A')}

"""

            markdown_content += """
---

## Bottlenecks Identified

"""

            for bottleneck in bottlenecks[:5]:  # Top 5
                markdown_content += f"""
### {bottleneck.get('type', 'Unknown').replace('_', ' ').title()}

- **Severity**: {bottleneck.get('severity', 'N/A').upper()}
- **Description**: {bottleneck.get('description', 'N/A')}
- **Metric**: {bottleneck.get('metric', 'N/A')}
- **Value**: {bottleneck.get('value', 0)}

"""

            markdown_content += """
---

## Recommended Action Items

"""

            for action in actions[:10]:  # Top 10
                markdown_content += f"""
### {action.get('action', 'N/A')} (Priority: {action.get('priority', 'N/A').upper()})

- **Category**: {action.get('category', 'N/A')}
- **Description**: {action.get('description', 'N/A')}
- **Estimated Effort**: {action.get('estimated_effort', 'N/A')}
- **Expected Impact**: {action.get('expected_impact', 'N/A')}

"""

            markdown_content += """
---

*Report generated by Stress Test Metrics Analyzer*
"""

            with open(output_file, "w") as f:
                f.write(markdown_content)

            self.logger.info(f"Markdown summary generated: {output_file}")
        except Exception as e:
            self.logger.error(f"Error generating markdown summary: {e}")


__all__ = ["StressTestAnalysisReport"]

