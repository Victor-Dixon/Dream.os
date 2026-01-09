#!/usr/bin/env python3
"""
Output Flywheel Metrics Tracker
=================================

<!-- SSOT Domain: analytics -->

Tracks metrics for the Output Flywheel system:
- artifacts_per_week
- repos_with_clean_readmes
- trading_days_documented
- publication_rate

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-01
Priority: MEDIUM
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class OutputFlywheelMetricsTracker:
    """Tracks metrics for Output Flywheel system."""

    def __init__(self, metrics_dir: Path = None):
        """Initialize metrics tracker."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        
        self.metrics_dir = metrics_dir
        self.data_dir = metrics_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_config_path = metrics_dir / "metrics_system.yaml"
        self.metrics_data_path = self.data_dir / "metrics_data.json"
        self.config: Dict[str, Any] = {}
        self.metrics_data: Dict[str, Any] = {}
        
        self.load_config()
        self.load_metrics_data()

    def load_config(self):
        """Load metrics system configuration."""
        if self.metrics_config_path.exists():
            with open(self.metrics_config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f) or {}
        else:
            self.config = {}

    def load_metrics_data(self):
        """Load existing metrics data."""
        if self.metrics_data_path.exists():
            with open(self.metrics_data_path, "r", encoding="utf-8") as f:
                self.metrics_data = json.load(f)
        else:
            self.metrics_data = {
                "artifacts": [],
                "repositories": [],
                "trading_sessions": [],
                "publications": [],
                "weekly_summaries": [],
                "last_updated": datetime.now().isoformat(),
            }
            self.save_metrics_data()

    def save_metrics_data(self):
        """Save metrics data to file."""
        self.metrics_data["last_updated"] = datetime.now().isoformat()
        with open(self.metrics_data_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics_data, f, indent=2)

    def record_artifact(
        self,
        artifact_id: str,
        artifact_type: str,
        creation_date: str = None,
        metadata: Dict[str, Any] = None,
    ):
        """Record a new artifact."""
        if creation_date is None:
            creation_date = datetime.now().isoformat()

        artifact = {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "creation_date": creation_date,
            "publication_status": "pending",
            "platforms_published": [],
            "metadata": metadata or {},
        }

        self.metrics_data["artifacts"].append(artifact)
        self.save_metrics_data()

    def record_publication(
        self,
        artifact_id: str,
        platform: str,
        status: str,
        publication_date: str = None,
        error_message: str = None,
    ):
        """Record publication attempt."""
        if publication_date is None:
            publication_date = datetime.now().isoformat()

        publication = {
            "artifact_id": artifact_id,
            "platform": platform,
            "publication_date": publication_date,
            "status": status,  # "success", "failed"
            "error_message": error_message,
        }

        self.metrics_data["publications"].append(publication)

        # Update artifact publication status
        for artifact in self.metrics_data["artifacts"]:
            if artifact["artifact_id"] == artifact_id:
                if status == "success":
                    if platform not in artifact["platforms_published"]:
                        artifact["platforms_published"].append(platform)
                    artifact["publication_status"] = "published"
                else:
                    artifact["publication_status"] = "failed"

        self.save_metrics_data()

    def record_repo_readme(
        self,
        repo_name: str,
        has_readme: bool,
        readme_quality_score: float = None,
        last_updated: str = None,
    ):
        """Record repository README status."""
        if last_updated is None:
            last_updated = datetime.now().isoformat()

        repo_data = {
            "repo_name": repo_name,
            "has_readme": has_readme,
            "readme_quality_score": readme_quality_score,
            "last_updated": last_updated,
            "tracked_date": datetime.now().isoformat(),
        }

        # Update or add repository
        existing_repo = None
        for i, repo in enumerate(self.metrics_data["repositories"]):
            if repo["repo_name"] == repo_name:
                existing_repo = i
                break

        if existing_repo is not None:
            self.metrics_data["repositories"][existing_repo] = repo_data
        else:
            self.metrics_data["repositories"].append(repo_data)

        self.save_metrics_data()

    def record_trading_day(
        self,
        session_date: str,
        journal_entry_exists: bool,
        trades_documented: int = 0,
        lessons_learned: bool = False,
    ):
        """Record trading day documentation status."""
        trading_session = {
            "session_date": session_date,
            "journal_entry_exists": journal_entry_exists,
            "trades_documented": trades_documented,
            "lessons_learned": lessons_learned,
            "tracked_date": datetime.now().isoformat(),
        }

        # Update or add trading session
        existing_session = None
        for i, session in enumerate(self.metrics_data["trading_sessions"]):
            if session["session_date"] == session_date:
                existing_session = i
                break

        if existing_session is not None:
            self.metrics_data["trading_sessions"][existing_session] = trading_session
        else:
            self.metrics_data["trading_sessions"].append(trading_session)

        self.save_metrics_data()

    def calculate_artifacts_per_week(self, week_start: str = None) -> int:
        """Calculate artifacts created in a week."""
        if week_start is None:
            # Get current week start (Monday)
            today = datetime.now()
            days_since_monday = today.weekday()
            week_start_date = today - timedelta(days=days_since_monday)
            week_start = week_start_date.isoformat()[:10]
        
        week_end_date = datetime.fromisoformat(week_start + "T00:00:00") + timedelta(days=7)
        week_end = week_end_date.isoformat()[:10]

        artifacts = self.metrics_data.get("artifacts", [])
        week_artifacts = [
            a for a in artifacts
            if week_start <= a["creation_date"][:10] < week_end
        ]

        return len(week_artifacts)

    def calculate_repos_with_clean_readmes(self) -> int:
        """Calculate number of repos with clean READMEs."""
        repos = self.metrics_data.get("repositories", [])
        
        clean_readme_count = 0
        for repo in repos:
            if repo.get("has_readme") and repo.get("readme_quality_score", 0) >= 0.7:
                clean_readme_count += 1

        return clean_readme_count

    def calculate_trading_days_documented(self, month: str = None) -> int:
        """Calculate number of trading days documented."""
        trading_sessions = self.metrics_data.get("trading_sessions", [])
        
        if month:
            documented = [
                s for s in trading_sessions
                if s["session_date"].startswith(month)
                and s.get("journal_entry_exists", False)
            ]
        else:
            documented = [
                s for s in trading_sessions
                if s.get("journal_entry_exists", False)
            ]

        return len(documented)

    def calculate_publication_rate(self, period: str = "all") -> float:
        """Calculate publication success rate."""
        artifacts = self.metrics_data.get("artifacts", [])
        publications = self.metrics_data.get("publications", [])

        if not artifacts:
            return 0.0

        # Filter by period if specified
        if period != "all":
            now = datetime.now()
            if period == "week":
                cutoff = now - timedelta(days=7)
            elif period == "month":
                cutoff = now - timedelta(days=30)
            else:
                cutoff = now

            artifacts = [
                a for a in artifacts
                if datetime.fromisoformat(a["creation_date"]) >= cutoff
            ]

        if not artifacts:
            return 0.0

        # Count published artifacts
        published_count = sum(
            1 for a in artifacts
            if a.get("publication_status") == "published"
            and a.get("platforms_published")
        )

        return (published_count / len(artifacts)) * 100.0

    def generate_weekly_summary(self) -> Dict[str, Any]:
        """Generate weekly metrics summary."""
        today = datetime.now()
        days_since_monday = today.weekday()
        week_start_date = today - timedelta(days=days_since_monday)
        week_start = week_start_date.isoformat()[:10]

        summary = {
            "week_start": week_start,
            "artifacts_per_week": self.calculate_artifacts_per_week(week_start),
            "repos_with_clean_readmes": self.calculate_repos_with_clean_readmes(),
            "trading_days_documented": self.calculate_trading_days_documented(),
            "publication_rate": self.calculate_publication_rate("week"),
            "generated_at": datetime.now().isoformat(),
        }

        # Add to weekly summaries
        if "weekly_summaries" not in self.metrics_data:
            self.metrics_data["weekly_summaries"] = []

        # Update or add weekly summary
        existing_summary = None
        for i, ws in enumerate(self.metrics_data["weekly_summaries"]):
            if ws["week_start"] == week_start:
                existing_summary = i
                break

        if existing_summary is not None:
            self.metrics_data["weekly_summaries"][existing_summary] = summary
        else:
            self.metrics_data["weekly_summaries"].append(summary)

        self.save_metrics_data()
        return summary

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        return {
            "artifacts_per_week": self.calculate_artifacts_per_week(),
            "repos_with_clean_readmes": self.calculate_repos_with_clean_readmes(),
            "trading_days_documented": self.calculate_trading_days_documented(),
            "publication_rate": self.calculate_publication_rate(),
            "timestamp": datetime.now().isoformat(),
        }


