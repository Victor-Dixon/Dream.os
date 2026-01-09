#!/usr/bin/env python3
"""
Unified Metrics Reader - Integration with Agent-8's Metrics Exporter
=====================================================================

<!-- SSOT Domain: analytics -->

Reads unified metrics from Agent-8's metrics exporter for monitoring and reporting.

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
from pathlib import Path
from typing import Any, Dict, Optional

# Handle imports
try:
    from src.services.metrics_exporter import MetricsExporter
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from src.services.metrics_exporter import MetricsExporter


class UnifiedMetricsReader:
    """Reads unified metrics from metrics exporter."""

    def __init__(self, metrics_export_path: Optional[Path] = None):
        """
        Initialize unified metrics reader.
        
        Args:
            metrics_export_path: Path to metrics_export.json (default: project root)
        """
        if metrics_export_path is None:
            metrics_export_path = Path("metrics_export.json")
        
        self.metrics_export_path = Path(metrics_export_path)
        self.exporter = MetricsExporter()

    def read_metrics_from_file(self) -> Optional[Dict[str, Any]]:
        """
        Read unified metrics from JSON file.
        
        Returns:
            Unified metrics dictionary or None if file doesn't exist
        """
        if not self.metrics_export_path.exists():
            return None
        
        try:
            with open(self.metrics_export_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def get_metrics(self, force_export: bool = False) -> Dict[str, Any]:
        """
        Get unified metrics (from file or fresh export).
        
        Args:
            force_export: Force fresh export instead of reading file
        
        Returns:
            Unified metrics dictionary
        """
        if force_export:
            return self.exporter.export_to_dict()
        
        # Try reading from file first
        metrics = self.read_metrics_from_file()
        if metrics is None:
            # File doesn't exist, export fresh
            return self.exporter.export_to_dict()
        
        return metrics

    def get_manifest_stats(self) -> Dict[str, Any]:
        """Get manifest statistics."""
        metrics = self.get_metrics()
        return metrics.get("manifest", {}).get("manifest_stats", {})

    def get_ssot_compliance(self) -> Dict[str, Any]:
        """Get SSOT compliance status."""
        metrics = self.get_metrics()
        return metrics.get("ssot", {}).get("ssot_compliance", {})

    def get_flywheel_metrics(self) -> Dict[str, Any]:
        """Get Output Flywheel metrics."""
        metrics = self.get_metrics()
        return metrics.get("flywheel", {}).get("flywheel_metrics", {})

    def get_summary(self) -> Dict[str, Any]:
        """Get unified metrics summary."""
        metrics = self.get_metrics()
        return metrics.get("summary", {})

    def export_fresh_metrics(self, output_path: Optional[Path] = None) -> Path:
        """
        Export fresh unified metrics.
        
        Args:
            output_path: Output file path (default: metrics_export.json)
        
        Returns:
            Path to exported file
        """
        if output_path is None:
            output_path = self.metrics_export_path
        
        return self.exporter.export_to_json(output_path)


