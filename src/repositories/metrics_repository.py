"""
Metrics Repository - SSOT for Metrics Data
==========================================

<!-- SSOT Domain: integration -->

Persistent storage for metrics data from MetricsEngine.
Provides SSOT for all metrics history and analytics.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-27
JET FUEL: Autonomous creation
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    from src.core.analytics.engines.metrics_engine import MetricsEngine
    METRICS_AVAILABLE = True
except ImportError:
    METRICS_AVAILABLE = False
    MetricsEngine = None


class MetricsRepository:
    """
    Repository for metrics data persistence.
    
    Provides SSOT for metrics history and analytics.
    """

    def __init__(
        self,
        metrics_history_file: str = "data/metrics_history.json",
    ):
        """
        Initialize metrics repository.

        Args:
            metrics_history_file: Path to metrics history storage
        """
        self.metrics_history_file = Path(metrics_history_file)
        self._ensure_history_file()

    def _ensure_history_file(self) -> None:
        """Ensure metrics history file exists."""
        if not self.metrics_history_file.exists():
            self.metrics_history_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_history({
                "metrics_snapshots": [],
                "metadata": {"version": "1.0", "created_at": datetime.now().isoformat()},
            })

    def _load_history(self) -> dict[str, Any]:
        """Load metrics history from file."""
        try:
            with open(self.metrics_history_file, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"metrics_snapshots": [], "metadata": {"version": "1.0"}}

    def _save_history(self, data: dict[str, Any]) -> bool:
        """Save metrics history to file."""
        try:
            with open(self.metrics_history_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except OSError:
            return False

    def save_metrics_snapshot(self, metrics: dict[str, Any], source: str = "system") -> bool:
        """
        Save metrics snapshot to history.

        Args:
            metrics: Metrics dictionary from MetricsEngine
            source: Source of metrics (e.g., "message_system", "queue")

        Returns:
            True if save successful, False otherwise
        """
        data = self._load_history()
        snapshots = data.get("metrics_snapshots", [])

        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "metrics": metrics,
            "metric_count": len(metrics),
        }

        snapshots.append(snapshot)
        data["metrics_snapshots"] = snapshots
        return self._save_history(data)

    def get_metrics_history(
        self, source: Optional[str] = None, limit: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """
        Get metrics history, optionally filtered by source.

        Args:
            source: Optional source to filter by
            limit: Optional maximum number of snapshots to return

        Returns:
            List of metrics snapshot dictionaries
        """
        data = self._load_history()
        snapshots = data.get("metrics_snapshots", [])

        if source:
            snapshots = [s for s in snapshots if s.get("source") == source]

        snapshots.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

        if limit:
            snapshots = snapshots[:limit]

        return snapshots

    def get_latest_metrics(self, source: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Get latest metrics snapshot."""
        history = self.get_metrics_history(source=source, limit=1)
        return history[0] if history else None

    def get_metrics_trend(
        self, metric_name: str, source: Optional[str] = None, limit: int = 100
    ) -> list[float]:
        """
        Get trend data for specific metric.

        Args:
            metric_name: Name of metric to track
            source: Optional source filter
            limit: Maximum snapshots to analyze

        Returns:
            List of metric values over time
        """
        history = self.get_metrics_history(source=source, limit=limit)
        trend = []
        for snapshot in history:
            metrics = snapshot.get("metrics", {})
            if metric_name in metrics:
                value = metrics[metric_name]
                if isinstance(value, (int, float)):
                    trend.append(value)
        return trend


