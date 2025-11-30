#!/usr/bin/env python3
"""
Stress Test Metrics Analysis Tool
==================================

Command-line tool to analyze stress test metrics and generate insights:
- Load dashboard JSON files
- Analyze latency patterns
- Identify bottlenecks
- Generate optimization recommendations
- Create visualization data
- Generate comprehensive reports

Usage:
    python -m tools.analyze_stress_test_metrics [dashboard_file] [options]

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-11-29
License: MIT
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.core.stress_test_analysis_report import StressTestAnalysisReport
from src.core.stress_test_metrics_analyzer import StressTestMetricsAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_latest_dashboard(output_dir: Path) -> Optional[Path]:
    """Find the latest stress test dashboard JSON file."""
    dashboard_files = list(output_dir.glob("stress_test_results_*.json"))
    if not dashboard_files:
        return None
    
    # Sort by modification time, get latest
    return max(dashboard_files, key=lambda p: p.stat().st_mtime)


def main():
    """Main analysis function."""
    parser = argparse.ArgumentParser(
        description="Analyze stress test metrics and generate insights"
    )
    parser.add_argument(
        "dashboard_file",
        nargs="?",
        type=Path,
        help="Path to stress test dashboard JSON file"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("stress_test_analysis_results"),
        help="Directory to save analysis results (default: stress_test_analysis_results)"
    )
    parser.add_argument(
        "--find-latest",
        action="store_true",
        help="Automatically find latest dashboard file"
    )
    parser.add_argument(
        "--visualization-only",
        action="store_true",
        help="Generate only visualization data"
    )

    args = parser.parse_args()

    # Find dashboard file
    dashboard_file = args.dashboard_file
    if args.find_latest or dashboard_file is None:
        output_dir = Path("stress_test_results")
        dashboard_file = find_latest_dashboard(output_dir)
        if dashboard_file is None:
            logger.error(f"No dashboard files found in {output_dir}")
            logger.info("Run a stress test first to generate metrics")
            return 1
        logger.info(f"Using latest dashboard: {dashboard_file}")

    if not dashboard_file.exists():
        logger.error(f"Dashboard file not found: {dashboard_file}")
        return 1

    # Load dashboard data
    logger.info(f"Loading dashboard from {dashboard_file}")
    try:
        with open(dashboard_file, "r") as f:
            dashboard_data = json.load(f)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return 1

    # Generate analysis report
    logger.info("Generating analysis report...")
    try:
        report_generator = StressTestAnalysisReport(dashboard_data)
        
        if args.visualization_only:
            analyzer = StressTestMetricsAnalyzer(dashboard_data)
            visualization_data = analyzer.generate_dashboard_visualization_data()
            
            output_file = args.output_dir / "visualization_data.json"
            args.output_dir.mkdir(exist_ok=True)
            with open(output_file, "w") as f:
                json.dump(visualization_data, f, indent=2)
            
            logger.info(f"Visualization data saved to {output_file}")
        else:
            report = report_generator.generate_full_report(args.output_dir)
            
            logger.info("✅ Analysis report generated successfully!")
            logger.info(f"   Report directory: {args.output_dir}")
            
            # Print summary
            summary = report.get("executive_summary", {})
            perf = summary.get("test_performance", {})
            logger.info(f"\n📊 SUMMARY:")
            logger.info(f"   Status: {perf.get('overall_status', 'N/A').upper()}")
            logger.info(f"   P99 Latency: {perf.get('p99_latency_ms', 0):.2f} ms")
            logger.info(f"   Throughput: {perf.get('throughput_msg_per_sec', 0):.2f} msg/sec")
            logger.info(f"   Critical Issues: {summary.get('critical_issues', 0)}")
            
            return 0
    except Exception as e:
        logger.error(f"Error generating report: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())

