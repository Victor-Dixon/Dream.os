#!/usr/bin/env python3
"""
Automated P0 Analytics Validation Tool
======================================

Validates GA4 and Facebook Pixel analytics configuration for P0 sites.

Usage:
    python tools/automated_p0_analytics_validation.py                    # Validate all P0 sites
    python tools/automated_p0_analytics_validation.py --validate-ready   # Validate only ready sites
    python tools/automated_p0_analytics_validation.py --site freerideinvestor.com  # Validate specific site

Features:
- Validates GA4 Measurement ID configuration
- Validates Facebook Pixel ID configuration
- Checks analytics tracking on live sites
- Generates validation reports
- Supports --validate-ready flag for sites with IDs configured

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-30
Purpose: Complete Tier 1 analytics validation for P0 sites
"""

import argparse
import json
import re
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# P0 sites to validate
P0_SITES = [
    "freerideinvestor.com",
    "tradingrobotplug.com",
    "dadudekc.com",
    "crosbyultimateevents.com"
]


@dataclass
class AnalyticsValidation:
    """Analytics validation result for a site."""
    site_name: str
    ga4_configured: bool
    ga4_measurement_id: Optional[str]
    pixel_configured: bool
    pixel_id: Optional[str]
    tracking_verified: bool
    issues: List[str]
    status: str  # "ready", "configured", "missing", "error"


