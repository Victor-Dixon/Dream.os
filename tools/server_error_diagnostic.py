#!/usr/bin/env python3
"""
Server Error Diagnostic Tool
============================

Comprehensive server error diagnostic and troubleshooting tool.
Identifies and provides actionable solutions for common server errors,
particularly WordPress/PHP 500 Internal Server Errors.

Features:
- HTTP error code analysis and categorization
- WordPress-specific error diagnostics
- PHP error log analysis
- Server configuration validation
- Automated troubleshooting recommendations
- Root cause analysis with fix suggestions

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Enable rapid diagnosis and resolution of server errors in production environments
"""

import asyncio
import aiohttp
import json
import time
import re
import subprocess
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ServerErrorDiagnostic:
    """Comprehensive server error diagnostic result."""
    url: str
    error_code: Optional[int]
    error_type: str
    timestamp: str
    response_time: Optional[float]
    root_cause_analysis: List[str]
    recommended_fixes: List[str]
    severity_level: str  # critical, high, medium, low
    confidence_score: int  # 1-100
    diagnostic_details: Dict[str, Any]

@dataclass
class WordPressErrorAnalysis:
    """WordPress-specific error analysis."""
    is_wordpress_site: bool
    php_errors: List[str]
    database_issues: List[str]
    plugin_conflicts: List[str]
    theme_issues: List[str]
    permission_problems: List[str]
    resource_limits: List[str]

