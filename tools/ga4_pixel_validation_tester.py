#!/usr/bin/env python3
"""
GA4/Pixel Configuration Validation Tester
Validates GA4 and Facebook Pixel configuration across P0 sites post-deployment

Usage:
    python tools/ga4_pixel_validation_tester.py --validate-all
    python tools/ga4_pixel_validation_tester.py --validate-site freerideinvestor.com
    python tools/ga4_pixel_validation_tester.py --test-configuration
"""

import argparse
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional


class GA4PixelValidationTester:
    """Validates GA4 and Facebook Pixel configuration across P0 sites"""

    def __init__(self):
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]

        # Known GA4 test measurement IDs (for validation testing)
        self.test_ga4_ids = [
            "G-XXXXXXXXXX",  # Placeholder for actual IDs
            "G-TEST123456",  # Test ID for validation
        ]

        # Known Facebook Pixel test IDs (for validation testing)
        self.test_pixel_ids = [
            "123456789012345",  # Placeholder for actual IDs
            "987654321098765",  # Test ID for validation
        ]

    def validate_ga4_pixel_config(self, site: str) -> Dict:
        """Comprehensive validation of GA4 and Facebook Pixel configuration"""
        result = {
            "site": site,
            "timestamp": datetime.now().isoformat(),
            "site_accessible": False,
            "ga4_detected": False,
            "pixel_detected": False,
            "ga4_measurement_id": None,
            "pixel_id": None,
            "live_tracking": False,
            "configuration_score": 0,
            "issues": [],
            "recommendations": []
        }

        try:
            # Test site accessibility
            response = requests.get(f"https://{site}", timeout=15)
            result["site_accessible"] = response.status_code == 200

            if not result["site_accessible"]:
                result["issues"].append(f"Site returned HTTP {response.status_code}")
                return result

            content = response.text.lower()

            # Check for GA4 (Google Analytics 4)
            ga4_patterns = [
                "gtag(", "gtag('config'", "googletagmanager.com/gtag",
                "google-analytics.com/analytics.js", "ga(", "analytics.js"
            ]

            for pattern in ga4_patterns:
                if pattern in content:
                    result["ga4_detected"] = True
                    break

            # Extract GA4 Measurement ID if possible
            import re
            ga4_id_match = re.search(r'G-([A-Z0-9]{10,})', content, re.IGNORECASE)
            if ga4_id_match:
                result["ga4_measurement_id"] = ga4_id_match.group(0)

            # Check for Facebook Pixel
            pixel_patterns = [
                "facebook.com/tr", "connect.facebook.net/en_US/fbevents.js",
                "fbq(", "facebook pixel", "pixel_id"
            ]

            for pattern in pixel_patterns:
                if pattern in content:
                    result["pixel_detected"] = True
                    break

            # Extract Facebook Pixel ID if possible
            pixel_id_match = re.search(r'(\d{15,})', content)
            if pixel_id_match and len(pixel_id_match.group(1)) >= 15:
                result["pixel_id"] = pixel_id_match.group(1)

            # Determine live tracking capability
            result["live_tracking"] = result["ga4_detected"] or result["pixel_detected"]

            # Calculate configuration score (0-100)
            score = 0
            if result["site_accessible"]:
                score += 30
            if result["ga4_detected"]:
                score += 35
            if result["pixel_detected"]:
                score += 35
            result["configuration_score"] = score

            # Generate recommendations
            if not result["ga4_detected"]:
                result["recommendations"].append("GA4 Measurement ID not configured in wp-config.php")
            if not result["pixel_detected"]:
                result["recommendations"].append("Facebook Pixel ID not configured in wp-config.php")
            if not result["live_tracking"]:
                result["recommendations"].append("No analytics tracking detected - configure both GA4 and Pixel")

        except requests.exceptions.RequestException as e:
            result["issues"].append(f"Connection error: {str(e)}")
        except Exception as e:
            result["issues"].append(f"Validation error: {str(e)}")

        return result

    def validate_configuration_integrity(self) -> Dict:
        """Validate that configuration changes are properly deployed"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "wp_config_files_checked": [],
            "configuration_integrity": True,
            "deployment_status": "UNKNOWN",
            "findings": []
        }

        # Check local wp-config files for GA4/Pixel configuration
        for site in self.p0_sites:
            config_path = f"sites/{site}/wp-config-analytics.php"
            try:
                with open(config_path, 'r') as f:
                    content = f.read().lower()

                has_ga4 = 'ga4' in content or 'gtag' in content
                has_pixel = 'pixel' in content or 'facebook' in content

                result["wp_config_files_checked"].append({
                    "site": site,
                    "file_exists": True,
                    "has_ga4_config": has_ga4,
                    "has_pixel_config": has_pixel
                })

                if not (has_ga4 and has_pixel):
                    result["configuration_integrity"] = False
                    result["findings"].append(f"{site}: Missing configuration in wp-config-analytics.php")

            except FileNotFoundError:
                result["wp_config_files_checked"].append({
                    "site": site,
                    "file_exists": False,
                    "has_ga4_config": False,
                    "has_pixel_config": False
                })
                result["configuration_integrity"] = False
                result["findings"].append(f"{site}: wp-config-analytics.php not found")

        # Determine deployment status
        if result["configuration_integrity"]:
            result["deployment_status"] = "READY_FOR_DEPLOYMENT"
        else:
            result["deployment_status"] = "CONFIGURATION_INCOMPLETE"

        return result

    def run_comprehensive_validation(self) -> Dict:
        """Run complete GA4/Pixel validation across all P0 sites"""
        results = {
            "validation_run": datetime.now().isoformat(),
            "sites_validated": len(self.p0_sites),
            "configuration_integrity": self.validate_configuration_integrity(),
            "site_validations": [],
            "summary": {
                "sites_accessible": 0,
                "ga4_configured": 0,
                "pixel_configured": 0,
                "fully_configured": 0,
                "average_score": 0
            }
        }

        total_score = 0

        # Validate each site
        for site in self.p0_sites:
            site_result = self.validate_ga4_pixel_config(site)
            results["site_validations"].append(site_result)

            if site_result["site_accessible"]:
                results["summary"]["sites_accessible"] += 1
            if site_result["ga4_detected"]:
                results["summary"]["ga4_configured"] += 1
            if site_result["pixel_detected"]:
                results["summary"]["pixel_configured"] += 1
            if site_result["ga4_detected"] and site_result["pixel_detected"]:
                results["summary"]["fully_configured"] += 1

            total_score += site_result["configuration_score"]

        results["summary"]["average_score"] = round(total_score / len(self.p0_sites), 1)

        return results

    def generate_report(self, results: Dict) -> str:
        """Generate human-readable validation report"""
        report = f"""# GA4/Pixel Configuration Validation Report
