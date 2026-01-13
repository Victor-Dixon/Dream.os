#!/usr/bin/env python3
"""
🎯 ANALYTICS SITE HEALTH CHECKER CLI
====================================

A command-line tool for automated analytics validation across multiple sites.
Performs comprehensive health checks including server status, configuration
presence, and tracking code deployment verification.

Author: Agent-4 (AI Integration & Swarm Coordination Specialist)
Created: 2026-01-13
Purpose: Demonstrate swarm force multiplication through CLI tool development

Usage:
    python tools/analytics_site_health_checker.py --all-sites
    python tools/analytics_site_health_checker.py --site freerideinvestor.com
    python tools/analytics_site_health_checker.py --export-json results.json
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnalyticsSiteHealthChecker:
    """
    Comprehensive analytics site health checker for TradingRobotPlug ecosystem.
    """

    def __init__(self):
        self.sites = [
            "https://tradingrobotplug.com",
            "https://freerideinvestor.com",
            "https://dadudekc.com",
            "https://crosbyultimateevents.com"
        ]

        self.timeout = 30  # seconds
        self.user_agent = "TradingRobotPlug Analytics Health Checker/1.0"

        # Expected GA4 and Facebook Pixel patterns
        self.ga4_patterns = [
            r"GA_MEASUREMENT_ID",
            r"GTAG",
            r"googletagmanager.com/gtag/js"
        ]

        self.pixel_patterns = [
            r"FACEBOOK_PIXEL_ID",
            r"fbq\(",
            r"connect.facebook.net"
        ]

        # Security check patterns
        self.security_headers = [
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "Referrer-Policy"
        ]

        self.vulnerable_patterns = [
            r"<script[^>]*src\s*=\s*[\"'][^\"']*[\"'][^>]*>",
            r"eval\s*\(",
            r"document\.write\s*\(",
            r"innerHTML\s*=\s*",
            r"outerHTML\s*=\s*"
        ]

    def check_server_health(self, url: str) -> Tuple[bool, str, int]:
        """
        Check basic server health and response.

        Returns:
            Tuple of (is_healthy, status_message, response_time_ms)
        """
        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, timeout=self.timeout, headers=headers)

            if response.status_code == 200:
                return True, "OK", response.elapsed.total_seconds() * 1000
            else:
                return False, f"HTTP {response.status_code}", response.elapsed.total_seconds() * 1000

        except requests.exceptions.RequestException as e:
            return False, f"Connection Error: {str(e)}", 0

    def check_tracking_codes(self, url: str) -> Tuple[bool, bool, str]:
        """
        Check for GA4 and Facebook Pixel tracking codes in page source.

        Returns:
            Tuple of (has_ga4, has_pixel, details)
        """
        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, timeout=self.timeout, headers=headers)

            if response.status_code != 200:
                return False, False, f"Cannot check tracking codes - HTTP {response.status_code}"

            soup = BeautifulSoup(response.text, 'html.parser')

            # Check for GA4
            ga4_found = False
            ga4_details = []

            # Check script tags for GA4
            for script in soup.find_all('script'):
                script_content = script.get('src', '') + script.get_text()
                for pattern in self.ga4_patterns:
                    if pattern.lower() in script_content.lower():
                        ga4_found = True
                        ga4_details.append(f"Found: {pattern}")
                        break

            # Check for Facebook Pixel
            pixel_found = False
            pixel_details = []

            # Check script tags for Pixel
            for script in soup.find_all('script'):
                script_content = script.get('src', '') + script.get_text()
                for pattern in self.pixel_patterns:
                    if pattern.lower() in script_content.lower():
                        pixel_found = True
                        pixel_details.append(f"Found: {pattern}")
                        break

            details = []
            if ga4_found:
                details.append(f"GA4: {', '.join(ga4_details)}")
            else:
                details.append("GA4: Not found")

            if pixel_found:
                details.append(f"Pixel: {', '.join(pixel_details)}")
            else:
                details.append("Pixel: Not found")

            return ga4_found, pixel_found, "; ".join(details)

        except Exception as e:
            return False, False, f"Error checking tracking codes: {str(e)}"

    def check_analytics_api(self, base_url: str) -> Tuple[bool, str]:
        """
        Check analytics API endpoints availability.

        Returns:
            Tuple of (api_available, details)
        """
        endpoints = [
            "/wp-json/tradingrobotplug/v1/analytics/performance",
            "/wp-json/tradingrobotplug/v1/analytics/events",
            "/wp-json/tradingrobotplug/v1/analytics/dashboard"
        ]

        results = []
        all_available = True

        for endpoint in endpoints:
            try:
                url = urljoin(base_url, endpoint)
                headers = {"User-Agent": self.user_agent}
                response = requests.get(url, timeout=self.timeout, headers=headers)

                if response.status_code == 200:
                    results.append(f"✅ {endpoint}: OK")
                else:
                    results.append(f"❌ {endpoint}: HTTP {response.status_code}")
                    all_available = False

            except requests.exceptions.RequestException as e:
                results.append(f"❌ {endpoint}: Connection failed")
                all_available = False

        return all_available, "\n".join(results)

    def check_security_headers(self, url: str) -> Tuple[int, str]:
        """
        Check for security headers in HTTP response.

        Returns:
            Tuple of (security_score, details)
        """
        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.head(url, timeout=self.timeout, headers=headers)

            present_headers = []
            missing_headers = []

            for header in self.security_headers:
                if header in response.headers:
                    present_headers.append(f"✅ {header}: {response.headers[header]}")
                else:
                    missing_headers.append(f"❌ {header}: Missing")

            security_score = len(present_headers) * 10  # 10 points per header (max 60)

            details = []
            if present_headers:
                details.append("Present Security Headers:")
                details.extend(present_headers)
            if missing_headers:
                details.append("\nMissing Security Headers:")
                details.extend(missing_headers)

            return security_score, "\n".join(details)

        except Exception as e:
            return 0, f"Security header check failed: {str(e)}"

    def check_vulnerable_content(self, url: str) -> Tuple[int, str]:
        """
        Check for potentially vulnerable content patterns.

        Returns:
            Tuple of (vulnerability_score, details)
        """
        try:
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, timeout=self.timeout, headers=headers)

            if response.status_code != 200:
                return 0, f"Cannot check content - HTTP {response.status_code}"

            content = response.text.lower()
            vulnerabilities = []

            for pattern in self.vulnerable_patterns:
                if pattern.lower() in content:
                    vulnerabilities.append(f"⚠️  Potential vulnerability: {pattern}")

            # Score: 20 points if no vulnerabilities found, 0 if found
            vulnerability_score = 20 if not vulnerabilities else 0

            if vulnerabilities:
                details = "Potential Security Issues Found:\n" + "\n".join(vulnerabilities)
            else:
                details = "✅ No obvious security vulnerabilities detected in content"

            return vulnerability_score, details

        except Exception as e:
            return 0, f"Content security check failed: {str(e)}"

    def check_https_enforcement(self, url: str) -> Tuple[int, str]:
        """
        Check if HTTPS is properly enforced.

        Returns:
            Tuple of (https_score, details)
        """
        try:
            https_score = 0
            details = []

            # Check if URL already uses HTTPS
            if url.startswith("https://"):
                https_score += 20
                details.append("✅ URL uses HTTPS")

                # Check for HSTS header
                headers = {"User-Agent": self.user_agent}
                response = requests.head(url, timeout=self.timeout, headers=headers)

                if "Strict-Transport-Security" in response.headers:
                    https_score += 10
                    details.append("✅ HSTS header present")
                else:
                    details.append("⚠️  HSTS header missing")

            else:
                details.append("❌ URL does not use HTTPS")

            return https_score, "; ".join(details)

        except Exception as e:
            return 0, f"HTTPS check failed: {str(e)}"

    def check_site_comprehensive(self, url: str) -> Dict:
        """
        Perform comprehensive health check for a single site.

        Returns:
            Dictionary with all health check results
        """
        logger.info(f"🔍 Checking {url}...")

        # Server health
        server_healthy, server_status, response_time = self.check_server_health(url)

        # Tracking codes
        has_ga4, has_pixel, tracking_details = self.check_tracking_codes(url)

        # API endpoints (only if server is healthy)
        if server_healthy:
            api_available, api_details = self.check_analytics_api(url)
        else:
            api_available, api_details = False, "Skipped - server unhealthy"

        # Security checks (only if server is healthy)
        if server_healthy:
            security_score, security_details = self.check_security_headers(url)
            vulnerability_score, vulnerability_details = self.check_vulnerable_content(url)
            https_score, https_details = self.check_https_enforcement(url)
        else:
            security_score, security_details = 0, "Skipped - server unhealthy"
            vulnerability_score, vulnerability_details = 0, "Skipped - server unhealthy"
            https_score, https_details = 0, "Skipped - server unhealthy"

        # Overall health score (extended to include security)
        health_score = 0
        if server_healthy:
            health_score += 20  # Reduced from 40 to make room for security
        if has_ga4:
            health_score += 15  # Reduced from 30
        if has_pixel:
            health_score += 10  # Reduced from 20
        if api_available:
            health_score += 5   # Reduced from 10
        health_score += security_score     # 0-60 points
        health_score += vulnerability_score # 0-20 points
        health_score += https_score         # 0-30 points

        # Determine status
        if health_score >= 80:
            status = "HEALTHY"
        elif health_score >= 60:
            status = "WARNING"
        else:
            status = "CRITICAL"

        return {
            "site": url,
            "status": status,
            "health_score": health_score,
            "server": {
                "healthy": server_healthy,
                "status": server_status,
                "response_time_ms": round(response_time, 2)
            },
            "analytics": {
                "ga4_configured": has_ga4,
                "pixel_configured": has_pixel,
                "tracking_details": tracking_details
            },
            "api": {
                "endpoints_available": api_available,
                "endpoint_details": api_details
            },
            "security": {
                "security_headers_score": security_score,
                "vulnerability_score": vulnerability_score,
                "https_score": https_score,
                "security_details": security_details,
                "vulnerability_details": vulnerability_details,
                "https_details": https_details
            },
            "recommendations": self.generate_recommendations(
                server_healthy, has_ga4, has_pixel, api_available,
                security_score, vulnerability_score, https_score
            )
        }

    def generate_recommendations(self, server_ok: bool, has_ga4: bool,
                               has_pixel: bool, api_ok: bool,
                               security_score: int, vulnerability_score: int,
                               https_score: int) -> List[str]:
        """Generate actionable recommendations based on check results."""
        recommendations = []

        if not server_ok:
            recommendations.append("🔴 CRITICAL: Fix server issues immediately - site is inaccessible")

        if not has_ga4:
            recommendations.append("🟡 HIGH: Deploy GA4 tracking code to enable analytics collection")

        if not has_pixel:
            recommendations.append("🟡 HIGH: Deploy Facebook Pixel for conversion tracking")

        if not api_ok and server_ok:
            recommendations.append("🟡 MEDIUM: Verify analytics API endpoints are properly configured")

        # Security recommendations
        if security_score < 30:
            recommendations.append("🟡 HIGH: Implement security headers (CSP, HSTS, X-Frame-Options, etc.)")

        if vulnerability_score < 20:
            recommendations.append("🟡 HIGH: Review and fix potential XSS/script injection vulnerabilities")

        if https_score < 30:
            recommendations.append("🟡 HIGH: Implement HTTPS and HSTS for secure communications")

        if server_ok and has_ga4 and has_pixel and api_ok and security_score >= 40 and vulnerability_score >= 20 and https_score >= 20:
            recommendations.append("✅ ALL SYSTEMS OPERATIONAL - Analytics and security fully functional")

        return recommendations

    def check_all_sites(self) -> List[Dict]:
        """Check health of all configured sites."""
        results = []

        for site in self.sites:
            try:
                result = self.check_site_comprehensive(site)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to check {site}: {str(e)}")
                results.append({
                    "site": site,
                    "status": "ERROR",
                    "health_score": 0,
                    "error": str(e)
                })

        return results

    def export_results(self, results: List[Dict], format: str = "json",
                      filename: Optional[str] = None) -> None:
        """Export results in specified format."""
        if format == "json":
            if not filename:
                filename = f"analytics_health_check_{int(__import__('time').time())}.json"

            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)

            logger.info(f"📄 Results exported to {filename}")

        elif format == "text":
            if not filename:
                filename = f"analytics_health_check_{int(__import__('time').time())}.txt"

            with open(filename, 'w') as f:
                f.write("🎯 Analytics Site Health Check Report\n")
                f.write("=" * 50 + "\n\n")

                for result in results:
                    f.write(f"Site: {result['site']}\n")
                    f.write(f"Status: {result['status']} ({result['health_score']}/100)\n")

                    if 'server' in result:
                        f.write(f"Server: {result['server']['status']} "
                               f"({result['server']['response_time_ms']}ms)\n")

                    if 'analytics' in result:
                        f.write(f"GA4: {'✅' if result['analytics']['ga4_configured'] else '❌'} | ")
                        f.write(f"Pixel: {'✅' if result['analytics']['pixel_configured'] else '❌'}\n")

                    if 'security' in result:
                        sec_score = result['security']['security_headers_score']
                        vuln_score = result['security']['vulnerability_score']
                        https_score = result['security']['https_score']
                        f.write(f"Security: Headers {sec_score}/60 | Vulnerabilities {vuln_score}/20 | HTTPS {https_score}/30\n")

                    if 'recommendations' in result:
                        f.write("Recommendations:\n")
                        for rec in result['recommendations']:
                            f.write(f"  • {rec}\n")

                    f.write("-" * 30 + "\n")

            logger.info(f"📄 Results exported to {filename}")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analytics Site Health Checker - Automated validation for TradingRobotPlug ecosystem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/analytics_site_health_checker.py --all-sites
  python tools/analytics_site_health_checker.py --site https://tradingrobotplug.com
  python tools/analytics_site_health_checker.py --all-sites --export-json results.json
  python tools/analytics_site_health_checker.py --all-sites --export-text report.txt
        """
    )

    parser.add_argument(
        "--all-sites",
        action="store_true",
        help="Check all configured sites"
    )

    parser.add_argument(
        "--site",
        type=str,
        help="Check specific site URL"
    )

    parser.add_argument(
        "--export-json",
        type=str,
        metavar="FILENAME",
        help="Export results to JSON file"
    )

    parser.add_argument(
        "--export-text",
        type=str,
        metavar="FILENAME",
        help="Export results to text file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    checker = AnalyticsSiteHealthChecker()

    if args.site:
        # Check single site
        result = checker.check_site_comprehensive(args.site)
        results = [result]

    elif args.all_sites:
        # Check all sites
        results = checker.check_all_sites()

    else:
        parser.print_help()
        return 1

    # Display results
    print("\n🎯 Analytics Site Health Check Results")
    print("=" * 50)

    for result in results:
        print(f"\n📊 {result['site']}")
        print(f"   Status: {result['status']} ({result['health_score']}/100)")

        if 'server' in result:
            status_emoji = "✅" if result['server']['healthy'] else "❌"
            print(f"   Server: {status_emoji} {result['server']['status']} "
                  f"({result['server']['response_time_ms']}ms)")

        if 'analytics' in result:
            ga4_emoji = "✅" if result['analytics']['ga4_configured'] else "❌"
            pixel_emoji = "✅" if result['analytics']['pixel_configured'] else "❌"
            print(f"   Analytics: GA4 {ga4_emoji} | Pixel {pixel_emoji}")
            print(f"   Details: {result['analytics']['tracking_details']}")

        if 'api' in result:
            api_emoji = "✅" if result['api']['endpoints_available'] else "❌"
            print(f"   API: {api_emoji} Endpoints available")

        if 'security' in result:
            sec_score = result['security']['security_headers_score']
            vuln_score = result['security']['vulnerability_score']
            https_score = result['security']['https_score']
            total_sec = sec_score + vuln_score + https_score
            sec_emoji = "✅" if total_sec >= 80 else "⚠️" if total_sec >= 60 else "❌"
            print(f"   Security: {sec_emoji} Headers: {sec_score}/60 | Vuln: {vuln_score}/20 | HTTPS: {https_score}/30")

        if 'recommendations' in result:
            print("   📋 Recommendations:")
            for rec in result['recommendations']:
                print(f"      • {rec}")

    # Export if requested
    if args.export_json:
        checker.export_results(results, "json", args.export_json)

    if args.export_text:
        checker.export_results(results, "text", args.export_text)

    # Summary
    healthy_sites = sum(1 for r in results if r.get('status') == 'HEALTHY')
    warning_sites = sum(1 for r in results if r.get('status') == 'WARNING')
    critical_sites = sum(1 for r in results if r.get('status') == 'CRITICAL')

    print("\n📈 Summary:")
    print(f"   ✅ Healthy: {healthy_sites}")
    print(f"   ⚠️  Warning: {warning_sites}")
    print(f"   🔴 Critical: {critical_sites}")
    print(f"   📊 Total Sites: {len(results)}")

    return 0

if __name__ == "__main__":
    sys.exit(main())