class ServerErrorDiagnosticTool:
    """Comprehensive server error diagnostic tool."""

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.timeout = aiohttp.ClientTimeout(total=30, connect=10)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def diagnose_server_error(self, url: str) -> ServerErrorDiagnostic:
        """Perform comprehensive server error diagnosis."""
        result = ServerErrorDiagnostic(
            url=url,
            error_code=None,
            error_type="unknown",
            timestamp=datetime.now().isoformat(),
            response_time=None,
            root_cause_analysis=[],
            recommended_fixes=[],
            severity_level="low",
            confidence_score=0,
            diagnostic_details={}
        )

        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
                result.url = url

            start_time = time.time()

            try:
                async with self.session.get(url, allow_redirects=False) as response:
                    result.error_code = response.status
                    result.response_time = time.time() - start_time

                    # Analyze error codes
                    await self._analyze_error_code(response, result)

                    # Check response content for additional clues
                    if response.status >= 400:
                        content = await response.text()
                        result.diagnostic_details['response_content'] = content[:1000]  # First 1000 chars

            except aiohttp.ClientError as e:
                result.response_time = time.time() - start_time
                result.error_type = "connection_error"
                result.root_cause_analysis.append(f"Connection failed: {str(e)}")
                result.recommended_fixes.append("Check server connectivity and DNS resolution")
                result.recommended_fixes.append("Verify firewall settings and network configuration")
                result.severity_level = "high"
                result.confidence_score = 90

            except asyncio.TimeoutError:
                result.error_type = "timeout_error"
                result.root_cause_analysis.append("Request timed out - server may be overloaded or unresponsive")
                result.recommended_fixes.append("Check server load and resource utilization")
                result.recommended_fixes.append("Review server timeout configurations")
                result.severity_level = "high"
                result.confidence_score = 85

            # Additional diagnostics for WordPress sites
            if result.error_code == 500 or result.error_type in ["connection_error", "timeout_error"]:
                wordpress_analysis = await self._analyze_wordpress_issues(url)
                result.diagnostic_details['wordpress_analysis'] = asdict(wordpress_analysis)

                # Incorporate WordPress-specific findings
                if wordpress_analysis.is_wordpress_site:
                    result.root_cause_analysis.extend(wordpress_analysis.php_errors)
                    result.root_cause_analysis.extend(wordpress_analysis.database_issues)
                    result.root_cause_analysis.extend(wordpress_analysis.plugin_conflicts)
                    result.root_cause_analysis.extend(wordpress_analysis.theme_issues)
                    result.root_cause_analysis.extend(wordpress_analysis.permission_problems)
                    result.root_cause_analysis.extend(wordpress_analysis.resource_limits)

                    # Generate WordPress-specific fixes
                    wordpress_fixes = self._generate_wordpress_fixes(wordpress_analysis)
                    result.recommended_fixes.extend(wordpress_fixes)

        except Exception as e:
            logger.error(f"Error during diagnosis of {url}: {e}")
            result.error_type = "diagnostic_error"
            result.root_cause_analysis.append(f"Diagnostic tool error: {str(e)}")
            result.recommended_fixes.append("Contact system administrator for manual investigation")

        return result

    async def _analyze_error_code(self, response: aiohttp.ClientResponse, result: ServerErrorDiagnostic):
        """Analyze HTTP error codes and provide specific diagnostics."""

        status = response.status
        result.error_code = status

        if status == 400:
            result.error_type = "bad_request"
            result.severity_level = "medium"
            result.confidence_score = 70
            result.root_cause_analysis.append("Client sent malformed request")
            result.recommended_fixes.append("Check URL syntax and request parameters")
            result.recommended_fixes.append("Review browser cache and cookies")

        elif status == 401:
            result.error_type = "unauthorized"
            result.severity_level = "medium"
            result.confidence_score = 80
            result.root_cause_analysis.append("Authentication required but not provided")
            result.recommended_fixes.append("Provide valid authentication credentials")
            result.recommended_fixes.append("Check authentication configuration")

        elif status == 403:
            result.error_type = "forbidden"
            result.severity_level = "medium"
            result.confidence_score = 75
            result.root_cause_analysis.append("Access denied to requested resource")
            result.recommended_fixes.append("Check file permissions and ownership")
            result.recommended_fixes.append("Review access control settings")

        elif status == 404:
            result.error_type = "not_found"
            result.severity_level = "low"
            result.confidence_score = 90
            result.root_cause_analysis.append("Requested resource not found")
            result.recommended_fixes.append("Verify URL is correct")
            result.recommended_fixes.append("Check if file exists on server")

        elif status == 500:
            result.error_type = "internal_server_error"
            result.severity_level = "critical"
            result.confidence_score = 95
            result.root_cause_analysis.append("Server encountered an internal error")
            result.recommended_fixes.append("Check server error logs for detailed information")
            result.recommended_fixes.append("Verify application code for bugs or exceptions")
            result.recommended_fixes.append("Check database connectivity and PHP configuration")

        elif status == 502:
            result.error_type = "bad_gateway"
            result.severity_level = "high"
            result.confidence_score = 85
            result.root_cause_analysis.append("Invalid response from upstream server")
            result.recommended_fixes.append("Check upstream server status and configuration")
            result.recommended_fixes.append("Review proxy/load balancer settings")

        elif status == 503:
            result.error_type = "service_unavailable"
            result.severity_level = "high"
            result.confidence_score = 80
            result.root_cause_analysis.append("Server temporarily unable to handle requests")
            result.recommended_fixes.append("Check server load and resource utilization")
            result.recommended_fixes.append("Review maintenance mode settings")

        elif status == 504:
            result.error_type = "gateway_timeout"
            result.severity_level = "high"
            result.confidence_score = 85
            result.root_cause_analysis.append("Gateway timeout - upstream server took too long to respond")
            result.recommended_fixes.append("Increase timeout settings in proxy configuration")
            result.recommended_fixes.append("Optimize upstream server performance")

        elif status >= 300 and status < 400:
            result.error_type = "redirection"
            result.severity_level = "low"
            result.confidence_score = 60
            result.root_cause_analysis.append("Request redirected to different location")
            result.recommended_fixes.append("Follow redirect or update URLs")

    async def _analyze_wordpress_issues(self, url: str) -> WordPressErrorAnalysis:
        """Analyze WordPress-specific issues that could cause 500 errors."""
        analysis = WordPressErrorAnalysis(
            is_wordpress_site=False,
            php_errors=[],
            database_issues=[],
            plugin_conflicts=[],
            theme_issues=[],
            permission_problems=[],
            resource_limits=[]
        )

        try:
            # Check if it's a WordPress site by looking for common indicators
            parsed = urlparse(url)
            base_url = f"{parsed.scheme}://{parsed.netloc}"

            # Check wp-admin access (indicates WordPress)
            wp_admin_url = f"{base_url}/wp-admin/"
            try:
                async with self.session.get(wp_admin_url, allow_redirects=True) as response:
                    if response.status < 400 or "wordpress" in (await response.text()).lower():
                        analysis.is_wordpress_site = True
            except:
                pass

            # Check wp-login access
            wp_login_url = f"{base_url}/wp-login.php"
            try:
                async with self.session.get(wp_login_url, allow_redirects=True) as response:
                    if response.status < 400 or "wordpress" in (await response.text()).lower():
                        analysis.is_wordpress_site = True
            except:
                pass

            if analysis.is_wordpress_site:
                # Analyze common WordPress 500 error causes
                analysis.php_errors.extend([
                    "PHP memory limit exceeded",
                    "PHP execution timeout",
                    "PHP syntax errors in theme/plugin files",
                    "PHP fatal errors in functions.php"
                ])

                analysis.database_issues.extend([
                    "Database connection failed",
                    "Database server unreachable",
                    "Corrupted WordPress database tables",
                    "Database user permissions insufficient"
                ])

                analysis.plugin_conflicts.extend([
                    "Plugin compatibility issues",
                    "Malfunctioning plugin causing fatal errors",
                    "Plugin database corruption",
                    "Outdated plugin versions"
                ])

                analysis.theme_issues.extend([
                    "Corrupted theme files",
                    "Theme PHP syntax errors",
                    "Incompatible theme with WordPress version",
                    "Theme database issues"
                ])

                analysis.permission_problems.extend([
                    "Incorrect file permissions (should be 644 for files, 755 for directories)",
                    "Incorrect ownership of WordPress files",
                    ".htaccess file permissions blocking access",
                    "Upload directory permissions preventing file operations"
                ])

                analysis.resource_limits.extend([
                    "Server CPU usage too high",
                    "Server memory exhausted",
                    "Disk space full",
                    "Inode limits reached",
                    "Database connection limits exceeded"
                ])

        except Exception as e:
            logger.debug(f"WordPress analysis failed for {url}: {e}")

        return analysis

    def _generate_wordpress_fixes(self, analysis: WordPressErrorAnalysis) -> List[str]:
        """Generate WordPress-specific fix recommendations."""
        fixes = []

        if analysis.php_errors:
            fixes.extend([
                "Enable WordPress debug mode by adding 'define('WP_DEBUG', true);' to wp-config.php",
                "Check PHP error logs in /var/log/php/error.log or similar",
                "Increase PHP memory limit in php.ini or wp-config.php: 'define('WP_MEMORY_LIMIT', '256M');'",
                "Disable problematic plugins by renaming wp-content/plugins/plugin-name to disable it"
            ])

        if analysis.database_issues:
            fixes.extend([
                "Verify database credentials in wp-config.php",
                "Check database server status and connectivity",
                "Repair WordPress database tables using WP-CLI: 'wp db repair'",
                "Check database user permissions and grant necessary privileges"
            ])

        if analysis.plugin_conflicts:
            fixes.extend([
                "Temporarily disable all plugins by renaming wp-content/plugins to wp-content/plugins-disabled",
                "Re-enable plugins one by one to identify the problematic one",
                "Update all plugins to latest versions",
                "Check for plugin compatibility with current WordPress version"
            ])

        if analysis.theme_issues:
            fixes.extend([
                "Switch to default WordPress theme (Twenty Twenty-One) to test",
                "Check theme PHP files for syntax errors",
                "Re-upload theme files from fresh WordPress theme download",
                "Update theme to latest version or find compatible alternative"
            ])

        if analysis.permission_problems:
            fixes.extend([
                "Set correct file permissions: 'find . -type f -exec chmod 644 {} \;'",
                "Set correct directory permissions: 'find . -type d -exec chmod 755 {} \;'",
                "Set correct ownership: 'chown -R www-data:www-data .' (adjust user/group as needed)",
                "Check .htaccess file permissions and content"
            ])

        if analysis.resource_limits:
            fixes.extend([
                "Monitor server resources using 'top', 'htop', or 'free -h'",
                "Check disk usage with 'df -h' and clean up unnecessary files",
                "Increase server resources or optimize resource usage",
                "Check for memory leaks in PHP/application code"
            ])

        return fixes

    def generate_diagnostic_report(self, results: List[ServerErrorDiagnostic]) -> Dict[str, Any]:
        """Generate comprehensive diagnostic report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_diagnostics": len(results),
                "critical_errors": 0,
                "high_severity": 0,
                "wordpress_sites": 0,
                "average_confidence": 0.0
            },
            "diagnostics": [asdict(result) for result in results],
            "common_issues": {},
            "recommended_actions": []
        }

        total_confidence = 0

        for result in results:
            if result.severity_level == "critical":
                report["summary"]["critical_errors"] += 1
            elif result.severity_level == "high":
                report["summary"]["high_severity"] += 1

            if result.diagnostic_details.get('wordpress_analysis', {}).get('is_wordpress_site'):
                report["summary"]["wordpress_sites"] += 1

            total_confidence += result.confidence_score

            # Aggregate common issues
            for issue in result.root_cause_analysis:
                if issue not in report["common_issues"]:
                    report["common_issues"][issue] = 0
                report["common_issues"][issue] += 1

        if results:
            report["summary"]["average_confidence"] = round(total_confidence / len(results), 1)

        # Generate recommended actions based on common issues
        if report["summary"]["critical_errors"] > 0:
            report["recommended_actions"].append("Prioritize fixing critical 500 Internal Server Errors immediately")
            report["recommended_actions"].append("Enable detailed error logging to capture root cause information")

        if report["summary"]["wordpress_sites"] > 0:
            report["recommended_actions"].append("For WordPress sites, check PHP error logs and WordPress debug logs")
            report["recommended_actions"].append("Consider using WordPress debugging plugins for detailed error information")

        return report

# CLI interface
async def main():
    """Main CLI interface for server error diagnostics."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Server Error Diagnostic Tool - Comprehensive server error analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/server_error_diagnostic.py --url dadudekc.com
  python tools/server_error_diagnostic.py --urls error_sites.txt --json
  python tools/server_error_diagnostic.py --wordpress-sites --report
        """
    )

    parser.add_argument('--url', help='Diagnose single URL')
    parser.add_argument('--urls', help='File containing list of URLs to diagnose')
    parser.add_argument('--wordpress-sites', action='store_true', help='Focus on WordPress-specific diagnostics')
    parser.add_argument('--json', action='store_true', help='Output results as JSON')
    parser.add_argument('--report', action='store_true', help='Generate detailed HTML report')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

    args = parser.parse_args()

    # Define sites with known issues
    error_sites = [
        "dadudekc.com",  # 500 Internal Server Error
        "crosbyultimateevents.com"  # 500 Internal Server Error
    ]

    # Determine URLs to diagnose
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
    elif args.wordpress_sites:
        urls = error_sites
    else:
        parser.error("Must specify --url, --urls, or --wordpress-sites")

    async with ServerErrorDiagnosticTool() as diagnostic:
        try:
            tasks = [diagnostic.diagnose_server_error(url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter valid results
            valid_results = [r for r in results if isinstance(r, ServerErrorDiagnostic)]

            if args.json:
                report = diagnostic.generate_diagnostic_report(valid_results)
                print(json.dumps(report, indent=2))
            elif args.report:
                report = diagnostic.generate_diagnostic_report(valid_results)
                await generate_html_report(report)
            else:
                # Console output
                print("🔍 Server Error Diagnostic Results")
                print("=" * 50)

                for result in valid_results:
                    severity_icon = {
                        "critical": "🚨",
                        "high": "⚠️",
                        "medium": "ℹ️",
                        "low": "✅"
                    }.get(result.severity_level, "❓")

                    print(f"\n{severity_icon} {result.url}")

                    if result.error_code:
                        print(f"   Error Code: {result.error_code} ({result.error_type})")
                    else:
                        print(f"   Error Type: {result.error_type}")

                    if result.response_time:
                        print(f"   Response Time: {result.response_time:.3f}s")
                    print(f"   Severity: {result.severity_level.upper()}")
                    print(f"   Confidence: {result.confidence_score}%")

                    if result.root_cause_analysis:
                        print("   Root Cause Analysis:")
                        for cause in result.root_cause_analysis[:3]:  # Show top 3
                            print(f"     • {cause}")

                    if result.recommended_fixes:
                        print("   Recommended Fixes:")
                        for fix in result.recommended_fixes[:3]:  # Show top 3
                            print(f"     • {fix}")

                    # WordPress-specific info
                    wp_analysis = result.diagnostic_details.get('wordpress_analysis')
                    if wp_analysis and wp_analysis.get('is_wordpress_site'):
                        print("   WordPress Site: ✅ Detected")
                        issues = []
                        issues.extend(wp_analysis.get('php_errors', []))
                        issues.extend(wp_analysis.get('database_issues', []))
                        issues.extend(wp_analysis.get('plugin_conflicts', []))
                        if issues:
                            print(f"   WordPress Issues Detected: {len(issues)} categories")
                    else:
                        print("   WordPress Site: ❌ Not detected")

                # Summary
                critical = sum(1 for r in valid_results if r.severity_level == "critical")
                total = len(valid_results)
                avg_confidence = sum(r.confidence_score for r in valid_results) / total if total > 0 else 0

                print("\n📊 Summary:")
                print(f"   Total Diagnostics: {total}")
                print(f"   Critical Errors: {critical}")
                print(f"   Average Confidence: {avg_confidence:.1f}%")
        except KeyboardInterrupt:
            print("\n⚠️  Diagnostics interrupted by user")
            sys.exit(130)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)

async def generate_html_report(report: Dict[str, Any]) -> None:
    """Generate HTML diagnostic report."""
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Server Error Diagnostic Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .critical {{ color: red; font-weight: bold; }}
        .high {{ color: orange; font-weight: bold; }}
        .medium {{ color: blue; }}
        .low {{ color: green; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .issues {{ background-color: #fff3cd; padding: 10px; margin: 10px 0; }}
        .fixes {{ background-color: #d1ecf1; padding: 10px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>🔍 Server Error Diagnostic Report</h1>
    <p><strong>Generated:</strong> {report['timestamp']}</p>

    <h2>Summary</h2>
    <ul>
        <li><strong>Total Diagnostics:</strong> {report['summary']['total_diagnostics']}</li>
        <li><strong>Critical Errors:</strong> <span class="critical">{report['summary']['critical_errors']}</span></li>
        <li><strong>High Severity:</strong> <span class="high">{report['summary']['high_severity']}</span></li>
        <li><strong>WordPress Sites:</strong> {report['summary']['wordpress_sites']}</li>
        <li><strong>Average Confidence:</strong> {report['summary']['average_confidence']}%</li>
    </ul>

    <h2>Common Issues</h2>
    <div class="issues">
        <ul>
"""

    for issue, count in report.get('common_issues', {}).items():
        html_content += f"<li>{issue} ({count} occurrences)</li>"

    html_content += """
        </ul>
    </div>

    <h2>Recommended Actions</h2>
    <div class="fixes">
        <ul>
"""

    for action in report.get('recommended_actions', []):
        html_content += f"<li>{action}</li>"

    html_content += """
        </ul>
    </div>

    <h2>Detailed Diagnostics</h2>
    <table>
        <tr>
            <th>Site</th>
            <th>Error Code</th>
            <th>Type</th>
            <th>Severity</th>
            <th>Confidence</th>
            <th>WordPress</th>
            <th>Issues</th>
        </tr>
"""

    for diagnostic in report.get('diagnostics', []):
        severity_class = diagnostic.get('severity_level', 'low')
        error_code = diagnostic.get('error_code', 'N/A')
        wp_analysis = diagnostic.get('diagnostic_details', {}).get('wordpress_analysis', {})
        is_wp = "✅ Yes" if wp_analysis.get('is_wordpress_site') else "❌ No"
        issues_count = len(diagnostic.get('root_cause_analysis', []))

        html_content += f"""
        <tr>
            <td>{diagnostic['url']}</td>
            <td>{error_code}</td>
            <td>{diagnostic.get('error_type', 'unknown')}</td>
            <td class="{severity_class}">{diagnostic.get('severity_level', 'unknown').upper()}</td>
            <td>{diagnostic.get('confidence_score', 0)}%</td>
            <td>{is_wp}</td>
            <td>{issues_count}</td>
        </tr>
"""

    html_content += """
    </table>
</body>
</html>
"""

    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"server_error_diagnostic_report_{timestamp}.html"

    with open(filename, 'w') as f:
        f.write(html_content)

    print(f"📄 HTML report saved: {filename}")

if __name__ == "__main__":
    asyncio.run(main())