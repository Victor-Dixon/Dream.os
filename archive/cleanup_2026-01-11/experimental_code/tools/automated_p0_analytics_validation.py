#!/usr/bin/env python3
"""
Automated P0 Analytics Validation Tool
======================================

Validates GA4 and Facebook Pixel configuration for all P0 sites.

Usage:
    python tools/automated_p0_analytics_validation.py --validate-ready
    python tools/automated_p0_analytics_validation.py --generate-report
    python tools/automated_p0_analytics_validation.py --validate-site freerideinvestor.com

<!-- SSOT Domain: analytics -->
"""

import argparse
import json
import os
import re
import requests
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AnalyticsValidation:
    """Analytics validation result for a site"""

    def __init__(self, site: str, accessible: bool, ga4_configured: bool,
                 pixel_configured: bool, issues: List[str] = None):
        self.site = site
        self.accessible = accessible
        self.ga4_configured = ga4_configured
        self.pixel_configured = pixel_configured
        self.issues = issues or []
        self.timestamp = datetime.now()

    @property
    def fully_configured(self) -> bool:
        """Whether both GA4 and Pixel are properly configured"""
        return self.ga4_configured and self.pixel_configured

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "site": self.site,
            "timestamp": self.timestamp.isoformat(),
            "accessible": self.accessible,
            "ga4_configured": self.ga4_configured,
            "pixel_configured": self.pixel_configured,
            "fully_configured": self.fully_configured,
            "issues": self.issues
        }

    def __str__(self) -> str:
        status = "✅ READY" if self.fully_configured and self.accessible else "❌ NOT READY"
        return f"{self.site}: {status}"


