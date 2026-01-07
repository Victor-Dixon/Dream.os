"""
Web Validation Service - Agent Cellphone V2
===========================================

SSOT Domain: web

Core service for web endpoint validation and testing.

Features:
- Parallel endpoint testing
- Health check validation
- Performance metrics collection
- Real-time monitoring
- Comprehensive reporting

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import asyncio
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

@dataclass
class EndpointResult:
    """Result of endpoint validation."""
    url: str
    method: str
    status_code: int
    response_time: float
    success: bool
    error: Optional[str] = None
    response_size: int = 0

@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    timestamp: float
    total_endpoints: int
    successful_tests: int
    failed_tests: int
    average_response_time: float
    results: List[EndpointResult]

class WebValidationService:
    """
    Service for comprehensive web endpoint validation.
    """

    def __init__(self, base_url: str = "http://localhost:8001", timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=10)

        # Default endpoints to test
        self.endpoints = [
            {"path": "/health", "method": "GET"},
            {"path": "/docs", "method": "GET"},
            {"path": "/openapi.json", "method": "GET"},
            {"path": "/redoc", "method": "GET"},
        ]

    def add_endpoint(self, path: str, method: str = "GET") -> None:
        """
        Add an endpoint to the test suite.

        Args:
            path: Endpoint path (e.g., "/health")
            method: HTTP method (default: GET)
        """
        self.endpoints.append({"path": path, "method": method})

    def set_base_url(self, base_url: str) -> None:
        """
        Set the base URL for testing.

        Args:
            base_url: Base URL for the web service
        """
        self.base_url = base_url.rstrip('/')

    async def run_validation_async(self) -> ValidationReport:
        """
        Run comprehensive validation asynchronously.

        Returns:
            Complete validation report
        """
        start_time = time.time()

        # Run tests in parallel using thread pool
        loop = asyncio.get_event_loop()
        futures = []

        for endpoint in self.endpoints:
            future = loop.run_in_executor(
                self.executor,
                self._test_endpoint_sync,
                endpoint
            )
            futures.append(future)

        # Wait for all tests to complete
        results = await asyncio.gather(*futures, return_exceptions=True)

        # Process results
        valid_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Create failed result for exceptions
                endpoint = self.endpoints[i]
                url = urljoin(self.base_url + '/', endpoint["path"].lstrip('/'))
                failed_result = EndpointResult(
                    url=url,
                    method=endpoint["method"],
                    status_code=0,
                    response_time=0.0,
                    success=False,
                    error=str(result)
                )
                valid_results.append(failed_result)
            else:
                valid_results.append(result)

        # Generate report
        successful_tests = sum(1 for r in valid_results if r.success)
        failed_tests = len(valid_results) - successful_tests
        avg_response_time = sum(r.response_time for r in valid_results) / len(valid_results) if valid_results else 0

        report = ValidationReport(
            timestamp=start_time,
            total_endpoints=len(valid_results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            average_response_time=avg_response_time,
            results=valid_results
        )

        logger.info(f"Validation completed: {successful_tests}/{len(valid_results)} successful")
        return report

    def run_validation_sync(self) -> ValidationReport:
        """
        Run comprehensive validation synchronously.

        Returns:
            Complete validation report
        """
        start_time = time.time()
        results = []

        # Test endpoints sequentially
        for endpoint in self.endpoints:
            result = self._test_endpoint_sync(endpoint)
            results.append(result)

        # Generate report
        successful_tests = sum(1 for r in results if r.success)
        failed_tests = len(results) - successful_tests
        avg_response_time = sum(r.response_time for r in results) / len(results) if results else 0

        report = ValidationReport(
            timestamp=start_time,
            total_endpoints=len(results),
            successful_tests=successful_tests,
            failed_tests=failed_tests,
            average_response_time=avg_response_time,
            results=results
        )

        logger.info(f"Validation completed: {successful_tests}/{len(results)} successful")
        return report

    def _test_endpoint_sync(self, endpoint: Dict[str, str]) -> EndpointResult:
        """
        Test a single endpoint synchronously.

        Args:
            endpoint: Endpoint configuration

        Returns:
            Endpoint test result
        """
        url = urljoin(self.base_url + '/', endpoint["path"].lstrip('/'))
        method = endpoint["method"]

        start_time = time.time()

        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=self.timeout,
                headers={"User-Agent": "WebValidationTestSuite/1.0"}
            )

            response_time = time.time() - start_time

            success = response.status_code < 400  # Consider 2xx and 3xx as success

            return EndpointResult(
                url=url,
                method=method,
                status_code=response.status_code,
                response_time=response_time,
                success=success,
                response_size=len(response.content)
            )

        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return EndpointResult(
                url=url,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error=str(e)
            )
        except Exception as e:
            response_time = time.time() - start_time
            return EndpointResult(
                url=url,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error=f"Unexpected error: {e}"
            )

    def generate_report_markdown(self, report: ValidationReport) -> str:
        """
        Generate a markdown report from validation results.

        Args:
            report: Validation report

        Returns:
            Markdown formatted report
        """
        lines = [
            "# Web Validation Report",
            f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))}",
            f"**Base URL:** {self.base_url}",
            "",
            "## Summary",
            f"- **Total Endpoints:** {report.total_endpoints}",
            f"- **Successful Tests:** {report.successful_tests}",
            f"- **Failed Tests:** {report.failed_tests}",
            f"- **Average Response Time:** {report.average_response_time:.3f}s",
            "",
            "## Results",
            "",
            "| Endpoint | Method | Status | Response Time | Success |",
            "|----------|--------|--------|---------------|---------|",
        ]

        for result in report.results:
            status = f"{result.status_code}" if result.status_code > 0 else "ERROR"
            success = "✅" if result.success else "❌"
            lines.append(
                f"| {result.url} | {result.method} | {status} | {result.response_time:.3f}s | {success} |"
            )

        # Add error details
        failed_results = [r for r in report.results if not r.success]
        if failed_results:
            lines.extend([
                "",
                "## Failed Tests",
                ""
            ])

            for result in failed_results:
                lines.extend([
                    f"### {result.url} ({result.method})",
                    f"- **Error:** {result.error or 'Unknown error'}",
                    f"- **Response Time:** {result.response_time:.3f}s",
                    ""
                ])

        return "\n".join(lines)

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get overall health status based on recent validation.

        Returns:
            Health status dictionary
        """
        try:
            # Run a quick health check
            health_result = self._test_endpoint_sync({"path": "/health", "method": "GET"})

            return {
                "healthy": health_result.success,
                "response_time": health_result.response_time,
                "status_code": health_result.status_code,
                "error": health_result.error,
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "healthy": False,
                "error": str(e),
                "timestamp": time.time()
            }

# Global service instance
validation_service = WebValidationService()

__all__ = [
    "WebValidationService",
    "EndpointResult",
    "ValidationReport",
    "validation_service"
]