def main():
    """CLI interface for metrics tracker."""
    import argparse

    parser = argparse.ArgumentParser(description="Output Flywheel Metrics Tracker")
    parser.add_argument(
        "--metrics-dir",
        type=str,
        default="systems/output_flywheel",
        help="Path to metrics system directory"
    )
    parser.add_argument(
        "action",
        choices=["track", "summary", "current", "report"],
        help="Action to perform"
    )

    args = parser.parse_args()

    metrics_dir = Path(args.metrics_dir)
    tracker = OutputFlywheelMetricsTracker(metrics_dir)

    if args.action == "current":
        metrics = tracker.get_current_metrics()
        print("\n📊 CURRENT METRICS")
        print("=" * 60)
        for key, value in metrics.items():
            if key != "timestamp":
                print(f"{key}: {value}")
        print()

    elif args.action == "summary":
        summary = tracker.generate_weekly_summary()
        print("\n📊 WEEKLY METRICS SUMMARY")
        print("=" * 60)
        for key, value in summary.items():
            if key != "generated_at":
                print(f"{key}: {value}")
        print()

    elif args.action == "report":
        # Generate full report
        print("\n📊 OUTPUT FLYWHEEL METRICS REPORT")
        print("=" * 60)
        print(f"\nLast Updated: {tracker.metrics_data.get('last_updated')}")
        print(f"Total Artifacts: {len(tracker.metrics_data.get('artifacts', []))}")
        print(f"Total Repositories: {len(tracker.metrics_data.get('repositories', []))}")
        print(f"Total Trading Sessions: {len(tracker.metrics_data.get('trading_sessions', []))}")
        print(f"Total Publications: {len(tracker.metrics_data.get('publications', []))}")
        print()
        
        current = tracker.get_current_metrics()
        print("CURRENT METRICS:")
        for key, value in current.items():
            if key != "timestamp":
                print(f"  {key}: {value}")
        print()


if __name__ == "__main__":
    main()