**Generated:** {results['validation_run']}
**Sites Validated:** {results['sites_validated']}

## Executive Summary
- **Sites Accessible:** {results['summary']['sites_accessible']}/{results['sites_validated']}
- **GA4 Configured:** {results['summary']['ga4_configured']}/{results['sites_validated']}
- **Pixel Configured:** {results['summary']['pixel_configured']}/{results['sites_validated']}
- **Fully Configured:** {results['summary']['fully_configured']}/{results['sites_validated']}
- **Average Score:** {results['summary']['average_score']}/100

## Configuration Integrity Status
- **Status:** {'✅ INTEGRITY VERIFIED' if results['configuration_integrity']['configuration_integrity'] else '⚠️ INTEGRITY ISSUES'}
- **Deployment Ready:** {'✅ READY' if results['configuration_integrity']['deployment_status'] == 'READY_FOR_DEPLOYMENT' else '❌ NEEDS ATTENTION'}

"""

        if results['configuration_integrity']['findings']:
            report += "### Configuration Issues Found\n"
            for finding in results['configuration_integrity']['findings']:
                report += f"- {finding}\n"
            report += "\n"

        report += "## Site-by-Site Validation Results\n"

        for site_result in results["site_validations"]:
            status_icon = "✅" if site_result["configuration_score"] == 100 else "⚠️" if site_result["configuration_score"] >= 30 else "❌"
            report += f"### {site_result['site']}\n"
            report += f"**Status:** {status_icon} ({site_result['configuration_score']}/100)\n"
            report += f"**Site Accessible:** {'✅' if site_result['site_accessible'] else '❌'}\n"
            report += f"**GA4 Detected:** {'✅' if site_result['ga4_detected'] else '❌'}"
            if site_result['ga4_measurement_id']:
                report += f" ({site_result['ga4_measurement_id']})"
            report += "\n"
            report += f"**Pixel Detected:** {'✅' if site_result['pixel_detected'] else '❌'}"
            if site_result['pixel_id']:
                report += f" ({site_result['pixel_id']})"
            report += "\n"
            report += f"**Live Tracking:** {'✅' if site_result['live_tracking'] else '❌'}\n"

            if site_result["issues"]:
                report += "**Issues:**\n"
                for issue in site_result["issues"]:
                    report += f"- {issue}\n"

            if site_result["recommendations"]:
                report += "**Recommendations:**\n"
                for rec in site_result["recommendations"]:
                    report += f"- {rec}\n"

            report += "\n"

        report += "## Next Steps for Agent-3\n"
        report += "1. Configure GA4 Measurement IDs in wp-config-analytics.php for unconfigured sites\n"
        report += "2. Configure Facebook Pixel IDs in wp-config-analytics.php for unconfigured sites\n"
        report += "3. Deploy configuration changes to remote sites\n"
        report += "4. Coordinate with Agent-4 for post-deployment validation\n"
        report += "5. Run this validation tool again to confirm successful deployment\n"

        return report


def main():
    parser = argparse.ArgumentParser(description="GA4/Pixel Configuration Validation Tester")
    parser.add_argument("--validate-all", action="store_true", help="Run comprehensive validation")
    parser.add_argument("--validate-site", help="Validate specific site")
    parser.add_argument("--test-configuration", action="store_true", help="Test configuration integrity only")
    parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    tester = GA4PixelValidationTester()

    if args.validate_site:
        result = tester.validate_ga4_pixel_config(args.validate_site)
        print(f"Site: {result['site']}")
        print(f"Score: {result['configuration_score']}/100")
        print(f"GA4: {'✅' if result['ga4_detected'] else '❌'}")
        print(f"Pixel: {'✅' if result['pixel_detected'] else '❌'}")
        if result['issues']:
            print("Issues:")
            for issue in result['issues']:
                print(f"  - {issue}")

    elif args.test_configuration:
        result = tester.validate_configuration_integrity()
        print("Configuration Integrity:")
        print(f"Status: {'✅' if result['configuration_integrity'] else '❌'}")
        print(f"Deployment: {result['deployment_status']}")
        if result['findings']:
            print("Findings:")
            for finding in result['findings']:
                print(f"  - {finding}")

    elif args.validate_all:
        results = tester.run_comprehensive_validation()
        report = tester.generate_report(results)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    else:
        print("Use --validate-all, --validate-site SITE, or --test-configuration")


if __name__ == "__main__":
    main()