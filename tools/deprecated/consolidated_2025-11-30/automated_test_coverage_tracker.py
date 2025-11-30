#!/usr/bin/env python3
"""
Automated Test Coverage Tracker
=================================

Tracks test coverage progress, identifies gaps, and generates reports.
Automates the test coverage expansion process.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-01-27
Priority: HIGH
V2 Compliance: <400 lines
"""

import json
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestCoverageTracker:
    """Automated test coverage tracking and reporting."""

    def __init__(self, project_root: Optional[Path] = None):
        """Initialize tracker."""
        self.project_root = project_root or Path(__file__).parent.parent
        self.reports_dir = self.project_root / "agent_workspaces" / "Agent-3" / "coverage_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def get_test_files(self) -> List[Path]:
        """Get all test files."""
        tests_dir = self.project_root / "tests"
        test_files = []
        
        if tests_dir.exists():
            test_files = list(tests_dir.rglob("test_*.py"))
        
        return test_files

    def count_tests_in_file(self, test_file: Path) -> int:
        """Count test methods in a test file."""
        try:
            content = test_file.read_text(encoding='utf-8')
            # Count test methods (def test_*)
            test_count = content.count("def test_")
            return test_count
        except Exception as e:
            logger.warning(f"Error reading {test_file}: {e}")
            return 0

    def analyze_test_coverage(self) -> Dict:
        """Analyze current test coverage status."""
        logger.info("Analyzing test coverage...")
        
        test_files = self.get_test_files()
        total_tests = 0
        file_details = []
        
        for test_file in test_files:
            test_count = self.count_tests_in_file(test_file)
            total_tests += test_count
            file_details.append({
                "file": str(test_file.relative_to(self.project_root)),
                "test_count": test_count,
                "exists": True
            })
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_test_files": len(test_files),
            "total_tests": total_tests,
            "test_files": file_details,
            "target_coverage": 85.0
        }
        
        return analysis

    def check_specific_files(self, target_files: List[str]) -> Dict:
        """Check coverage for specific target files."""
        logger.info(f"Checking {len(target_files)} target files...")
        
        results = {}
        for target_file in target_files:
            # Find corresponding test file
            test_file_name = f"test_{Path(target_file).name}"
            test_file = None
            
            # Search for test file
            tests_dir = self.project_root / "tests"
            if tests_dir.exists():
                for test_path in tests_dir.rglob(test_file_name):
                    test_file = test_path
                    break
            
            if test_file and test_file.exists():
                test_count = self.count_tests_in_file(test_file)
                results[target_file] = {
                    "test_file": str(test_file.relative_to(self.project_root)),
                    "test_count": test_count,
                    "status": "has_tests"
                }
            else:
                results[target_file] = {
                    "test_file": None,
                    "test_count": 0,
                    "status": "no_tests"
                }
        
        return results

    def generate_coverage_report(self) -> Dict:
        """Generate comprehensive coverage report."""
        logger.info("Generating coverage report...")
        
        analysis = self.analyze_test_coverage()
        
        # Check specific infrastructure files from assignment
        infrastructure_files = [
            "src/core/managers/core_monitoring_manager.py",
            "src/core/managers/core_results_manager.py",
            "src/core/message_queue_statistics.py",
            "src/core/message_queue_helpers.py",
            "src/core/message_queue_async_processor.py"
        ]
        
        specific_checks = self.check_specific_files(infrastructure_files)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_analysis": analysis,
            "infrastructure_files": specific_checks,
            "summary": {
                "total_test_files": analysis["total_test_files"],
                "total_tests": analysis["total_tests"],
                "infrastructure_files_checked": len(infrastructure_files),
                "infrastructure_files_with_tests": sum(
                    1 for r in specific_checks.values() if r["status"] == "has_tests"
                )
            }
        }
        
        # Save report
        report_file = self.reports_dir / f"coverage_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report saved to: {report_file}")
        return report

    def print_summary(self, report: Dict):
        """Print human-readable summary."""
        print("\n" + "=" * 70)
        print("📊 AUTOMATED TEST COVERAGE TRACKER - SUMMARY")
        print("=" * 70)
        print(f"Timestamp: {report['timestamp']}")
        print()
        
        summary = report["summary"]
        print(f"Total Test Files: {summary['total_test_files']}")
        print(f"Total Tests: {summary['total_tests']}")
        print()
        
        print("Infrastructure Files Status:")
        infra = report["infrastructure_files"]
        for file_path, file_data in infra.items():
            status_icon = "✅" if file_data["status"] == "has_tests" else "❌"
            test_count = file_data["test_count"]
            print(f"  {status_icon} {Path(file_path).name}: {test_count} tests")
            if file_data["test_file"]:
                print(f"      Test file: {file_data['test_file']}")
        print()
        
        print("=" * 70)
        print(f"📊 Full report: {self.reports_dir}")
        print("=" * 70 + "\n")


def main():
    """Main entry point."""
    tracker = TestCoverageTracker()
    report = tracker.generate_coverage_report()
    tracker.print_summary(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())