class AutomatedP0AnalyticsValidator:
    """Validates analytics configuration for P0 sites."""

    def __init__(self):
        """Initialize the validator."""
        self.sites_dir = Path("../../websites")
        self.sites = P0_SITES

    def check_wp_config(self, site_name: str) -> Dict[str, Optional[str]]:
        """Check wp-config-analytics.php for analytics constants (local or remote)."""
        # Try local config first
        config_path = self.sites_dir / site_name / "wp-config-analytics.php"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                constants = {}
                patterns = {
                    'GA4_MEASUREMENT_ID': r'define\s*\(\s*[\'"]GA4_MEASUREMENT_ID[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                    'FACEBOOK_PIXEL_ID': r'define\s*\(\s*[\'"]FACEBOOK_PIXEL_ID[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                }

                for const_name, pattern in patterns.items():
                    match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                    if match:
                        constants[const_name] = match.group(1)
                    else:
                        constants[const_name] = None

                return constants

            except Exception as e:
                return {
                    'GA4_MEASUREMENT_ID': None,
                    'FACEBOOK_PIXEL_ID': None,
                    'error': str(e)
                }
        
        # If local config not found, check live site for tracking codes
        # This validates that IDs are configured and tracking
        try:
            url = f"https://{site_name}"
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            content = response.text

            constants = {}
            
            # Extract GA4 Measurement ID from page source
            ga4_patterns = [
                r'gtag\([\'"]config[\'"]\s*,\s*[\'"](G-[A-Z0-9]{10})[\'"]',
                r'google-analytics\.com/gtag/js\?id=([G][A-Z0-9]{10})',
                r'GA_MEASUREMENT_ID[\'"]\s*:\s*[\'"](G-[A-Z0-9]{10})[\'"]',
            ]
            for pattern in ga4_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    constants['GA4_MEASUREMENT_ID'] = match.group(1)
                    break
            if 'GA4_MEASUREMENT_ID' not in constants:
                constants['GA4_MEASUREMENT_ID'] = None

            # Extract Facebook Pixel ID from page source
            pixel_patterns = [
                r'fbq\([\'"]init[\'"]\s*,\s*[\'"](\d{15,16})[\'"]',
                r'connect\.facebook\.net/en_US/fbevents\.js#.*?id=(\d{15,16})',
                r'FACEBOOK_PIXEL_ID[\'"]\s*:\s*[\'"](\d{15,16})[\'"]',
            ]
            for pattern in pixel_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    constants['FACEBOOK_PIXEL_ID'] = match.group(1)
                    break
            if 'FACEBOOK_PIXEL_ID' not in constants:
                constants['FACEBOOK_PIXEL_ID'] = None

            return constants

        except Exception as e:
            return {
                'GA4_MEASUREMENT_ID': None,
                'FACEBOOK_PIXEL_ID': None,
                'error': f'Live site check failed: {str(e)}'
            }

    def check_live_tracking(self, site_name: str, ga4_id: Optional[str], pixel_id: Optional[str]) -> bool:
        """Check if analytics tracking is present on live site."""
        try:
            url = f"https://{site_name}"
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            content = response.text

            # Check for GA4 tracking
            ga4_found = False
            if ga4_id:
                # Check for gtag or GA4 script
                ga4_patterns = [
                    rf'gtag\([\'"]config[\'"]\s*,\s*[\'"]{re.escape(ga4_id)}[\'"]',
                    rf'G-[A-Z0-9]{{10}}',
                    rf'google-analytics\.com',
                ]
                ga4_found = any(re.search(pattern, content, re.IGNORECASE) for pattern in ga4_patterns)

            # Check for Facebook Pixel
            pixel_found = False
            if pixel_id:
                pixel_patterns = [
                    rf'fbq\([\'"]init[\'"]\s*,\s*[\'"]{re.escape(pixel_id)}[\'"]',
                    rf'connect\.facebook\.net',
                ]
                pixel_found = any(re.search(pattern, content, re.IGNORECASE) for pattern in pixel_patterns)

            return ga4_found or pixel_found

        except Exception as e:
            return False

    def validate_site(self, site_name: str, validate_ready_only: bool = False) -> AnalyticsValidation:
        """Validate analytics configuration for a site."""
        issues = []
        
        # Check wp-config.php
        config_constants = self.check_wp_config(site_name)
        
        if 'error' in config_constants:
            return AnalyticsValidation(
                site_name=site_name,
                ga4_configured=False,
                ga4_measurement_id=None,
                pixel_configured=False,
                pixel_id=None,
                tracking_verified=False,
                issues=[f"Config check error: {config_constants['error']}"],
                status="error"
            )

        ga4_id = config_constants.get('GA4_MEASUREMENT_ID')
        pixel_id = config_constants.get('FACEBOOK_PIXEL_ID')

        ga4_configured = ga4_id is not None and ga4_id.strip() != '' and ga4_id != 'YOUR_GA4_MEASUREMENT_ID'
        pixel_configured = pixel_id is not None and pixel_id.strip() != '' and pixel_id != 'YOUR_FACEBOOK_PIXEL_ID'

        # If validate-ready-only and not both configured, skip
        if validate_ready_only and not (ga4_configured and pixel_configured):
            return AnalyticsValidation(
                site_name=site_name,
                ga4_configured=ga4_configured,
                ga4_measurement_id=ga4_id,
                pixel_configured=pixel_configured,
                pixel_id=pixel_id,
                tracking_verified=False,
                issues=["Not ready for validation - IDs not fully configured"],
                status="missing"
            )

        # Check for missing IDs
        if not ga4_configured:
            issues.append("GA4 Measurement ID not configured or using placeholder")
        if not pixel_configured:
            issues.append("Facebook Pixel ID not configured or using placeholder")

        # Check live tracking if both are configured
        tracking_verified = False
        if ga4_configured and pixel_configured:
            tracking_verified = self.check_live_tracking(site_name, ga4_id, pixel_id)
            if not tracking_verified:
                issues.append("Analytics tracking not detected on live site")

        # Determine status
        if issues:
            if 'error' in str(issues):
                status = "error"
            elif "Not ready" in str(issues):
                status = "missing"
            else:
                status = "configured"  # IDs configured but issues found
        else:
            status = "ready"  # All good

        return AnalyticsValidation(
            site_name=site_name,
            ga4_configured=ga4_configured,
            ga4_measurement_id=ga4_id,
            pixel_configured=pixel_configured,
            pixel_id=pixel_id,
            tracking_verified=tracking_verified,
            issues=issues,
            status=status
        )

    def validate_all_sites(self, validate_ready_only: bool = False) -> List[AnalyticsValidation]:
        """Validate analytics for all P0 sites."""
        results = []
        for site in self.sites:
            validation = self.validate_site(site, validate_ready_only)
            results.append(validation)
        return results

    def generate_report(self, results: List[AnalyticsValidation]) -> str:
        """Generate validation report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        ready_count = sum(1 for r in results if r.status == "ready")
        configured_count = sum(1 for r in results if r.status == "configured")
        missing_count = sum(1 for r in results if r.status == "missing")
        error_count = sum(1 for r in results if r.status == "error")

        report = f"""# Tier 1 Analytics Validation Report
**Generated:** {timestamp}
**Tool:** tools/automated_p0_analytics_validation.py
**Sites Validated:** {len(results)}

## Executive Summary
- **✅ Ready (Fully Validated):** {ready_count}/{len(results)}
- **⚠️ Configured (Issues Found):** {configured_count}/{len(results)}
- **❌ Missing (Not Configured):** {missing_count}/{len(results)}
- **🔴 Error:** {error_count}/{len(results)}

## Site-by-Site Validation

"""

        for result in results:
            report += f"### {result.site_name}\n"
            report += f"**Status:** {result.status.upper()}\n\n"
            
            report += "**Configuration:**\n"
            ga4_status = "✅" if result.ga4_configured else "❌"
            pixel_status = "✅" if result.pixel_configured else "❌"
            report += f"- {ga4_status} GA4 Measurement ID: {result.ga4_measurement_id or 'NOT SET'}\n"
            report += f"- {pixel_status} Facebook Pixel ID: {result.pixel_id or 'NOT SET'}\n"
            
            if result.tracking_verified:
                report += f"- ✅ Live Tracking: Verified\n"
            else:
                report += f"- ❌ Live Tracking: Not verified\n"
            
            if result.issues:
                report += "\n**Issues:**\n"
                for issue in result.issues:
                    report += f"- ❌ {issue}\n"
            
            report += "\n"

        # Summary
        if ready_count == len(results):
            report += "## ✅ All Sites Validated\nAll P0 sites have analytics properly configured and tracking.\n"
        else:
            report += f"## ⚠️ Action Required\n{len(results) - ready_count} site(s) need attention.\n"

        return report

    def save_report(self, report: str, output_file: Optional[str] = None) -> Path:
        """Save report to file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reports/p0_analytics_validation_{timestamp}.md"

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate analytics configuration for P0 sites"
    )
    parser.add_argument(
        "--validate-ready",
        action="store_true",
        help="Validate only sites with IDs configured (ready for validation)"
    )
    parser.add_argument(
        "--site",
        help="Validate specific site only"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: auto-generated)"
    )

    args = parser.parse_args()

    validator = AutomatedP0AnalyticsValidator()

    if args.site:
        # Validate single site
        result = validator.validate_site(args.site, args.validate_ready)
        print(f"Analytics Validation for {args.site}:")
        print(f"  Status: {result.status.upper()}")
        print(f"  GA4 Configured: {'✅' if result.ga4_configured else '❌'}")
        print(f"  Pixel Configured: {'✅' if result.pixel_configured else '❌'}")
        print(f"  Tracking Verified: {'✅' if result.tracking_verified else '❌'}")
        if result.issues:
            print("  Issues:")
            for issue in result.issues:
                print(f"    - {issue}")
    else:
        # Validate all sites
        results = validator.validate_all_sites(args.validate_ready)
        
        print("Tier 1 Analytics Validation:")
        print("=" * 50)
        for result in results:
            print(f"\n{result.site_name}:")
            print(f"  Status: {result.status.upper()}")
            ga4_status = "✅" if result.ga4_configured else "❌"
            pixel_status = "✅" if result.pixel_configured else "❌"
            print(f"  {ga4_status} GA4: {result.ga4_measurement_id or 'NOT SET'}")
            print(f"  {pixel_status} Pixel: {result.pixel_id or 'NOT SET'}")
            if result.tracking_verified:
                print(f"  ✅ Live Tracking: Verified")
            if result.issues:
                print("  Issues:")
                for issue in result.issues:
                    print(f"    - {issue}")

        # Generate and save report
        report = validator.generate_report(results)
        report_path = validator.save_report(report, args.output)

        print(f"\nReport saved: {report_path}")
        
        ready_count = sum(1 for r in results if r.status == "ready")
        if ready_count == len(results):
            print("✅ All sites validated successfully")
        else:
            print(f"⚠️ {len(results) - ready_count} site(s) need attention")


if __name__ == "__main__":
    main()

