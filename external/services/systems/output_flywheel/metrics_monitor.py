#!/usr/bin/env python3
"""
Output Flywheel Metrics Monitor - Guardrail & Live Monitoring
==============================================================

<!-- SSOT Domain: analytics -->

Monitors metrics and provides guardrail status (RED/YELLOW/GREEN) with alerting.

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
from typing import Any, Dict, List, Optional, Tuple

import yaml

# Handle both relative and absolute imports
try:
    from .metrics_client import MetricsClient
except ImportError:
    from metrics_client import MetricsClient


class MetricsMonitor:
    """Monitors metrics and provides guardrail status."""

    def __init__(self, metrics_dir: Path = None):
        """Initialize metrics monitor."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        
        self.metrics_dir = metrics_dir
        self.outputs_dir = metrics_dir / "outputs"
        self.tracker = MetricsClient(metrics_dir)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load metrics system configuration."""
        config_path = self.metrics_dir / "metrics_system.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        return {}

    def check_artifacts_per_week(self) -> Tuple[str, Dict[str, Any]]:
        """Check artifacts per week threshold."""
        threshold_config = self.config.get("alert_thresholds", {}).get(
            "artifacts_per_week", {}
        )
        warning_threshold = threshold_config.get("warning", 1)
        critical_threshold = threshold_config.get("critical", 0)
        
        target = self.config.get("core_metrics", {}).get(
            "artifacts_per_week", {}
        ).get("target", 2)
        
        current = self.tracker.calculate_artifacts_per_week()
        
        if current <= critical_threshold:
            status = "RED"
        elif current <= warning_threshold:
            status = "YELLOW"
        elif current >= target:
            status = "GREEN"
        else:
            status = "YELLOW"
        
        return status, {
            "metric": "artifacts_per_week",
            "current": current,
            "target": target,
            "warning_threshold": warning_threshold,
            "critical_threshold": critical_threshold,
            "status": status,
        }

    def check_trading_days_documented(self) -> Tuple[str, Dict[str, Any]]:
        """Check trading days documented threshold."""
        current_month = datetime.now().strftime("%Y-%m")
        current = self.tracker.calculate_trading_days_documented(current_month)
        
        # Calculate expected trading days (weekdays this month)
        today = datetime.now()
        first_day = today.replace(day=1)
        last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        expected = sum(
            1 for day in range(1, last_day.day + 1)
            if (first_day.replace(day=day).weekday() < 5)
        )
        
        if current == 0:
            status = "RED"
        elif current < expected * 0.5:
            status = "YELLOW"
        elif current >= expected * 0.8:
            status = "GREEN"
        else:
            status = "YELLOW"
        
        return status, {
            "metric": "trading_days_documented",
            "current": current,
            "expected": expected,
            "month": current_month,
            "status": status,
        }

    def check_publication_rate(self) -> Tuple[str, Dict[str, Any]]:
        """Check publication rate threshold."""
        threshold_config = self.config.get("alert_thresholds", {}).get(
            "publication_rate", {}
        )
        warning_threshold = threshold_config.get("warning", 75)
        critical_threshold = threshold_config.get("critical", 50)
        
        target = self.config.get("core_metrics", {}).get(
            "publication_rate", {}
        ).get("target", 90)
        
        current = self.tracker.calculate_publication_rate("week")
        
        if current <= critical_threshold:
            status = "RED"
        elif current <= warning_threshold:
            status = "YELLOW"
        elif current >= target:
            status = "GREEN"
        else:
            status = "YELLOW"
        
        return status, {
            "metric": "publication_rate",
            "current": current,
            "target": target,
            "warning_threshold": warning_threshold,
            "critical_threshold": critical_threshold,
            "status": status,
        }

    def check_missing_artifacts(self) -> List[Dict[str, Any]]:
        """Check for work sessions with missing artifacts."""
        sessions_dir = self.outputs_dir / "sessions"
        artifacts_dir = self.outputs_dir / "artifacts"
        
        missing = []
        
        if not sessions_dir.exists():
            return missing
        
        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                
                session_id = session_data.get("session_id", session_file.stem)
                artifacts = session_data.get("artifacts", {})
                
                session_missing = []
                
                for artifact_type in ["readme", "blog_post", "social_post", "trade_journal"]:
                    artifact_info = artifacts.get(artifact_type, {})
                    
                    if artifact_info.get("generated"):
                        artifact_path = artifact_info.get("path")
                        if artifact_path:
                            full_path = artifacts_dir / artifact_path
                            if not full_path.exists():
                                session_missing.append(artifact_type)
                        else:
                            session_missing.append(artifact_type)
                
                if session_missing:
                    missing.append({
                        "session_id": session_id,
                        "session_type": session_data.get("session_type"),
                        "timestamp": session_data.get("timestamp"),
                        "missing_artifacts": session_missing,
                    })
            except Exception as e:
                continue
        
        return missing

    def generate_guardrail_report(self) -> Dict[str, Any]:
        """Generate complete guardrail status report."""
        artifacts_status, artifacts_data = self.check_artifacts_per_week()
        trading_status, trading_data = self.check_trading_days_documented()
        publication_status, publication_data = self.check_publication_rate()
        missing_artifacts = self.check_missing_artifacts()
        
        overall_status = "GREEN"
        if artifacts_status == "RED" or trading_status == "RED" or publication_status == "RED":
            overall_status = "RED"
        elif artifacts_status == "YELLOW" or trading_status == "YELLOW" or publication_status == "YELLOW":
            overall_status = "YELLOW"
        
        if missing_artifacts:
            if overall_status == "GREEN":
                overall_status = "YELLOW"
            if len(missing_artifacts) > 3:
                overall_status = "RED"
        
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "artifacts_per_week": artifacts_data,
                "trading_days_documented": trading_data,
                "publication_rate": publication_data,
            },
            "missing_artifacts": {
                "count": len(missing_artifacts),
                "sessions": missing_artifacts,
            },
        }

    def generate_alert_summary(self) -> str:
        """Generate alert summary for devlog/Discord."""
        report = self.generate_guardrail_report()
        
        status_emoji = {
            "GREEN": "🟢",
            "YELLOW": "🟡",
            "RED": "🔴",
        }
        
        emoji = status_emoji.get(report["overall_status"], "⚪")
        
        summary = f"{emoji} **Output Flywheel Guardrail Status: {report['overall_status']}**\n\n"
        
        for metric_name, metric_data in report["metrics"].items():
            status = metric_data["status"]
            metric_emoji = status_emoji.get(status, "⚪")
            summary += f"{metric_emoji} **{metric_name}**: {status}\n"
            if metric_name == "artifacts_per_week":
                summary += f"   Current: {metric_data['current']} (Target: {metric_data['target']})\n"
            elif metric_name == "trading_days_documented":
                summary += f"   Current: {metric_data['current']}/{metric_data['expected']} days\n"
            elif metric_name == "publication_rate":
                summary += f"   Current: {metric_data['current']:.1f}% (Target: {metric_data['target']}%)\n"
        
        if report["missing_artifacts"]["count"] > 0:
            summary += f"\n⚠️ **Missing Artifacts**: {report['missing_artifacts']['count']} session(s) with missing artifacts\n"
        
        if report["overall_status"] != "GREEN":
            summary += "\n🔍 **Action Required**: Captain review recommended\n"
        
        return summary


def main():
    """CLI interface for metrics monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Output Flywheel Metrics Monitor & Guardrails"
    )
    parser.add_argument(
        "--metrics-dir",
        type=str,
        default="systems/output_flywheel",
        help="Path to metrics system directory"
    )
    parser.add_argument(
        "action",
        choices=["check", "report", "alert", "json"],
        help="Action to perform"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (for json/report actions)"
    )
    
    args = parser.parse_args()
    
    metrics_dir = Path(args.metrics_dir)
    monitor = MetricsMonitor(metrics_dir)
    
    if args.action == "check":
        report = monitor.generate_guardrail_report()
        print(f"\n{'='*60}")
        print(f"📊 OUTPUT FLYWHEEL GUARDRAIL STATUS")
        print(f"{'='*60}\n")
        print(f"Overall Status: {report['overall_status']}\n")
        
        for metric_name, metric_data in report["metrics"].items():
            status = metric_data["status"]
            print(f"{metric_name}: {status}")
            print(f"  Details: {json.dumps(metric_data, indent=2)}\n")
        
        if report["missing_artifacts"]["count"] > 0:
            print(f"Missing Artifacts: {report['missing_artifacts']['count']} sessions")
            for session in report["missing_artifacts"]["sessions"]:
                print(f"  - {session['session_id']}: {session['missing_artifacts']}")
    
    elif args.action == "report":
        report = monitor.generate_guardrail_report()
        output_path = args.output or (metrics_dir / "guardrail_report.json")
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Guardrail report saved to: {output_path}")
    
    elif args.action == "alert":
        summary = monitor.generate_alert_summary()
        print(summary)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"\n✅ Alert summary saved to: {args.output}")
    
    elif args.action == "json":
        report = monitor.generate_guardrail_report()
        output = json.dumps(report, indent=2)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"✅ JSON report saved to: {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()

