#!/usr/bin/env python3
"""
Web Validation Test Suite - Agent Cellphone V2
==============================================

Comprehensive web endpoint validation framework for FastAPI services.

Features:
- Parallel endpoint testing
- Health check validation
- Performance metrics collection
- Infrastructure monitoring
- Real-time dashboard generation

V2 Compliant: <300 lines per function
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-07
"""

import asyncio
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor
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
    health_status: Dict[str, Any]
    performance_metrics: Dict[str, Any]

class WebValidationTestSuite:
    """Comprehensive web endpoint validation framework."""

    def __init__(self, base_url: str = "http://localhost:8001", timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

        # Define all endpoints to test
        self.endpoints = [
            {"path": "/health", "method": "GET", "description": "Health Check"},
            {"path": "/docs", "method": "GET", "description": "API Documentation"},
            {"path": "/redoc", "method": "GET", "description": "API Documentation (ReDoc)"},
            {"path": "/", "method": "GET", "description": "Dashboard"},
            {"path": "/offline", "method": "GET", "description": "Offline Page"},
            {"path": "/performance/metrics", "method": "GET", "description": "Performance Metrics"},
            {"path": "/analytics/config", "method": "GET", "description": "Analytics Config"},
        ]

    async def run_parallel_validation(self, max_concurrent: int = 5) -> ValidationReport:
        """
        Run comprehensive parallel endpoint validation.

        Args:
            max_concurrent: Maximum concurrent requests

        Returns:
            Complete validation report
        """
        start_time = time.time()

        # Create semaphore for concurrency control
        semaphore = asyncio.Semaphore(max_concurrent)

        async def test_endpoint(endpoint: dict) -> EndpointResult:
            async with semaphore:
                return await self._test_single_endpoint(endpoint)

        # Run all endpoint tests in parallel
        tasks = [test_endpoint(ep) for ep in self.endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        successful_results = []
        failed_results = []

        for result in results:
            if isinstance(result, Exception):
                # Handle exceptions
                failed_results.append(EndpointResult(
                    url="unknown",
                    method="unknown",
                    status_code=0,
                    response_time=0.0,
                    success=False,
                    error=str(result)
                ))
            elif result.success:
                successful_results.append(result)
            else:
                failed_results.append(result)

        all_results = successful_results + failed_results

        # Calculate metrics
        total_time = time.time() - start_time
        avg_response_time = sum(r.response_time for r in all_results) / len(all_results) if all_results else 0

        # Get health status and performance metrics
        health_status = await self._get_health_status()
        performance_metrics = await self._get_performance_metrics()

        return ValidationReport(
            timestamp=start_time,
            total_endpoints=len(self.endpoints),
            successful_tests=len(successful_results),
            failed_tests=len(failed_results),
            average_response_time=avg_response_time,
            results=all_results,
            health_status=health_status,
            performance_metrics=performance_metrics
        )

    async def _test_single_endpoint(self, endpoint: dict) -> EndpointResult:
        """Test a single endpoint."""
        url = urljoin(self.base_url + '/', endpoint["path"].lstrip('/'))
        method = endpoint["method"]

        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout
            )

            response_time = time.time() - start_time

            return EndpointResult(
                url=url,
                method=method,
                status_code=response.status_code,
                response_time=response_time,
                success=response.status_code < 400,
                response_size=len(response.content)
            )

        except Exception as e:
            response_time = time.time() - start_time
            return EndpointResult(
                url=url,
                method=method,
                status_code=0,
                response_time=response_time,
                success=False,
                error=str(e)
            )

    async def _get_health_status(self) -> Dict[str, Any]:
        """Get current health status."""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            response = self.session.get(
                f"{self.base_url}/performance/metrics",
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def generate_monitoring_dashboard(self, report: ValidationReport) -> str:
        """
        Generate HTML monitoring dashboard.

        Args:
            report: Validation report to display

        Returns:
            HTML dashboard content
        """
        success_rate = (report.successful_tests / report.total_endpoints * 100) if report.total_endpoints > 0 else 0

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Web Infrastructure Monitoring Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
                .metric-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }}
                .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .card.success {{ border-left: 5px solid #28a745; }}
                .card.warning {{ border-left: 5px solid #ffc107; }}
                .card.error {{ border-left: 5px solid #dc3545; }}
                .status-indicator {{ display: inline-block; width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }}
                .status-healthy {{ background: #28a745; }}
                .status-unhealthy {{ background: #dc3545; }}
                .status-unknown {{ background: #ffc107; }}
                .results-table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .results-table th, .results-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                .results-table th {{ background: #f8f9fa; font-weight: 600; }}
                .results-table tr:hover {{ background: #f8f9fa; }}
                .success {{ color: #28a745; }}
                .error {{ color: #dc3545; }}
                .warning {{ color: #ffc107; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Web Infrastructure Monitoring Dashboard</h1>
                    <p>Real-time validation results for Agent Cellphone V2 FastAPI Services</p>
                    <small>Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(report.timestamp))}</small>
                </div>

                <div class="metric-cards">
                    <div class="card success">
                        <h3>Overall Health</h3>
                        <div>
                            <span class="status-indicator status-{report.health_status.get('overall_status', 'unknown').lower()}"></span>
                            {report.health_status.get('overall_status', 'Unknown').title()}
                        </div>
                    </div>

                    <div class="card {'success' if success_rate >= 80 else 'warning' if success_rate >= 50 else 'error'}">
                        <h3>Success Rate</h3>
                        <div>{success_rate:.1f}%</div>
                        <small>{report.successful_tests}/{report.total_endpoints} endpoints</small>
                    </div>

                    <div class="card {'success' if report.average_response_time < 1.0 else 'warning' if report.average_response_time < 5.0 else 'error'}">
                        <h3>Average Response Time</h3>
                        <div>{report.average_response_time:.2f}s</div>
                    </div>

                    <div class="card {'success' if report.failed_tests == 0 else 'error'}">
                        <h3>Failed Tests</h3>
                        <div>{report.failed_tests}</div>
                        <small>Endpoints with issues</small>
                    </div>
                </div>

                <div class="card">
                    <h3>📊 Endpoint Test Results</h3>
                    <table class="results-table">
                        <thead>
                            <tr>
                                <th>Endpoint</th>
                                <th>Method</th>
                                <th>Status</th>
                                <th>Response Time</th>
                                <th>Size</th>
                            </tr>
                        </thead>
                        <tbody>
        """

        for result in report.results:
            status_class = "success" if result.success else "error"
            status_text = f"✅ {result.status_code}" if result.success else f"❌ {result.status_code or 'ERROR'}"

            html += f"""
                            <tr>
                                <td>{result.url.replace(self.base_url, '')}</td>
                                <td><code>{result.method}</code></td>
                                <td class="{status_class}">{status_text}</td>
                                <td>{result.response_time:.2f}s</td>
                                <td>{result.response_size:,} bytes</td>
                            </tr>
            """

        html += """
                        </tbody>
                    </table>
                </div>

                <div class="card">
                    <h3>🔧 Health Status Details</h3>
                    <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">""" + str(report.health_status) + """</pre>
                </div>

                <div class="card">
                    <h3>⚡ Performance Metrics</h3>
                    <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">""" + str(report.performance_metrics) + """</pre>
                </div>
            </div>
        </body>
        </html>
        """

        return html

async def main():
    """Main validation execution."""
    print("🚀 Starting Web Validation Test Suite...")
    print("=" * 50)

    suite = WebValidationTestSuite()

    try:
        # Run parallel validation
        report = await suite.run_parallel_validation(max_concurrent=5)

        # Generate and save dashboard
        dashboard_html = suite.generate_monitoring_dashboard(report)

        with open("web_monitoring_dashboard.html", "w", encoding="utf-8") as f:
            f.write(dashboard_html)

        # Print summary
        print("📊 Validation Complete!")
        print(f"   ✅ Successful: {report.successful_tests}/{report.total_endpoints}")
        print(f"   ❌ Failed: {report.failed_tests}/{report.total_endpoints}")
        print(f"   ⏱️  Average Response Time: {report.average_response_time:.2f}s")
        print(f"   📊 Dashboard saved: web_monitoring_dashboard.html")

        # Print detailed results
        print("\n🔍 Detailed Results:")
        for result in report.results:
            status = "✅" if result.success else "❌"
            error_info = f" - {result.error}" if result.error else ""
            print(f"   {status} {result.method} {result.url.replace(suite.base_url, '')} - {result.response_time:.2f}s{error_info}")

        return report

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())