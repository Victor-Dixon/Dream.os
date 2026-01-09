#!/usr/bin/env python3
"""
Canonical Metrics Client - Unified Metrics Interface
======================================================

<!-- SSOT Domain: analytics -->

Consolidates unified metrics reading (Agent-8 exporter) and Output Flywheel
metrics tracking into a single canonical client.

Replaces:
- unified_metrics_reader.py
- metrics_tracker.py

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliant: Yes (<300 lines)
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Handle imports - MetricsExporter is optional (Agent-8 unified metrics)
MetricsExporter = None
try:
    from src.services.metrics_exporter import MetricsExporter
except ImportError:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from src.services.metrics_exporter import MetricsExporter
    except ImportError:
        # MetricsExporter not available - unified metrics will be None
        MetricsExporter = None


class MetricsClient:
    """Canonical metrics client for unified and flywheel metrics."""

    def __init__(self, metrics_dir: Path = None, metrics_export_path: Optional[Path] = None):
        """Initialize metrics client."""
        if metrics_dir is None:
            metrics_dir = Path(__file__).parent
        
        self.metrics_dir = metrics_dir
        self.data_dir = metrics_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Unified metrics (Agent-8 exporter) - optional
        if metrics_export_path is None:
            metrics_export_path = Path("metrics_export.json")
        self.metrics_export_path = Path(metrics_export_path)
        self.exporter = MetricsExporter() if MetricsExporter else None
        
        # Flywheel metrics tracking
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
        """Load existing flywheel metrics data."""
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
        """Save flywheel metrics data."""
        self.metrics_data["last_updated"] = datetime.now().isoformat()
        with open(self.metrics_data_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics_data, f, indent=2)

    # Unified Metrics (Agent-8 exporter)
    def read_unified_metrics(self) -> Optional[Dict[str, Any]]:
        """Read unified metrics from JSON file."""
        if not self.metrics_export_path.exists():
            return None
        try:
            with open(self.metrics_export_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def get_unified_metrics(self, force_export: bool = False) -> Optional[Dict[str, Any]]:
        """Get unified metrics (from file or fresh export)."""
        if self.exporter is None:
            return self.read_unified_metrics()
        if force_export:
            return self.exporter.export_to_dict()
        metrics = self.read_unified_metrics()
        return metrics if metrics else self.exporter.export_to_dict()

    def get_manifest_stats(self) -> Dict[str, Any]:
        """Get manifest statistics."""
        return self.get_unified_metrics().get("manifest", {}).get("manifest_stats", {})

    def get_ssot_compliance(self) -> Dict[str, Any]:
        """Get SSOT compliance status."""
        return self.get_unified_metrics().get("ssot", {}).get("ssot_compliance", {})

    def get_flywheel_metrics_unified(self) -> Dict[str, Any]:
        """Get Output Flywheel metrics from unified metrics."""
        return self.get_unified_metrics().get("flywheel", {}).get("flywheel_metrics", {})

    # Flywheel Metrics Tracking
    def record_artifact(self, artifact_id: str, artifact_type: str, creation_date: str = None, metadata: Dict[str, Any] = None):
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

    def record_publication(self, artifact_id: str, platform: str, status: str, publication_date: str = None, error_message: str = None):
        """Record publication attempt."""
        if publication_date is None:
            publication_date = datetime.now().isoformat()
        publication = {
            "artifact_id": artifact_id,
            "platform": platform,
            "publication_date": publication_date,
            "status": status,
            "error_message": error_message,
        }
        self.metrics_data["publications"].append(publication)
        for artifact in self.metrics_data["artifacts"]:
            if artifact["artifact_id"] == artifact_id:
                if status == "success":
                    if platform not in artifact["platforms_published"]:
                        artifact["platforms_published"].append(platform)
                    artifact["publication_status"] = "published"
                else:
                    artifact["publication_status"] = "failed"
        self.save_metrics_data()

    def calculate_artifacts_per_week(self, week_start: str = None) -> int:
        """Calculate artifacts created in a week."""
        if week_start is None:
            today = datetime.now()
            days_since_monday = today.weekday()
            week_start_date = today - timedelta(days=days_since_monday)
            week_start = week_start_date.isoformat()[:10]
        week_end_date = datetime.fromisoformat(week_start + "T00:00:00") + timedelta(days=7)
        week_end = week_end_date.isoformat()[:10]
        artifacts = self.metrics_data.get("artifacts", [])
        return len([a for a in artifacts if week_start <= a["creation_date"][:10] < week_end])

    def calculate_repos_with_clean_readmes(self) -> int:
        """Calculate number of repos with clean READMEs."""
        repos = self.metrics_data.get("repositories", [])
        return sum(1 for repo in repos if repo.get("has_readme") and repo.get("readme_quality_score", 0) >= 0.7)

    def calculate_trading_days_documented(self, month: str = None) -> int:
        """Calculate number of trading days documented."""
        trading_sessions = self.metrics_data.get("trading_sessions", [])
        if month:
            documented = [s for s in trading_sessions if s["session_date"].startswith(month) and s.get("journal_entry_exists", False)]
        else:
            documented = [s for s in trading_sessions if s.get("journal_entry_exists", False)]
        return len(documented)

    def calculate_publication_rate(self, period: str = "all") -> float:
        """Calculate publication success rate."""
        artifacts = self.metrics_data.get("artifacts", [])
        if not artifacts:
            return 0.0
        if period != "all":
            now = datetime.now()
            cutoff = now - timedelta(days=7 if period == "week" else 30 if period == "month" else 0)
            artifacts = [a for a in artifacts if datetime.fromisoformat(a["creation_date"]) >= cutoff]
        if not artifacts:
            return 0.0
        published_count = sum(1 for a in artifacts if a.get("publication_status") == "published" and a.get("platforms_published"))
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
        if "weekly_summaries" not in self.metrics_data:
            self.metrics_data["weekly_summaries"] = []
        existing = next((i for i, ws in enumerate(self.metrics_data["weekly_summaries"]) if ws["week_start"] == week_start), None)
        if existing is not None:
            self.metrics_data["weekly_summaries"][existing] = summary
        else:
            self.metrics_data["weekly_summaries"].append(summary)
        self.save_metrics_data()
        return summary

    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current flywheel metrics snapshot."""
        return {
            "artifacts_per_week": self.calculate_artifacts_per_week(),
            "repos_with_clean_readmes": self.calculate_repos_with_clean_readmes(),
            "trading_days_documented": self.calculate_trading_days_documented(),
            "publication_rate": self.calculate_publication_rate(),
            "timestamp": datetime.now().isoformat(),
        }

    def get_metrics_summary(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> Dict[str, Any]:
        """
        Provide a consolidated metrics summary.

        - Uses weekly summary as the primary rollup.
        - Includes current snapshot and unified metrics (if available).
        """
        weekly = self.generate_weekly_summary()
        current = self.get_current_metrics()
        unified = self.get_unified_metrics() or {}
        return {
            "weekly_summary": weekly,
            "current_snapshot": current,
            "unified_metrics": unified,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "generated_at": datetime.now().isoformat(),
        }

    def export_fresh_unified_metrics(self, output_path: Optional[Path] = None) -> Optional[Path]:
        """Export fresh unified metrics."""
        if self.exporter is None:
            return None
        if output_path is None:
            output_path = self.metrics_export_path
        return self.exporter.export_to_json(output_path)


def main():
    """CLI interface for metrics client."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Canonical Metrics Client")
    parser.add_argument("--metrics-dir", type=str, default="systems/output_flywheel", help="Metrics directory")
    parser.add_argument("action", choices=["unified", "flywheel", "current", "summary"], help="Action to perform")
    
    args = parser.parse_args()
    metrics_dir = Path(args.metrics_dir)
    client = MetricsClient(metrics_dir)
    
    if args.action == "unified":
        metrics = client.get_unified_metrics()
        print("\n📊 UNIFIED METRICS")
        print("=" * 60)
        print(json.dumps(metrics.get("summary", {}), indent=2))
    elif args.action == "flywheel":
        metrics = client.get_current_metrics()
        print("\n📊 FLYWHEEL METRICS")
        print("=" * 60)
        for key, value in metrics.items():
            if key != "timestamp":
                print(f"{key}: {value}")
    elif args.action == "current":
        metrics = client.get_current_metrics()
        print("\n📊 CURRENT METRICS")
        print("=" * 60)
        for key, value in metrics.items():
            if key != "timestamp":
                print(f"{key}: {value}")
    elif args.action == "summary":
        summary = client.generate_weekly_summary()
        print("\n📊 WEEKLY SUMMARY")
        print("=" * 60)
        for key, value in summary.items():
            if key != "generated_at":
                print(f"{key}: {value}")


if __name__ == "__main__":
    main()


