#!/usr/bin/env python3
"""
Runtime Error Integration Tester
Validates Phase 3 runtime error fixes across swarm ecosystem

Usage:
    python tools/runtime_error_integration_tester.py --test-site dadudekc.com
    python tools/runtime_error_integration_tester.py --test-all
    python tools/runtime_error_integration_tester.py --validate-ga4
"""

import argparse
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional


class RuntimeErrorIntegrationTester:
    """Integration testing framework for Phase 3 runtime errors"""

    def __init__(self):
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]
        self.results = {}

    def test_site_availability(self, site: str) -> Dict:
        """Test basic site availability and catch 500 errors"""
        result = {
            "site": site,
            "timestamp": datetime.now().isoformat(),
            "status": "UNKNOWN",
            "response_code": None,
            "error": None,
            "response_time": None
        }

        try:
            start_time = time.time()
            response = requests.get(f"https://{site}", timeout=10)
            end_time = time.time()

            result["response_code"] = response.status_code
            result["response_time"] = round(end_time - start_time, 2)

            if response.status_code == 200:
                result["status"] = "SUCCESS"
            elif response.status_code == 500:
                result["status"] = "CRITICAL_ERROR"
                result["error"] = "500 Internal Server Error"
            else:
                result["status"] = f"HTTP_{response.status_code}"

        except requests.exceptions.RequestException as e:
            result["status"] = "CONNECTION_ERROR"
            result["error"] = str(e)

        return result

    def validate_ga4_pixel_config(self, site: str) -> Dict:
        """Validate GA4 and Facebook Pixel configuration"""
        result = {
            "site": site,
            "timestamp": datetime.now().isoformat(),
            "ga4_configured": False,
            "pixel_configured": False,
            "live_tracking": False,
            "issues": []
        }

        try:
            response = requests.get(f"https://{site}", timeout=10)

            if response.status_code == 200:
                content = response.text.lower()

                # Check for GA4 (Google Analytics 4)
                if "gtag(" in content or "ga(" in content or "googletagmanager.com" in content:
                    result["ga4_configured"] = True

                # Check for Facebook Pixel
                if "facebook" in content and "pixel" in content:
                    result["pixel_configured"] = True

                # Check for live tracking capability
                if result["ga4_configured"] or result["pixel_configured"]:
                    result["live_tracking"] = True
                else:
                    result["issues"].append("No analytics tracking detected")

            else:
                result["issues"].append(f"Site returned HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            result["issues"].append(f"Connection error: {str(e)}")

        return result

    def run_integration_test(self, site: Optional[str] = None) -> Dict:
        """Run complete integration test suite"""
        sites_to_test = [site] if site else self.p0_sites
        results = {
            "test_run": datetime.now().isoformat(),
            "sites_tested": len(sites_to_test),
            "availability_results": [],
            "analytics_results": [],
            "summary": {
                "total_sites": len(sites_to_test),
                "available_sites": 0,
                "error_sites": 0,
                "ga4_configured": 0,
                "pixel_configured": 0
            }
        }

        for test_site in sites_to_test:
            # Test site availability
            avail_result = self.test_site_availability(test_site)
            results["availability_results"].append(avail_result)

            if avail_result["status"] == "SUCCESS":
                results["summary"]["available_sites"] += 1
            elif avail_result["status"] == "CRITICAL_ERROR":
                results["summary"]["error_sites"] += 1

            # Test analytics configuration
            analytics_result = self.validate_ga4_pixel_config(test_site)
            results["analytics_results"].append(analytics_result)

            if analytics_result["ga4_configured"]:
                results["summary"]["ga4_configured"] += 1
            if analytics_result["pixel_configured"]:
                results["summary"]["pixel_configured"] += 1

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable test report"""
        report = f"""# Runtime Error Integration Test Report
**Generated:** {results['test_run']}
**Sites Tested:** {results['sites_tested']}

## Executive Summary
- **Available Sites:** {results['summary']['available_sites']}/{results['summary']['total_sites']}
- **Error Sites:** {results['summary']['error_sites']}/{results['summary']['total_sites']}
- **GA4 Configured:** {results['summary']['ga4_configured']}/{results['summary']['total_sites']}
- **Pixel Configured:** {results['summary']['pixel_configured']}/{results['summary']['total_sites']}

## Site Availability Results
"""

        for result in results["availability_results"]:
            status_icon = "✅" if result["status"] == "SUCCESS" else "🔴" if result["status"] == "CRITICAL_ERROR" else "⚠️"
            report += f"### {result['site']}\n"
            report += f"**Status:** {status_icon} {result['status']}\n"
            if result["response_code"]:
                report += f"**Response Code:** {result['response_code']}\n"
            if result["response_time"]:
                report += f"**Response Time:** {result['response_time']}s\n"
            if result["error"]:
                report += f"**Error:** {result['error']}\n"
            report += "\n"

        report += "## Analytics Configuration Results\n"

        for result in results["analytics_results"]:
            ga4_status = "✅" if result["ga4_configured"] else "❌"
            pixel_status = "✅" if result["pixel_configured"] else "❌"
            report += f"### {result['site']}\n"
            report += f"**GA4:** {ga4_status} {'Configured' if result['ga4_configured'] else 'Not Set'}\n"
            report += f"**Facebook Pixel:** {pixel_status} {'Configured' if result['pixel_configured'] else 'Not Set'}\n"
            if result["issues"]:
                report += "**Issues:**\n"
                for issue in result["issues"]:
                    report += f"- {issue}\n"
            report += "\n"

        return report


def main():
    parser = argparse.ArgumentParser(description="Runtime Error Integration Tester")
    parser.add_argument("--test-site", help="Test specific site")
    parser.add_argument("--test-all", action="store_true", help="Test all P0 sites")
    parser.add_argument("--validate-ga4", action="store_true", help="Focus on GA4/Pixel validation")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    tester = RuntimeErrorIntegrationTester()

    if args.test_site:
        results = tester.run_integration_test(args.test_site)
    elif args.test_all or args.validate_ga4:
        results = tester.run_integration_test()
    else:
        print("Use --test-site SITE, --test-all, or --validate-ga4")
        return

    report = tester.generate_report(results)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()