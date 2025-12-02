"""
Metrics Exporter - Unified Export for Manifest + SSOT Metrics
=============================================================

Exports manifest and SSOT metrics in a unified format for monitoring,
reporting, and analysis.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-02
Priority: HIGH
V2 Compliance: <300 lines, <200 lines per class, <30 lines per function
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MetricsExporter:
    """
    Unified metrics exporter for manifest and SSOT metrics.
    
    Combines data from:
    - ManifestSystem (session/artifact tracking)
    - SSOTVerifier (compliance verification)
    - MetricsTracker (Output Flywheel metrics)
    """

    def __init__(
        self,
        output_flywheel_path: Optional[Path] = None
    ):
        """
        Initialize metrics exporter.
        
        Args:
            output_flywheel_path: Path to output_flywheel system
        """
        if output_flywheel_path is None:
            output_flywheel_path = Path(__file__).parent.parent.parent / "systems" / "output_flywheel"
        
        self.output_flywheel_path = Path(output_flywheel_path)
        self._load_components()

    def _load_components(self):
        """Load manifest system, SSOT verifier, and metrics tracker."""
        try:
            from systems.output_flywheel.manifest_system import ManifestSystem
            from systems.output_flywheel.ssot_verifier import SSOTVerifier
            from systems.output_flywheel.metrics_tracker import OutputFlywheelMetricsTracker
            
            manifest_path = self.output_flywheel_path / "outputs" / "sessions" / "manifest.json"
            self.manifest_system = ManifestSystem(manifest_path)
            self.ssot_verifier = SSOTVerifier(self.output_flywheel_path)
            self.metrics_tracker = OutputFlywheelMetricsTracker(self.output_flywheel_path)
            
            logger.info("✅ Metrics exporter components loaded")
        except ImportError as e:
            logger.error(f"❌ Failed to load components: {e}")
            raise

    def export_manifest_metrics(self) -> Dict[str, Any]:
        """
        Export manifest system metrics.
        
        Returns:
            Manifest metrics dictionary
        """
        stats = self.manifest_system.get_manifest_stats()
        compliance = self.manifest_system.verify_ssot_compliance()
        
        return {
            "manifest_stats": {
                "total_sessions": stats.get("total_sessions", 0),
                "total_artifacts": stats.get("total_artifacts", 0),
                "sessions_by_type": stats.get("sessions_by_type", {}),
                "artifacts_by_type": stats.get("artifacts_by_type", {}),
                "artifacts_by_status": stats.get("artifacts_by_status", {}),
                "duplicate_hashes": stats.get("duplicate_hashes", 0),
            },
            "manifest_ssot_compliance": {
                "compliant": compliance.get("compliant", False),
                "violations": compliance.get("violations", []),
                "warnings": compliance.get("warnings", []),
                "timestamp": compliance.get("timestamp"),
            }
        }

    def export_ssot_metrics(self) -> Dict[str, Any]:
        """
        Export SSOT verification metrics.
        
        Returns:
            SSOT metrics dictionary
        """
        ssot_report = self.ssot_verifier.verify_all()
        
        return {
            "ssot_compliance": {
                "overall_compliant": ssot_report.get("compliant", False),
                "total_violations": ssot_report.get("total_violations", 0),
                "total_warnings": ssot_report.get("total_warnings", 0),
                "timestamp": ssot_report.get("timestamp"),
            },
            "work_session_ssot": {
                "compliant": ssot_report.get("work_session_ssot", {}).get("compliant", False),
                "violations": ssot_report.get("work_session_ssot", {}).get("violations", []),
                "warnings": ssot_report.get("work_session_ssot", {}).get("warnings", []),
                "total_sessions": ssot_report.get("work_session_ssot", {}).get("total_sessions", 0),
            },
            "artifact_ssot": {
                "compliant": ssot_report.get("artifact_ssot", {}).get("compliant", False),
                "violations": ssot_report.get("artifact_ssot", {}).get("violations", []),
                "warnings": ssot_report.get("artifact_ssot", {}).get("warnings", []),
                "total_artifacts": ssot_report.get("artifact_ssot", {}).get("total_artifacts", 0),
                "duplicate_names": ssot_report.get("artifact_ssot", {}).get("duplicate_names", 0),
            },
            "pipeline_ssot": {
                "compliant": ssot_report.get("pipeline_ssot", {}).get("compliant", False),
                "violations": ssot_report.get("pipeline_ssot", {}).get("violations", []),
                "warnings": ssot_report.get("pipeline_ssot", {}).get("warnings", []),
                "pipelines_checked": ssot_report.get("pipeline_ssot", {}).get("pipelines_checked", 0),
            },
            "manifest_ssot": {
                "compliant": ssot_report.get("manifest_ssot", {}).get("compliant", False),
                "violations": ssot_report.get("manifest_ssot", {}).get("violations", []),
                "warnings": ssot_report.get("manifest_ssot", {}).get("warnings", []),
                "manifest_exists": ssot_report.get("manifest_ssot", {}).get("manifest_exists", False),
            }
        }

    def export_flywheel_metrics(self) -> Dict[str, Any]:
        """
        Export Output Flywheel metrics.
        
        Returns:
            Flywheel metrics dictionary
        """
        current_metrics = self.metrics_tracker.get_current_metrics()
        
        return {
            "flywheel_metrics": {
                "artifacts_per_week": current_metrics.get("artifacts_per_week", 0),
                "repos_with_clean_readmes": current_metrics.get("repos_with_clean_readmes", 0),
                "trading_days_documented": current_metrics.get("trading_days_documented", 0),
                "publication_rate": current_metrics.get("publication_rate", 0.0),
                "timestamp": current_metrics.get("timestamp"),
            }
        }

    def export_unified_metrics(self) -> Dict[str, Any]:
        """
        Export all metrics in unified format.
        
        Returns:
            Unified metrics dictionary with manifest, SSOT, and flywheel metrics
        """
        manifest_metrics = self.export_manifest_metrics()
        ssot_metrics = self.export_ssot_metrics()
        flywheel_metrics = self.export_flywheel_metrics()
        
        return {
            "export_timestamp": datetime.now().isoformat(),
            "export_version": "1.0.0",
            "manifest": manifest_metrics,
            "ssot": ssot_metrics,
            "flywheel": flywheel_metrics,
            "summary": {
                "total_sessions": manifest_metrics["manifest_stats"]["total_sessions"],
                "total_artifacts": manifest_metrics["manifest_stats"]["total_artifacts"],
                "ssot_compliant": ssot_metrics["ssot_compliance"]["overall_compliant"],
                "ssot_violations": ssot_metrics["ssot_compliance"]["total_violations"],
                "artifacts_per_week": flywheel_metrics["flywheel_metrics"]["artifacts_per_week"],
                "publication_rate": flywheel_metrics["flywheel_metrics"]["publication_rate"],
            }
        }

    def export_to_json(
        self,
        output_path: Optional[Path] = None,
        pretty: bool = True
    ) -> Path:
        """
        Export unified metrics to JSON file.
        
        Args:
            output_path: Output file path (default: metrics_export.json)
            pretty: Pretty print JSON (default: True)
        
        Returns:
            Path to exported file
        """
        if output_path is None:
            output_path = Path("metrics_export.json")
        
        output_path = Path(output_path)
        metrics = self.export_unified_metrics()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(metrics, f, indent=2, ensure_ascii=False)
            else:
                json.dump(metrics, f, ensure_ascii=False)
        
        logger.info(f"✅ Metrics exported to: {output_path}")
        return output_path

    def export_to_dict(self) -> Dict[str, Any]:
        """
        Export unified metrics as dictionary.
        
        Returns:
            Unified metrics dictionary
        """
        return self.export_unified_metrics()


def main():
    """CLI interface for metrics exporter."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Export manifest + SSOT metrics in unified format"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="metrics_export.json",
        help="Output file path (default: metrics_export.json)"
    )
    parser.add_argument(
        "--output-flywheel-path",
        type=str,
        default=None,
        help="Path to output_flywheel system"
    )
    parser.add_argument(
        "--format",
        choices=["json", "dict"],
        default="json",
        help="Output format (default: json)"
    )
    
    args = parser.parse_args()
    
    # Initialize exporter
    output_flywheel_path = Path(args.output_flywheel_path) if args.output_flywheel_path else None
    exporter = MetricsExporter(output_flywheel_path)
    
    # Export metrics
    if args.format == "json":
        output_path = exporter.export_to_json(args.output)
        print(f"\n✅ Metrics exported to: {output_path}")
        print(f"📊 Summary:")
        metrics = exporter.export_unified_metrics()
        summary = metrics.get("summary", {})
        for key, value in summary.items():
            print(f"   {key}: {value}")
    else:
        metrics = exporter.export_to_dict()
        print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

