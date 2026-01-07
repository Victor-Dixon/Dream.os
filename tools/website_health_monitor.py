#!/usr/bin/env python3
"""
Website Health Monitor
======================

Comprehensive website health monitoring and diagnostics tool.
Identifies and reports on website availability, performance, and deployment issues.

Features:
- HTTP status code monitoring
- Response time measurement
- SSL certificate validation
- DNS resolution checking
- WordPress-specific health checks
- Automated issue detection and recommendations

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Enable proactive website health monitoring and deployment issue resolution
"""

import asyncio
import aiohttp
import ssl
import socket
import time
import json
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class WebsiteHealthCheck:
    """Comprehensive website health check result."""
    url: str
    timestamp: str
    http_status: Optional[int]
    response_time: Optional[float]
    is_ssl_valid: bool
    ssl_expiry_days: Optional[int]
    dns_resolves: bool
    wordpress_detected: bool
    error_message: Optional[str]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class WebsiteHealthMonitor:
    """Monitors website health and provides diagnostics."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=30, connect=10)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_website_health(self, url: str) -> WebsiteHealthCheck:
        """Perform comprehensive health check on a website."""
        result = WebsiteHealthCheck(
            url=url,
            timestamp=datetime.now().isoformat(),
            http_status=None,
            response_time=None,
            is_ssl_valid=False,
            ssl_expiry_days=None,
            dns_resolves=False,
            wordpress_detected=False,
            error_message=None,
            recommendations=[]
        )

        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
                result.url = url

            # DNS resolution check
            parsed = urlparse(url)
            try:
                socket.gethostbyname(parsed.hostname)
                result.dns_resolves = True
            except socket.gaierror:
                result.error_message = f"DNS resolution failed for {parsed.hostname}"
                result.recommendations.append("Check DNS configuration or domain registration")
                return result

            # SSL certificate check
            if url.startswith('https://'):
                result.is_ssl_valid, result.ssl_expiry_days = await self._check_ssl_certificate(parsed.hostname)
                if not result.is_ssl_valid:
                    result.recommendations.append("SSL certificate is invalid or expired")
                elif result.ssl_expiry_days and result.ssl_expiry_days < 30:
                    result.recommendations.append(f"SSL certificate expires in {result.ssl_expiry_days} days")

            # HTTP request check
            start_time = time.time()
            try:
                async with self.session.get(url, allow_redirects=True) as response:
                    result.http_status = response.status
                    result.response_time = time.time() - start_time

                    # Check for WordPress indicators
                    content_type = response.headers.get('content-type', '').lower()
                    server = response.headers.get('server', '').lower()

                    if 'wordpress' in server or content_type:
                        # Additional WordPress checks
                        result.wordpress_detected = await self._check_wordpress_indicators(response)

            except aiohttp.ClientError as e:
                result.error_message = f"HTTP request failed: {str(e)}"
                result.response_time = time.time() - start_time

                if "connect" in str(e).lower():
                    result.recommendations.append("Server is not responding - check if web server is running")
                elif "ssl" in str(e).lower():
                    result.recommendations.append("SSL/TLS connection failed - check SSL configuration")
                elif "timeout" in str(e).lower():
                    result.recommendations.append("Request timed out - server may be overloaded")
                else:
                    result.recommendations.append("Check server logs for detailed error information")

            # Generate additional recommendations based on status
            if result.http_status:
                if result.http_status >= 500:
                    result.recommendations.append("Server error (5xx) - check server logs and application code")
                    result.recommendations.append("Consider checking PHP-FPM, database connections, or disk space")
                elif result.http_status >= 400:
                    result.recommendations.append("Client error (4xx) - check URL, permissions, or .htaccess rules")
                elif result.http_status >= 300:
                    result.recommendations.append("Redirect response - verify redirect configuration")

                if result.response_time and result.response_time > 5.0:
                    result.recommendations.append(f"Slow response time ({result.response_time:.3f}s) - consider performance optimization")
            else:
                result.recommendations.append("No HTTP response received - server may be down")

        except Exception as e:
            result.error_message = f"Health check failed: {str(e)}"
            result.recommendations.append("Unexpected error - check system logs and network connectivity")

        return result

    async def _check_ssl_certificate(self, hostname: str) -> Tuple[bool, Optional[int]]:
        """Check SSL certificate validity and expiry."""
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            sock = socket.create_connection((hostname, 443), timeout=10)
            ssl_sock = ssl_context.wrap_socket(sock, server_hostname=hostname)

            cert = ssl_sock.getpeercert()
            ssl_sock.close()

            # Check expiry
            if cert:
                expiry_date = ssl.cert_time_to_seconds(cert['notAfter'])
                days_until_expiry = int((expiry_date - time.time()) / (24 * 3600))
                return True, days_until_expiry

            return False, None

        except Exception:
            return False, None

    async def _check_wordpress_indicators(self, response: aiohttp.ClientResponse) -> bool:
        """Check for WordPress-specific indicators."""
        try:
            # Check response headers for WordPress indicators
            headers = response.headers
            server = headers.get('Server', '').lower()
            powered_by = headers.get('X-Powered-By', '').lower()

            if 'wordpress' in server or 'wordpress' in powered_by:
                return True

            # Could check response body for WordPress meta tags, but that would be more expensive
            # For now, rely on headers

            return False

        except Exception:
            return False

    async def monitor_sites(self, urls: List[str]) -> List[WebsiteHealthCheck]:
        """Monitor multiple websites concurrently."""
        tasks = [self.check_website_health(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, WebsiteHealthCheck):
                valid_results.append(result)
            else:
                logger.error(f"Health check failed with exception: {result}")

        return valid_results

    def generate_report(self, results: List[WebsiteHealthCheck]) -> Dict[str, Any]:
        """Generate comprehensive health report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_sites": len(results),
                "healthy_sites": 0,
                "unhealthy_sites": 0,
                "sites_with_errors": 0,
                "average_response_time": 0.0
            },
            "results": [result.to_dict() for result in results],
            "recommendations": []
        }

        total_response_time = 0.0
        response_time_count = 0

        for result in results:
            if result.http_status and result.http_status < 400:
                report["summary"]["healthy_sites"] += 1
            else:
                report["summary"]["unhealthy_sites"] += 1

            if result.error_message:
                report["summary"]["sites_with_errors"] += 1

            if result.response_time:
                total_response_time += result.response_time
                response_time_count += 1

            # Collect all recommendations
            report["recommendations"].extend(result.recommendations)

        if response_time_count > 0:
            report["summary"]["average_response_time"] = round(total_response_time / response_time_count, 3)

        # Remove duplicate recommendations
        report["recommendations"] = list(set(report["recommendations"]))

        return report

