#!/usr/bin/env python3
"""
File Locking Monitor & Optimizer - Agent-3
============================================

Monitors file locking errors, tracks metrics, and provides optimization recommendations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
V2 Compliant: <400 lines
"""

import json
import logging
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileLockingMonitor:
    """Monitor and track file locking errors."""

    def __init__(self, metrics_file: Path = Path("data/file_locking_metrics.json")):
        """Initialize monitor."""
        self.metrics_file = metrics_file
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_metrics_file()

    def _ensure_metrics_file(self) -> None:
        """Ensure metrics file exists."""
        if not self.metrics_file.exists():
            self._save_metrics({
                "errors": [],
                "retry_success": [],
                "concurrency_events": [],
                "summary": {
                    "total_errors": 0,
                    "winerror_5_count": 0,
                    "winerror_32_count": 0,
                    "retry_success_count": 0,
                    "retry_failure_count": 0,
                    "max_retries_needed": 0,
                    "avg_retry_delay": 0.0,
                    "high_concurrency_count": 0,
                },
                "last_updated": datetime.now().isoformat(),
            })

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from file."""
        try:
            with open(self.metrics_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "errors": [],
                "retry_success": [],
                "concurrency_events": [],
                "summary": {},
            }

    def _save_metrics(self, metrics: Dict[str, Any]) -> None:
        """Save metrics to file."""
        try:
            metrics["last_updated"] = datetime.now().isoformat()
            with open(self.metrics_file, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

    def record_error(
        self,
        error_type: str,
        winerror_code: Optional[int] = None,
        attempt: int = 0,
        delay: float = 0.0,
        file_path: str = "",
    ) -> None:
        """Record a file locking error."""
        metrics = self._load_metrics()

        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "winerror_code": winerror_code,
            "attempt": attempt,
            "delay": delay,
            "file_path": file_path,
        }

        metrics["errors"].append(error_entry)

        # Update summary
        summary = metrics.get("summary", {})
        summary["total_errors"] = summary.get("total_errors", 0) + 1

        if winerror_code == 5:
            summary["winerror_5_count"] = summary.get("winerror_5_count", 0) + 1
        elif winerror_code == 32:
            summary["winerror_32_count"] = summary.get("winerror_32_count", 0) + 1

        # Keep only last 1000 errors
        if len(metrics["errors"]) > 1000:
            metrics["errors"] = metrics["errors"][-1000:]

        self._save_metrics(metrics)

    def record_retry_success(
        self,
        attempts: int,
        total_delay: float,
        winerror_code: Optional[int] = None,
    ) -> None:
        """Record successful retry."""
        metrics = self._load_metrics()

        success_entry = {
            "timestamp": datetime.now().isoformat(),
            "attempts": attempts,
            "total_delay": total_delay,
            "winerror_code": winerror_code,
        }

        metrics["retry_success"].append(success_entry)

        # Update summary
        summary = metrics.get("summary", {})
        summary["retry_success_count"] = summary.get("retry_success_count", 0) + 1
        summary["max_retries_needed"] = max(
            summary.get("max_retries_needed", 0), attempts
        )

        # Calculate average retry delay
        all_delays = [e["total_delay"] for e in metrics["retry_success"]]
        if all_delays:
            summary["avg_retry_delay"] = sum(all_delays) / len(all_delays)

        # Keep only last 1000 successes
        if len(metrics["retry_success"]) > 1000:
            metrics["retry_success"] = metrics["retry_success"][-1000:]

        self._save_metrics(metrics)

    def record_retry_failure(
        self,
        attempts: int,
        winerror_code: Optional[int] = None,
    ) -> None:
        """Record failed retry (exhausted all attempts)."""
        metrics = self._load_metrics()

        # Update summary
        summary = metrics.get("summary", {})
        summary["retry_failure_count"] = summary.get("retry_failure_count", 0) + 1

        self._save_metrics(metrics)

    def record_concurrency_event(
        self,
        concurrent_writes: int,
        time_window_seconds: float = 1.0,
    ) -> None:
        """Record high concurrency scenario."""
        metrics = self._load_metrics()

        event_entry = {
            "timestamp": datetime.now().isoformat(),
            "concurrent_writes": concurrent_writes,
            "time_window_seconds": time_window_seconds,
        }

        metrics["concurrency_events"].append(event_entry)

        # Update summary
        summary = metrics.get("summary", {})
        if concurrent_writes >= 3:  # High concurrency threshold
            summary["high_concurrency_count"] = (
                summary.get("high_concurrency_count", 0) + 1
            )

        # Keep only last 500 events
        if len(metrics["concurrency_events"]) > 500:
            metrics["concurrency_events"] = metrics["concurrency_events"][-500:]

        self._save_metrics(metrics)

    def get_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get summary statistics for last N hours."""
        metrics = self._load_metrics()
        cutoff_time = datetime.now() - timedelta(hours=hours)

        # Filter recent errors
        recent_errors = [
            e
            for e in metrics.get("errors", [])
            if datetime.fromisoformat(e["timestamp"]) > cutoff_time
        ]

        # Filter recent successes
        recent_successes = [
            s
            for s in metrics.get("retry_success", [])
            if datetime.fromisoformat(s["timestamp"]) > cutoff_time
        ]

        # Calculate statistics
        winerror_5_recent = sum(1 for e in recent_errors if e.get("winerror_code") == 5)
        winerror_32_recent = sum(1 for e in recent_errors if e.get("winerror_code") == 32)

        if recent_successes:
            avg_attempts = sum(s["attempts"] for s in recent_successes) / len(
                recent_successes
            )
            avg_delay = sum(s["total_delay"] for s in recent_successes) / len(
                recent_successes
            )
            max_attempts = max(s["attempts"] for s in recent_successes)
        else:
            avg_attempts = 0.0
            avg_delay = 0.0
            max_attempts = 0

        return {
            "period_hours": hours,
            "total_errors": len(recent_errors),
            "winerror_5_count": winerror_5_recent,
            "winerror_32_count": winerror_32_recent,
            "retry_success_count": len(recent_successes),
            "retry_failure_count": metrics.get("summary", {}).get(
                "retry_failure_count", 0
            ),
            "avg_attempts_needed": round(avg_attempts, 2),
            "max_attempts_needed": max_attempts,
            "avg_retry_delay_seconds": round(avg_delay, 3),
            "success_rate": (
                len(recent_successes)
                / (len(recent_errors) + len(recent_successes))
                if (len(recent_errors) + len(recent_successes)) > 0
                else 1.0
            ),
        }

    def generate_report(self, hours: int = 24) -> str:
        """Generate human-readable report."""
        summary = self.get_summary(hours)
        metrics = self._load_metrics()

        report = []
        report.append("=" * 70)
        report.append("📊 File Locking Monitor Report")
        report.append("=" * 70)
        report.append("")
        report.append(f"Period: Last {hours} hours")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Error Summary
        report.append("🔴 Error Summary:")
        report.append("-" * 70)
        report.append(f"Total Errors: {summary['total_errors']}")
        report.append(f"WinError 5 (Access Denied): {summary['winerror_5_count']}")
        report.append(f"WinError 32 (File in Use): {summary['winerror_32_count']}")
        report.append("")

        # Retry Performance
        report.append("🔄 Retry Performance:")
        report.append("-" * 70)
        report.append(f"Retry Successes: {summary['retry_success_count']}")
        report.append(f"Retry Failures: {summary['retry_failure_count']}")
        report.append(
            f"Success Rate: {summary['success_rate'] * 100:.1f}%"
        )
        report.append("")

        # Retry Statistics
        report.append("📈 Retry Statistics:")
        report.append("-" * 70)
        report.append(f"Average Attempts Needed: {summary['avg_attempts_needed']}")
        report.append(f"Max Attempts Needed: {summary['max_attempts_needed']}")
        report.append(
            f"Average Retry Delay: {summary['avg_retry_delay_seconds']:.3f}s"
        )
        report.append("")

        # Recommendations
        report.append("💡 Recommendations:")
        report.append("-" * 70)

        if summary["retry_failure_count"] > 0:
            report.append(
                "⚠️ CRITICAL: Retry failures detected - consider increasing max_retries"
            )

        if summary["max_attempts_needed"] >= 7:
            report.append(
                "⚠️ WARNING: Max retries approaching limit (8) - consider increasing"
            )

        if summary["avg_retry_delay_seconds"] > 1.5:
            report.append(
                "⚠️ WARNING: Average retry delay high - consider optimizing base_delay"
            )

        if summary["winerror_32_count"] > summary["winerror_5_count"] * 2:
            report.append(
                "⚠️ INFO: WinError 32 (file in use) more common - high concurrency scenario"
            )

        if summary["total_errors"] == 0:
            report.append("✅ No errors in monitoring period - system healthy")

        report.append("")

        return "\n".join(report)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="File Locking Monitor")
    parser.add_argument(
        "--report", action="store_true", help="Generate and display report"
    )
    parser.add_argument(
        "--hours", type=int, default=24, help="Hours to analyze (default: 24)"
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save report to file",
    )

    args = parser.parse_args()

    monitor = FileLockingMonitor()

    if args.report:
        report = monitor.generate_report(args.hours)
        print(report)

        if args.save_report:
            report_file = Path(
                f"agent_workspaces/Agent-3/file_locking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            report_file.parent.mkdir(parents=True, exist_ok=True)
            report_file.write_text(report)
            print(f"\n✅ Report saved: {report_file}")
    else:
        # Show current summary
        summary = monitor.get_summary(args.hours)
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())

