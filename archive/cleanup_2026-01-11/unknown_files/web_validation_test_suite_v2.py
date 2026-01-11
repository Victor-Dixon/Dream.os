"""
Web Validation Test Suite V2 - Agent Cellphone V2
================================================

SSOT Domain: web

Refactored web endpoint validation framework using service architecture.

Features:
- Parallel endpoint testing
- Health check validation
- Performance metrics collection
- Comprehensive reporting
- Real-time monitoring

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import asyncio
import time
import logging
import argparse
from pathlib import Path

from src.web.validation_service import (
    validation_service,
    ValidationReport,
    EndpointResult
)

logger = logging.getLogger(__name__)

class WebValidationTestSuite:
    """
    Comprehensive web endpoint validation framework.
    """

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.validation_service = validation_service
        self.validation_service.set_base_url(base_url)

        # Add default endpoints
        self._setup_default_endpoints()

    def _setup_default_endpoints(self):
        """Setup default endpoints for testing."""
        default_endpoints = [
            ("/health", "GET"),
            ("/docs", "GET"),
            ("/openapi.json", "GET"),
            ("/redoc", "GET"),
        ]

        for path, method in default_endpoints:
            self.validation_service.add_endpoint(path, method)

    async def run_full_validation(self) -> ValidationReport:
        """
        Run comprehensive validation of all endpoints.

        Returns:
            Complete validation report
        """
        logger.info("Starting comprehensive web validation...")
        report = await self.validation_service.run_validation_async()

        logger.info(
            f"Validation completed: {report.successful_tests}/{report.total_endpoints} successful "
            f"(avg: {report.average_response_time:.3f}s)"
        )

        return report

    def run_quick_health_check(self) -> dict:
        """
        Run quick health check of the service.

        Returns:
            Health status dictionary
        """
        logger.info("Running quick health check...")
        health_status = self.validation_service.get_health_status()

        status_msg = "healthy" if health_status["healthy"] else "unhealthy"
        logger.info(f"Health check result: {status_msg}")

        return health_status

    def generate_detailed_report(self, report: ValidationReport) -> str:
        """
        Generate detailed markdown report.

        Args:
            report: Validation report

        Returns:
            Markdown formatted report
        """
        return self.validation_service.generate_report_markdown(report)

    def save_report(self, report: ValidationReport, filename: str = None) -> str:
        """
        Save validation report to file.

        Args:
            report: Validation report
            filename: Output filename (optional)

        Returns:
            Path to saved report file
        """
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"web_validation_report_{timestamp}.md"

        report_content = self.generate_detailed_report(report)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"Report saved to: {filename}")
        return filename

    def add_custom_endpoint(self, path: str, method: str = "GET"):
        """
        Add custom endpoint for testing.

        Args:
            path: Endpoint path
            method: HTTP method
        """
        self.validation_service.add_endpoint(path, method)
        logger.info(f"Added custom endpoint: {method} {path}")

async def main():
    """
    Main entry point for the web validation test suite.
    """
    parser = argparse.ArgumentParser(description="Web Validation Test Suite")
    parser.add_argument(
        "--url",
        default="http://localhost:8001",
        help="Base URL for testing (default: http://localhost:8001)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick health check only"
    )
    parser.add_argument(
        "--save-report",
        action="store_true",
        help="Save detailed report to file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    try:
        # Create test suite
        test_suite = WebValidationTestSuite(args.url)

        if args.quick:
            # Quick health check
            health = test_suite.run_quick_health_check()

            print("🩺 Quick Health Check Results:")
            print(f"  Healthy: {'✅' if health['healthy'] else '❌'}")
            print(f"  Response Time: {health.get('response_time', 'N/A'):.3f}s")
            print(f"  Status Code: {health.get('status_code', 'N/A')}")

            if not health["healthy"]:
                print(f"  Error: {health.get('error', 'Unknown error')}")
                return 1

        else:
            # Full validation
            print(f"🚀 Starting web validation for: {args.url}")
            report = await test_suite.run_full_validation()

            print("\n📊 Validation Summary:")
            print(f"  Total Endpoints: {report.total_endpoints}")
            print(f"  Successful: {report.successful_tests}")
            print(f"  Failed: {report.failed_tests}")
            print(f"  Average Response Time: {report.average_response_time:.3f}s")

            if args.save_report:
                report_file = test_suite.save_report(report)
                print(f"  📄 Detailed report saved: {report_file}")

            # Show failed tests
            failed_results = [r for r in report.results if not r.success]
            if failed_results:
                print("\n❌ Failed Tests:")
                for result in failed_results:
                    print(f"  • {result.method} {result.url}")
                    if result.error:
                        print(f"    Error: {result.error}")

            # Return exit code based on success
            return 0 if report.failed_tests == 0 else 1

    except Exception as e:
        logger.error(f"Test suite failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)