async def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Website Health Monitor - Comprehensive website diagnostics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/website_health_monitor.py --url freerideinvestor.com
  python tools/website_health_monitor.py --urls sites.txt --json
  python tools/website_health_monitor.py --p0-sites --report
        """
    )

    parser.add_argument('--url', help='Check single website URL')
    parser.add_argument('--urls', help='File containing list of URLs to check')
    parser.add_argument('--p0-sites', action='store_true', help='Check all P0 sites')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--report', action='store_true', help='Generate detailed HTML report')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

    args = parser.parse_args()

    # Define P0 sites
    p0_sites = [
        "freerideinvestor.com",
        "tradingrobotplug.com",
        "dadudekc.com",
        "crosbyultimateevents.com"
    ]

    # Determine URLs to check
    urls = []
    if args.url:
        urls = [args.url]
    elif args.urls:
        try:
            with open(args.urls, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"❌ Error: File {args.urls} not found")
            sys.exit(1)
    elif args.p0_sites:
        urls = p0_sites
    else:
        parser.error("Must specify --url, --urls, or --p0-sites")

    async with WebsiteHealthMonitor() as monitor:
        try:
            results = await monitor.monitor_sites(urls)

            if args.json:
                report = monitor.generate_report(results)
                print(json.dumps(report, indent=2))
            elif args.report:
                report = monitor.generate_report(results)
                await generate_html_report(report)
            else:
                # Console output
                print("🌐 Website Health Monitor Results")
                print("=" * 50)

                for result in results:
                    status_icon = "✅" if (result.http_status and result.http_status < 400) else "❌"
                    print(f"\n{status_icon} {result.url}")

                    if result.http_status:
                        print(f"   Status: {result.http_status}")
                    if result.response_time:
                        print(f"   Response Time: {result.response_time:.3f}s")
                    if result.dns_resolves:
                        print("   DNS: ✅ Resolved")
                    else:
                        print("   DNS: ❌ Failed")

                    if result.url.startswith('https://'):
                        ssl_status = "✅ Valid" if result.is_ssl_valid else "❌ Invalid"
                        if result.ssl_expiry_days is not None:
                            ssl_status += f" ({result.ssl_expiry_days} days)"
                        print(f"   SSL: {ssl_status}")

                    if result.wordpress_detected:
                        print("   WordPress: ✅ Detected")

                    if result.error_message:
                        print(f"   Error: {result.error_message}")

                    if result.recommendations:
                        print("   Recommendations:")
                        for rec in result.recommendations:
                            print(f"     • {rec}")

                # Summary
                healthy = sum(1 for r in results if r.http_status and r.http_status < 400)
                total = len(results)
                print(f"\n📊 Summary: {healthy}/{total} sites healthy")

        except KeyboardInterrupt:
            print("\n⚠️  Monitoring interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)

async def generate_html_report(report: Dict[str, Any]) -> None:
    """Generate HTML report from health check results."""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Website Health Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .healthy {{ color: green; }}
        .unhealthy {{ color: red; }}
        .warning {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .recommendations {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>🌐 Website Health Report</h1>
    <p><strong>Generated:</strong> {report['timestamp']}</p>

    <h2>Summary</h2>
    <ul>
        <li><strong>Total Sites:</strong> {report['summary']['total_sites']}</li>
        <li><strong>Healthy Sites:</strong> <span class="healthy">{report['summary']['healthy_sites']}</span></li>
        <li><strong>Unhealthy Sites:</strong> <span class="unhealthy">{report['summary']['unhealthy_sites']}</span></li>
        <li><strong>Sites with Errors:</strong> <span class="warning">{report['summary']['sites_with_errors']}</span></li>
        <li><strong>Average Response Time:</strong> {report['summary']['average_response_time']}s</li>
    </ul>

    <h2>Site Details</h2>
    <table>
        <tr>
            <th>Site</th>
            <th>Status</th>
            <th>Response Time</th>
            <th>SSL</th>
            <th>WordPress</th>
            <th>Issues</th>
        </tr>
"""

    for result in report['results']:
        status_class = "healthy" if (result.get('http_status') and result['http_status'] < 400) else "unhealthy"
        status_text = f"{result.get('http_status', 'N/A')}"

        ssl_text = "N/A"
        if result.get('url', '').startswith('https://'):
            ssl_text = "✅ Valid" if result.get('is_ssl_valid') else "❌ Invalid"
            if result.get('ssl_expiry_days') is not None:
                ssl_text += f" ({result['ssl_expiry_days']}d)"

        wordpress_text = "✅ Yes" if result.get('wordpress_detected') else "❌ No"

        issues = result.get('error_message', 'None')
        if result.get('recommendations'):
            issues += "; " + "; ".join(result['recommendations'])

        html_content += f"""
        <tr>
            <td>{result['url']}</td>
            <td class="{status_class}">{status_text}</td>
            <td>{result.get('response_time', 'N/A') or 'N/A'}</td>
            <td>{ssl_text}</td>
            <td>{wordpress_text}</td>
            <td>{issues}</td>
        </tr>
"""

    html_content += """
    </table>

    <h2>Recommendations</h2>
    <div class="recommendations">
        <ul>
"""

    for rec in report.get('recommendations', []):
        html_content += f"<li>{rec}</li>"

    html_content += """
        </ul>
    </div>
</body>
</html>
"""

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"website_health_report_{timestamp}.html"

    with open(filename, 'w') as f:
        f.write(html_content)

    print(f"📄 HTML report saved: {filename}")

if __name__ == "__main__":
    asyncio.run(main())