class AutomatedP0AnalyticsValidator:
    """Validates analytics configuration for P0 sites"""

    def __init__(self):
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]

        # Placeholder patterns to detect (these indicate missing real IDs)
        self.placeholder_patterns = [
            "G-XXXXXXXXXX",
            "G-XYZ789GHI5",
            "G-ABC123DEF4",
            "000000000000000",
            "876543210987654",
            "987654321098765",
            "123456789012345"
        ]

    def check_site_accessibility(self, site: str) -> Tuple[bool, str]:
        """
        Check if site is accessible and get basic health info.

        Returns:
            Tuple of (is_accessible, status_message)
        """
        try:
            url = f"https://{site}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                return True, f"HTTP {response.status_code} - OK"
            elif response.status_code == 500:
                return False, f"HTTP {response.status_code} - Server Error"
            else:
                return True, f"HTTP {response.status_code} - Accessible"

        except requests.exceptions.RequestException as e:
            return False, f"Connection failed: {str(e)}"

    def check_wp_config_analytics(self, site: str) -> Tuple[bool, bool, List[str]]:
        """
        Check wp-config.php for GA4 and Facebook Pixel configuration.

        Returns:
            Tuple of (ga4_configured, pixel_configured, issues)
        """
        issues = []

        # Check local config file if it exists
        config_paths = [
            Path(f"sites/{site}/wp-config.php"),
            Path(f"sites/{site}/wp/wp-config.php")
        ]

        config_found = False
        for config_path in config_paths:
            if config_path.exists():
                config_found = True
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for GA4 constant
                    ga4_match = re.search(r"define\s*\(\s*['\"]GA4_MEASUREMENT_ID['\"]\s*,\s*['\"]([^'\"]+)['\"]", content, re.IGNORECASE)
                    ga4_id = ga4_match.group(1) if ga4_match else None

                    # Check for Facebook Pixel constant
                    pixel_match = re.search(r"define\s*\(\s*['\"]FACEBOOK_PIXEL_ID['\"]\s*,\s*['\"]([^'\"]+)['\"]", content, re.IGNORECASE)
                    pixel_id = pixel_match.group(1) if pixel_match else None

                    # Validate GA4 ID
                    ga4_configured = False
                    if ga4_id:
                        if any(pattern in ga4_id for pattern in self.placeholder_patterns):
                            issues.append(f"GA4 ID is placeholder: {ga4_id}")
                        elif ga4_id.startswith('G-') and len(ga4_id) > 5:
                            ga4_configured = True
                        else:
                            issues.append(f"GA4 ID format invalid: {ga4_id}")
                    else:
                        issues.append("GA4_MEASUREMENT_ID constant not defined")

                    # Validate Pixel ID
                    pixel_configured = False
                    if pixel_id:
                        if any(pattern in pixel_id for pattern in self.placeholder_patterns):
                            issues.append(f"Facebook Pixel ID is placeholder: {pixel_id}")
                        elif pixel_id.isdigit() and len(pixel_id) >= 15:
                            pixel_configured = True
                        else:
                            issues.append(f"Facebook Pixel ID format invalid: {pixel_id}")
                    else:
                        issues.append("FACEBOOK_PIXEL_ID constant not defined")

                    return ga4_configured, pixel_configured, issues

                except Exception as e:
                    issues.append(f"Error reading config file: {str(e)}")
                    return False, False, issues

        if not config_found:
            issues.append("wp-config.php not found in expected locations")
            return False, False, issues

    def validate_site(self, site: str) -> AnalyticsValidation:
        """Validate analytics configuration for a single site"""
        # Check accessibility
        accessible, access_message = self.check_site_accessibility(site)

        if not accessible:
            return AnalyticsValidation(
                site=site,
                accessible=False,
                ga4_configured=False,
                pixel_configured=False,
                issues=[access_message]
            )

        # Check configuration
        ga4_configured, pixel_configured, config_issues = self.check_wp_config_analytics(site)

        all_issues = config_issues

        return AnalyticsValidation(
            site=site,
            accessible=accessible,
            ga4_configured=ga4_configured,
            pixel_configured=pixel_configured,
            issues=all_issues
        )

    def validate_all_sites(self) -> List[AnalyticsValidation]:
        """Validate analytics configuration for all P0 sites"""
        results = []
        for site in self.p0_sites:
            print(f"🔍 Validating {site}...")
            result = self.validate_site(site)
            results.append(result)
            print(f"   {result}")

        return results

    def generate_report(self, results: List[AnalyticsValidation]) -> str:
        """Generate a comprehensive validation report"""
        total_sites = len(results)
        accessible_sites = sum(1 for r in results if r.accessible)
        ga4_configured = sum(1 for r in results if r.ga4_configured)
        pixel_configured = sum(1 for r in results if r.pixel_configured)
        fully_configured = sum(1 for r in results if r.fully_configured and r.accessible)

        report = f"""# P0 Analytics Validation Report
**Generated:** {datetime.now().isoformat()}
**Agent:** Agent-5 (Business Intelligence)

## Executive Summary
- **Sites Tested:** {total_sites}
- **Sites Accessible:** {accessible_sites}/{total_sites}
- **GA4 Configured:** {ga4_configured}/{total_sites}
- **Pixel Configured:** {pixel_configured}/{total_sites}
- **Fully Configured:** {fully_configured}/{total_sites}

## Site-by-Site Results

"""

        for result in results:
            status_emoji = "✅" if result.fully_configured and result.accessible else "❌"
            status_text = 'READY' if result.fully_configured and result.accessible else 'NOT READY'
            report += f"""### {result.site}
**Status:** {status_emoji} {status_text}
- **Accessible:** {'✅' if result.accessible else '❌'}
- **GA4 Configured:** {'✅' if result.ga4_configured else '❌'}
- **Pixel Configured:** {'✅' if result.pixel_configured else '❌'}

"""

            if result.issues:
                report += "**Issues:**\n"
                for issue in result.issues:
                    report += f"- {issue}\n"
            else:
                report += "**No issues detected**\n"

            report += "\n"

        # Recommendations
        report += "## Recommendations\n\n"

        if fully_configured == total_sites:
            report += "🎉 **All sites are fully configured and ready for analytics validation!**\n\n"
            report += "Next steps:\n"
            report += "1. Run live analytics verification tests\n"
            report += "2. Monitor GA4 real-time reports\n"
            report += "3. Verify Facebook Pixel events\n"
        else:
            report += "⚠️ **Configuration issues detected. Action required:**\n\n"

            sites_needing_ga4 = [r.site for r in results if not r.ga4_configured]
            sites_needing_pixel = [r.site for r in results if not r.pixel_configured]
            inaccessible_sites = [r.site for r in results if not r.accessible]

            if inaccessible_sites:
                report += f"**Sites with accessibility issues:** {', '.join(inaccessible_sites)}\n"
                report += "- Contact infrastructure team to resolve server issues\n\n"

            if sites_needing_ga4:
                report += f"**Sites needing GA4 configuration:** {', '.join(sites_needing_ga4)}\n"
                report += "- Deploy real GA4 Measurement IDs to wp-config.php\n\n"

            if sites_needing_pixel:
                report += f"**Sites needing Facebook Pixel configuration:** {', '.join(sites_needing_pixel)}\n"
                report += "- Deploy real Facebook Pixel IDs to wp-config.php\n\n"

            report += "Once configurations are deployed, re-run this validation.\n"

        return report

    def save_report(self, report: str, filename: Optional[str] = None) -> str:
        """Save report to file and return the filename"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/consolidated/analytics/p0_analytics_validation_{timestamp}.md"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)

        return filename


def main():
    parser = argparse.ArgumentParser(description="Automated P0 Analytics Validation Tool")
    parser.add_argument("--validate-ready", action="store_true",
                       help="Validate all P0 sites and show readiness status")
    parser.add_argument("--generate-report", action="store_true",
                       help="Generate and save comprehensive validation report")
    parser.add_argument("--validate-site", type=str,
                       help="Validate a specific site")
    parser.add_argument("--output", type=str,
                       help="Output file for report (default: auto-generated)")

    args = parser.parse_args()

    if not any([args.validate_ready, args.generate_report, args.validate_site]):
        print("❌ ERROR: Must specify --validate-ready, --generate-report, or --validate-site")
        sys.exit(1)

    validator = AutomatedP0AnalyticsValidator()

    if args.validate_site:
        print(f"🔍 Validating {args.validate_site}...")
        result = validator.validate_site(args.validate_site)
        print(f"   {result}")
        if result.issues:
            print("   Issues:")
            for issue in result.issues:
                print(f"   - {issue}")

    elif args.validate_ready or args.generate_report:
        results = validator.validate_all_sites()

        if args.generate_report:
            report = validator.generate_report(results)
            filename = validator.save_report(report, args.output)
            print(f"\n📄 Report saved to: {filename}")

            # Also print summary to console
            fully_configured = sum(1 for r in results if r.fully_configured and r.accessible)
            total_sites = len(results)
            print(f"\n📊 Summary: {fully_configured}/{total_sites} sites fully configured")

            if fully_configured == total_sites:
                print("🎉 All P0 sites are ready for analytics validation!")
            else:
                print("⚠️ Some sites need configuration before analytics validation can proceed.")


if __name__ == "__main__":
    main()