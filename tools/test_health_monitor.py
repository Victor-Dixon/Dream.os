#!/usr/bin/env python3
"""
Test Health Monitor CLI Tool

A comprehensive test suite health monitoring and analysis tool that:
- Monitors test collection and execution health
- Identifies flaky tests through multiple runs
- Analyzes test coverage patterns
- Suggests improvements and automated fixes
- Provides CI/CD readiness assessment

Usage:
    python tools/test_health_monitor.py --analyze
    python tools/test_health_monitor.py --flaky-detect --runs 5
    python tools/test_health_monitor.py --coverage-report

<!-- SSOT Domain: infrastructure -->
"""
    python tools/test_health_monitor.py --suggest-fixes
"""

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict, Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import logging

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """Represents a single test execution result."""
    test_path: str
    test_name: str
    status: str  # passed, failed, error, skipped
    duration: float
    error_message: Optional[str] = None


@dataclass
class FlakyTestReport:
    """Report for potentially flaky tests."""
    test_path: str
    test_name: str
    pass_rate: float
    total_runs: int
    failure_patterns: List[str]
    recommendation: str


@dataclass
class TestHealthReport:
    """Comprehensive test health assessment."""
    total_tests: int
    passed_tests: int
    failed_tests: int
    skipped_tests: int
    error_tests: int
    collection_errors: int
    average_duration: float
    slowest_tests: List[Tuple[str, float]]
    flaky_tests: List[FlakyTestReport]
    coverage_gaps: List[str]
    suggestions: List[str]
    health_score: int  # 0-100


class TestHealthMonitor:
    """Main test health monitoring class."""

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.test_results: List[TestResult] = []

    def run_pytest_collection(self) -> Tuple[int, str]:
        """Run pytest collection only to check for errors."""
        try:
            cmd = [
                sys.executable, "-m", "pytest",
                "--collect-only",
                "--quiet",
                "--tb=no",
                str(self.project_root)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300
            )

            return result.returncode, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return 1, "Collection timed out after 5 minutes"
        except Exception as e:
            return 1, f"Collection failed: {e}"

    def run_pytest_with_coverage(self) -> Tuple[int, str]:
        """Run pytest with coverage analysis."""
        try:
            cmd = [
                sys.executable, "-m", "pytest",
                "--cov=src",
                "--cov-report=json",
                "--cov-report=term-missing",
                "--tb=short",
                str(self.project_root)
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=600  # 10 minutes
            )

            return result.returncode, result.stdout + result.stderr

        except subprocess.TimeoutExpired:
            return 1, "Test execution timed out after 10 minutes"
        except Exception as e:
            return 1, f"Test execution failed: {e}"

    def parse_test_output(self, output: str) -> List[TestResult]:
        """Parse pytest output to extract test results."""
        results = []
        lines = output.split('\n')

        current_test = None
        for line in lines:
            line = line.strip()

            # Look for test start
            if line.startswith('tests/') and '::' in line:
                current_test = line.split('::')[0]

            # Look for test results
            elif 'PASSED' in line or 'FAILED' in line or 'ERROR' in line or 'SKIPPED' in line:
                if current_test:
                    # Extract status and duration
                    status = 'passed' if 'PASSED' in line else 'failed' if 'FAILED' in line else 'error' if 'ERROR' in line else 'skipped'

                    # Try to extract duration
                    duration = 0.0
                    if ' in ' in line:
                        try:
                            duration_str = line.split(' in ')[1].split('s')[0]
                            duration = float(duration_str)
                        except (ValueError, IndexError):
                            pass

                    results.append(TestResult(
                        test_path=current_test,
                        test_name=line.split('::')[1].split()[0] if '::' in line else 'unknown',
                        status=status,
                        duration=duration
                    ))

        return results

    def detect_flaky_tests(self, num_runs: int = 5) -> List[FlakyTestReport]:
        """Run tests multiple times to detect flaky behavior."""
        logger.info(f"Running {num_runs} test iterations to detect flaky tests...")

        all_results = []

        for run in range(num_runs):
            logger.info(f"Run {run + 1}/{num_runs}")
            returncode, output = self.run_pytest_collection()

            if returncode == 0:
                results = self.parse_test_output(output)
                all_results.append(results)

        # Analyze results for flakiness
        flaky_reports = []

        if not all_results:
            return flaky_reports

        # Group by test
        test_runs = defaultdict(list)

        for run_results in all_results:
            for result in run_results:
                test_key = f"{result.test_path}::{result.test_name}"
                test_runs[test_key].append(result.status)

        # Identify flaky tests (not all passes or all fails)
        for test_key, statuses in test_runs.items():
            if len(statuses) >= num_runs:
                pass_count = statuses.count('passed')
                total_count = len(statuses)
                pass_rate = pass_count / total_count

                # Consider flaky if not all passes and not all fails
                if 0 < pass_rate < 1:
                    failure_patterns = [s for s in statuses if s != 'passed']
                    pattern_counts = Counter(failure_patterns)

                    recommendation = self._generate_flaky_recommendation(statuses)

                    flaky_reports.append(FlakyTestReport(
                        test_path=test_key.split('::')[0],
                        test_name=test_key.split('::')[1],
                        pass_rate=pass_rate,
                        total_runs=total_count,
                        failure_patterns=list(pattern_counts.keys()),
                        recommendation=recommendation
                    ))

        return flaky_reports

    def _generate_flaky_recommendation(self, statuses: List[str]) -> str:
        """Generate recommendations for flaky tests."""
        if 'error' in statuses:
            return "Test has import or setup errors - check dependencies and mocking"
        elif 'failed' in statuses:
            return "Test has assertion failures - review test logic and data setup"
        else:
            return "Test has intermittent issues - add retry logic or investigate race conditions"

    def analyze_coverage_gaps(self) -> List[str]:
        """Analyze coverage report for gaps."""
        gaps = []

        # Check for coverage report
        coverage_file = self.project_root / ".coverage"
        if not coverage_file.exists():
            gaps.append("No coverage data found - run tests with --cov flag")
            return gaps

        # Basic coverage analysis
        try:
            import coverage
            cov = coverage.Coverage()
            cov.load()

            # Get missing lines
            missing_lines = cov.get_missing_lines()

            if missing_lines:
                total_missing = sum(len(lines) for lines in missing_lines.values())
                gaps.append(f"{total_missing} lines missing coverage across {len(missing_lines)} files")

                # Find files with most missing coverage
                sorted_files = sorted(missing_lines.items(), key=lambda x: len(x[1]), reverse=True)
                for file_path, lines in sorted_files[:5]:
                    gaps.append(f"  {file_path}: {len(lines)} uncovered lines")

        except ImportError:
            gaps.append("Coverage analysis requires 'coverage' package")
        except Exception as e:
            gaps.append(f"Coverage analysis failed: {e}")

        return gaps

    def generate_suggestions(self, report: TestHealthReport) -> List[str]:
        """Generate improvement suggestions based on test health."""
        suggestions = []

        # Collection errors
        if report.collection_errors > 0:
            suggestions.append(f"Fix {report.collection_errors} collection errors - likely import or naming issues")
            suggestions.append("Check for circular imports and naming conflicts with pytest")

        # Failed tests
        if report.failed_tests > 0:
            suggestions.append(f"Address {report.failed_tests} failing tests - review error messages")
            suggestions.append("Ensure test data setup matches production expectations")

        # Skipped tests
        if report.skipped_tests > report.total_tests * 0.1:  # More than 10% skipped
            suggestions.append(f"Review {report.skipped_tests} skipped tests - ensure they're intentionally skipped")

        # Slow tests
        if report.slowest_tests:
            slowest = report.slowest_tests[0]
            if slowest[1] > 10:  # Tests taking more than 10 seconds
                suggestions.append(f"Optimize slowest test ({slowest[0]}: {slowest[1]:.2f}s) - consider mocking or parallelization")

        # Flaky tests
        if report.flaky_tests:
            suggestions.append(f"Address {len(report.flaky_tests)} flaky tests - add retry logic or investigate race conditions")

        # Coverage gaps
        if report.coverage_gaps:
            suggestions.append("Improve test coverage - target files with highest missing line counts")

        return suggestions

    def calculate_health_score(self, report: TestHealthReport) -> int:
        """Calculate overall test health score (0-100)."""
        score = 100

        # Collection errors are critical
        if report.collection_errors > 0:
            score -= min(50, report.collection_errors * 10)

        # Failed tests
        if report.total_tests > 0:
            failure_rate = report.failed_tests / report.total_tests
            score -= min(30, failure_rate * 100)

        # Flaky tests
        score -= min(20, len(report.flaky_tests) * 5)

        return max(0, int(score))

    def generate_full_report(self) -> TestHealthReport:
        """Generate comprehensive test health report."""
        logger.info("Generating full test health report...")

        # Run collection
        collection_code, collection_output = self.run_pytest_collection()
        collection_errors = collection_output.count("ERROR") if collection_code != 0 else 0

        # Parse basic results
        returncode, output = self.run_pytest_with_coverage()
        test_results = self.parse_test_output(output)

        # Calculate statistics
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.status == 'passed'])
        failed_tests = len([r for r in test_results if r.status == 'failed'])
        skipped_tests = len([r for r in test_results if r.status == 'skipped'])
        error_tests = len([r for r in test_results if r.status == 'error'])

        # Average duration
        durations = [r.duration for r in test_results if r.duration > 0]
        average_duration = sum(durations) / len(durations) if durations else 0

        # Slowest tests
        sorted_by_duration = sorted(
            [(f"{r.test_path}::{r.test_name}", r.duration) for r in test_results if r.duration > 0],
            key=lambda x: x[1],
            reverse=True
        )
        slowest_tests = sorted_by_duration[:5]

        # Flaky tests (run quick detection)
        flaky_tests = self.detect_flaky_tests(num_runs=3)

        # Coverage gaps
        coverage_gaps = self.analyze_coverage_gaps()

        # Create report
        report = TestHealthReport(
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            skipped_tests=skipped_tests,
            error_tests=error_tests,
            collection_errors=collection_errors,
            average_duration=average_duration,
            slowest_tests=slowest_tests,
            flaky_tests=flaky_tests,
            coverage_gaps=coverage_gaps,
            suggestions=[],
            health_score=0
        )

        # Generate suggestions and final score
        report.suggestions = self.generate_suggestions(report)
        report.health_score = self.calculate_health_score(report)

        return report

    def print_report(self, report: TestHealthReport):
        """Print formatted test health report."""
        print("🔍 TEST HEALTH MONITOR REPORT")
        print("=" * 50)
        print(f"Health Score: {report.health_score}/100 {'🟢' if report.health_score >= 80 else '🟡' if report.health_score >= 60 else '🔴'}")
        print()

        print("📊 TEST STATISTICS")
        print(f"Total Tests: {report.total_tests}")
        print(f"Passed: {report.passed_tests} ({report.passed_tests/report.total_tests*100:.1f}%)" if report.total_tests > 0 else "Passed: 0")
        print(f"Failed: {report.failed_tests}")
        print(f"Skipped: {report.skipped_tests}")
        print(f"Errors: {report.error_tests}")
        print(f"Collection Errors: {report.collection_errors}")
        print(".2f")
        print()

        if report.slowest_tests:
            print("🐌 SLOWEST TESTS")
            for test_name, duration in report.slowest_tests[:3]:
                print(".2f")
            print()

        if report.flaky_tests:
            print("🎲 FLAKY TESTS DETECTED")
            for flaky in report.flaky_tests[:3]:
                print(f"• {flaky.test_path}::{flaky.test_name} ({flaky.pass_rate:.1%} pass rate)")
                print(f"  Recommendation: {flaky.recommendation}")
            print()

        if report.coverage_gaps:
            print("📈 COVERAGE GAPS")
            for gap in report.coverage_gaps[:3]:
                print(f"• {gap}")
            print()

        if report.suggestions:
            print("💡 IMPROVEMENT SUGGESTIONS")
            for suggestion in report.suggestions[:5]:
                print(f"• {suggestion}")
            print()

        print("🐝 WE. ARE. SWARM. ⚡🔥")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Test Health Monitor CLI")
    parser.add_argument("--analyze", action="store_true", help="Run full health analysis")
    parser.add_argument("--flaky-detect", action="store_true", help="Detect flaky tests")
    parser.add_argument("--runs", type=int, default=5, help="Number of runs for flaky detection")
    parser.add_argument("--coverage-report", action="store_true", help="Analyze test coverage")
    parser.add_argument("--suggest-fixes", action="store_true", help="Generate improvement suggestions")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    # Initialize monitor
    monitor = TestHealthMonitor()

    if args.analyze:
        report = monitor.generate_full_report()
        if args.json:
            print(json.dumps({
                "health_score": report.health_score,
                "total_tests": report.total_tests,
                "passed_tests": report.passed_tests,
                "failed_tests": report.failed_tests,
                "skipped_tests": report.skipped_tests,
                "collection_errors": report.collection_errors,
                "suggestions": report.suggestions
            }, indent=2))
        else:
            monitor.print_report(report)

    elif args.flaky_detect:
        flaky_tests = monitor.detect_flaky_tests(args.runs)
        if args.json:
            print(json.dumps([{
                "test_path": f.test_path,
                "test_name": f.test_name,
                "pass_rate": f.pass_rate,
                "total_runs": f.total_runs,
                "recommendation": f.recommendation
            } for f in flaky_tests], indent=2))
        else:
            if flaky_tests:
                print(f"🎲 Found {len(flaky_tests)} potentially flaky tests:")
                for flaky in flaky_tests:
                    print(f"• {flaky.test_path}::{flaky.test_name}")
                    print(".1%")
                    print(f"  Recommendation: {flaky.recommendation}")
                    print()
            else:
                print("✅ No flaky tests detected")

    elif args.coverage_report:
        gaps = monitor.analyze_coverage_gaps()
        if args.json:
            print(json.dumps({"coverage_gaps": gaps}, indent=2))
        else:
            print("📈 COVERAGE ANALYSIS")
            for gap in gaps:
                print(f"• {gap}")

    elif args.suggest_fixes:
        report = monitor.generate_full_report()
        suggestions = monitor.generate_suggestions(report)
        if args.json:
            print(json.dumps({"suggestions": suggestions}, indent=2))
        else:
            print("💡 IMPROVEMENT SUGGESTIONS")
            for suggestion in suggestions:
                print(f"• {suggestion}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
