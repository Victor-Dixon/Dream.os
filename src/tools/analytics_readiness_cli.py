#!/usr/bin/env python3
"""
Analytics Validation Readiness CLI Tool
Part of Agent-8's documentation/CLI readiness package delivery
"""

import argparse
import sys
import os
from pathlib import Path

class AnalyticsReadinessCLI:
    """CLI tool for analytics validation readiness checking"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent.parent

    def check_websites_directory(self):
        """Check if websites directory exists and has expected structure"""
        websites_dir = self.project_root / "websites"
        if not websites_dir.exists():
            print(f"❌ Websites directory not found: {websites_dir}")
            return False

        print(f"✅ Websites directory found: {websites_dir}")

        # Check for expected site directories
        expected_sites = ["freerideinvestor.com", "tradingrobotplug.com", "dadudekc.com", "crosbyultimateevents.com"]
        found_sites = []

        for site in expected_sites:
            site_dir = websites_dir / site
            if site_dir.exists():
                found_sites.append(site)
                print(f"  ✅ {site}")
            else:
                print(f"  ❌ {site} - directory not found")

        print(f"\n📊 Found {len(found_sites)}/{len(expected_sites)} expected site directories")
        return len(found_sites) > 0

    def check_analytics_configs(self):
        """Check for analytics configuration files"""
        websites_dir = self.project_root / "websites"
        if not websites_dir.exists():
            print("❌ Websites directory not found")
            return False

        print("🔍 Checking analytics configuration files...")

        configs_found = 0
        total_sites = 0

        for site_dir in websites_dir.iterdir():
            if site_dir.is_dir():
                total_sites += 1
                config_file = site_dir / "wp-config-analytics.php"
                if config_file.exists():
                    configs_found += 1
                    print(f"  ✅ {site_dir.name}/wp-config-analytics.php")
                else:
                    print(f"  ❌ {site_dir.name}/wp-config-analytics.php - not found")

        print(f"\n📊 Found {configs_found}/{total_sites} analytics config files")
        return configs_found > 0

    def validate_id_formats(self):
        """Validate analytics ID formats in config files"""
        websites_dir = self.project_root / "websites"
        if not websites_dir.exists():
            print("❌ Websites directory not found")
            return False

        print("🔍 Validating analytics ID formats...")

        valid_configs = 0
        total_checked = 0

        for site_dir in websites_dir.iterdir():
            if site_dir.is_dir():
                config_file = site_dir / "wp-config-analytics.php"
                if config_file.exists():
                    total_checked += 1
                    try:
                        content = config_file.read_text()

                        # Check for GA4 ID format (G-XXXXXXXXXX)
                        ga4_match = None
                        for line in content.split('\n'):
                            if 'GA4_MEASUREMENT_ID' in line and 'define(' in line:
                                # Extract the ID value
                                if "'" in line:
                                    parts = line.split("'")
                                    if len(parts) >= 4:
                                        ga4_id = parts[3]
                                        if ga4_id.startswith('G-') and len(ga4_id) == 11:
                                            ga4_match = ga4_id
                                            break

                        # Check for Facebook Pixel ID format (15-16 digits)
                        pixel_match = None
                        for line in content.split('\n'):
                            if 'FACEBOOK_PIXEL_ID' in line and 'define(' in line:
                                if "'" in line:
                                    parts = line.split("'")
                                    if len(parts) >= 4:
                                        pixel_id = parts[3]
                                        if pixel_id.isdigit() and 15 <= len(pixel_id) <= 16:
                                            pixel_match = pixel_id
                                            break

                        if ga4_match and pixel_match:
                            valid_configs += 1
                            print(f"  ✅ {site_dir.name} - Valid IDs found")
                        else:
                            print(f"  ⚠️  {site_dir.name} - IDs may be placeholder or invalid format")

                    except Exception as e:
                        print(f"  ❌ {site_dir.name} - Error reading config: {e}")

        print(f"\n📊 Validated {valid_configs}/{total_checked} config files with proper ID formats")
        return valid_configs > 0

    def generate_readiness_report(self):
        """Generate a comprehensive readiness report"""
        print("📋 ANALYTICS VALIDATION READINESS REPORT")
        print("=" * 50)

        # Check components
        websites_ok = self.check_websites_directory()
        configs_ok = self.check_analytics_configs()
        ids_ok = self.validate_id_formats()

        print("\n" + "=" * 50)
        print("📊 READINESS SUMMARY")
        print("=" * 50)

        readiness_score = sum([websites_ok, configs_ok, ids_ok]) / 3 * 100

        if readiness_score == 100:
            print("🎉 STATUS: FULLY READY FOR ANALYTICS VALIDATION")
        elif readiness_score >= 66:
            print("⚠️  STATUS: MOSTLY READY - Requires real analytics IDs")
        elif readiness_score >= 33:
            print("❌ STATUS: BLOCKED - Infrastructure issues need resolution")
        else:
            print("🚫 STATUS: NOT READY - Major setup required")

        print(".1f"
        print("\n🔧 NEXT STEPS:")
        if not websites_ok:
            print("  - Create websites directory structure")
        if not configs_ok:
            print("  - Generate wp-config-analytics.php files for each site")
        if not ids_ok:
            print("  - Obtain real GA4 Measurement IDs and Facebook Pixel IDs")
            print("  - Replace placeholder values in configuration files")

        print("\n📖 REFERENCE: See docs/TIER1_ANALYTICS_VALIDATION_ASSESSMENT.md for detailed procedures")

    def run(self):
        """Main CLI execution"""
        parser = argparse.ArgumentParser(
            description="Analytics Validation Readiness CLI Tool",
            epilog="Part of Agent-8's documentation/CLI readiness package"
        )

        parser.add_argument(
            '--check-sites',
            action='store_true',
            help='Check websites directory structure'
        )

        parser.add_argument(
            '--check-configs',
            action='store_true',
            help='Check analytics configuration files'
        )

        parser.add_argument(
            '--validate-ids',
            action='store_true',
            help='Validate analytics ID formats'
        )

        parser.add_argument(
            '--full-report',
            action='store_true',
            help='Generate comprehensive readiness report'
        )

        args = parser.parse_args()

        # If no specific args, show help
        if not any([args.check_sites, args.check_configs, args.validate_ids, args.full_report]):
            parser.print_help()
            return

        print("🚀 Analytics Validation Readiness CLI Tool")
        print("Part of Agent-8's documentation/CLI readiness package delivery\n")

        if args.check_sites:
            self.check_websites_directory()
        elif args.check_configs:
            self.check_analytics_configs()
        elif args.validate_ids:
            self.validate_id_formats()
        elif args.full_report:
            self.generate_readiness_report()

def main():
    """Entry point"""
    cli = AnalyticsReadinessCLI()
    cli.run()

if __name__ == "__main__":
    main()