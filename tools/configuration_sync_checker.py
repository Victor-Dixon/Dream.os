#!/usr/bin/env python3
"""
Configuration Sync Checker Tool
===============================

Verifies wp-config.php sync across environments and detects configuration drift.

Usage:
    python tools/configuration_sync_checker.py                    # Check all sites
    python tools/configuration_sync_checker.py --site freerideinvestor.com  # Check specific site
    python tools/configuration_sync_checker.py --report-only     # Generate report only

Features:
- Compares wp-config.php files across WordPress sites
- Detects configuration drift in database settings
- Validates analytics configuration (GA4/Pixel IDs)
- Generates sync status reports
- Identifies missing configuration files

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-27
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConfigAnalysis:
    """Configuration analysis result for a site."""
    site_name: str
    config_exists: bool
    constants: Dict[str, Optional[str]]
    issues: List[str]
    recommendations: List[str]


class ConfigurationSyncChecker:
    """Checks WordPress configuration sync across sites."""

    def __init__(self, sites_dir: Optional[Path] = None):
        """Initialize the checker."""
        self.sites_dir = sites_dir or Path("websites/sites")
        self.sites = [
            "freerideinvestor.com",
            "dadudekc.com",
            "crosbyultimateevents.com",
            "tradingrobotplug.com"
        ]

        # Key constants to check
        self.key_constants = [
            "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST",
            "GA4_MEASUREMENT_ID", "FACEBOOK_PIXEL_ID"
        ]

    def extract_wp_config_constants(self, config_path: Path) -> Dict[str, Optional[str]]:
        """Extract key constants from wp-config.php file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            constants = {}

            # Patterns for different constant definitions
            patterns = {
                'DB_NAME': r'define\s*\(\s*[\'"]DB_NAME[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                'DB_USER': r'define\s*\(\s*[\'"]DB_USER[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                'DB_PASSWORD': r'define\s*\(\s*[\'"]DB_PASSWORD[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                'DB_HOST': r'define\s*\(\s*[\'"]DB_HOST[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
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
            return {'error': str(e)}

    def analyze_site_config(self, site_name: str) -> ConfigAnalysis:
        """Analyze configuration for a specific site."""
        config_path = self.sites_dir / site_name / "wp-config.php"
        issues = []
        recommendations = []

        if not config_path.exists():
            return ConfigAnalysis(
                site_name=site_name,
                config_exists=False,
                constants={},
                issues=["wp-config.php file not found"],
                recommendations=["Deploy wp-config.php file to site"]
            )

        constants = self.extract_wp_config_constants(config_path)

        if 'error' in constants:
            return ConfigAnalysis(
                site_name=site_name,
                config_exists=True,
                constants={},
                issues=[f"Failed to parse config: {constants['error']}"],
                recommendations=["Fix wp-config.php syntax errors"]
            )

        # Check for missing critical constants
        critical_constants = ['DB_NAME', 'DB_USER', 'DB_HOST']
        for const in critical_constants:
            if not constants.get(const):
                issues.append(f"Missing critical constant: {const}")
                recommendations.append(f"Add {const} definition to wp-config.php")

        # Check for analytics constants
        analytics_constants = ['GA4_MEASUREMENT_ID', 'FACEBOOK_PIXEL_ID']
        for const in analytics_constants:
            if not constants.get(const):
                issues.append(f"Missing analytics constant: {const}")
                recommendations.append(f"Configure {const} for analytics tracking")

        return ConfigAnalysis(
            site_name=site_name,
            config_exists=True,
            constants=constants,
            issues=issues,
            recommendations=recommendations
        )

    def analyze_all_sites(self) -> List[ConfigAnalysis]:
        """Analyze configurations for all sites."""
        results = []
        for site in self.sites:
            analysis = self.analyze_site_config(site)
            results.append(analysis)
        return results

    def compare_configs(self, results: List[ConfigAnalysis]) -> List[str]:
        """Compare configurations across sites to detect drift."""
        issues = []

        # Find a baseline site (first one with complete config)
        baseline = None
        for result in results:
            if (result.config_exists and 'error' not in result.constants and
                result.constants.get('DB_NAME')):
                baseline = result
                break

        if not baseline:
            issues.append("No baseline configuration found for comparison")
            return issues

        # Compare each site to baseline
        for result in results:
            if result.site_name == baseline.site_name:
                continue

            if not result.config_exists:
                issues.append(f"{result.site_name}: Configuration file missing")
                continue

            if 'error' in result.constants:
                issues.append(f"{result.site_name}: Configuration parsing error")
                continue

            # Check database consistency (should be unique per site)
            db_constants = ['DB_NAME']
            for const in db_constants:
                baseline_val = baseline.constants.get(const)
                current_val = result.constants.get(const)
                if baseline_val and current_val and baseline_val == current_val:
                    issues.append(f"{result.site_name}: {const} matches baseline (should be unique)")

            # Check environment consistency (should be similar)
            env_constants = ['DB_HOST']
            for const in env_constants:
                baseline_val = baseline.constants.get(const)
                current_val = result.constants.get(const)
                if baseline_val and current_val and baseline_val != current_val:
                    issues.append(f"{result.site_name}: {const} differs from baseline environment")

        return issues

    def generate_report(self, results: List[ConfigAnalysis], sync_issues: List[str]) -> str:
        """Generate comprehensive status report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Configuration Sync Status Report
**Generated:** {timestamp}
**Tool:** tools/configuration_sync_checker.py

## Executive Summary
- **Sites Analyzed:** {len(results)}
- **Sites with Config Files:** {sum(1 for r in results if r.config_exists)}
- **Sites with Issues:** {sum(1 for r in results if r.issues)}
- **Sync Issues:** {len(sync_issues)}

## Site-by-Site Analysis

"""

        for result in results:
            report += f"### {result.site_name}\n"
            if not result.config_exists:
                report += "**Status:** ❌ CONFIG FILE MISSING\n"
                if result.recommendations:
                    report += "**Recommendations:**\n"
                    for rec in result.recommendations:
                        report += f"- {rec}\n"
                report += "\n"
                continue

            report += "**Status:** ✅ CONFIG FILE FOUND\n"

            if 'error' in result.constants:
                report += f"**Parse Error:** {result.constants['error']}\n"
            else:
                report += "**Constants:**\n"
                for const in self.key_constants:
                    value = result.constants.get(const)
                    status = "✅" if value else "❌"
                    display_value = value if value else "NOT SET"
                    report += f"- {status} {const}: {display_value}\n"

            if result.issues:
                report += "**Issues:**\n"
                for issue in result.issues:
                    report += f"- ❌ {issue}\n"

            if result.recommendations:
                report += "**Recommendations:**\n"
                for rec in result.recommendations:
                    report += f"- {rec}\n"

            report += "\n"

        if sync_issues:
            report += "## Cross-Site Sync Issues\n\n"
            for issue in sync_issues:
                report += f"- ❌ {issue}\n"
            report += "\n"

        # Summary
        total_issues = sum(len(r.issues) for r in results) + len(sync_issues)
        if total_issues == 0:
            report += "## ✅ All Clear\nAll configurations are properly synchronized.\n"
        else:
            report += f"## ⚠️ Action Required\n**Total Issues:** {total_issues}\n\n"
            report += "Run this tool periodically to monitor configuration sync status.\n"

        return report

    def save_report(self, report: str, output_file: Optional[str] = None) -> Path:
        """Save report to file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reports/configuration_sync_report_{timestamp}.md"

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return output_path


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Check WordPress configuration sync across sites"
    )
    parser.add_argument(
        "--site",
        help="Check specific site only"
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Generate report only (no console output)"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: auto-generated)"
    )

    args = parser.parse_args()

    checker = ConfigurationSyncChecker()

    if args.site:
        # Check single site
        result = checker.analyze_site_config(args.site)
        if not args.report_only:
            print(f"Configuration analysis for {args.site}:")
            print(f"  Config exists: {result.config_exists}")
            if result.issues:
                print("  Issues:")
                for issue in result.issues:
                    print(f"    - {issue}")
            if result.recommendations:
                print("  Recommendations:")
                for rec in result.recommendations:
                    print(f"    - {rec}")
    else:
        # Check all sites
        results = checker.analyze_all_sites()
        sync_issues = checker.compare_configs(results)

        if not args.report_only:
            print("Configuration Sync Analysis:")
            print("=" * 50)
            for result in results:
                print(f"\n{result.site_name}:")
                if not result.config_exists:
                    print("  ❌ Config file missing")
                elif 'error' in result.constants:
                    print(f"  ❌ Parse error: {result.constants['error']}")
                else:
                    for const in checker.key_constants:
                        value = result.constants.get(const)
                        status = "✅" if value else "❌"
                        print(f"  {status} {const}: {value or 'NOT SET'}")

            if sync_issues:
                print("\nSync Issues:")
                for issue in sync_issues:
                    print(f"  ❌ {issue}")

        # Generate and save report
        report = checker.generate_report(results, sync_issues)
        report_path = checker.save_report(report, args.output)

        if not args.report_only:
            print(f"\nReport saved: {report_path}")
            total_issues = sum(len(r.issues) for r in results) + len(sync_issues)
            if total_issues == 0:
                print("✅ All configurations synchronized")
            else:
                print(f"⚠️ {total_issues} issues found - review report")


if __name__ == "__main__":
    main()
