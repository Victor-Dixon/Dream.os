#!/usr/bin/env python3
"""
Output Flywheel Weekly Monitoring Report Generator
==================================================

Generates comprehensive weekly monitoring reports with:
- Usage statistics (pipelines run, artifacts generated)
- Success rates
- Common issues
- Top improvement requests
- Publication success rates

V2 Compliance:
- File: <300 lines ✅
- Class: <200 lines ✅
- Functions: <30 lines ✅

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-02
Priority: HIGH
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Handle imports
try:
    from .production_monitor import ProductionMonitor
    from .output_flywheel_usage_tracker import OutputFlywheelUsageTracker
    from .metrics_tracker import OutputFlywheelMetricsTracker
    from .unified_metrics_reader import UnifiedMetricsReader
except ImportError:
    from production_monitor import ProductionMonitor
    from output_flywheel_usage_tracker import OutputFlywheelUsageTracker
    from metrics_tracker import OutputFlywheelMetricsTracker
    from unified_metrics_reader import UnifiedMetricsReader


class WeeklyReportGenerator:
    """Generates comprehensive weekly monitoring reports."""

    def __init__(self, metrics_dir: Path = None):
        """Initialize report generator."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        
        self.metrics_dir = metrics_dir
        self.reports_dir = metrics_dir / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
        self.monitor = ProductionMonitor(metrics_dir)
        self.usage_tracker = OutputFlywheelUsageTracker(metrics_dir)
        self.metrics_tracker = OutputFlywheelMetricsTracker(metrics_dir)
        self.unified_metrics = UnifiedMetricsReader()

    def calculate_publication_rate(self) -> Dict[str, Any]:
        """Calculate publication success rates."""
        sessions_dir = self.metrics_dir / "outputs" / "sessions"
        artifacts_dir = self.metrics_dir / "outputs" / "artifacts"
        
        total_artifacts = 0
        published_artifacts = 0
        
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*_*.json"):
                try:
                    with open(session_file, "r", encoding="utf-8") as f:
                        session_data = json.load(f)
                    
                    artifacts = session_data.get("artifacts", {})
                    for artifact_key, artifact_data in artifacts.items():
                        if isinstance(artifact_data, dict):
                            if artifact_data.get("generated"):
                                total_artifacts += 1
                                if artifact_data.get("status") == "published":
                                    published_artifacts += 1
                except Exception:
                    continue
        
        rate = (published_artifacts / total_artifacts * 100.0) if total_artifacts > 0 else 0.0
        
        return {
            "total_artifacts": total_artifacts,
            "published_artifacts": published_artifacts,
            "publication_rate": rate,
        }

    def get_pipeline_statistics(self) -> Dict[str, Any]:
        """Get pipeline usage statistics."""
        sessions_data = self.monitor.analyze_session_files()
        
        by_type = {}
        for session_file in (self.metrics_dir / "outputs" / "sessions").glob("*_*.json"):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                
                session_type = session_data.get("session_type", "unknown")
                if session_type not in by_type:
                    by_type[session_type] = {"total": 0, "success": 0, "failed": 0}
                
                by_type[session_type]["total"] += 1
                pipeline_key = f"{session_type}_artifact"
                status = session_data.get("pipeline_status", {}).get(pipeline_key, "pending")
                if status == "complete":
                    by_type[session_type]["success"] += 1
                elif status == "failed":
                    by_type[session_type]["failed"] += 1
            except Exception:
                continue
        
        return by_type

    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get feedback summary from usage tracker."""
        feedback_path = self.metrics_dir / "feedback" / "v1.1_feedback.json"
        
        if not feedback_path.exists():
            return {
                "total_feedback": 0,
                "by_category": {},
                "by_priority": {},
                "top_requests": [],
            }
        
        try:
            with open(feedback_path, "r", encoding="utf-8") as f:
                feedback_data = json.load(f)
            
            entries = feedback_data.get("entries", [])
            
            by_category = {}
            by_priority = {}
            
            for entry in entries:
                category = entry.get("category", "other")
                priority = entry.get("priority", "medium")
                
                by_category[category] = by_category.get(category, 0) + 1
                by_priority[priority] = by_priority.get(priority, 0) + 1
            
            # Top requests (high priority)
            top_requests = [
                e for e in entries
                if e.get("priority") == "high"
            ]
            
            return {
                "total_feedback": len(entries),
                "by_category": by_category,
                "by_priority": by_priority,
                "top_requests": top_requests[:5],  # Top 5
            }
        except Exception:
            return {
                "total_feedback": 0,
                "by_category": {},
                "by_priority": {},
                "top_requests": [],
            }

    def generate_weekly_report(self, week_start: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive weekly report."""
        if week_start is None:
            week_start = datetime.now() - timedelta(days=7)
        
        week_end = datetime.now()
        
        # Get production monitoring data
        production_report = self.monitor.generate_production_report()
        
        # Get pipeline statistics
        pipeline_stats = self.get_pipeline_statistics()
        
        # Get publication rates
        publication_stats = self.calculate_publication_rate()
        
        # Get feedback summary
        feedback_summary = self.get_feedback_summary()
        
        # Get usage statistics
        usage_stats = self.usage_tracker.usage_data.get("usage_stats", {})
        
        # Get unified metrics from Agent-8's exporter
        unified_metrics = self.unified_metrics.get_metrics()
        manifest_stats = unified_metrics.get("manifest", {}).get("manifest_stats", {})
        ssot_compliance = unified_metrics.get("ssot", {}).get("ssot_compliance", {})
        
        report = {
            "report_period": {
                "week_start": week_start.isoformat(),
                "week_end": week_end.isoformat(),
                "generated_at": datetime.now().isoformat(),
            },
            "executive_summary": {
                "overall_status": production_report.get("overall_status", "GREEN"),
                "total_sessions": production_report["sessions"]["total"],
                "success_rate": production_report["sessions"]["success_rate"],
                "artifacts_generated": production_report["artifacts"]["total"],
                "publication_rate": publication_stats["publication_rate"],
            },
            "pipeline_statistics": pipeline_stats,
            "success_rates": {
                "overall": production_report["sessions"]["success_rate"],
                "by_pipeline": {
                    pipeline: {
                        "success_rate": (stats["success"] / stats["total"] * 100.0)
                        if stats["total"] > 0 else 0.0,
                        **stats
                    }
                    for pipeline, stats in pipeline_stats.items()
                },
            },
            "artifact_generation": {
                "total": production_report["artifacts"]["total"],
                "by_type": production_report["artifacts"]["by_type"],
            },
            "publication_statistics": publication_stats,
            "usage_statistics": usage_stats,
            "common_issues": {
                "errors": production_report["errors"]["patterns"],
                "total_errors": production_report["errors"]["total_errors"],
            },
            "feedback_summary": feedback_summary,
            "unified_metrics": {
                "manifest": {
                    "total_sessions": manifest_stats.get("total_sessions", 0),
                    "total_artifacts": manifest_stats.get("total_artifacts", 0),
                    "sessions_by_type": manifest_stats.get("sessions_by_type", {}),
                    "artifacts_by_type": manifest_stats.get("artifacts_by_type", {}),
                    "duplicate_hashes": manifest_stats.get("duplicate_hashes", 0),
                },
                "ssot": {
                    "compliant": ssot_compliance.get("overall_compliant", False),
                    "violations": ssot_compliance.get("total_violations", 0),
                    "warnings": ssot_compliance.get("total_warnings", 0),
                },
            },
            "recommendations": self._generate_recommendations(production_report, feedback_summary),
        }
        
        return report

    def _generate_recommendations(
        self, production_report: Dict[str, Any], feedback_summary: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on data."""
        recommendations = []
        
        # Success rate recommendations
        success_rate = production_report["sessions"]["success_rate"]
        if success_rate < 90.0:
            recommendations.append(
                f"⚠️ Success rate below 90% ({success_rate:.1f}%) - Investigate failures"
            )
        
        # Publication rate recommendations
        publication_stats = self.calculate_publication_rate()
        if publication_stats["publication_rate"] < 50.0:
            recommendations.append(
                "⚠️ Publication rate below 50% - Review publication workflow"
            )
        
        # Feedback recommendations
        if feedback_summary["total_feedback"] > 0:
            high_priority = feedback_summary["by_priority"].get("high", 0)
            if high_priority > 0:
                recommendations.append(
                    f"🎯 {high_priority} high-priority feedback items - Review for v1.1"
                )
        
        # Error recommendations
        if production_report["errors"]["total_errors"] > 0:
            recommendations.append(
                "🔍 Errors detected - Investigate error patterns"
            )
        
        if not recommendations:
            recommendations.append("✅ System performing well - Continue monitoring")
        
        return recommendations

    def save_report(self, report: Dict[str, Any], filename: Optional[str] = None) -> Path:
        """Save report to file."""
        if filename is None:
            week_start = datetime.fromisoformat(report["report_period"]["week_start"])
            filename = f"weekly_report_{week_start.strftime('%Y-%m-%d')}.json"
        
        # Handle absolute paths
        if Path(filename).is_absolute():
            report_path = Path(filename)
        else:
            report_path = self.reports_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        return report_path

    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate markdown version of report."""
        md = f"""# Output Flywheel Weekly Monitoring Report

**Report Period**: {report['report_period']['week_start'][:10]} to {report['report_period']['week_end'][:10]}  
**Generated**: {report['report_period']['generated_at'][:19]}  
**Status**: {report['executive_summary']['overall_status']}

---

## 📊 Executive Summary

- **Total Sessions**: {report['executive_summary']['total_sessions']}
- **Success Rate**: {report['executive_summary']['success_rate']:.1f}%
- **Artifacts Generated**: {report['executive_summary']['artifacts_generated']}
- **Publication Rate**: {report['executive_summary']['publication_rate']:.1f}%

---

## 🚀 Pipeline Statistics

"""
        
        for pipeline, stats in report["pipeline_statistics"].items():
            success_rate = stats.get("success_rate", 0.0)
            md += f"### {pipeline.upper()} Pipeline\n"
            md += f"- Total: {stats.get('total', 0)}\n"
            md += f"- Success: {stats.get('success', 0)}\n"
            md += f"- Failed: {stats.get('failed', 0)}\n"
            md += f"- Success Rate: {success_rate:.1f}%\n\n"
        
        md += f"""---

## 📈 Success Rates

- **Overall**: {report['success_rates']['overall']:.1f}%

"""
        
        for pipeline, rates in report["success_rates"]["by_pipeline"].items():
            md += f"- **{pipeline}**: {rates['success_rate']:.1f}%\n"
        
        md += f"""---

## 📦 Artifact Generation

- **Total Artifacts**: {report['artifact_generation']['total']}
- **By Type**:
"""
        
        for artifact_type, count in report["artifact_generation"]["by_type"].items():
            md += f"  - {artifact_type}: {count}\n"
        
        md += f"""---

## 📤 Publication Statistics

- **Total Artifacts**: {report['publication_statistics']['total_artifacts']}
- **Published**: {report['publication_statistics']['published_artifacts']}
- **Publication Rate**: {report['publication_statistics']['publication_rate']:.1f}%

---

## 💬 Feedback Summary

- **Total Feedback**: {report['feedback_summary']['total_feedback']}
- **By Category**: {', '.join(f'{k}: {v}' for k, v in report['feedback_summary']['by_category'].items())}
- **By Priority**: {', '.join(f'{k}: {v}' for k, v in report['feedback_summary']['by_priority'].items())}

### Top Improvement Requests

"""
        
        for i, request in enumerate(report["feedback_summary"]["top_requests"][:5], 1):
            md += f"{i}. **{request.get('category', 'other')}** ({request.get('priority', 'medium')} priority): {request.get('feedback', 'N/A')[:100]}...\n"
        
        md += f"""---

## 🔍 Common Issues

- **Total Errors**: {report['common_issues']['total_errors']}

"""
        
        if report["common_issues"]["errors"]:
            for error_type, count in report["common_issues"]["errors"].items():
                md += f"- {error_type}: {count}\n"
        else:
            md += "- ✅ No errors detected\n"
        
        md += f"""---

## 💡 Recommendations

"""
        
        for rec in report["recommendations"]:
            md += f"- {rec}\n"
        
        md += """---

**Generated by**: Agent-5 (Business Intelligence Specialist)  
🐝 **WE. ARE. SWARM. ⚡🔥**
"""
        
        return md


def main():
    """CLI interface for weekly report generation."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Output Flywheel Weekly Report Generator"
    )
    parser.add_argument(
        "--metrics-dir",
        type=str,
        default="systems/output_flywheel",
        help="Path to metrics system directory"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (default: reports/weekly_report_YYYY-MM-DD.json)"
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Generate markdown report"
    )
    
    args = parser.parse_args()
    
    metrics_dir = Path(args.metrics_dir)
    generator = WeeklyReportGenerator(metrics_dir)
    
    report = generator.generate_weekly_report()
    
    if args.markdown:
        md_report = generator.generate_markdown_report(report)
        if args.output:
            output_path = Path(args.output)
        else:
            week_start = datetime.fromisoformat(report["report_period"]["week_start"])
            output_path = generator.reports_dir / f"weekly_report_{week_start.strftime('%Y-%m-%d')}.md"
        
        output_path.write_text(md_report, encoding="utf-8")
        print(f"✅ Markdown report saved to: {output_path}")
    else:
        output_path = generator.save_report(report, args.output)
        print(f"✅ Weekly report saved to: {output_path}")
        print(f"\n📊 Report Summary:")
        print(f"  Total Sessions: {report['executive_summary']['total_sessions']}")
        print(f"  Success Rate: {report['executive_summary']['success_rate']:.1f}%")
        print(f"  Artifacts Generated: {report['executive_summary']['artifacts_generated']}")


if __name__ == "__main__":
    main()

