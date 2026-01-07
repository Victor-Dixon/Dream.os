#!/usr/bin/env python3
"""
Analytics Validation Scheduler & Health Check Tool
==================================================

Monitors GA4/Pixel readiness for P0 sites and generates status reports.
Stateful scheduler that tracks last snapshot and reports changes.

Usage:
    python tools/analytics_validation_scheduler.py                    # Check all sites, show status
    python tools/analytics_validation_scheduler.py --validate-on-ready # Validate ready sites only
    python tools/analytics_validation_scheduler.py --watch --interval 300  # Watch mode, check every 5 min
    python tools/analytics_validation_scheduler.py --site freerideinvestor.com  # Check specific site

Features:
- Stateful monitoring with snapshot persistence
- Change detection and markdown report generation
- Watch mode with configurable intervals
- Optional --validate-on-ready flag for automated validation
- Comprehensive status reporting

Author: Agent-5 (Business Intelligence Specialist)
Created: 2025-12-27
Purpose: Complete Tier 1 analytics validation monitoring
"""

import argparse
import json
import os
import re
import requests
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class SiteAnalyticsStatus:
    """Analytics status for a single site."""
    site_name: str
    ga4_measurement_id: Optional[str] = None
    facebook_pixel_id: Optional[str] = None
    ga4_configured: bool = False
    pixel_configured: bool = False
    tracking_verified: bool = False
    last_checked: Optional[str] = None
    status: str = "unknown"  # "ready", "configured", "missing", "error"
    issues: List[str] = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []


@dataclass
class AnalyticsSnapshot:
    """Complete analytics validation snapshot."""
    timestamp: str
    sites: Dict[str, SiteAnalyticsStatus]
    summary: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "sites": {name: asdict(status) for name, status in self.sites.items()},
            "summary": self.summary
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalyticsSnapshot':
        sites = {}
        for name, site_data in data["sites"].items():
            sites[name] = SiteAnalyticsStatus(**site_data)
        return cls(
            timestamp=data["timestamp"],
            sites=sites,
            summary=data["summary"]
        )


class AnalyticsValidationScheduler:
    """Stateful analytics validation scheduler with health monitoring."""

    def __init__(self):
        """Initialize the scheduler."""
        self.p0_sites = [
            "freerideinvestor.com",
            "tradingrobotplug.com",
            "dadudekc.com",
            "crosbyultimateevents.com"
        ]
        self.state_file = Path("analytics_validation_state.json")
        self.sites_dir = Path("websites/sites")

    def load_last_snapshot(self) -> Optional[AnalyticsSnapshot]:
        """Load the last saved snapshot."""
        if not self.state_file.exists():
            return None

        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return AnalyticsSnapshot.from_dict(data)
        except Exception as e:
            print(f"Warning: Could not load state file: {e}")
            return None

    def save_snapshot(self, snapshot: AnalyticsSnapshot) -> None:
        """Save snapshot to state file."""
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(snapshot.to_dict(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save state file: {e}")

    def check_wp_config(self, site_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Check wp-config.php for analytics constants."""
        config_path = self.sites_dir / site_name / "wp-config.php"

        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                ga4_match = re.search(
                    r'define\s*\(\s*[\'"]GA4_MEASUREMENT_ID[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                    content, re.IGNORECASE | re.MULTILINE
                )
                pixel_match = re.search(
                    r'define\s*\(\s*[\'"]FACEBOOK_PIXEL_ID[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
                    content, re.IGNORECASE | re.MULTILINE
                )

                ga4_id = ga4_match.group(1) if ga4_match else None
                pixel_id = pixel_match.group(1) if pixel_match else None

                return ga4_id, pixel_id, None

            except Exception as e:
                return None, None, str(e)

        # Check live site if local config not found
        try:
            url = f"https://{site_name}"
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            content = response.text

            # Extract GA4 ID
            ga4_patterns = [
                r'gtag\([\'"]config[\'"]\s*,\s*[\'"](G-[A-Z0-9]{10})[\'"]',
                r'google-analytics\.com/gtag/js\?id=([G][A-Z0-9]{10})',
            ]
            ga4_id = None
            for pattern in ga4_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    ga4_id = match.group(1)
                    break

            # Extract Pixel ID
            pixel_patterns = [
                r'fbq\([\'"]init[\'"]\s*,\s*[\'"](\d{15,16})[\'"]',
                r'connect\.facebook\.net/en_US/fbevents\.js#.*?id=(\d{15,16})',
            ]
            pixel_id = None
            for pattern in pixel_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    pixel_id = match.group(1)
                    break

            return ga4_id, pixel_id, None

        except Exception as e:
            return None, None, f"Live site check failed: {str(e)}"

    def check_live_tracking(self, site_name: str, ga4_id: Optional[str], pixel_id: Optional[str]) -> bool:
        """Check if analytics tracking is active on live site."""
        try:
            url = f"https://{site_name}"
            response = requests.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            content = response.text

            tracking_found = False

            # Check GA4
            if ga4_id:
                ga4_patterns = [
                    rf'gtag\([\'"]config[\'"]\s*,\s*[\'"]{re.escape(ga4_id)}[\'"]',
                    rf'G-[A-Z0-9]{{10}}',
                    rf'google-analytics\.com',
                ]
                tracking_found = tracking_found or any(
                    re.search(pattern, content, re.IGNORECASE) for pattern in ga4_patterns
                )

            # Check Pixel
            if pixel_id:
                pixel_patterns = [
                    rf'fbq\([\'"]init[\'"]\s*,\s*[\'"]{re.escape(pixel_id)}[\'"]',
                    rf'connect\.facebook\.net',
                ]
                tracking_found = tracking_found or any(
                    re.search(pattern, content, re.IGNORECASE) for pattern in pixel_patterns
                )

            return tracking_found

        except Exception:
            return False

    def validate_site(self, site_name: str, validate_ready_only: bool = False) -> SiteAnalyticsStatus:
        """Validate analytics configuration for a site."""
        status = SiteAnalyticsStatus(site_name=site_name)
        status.last_checked = datetime.now().isoformat()

        # Check configuration
        ga4_id, pixel_id, error = self.check_wp_config(site_name)

        if error:
            status.status = "error"
            status.issues.append(f"Configuration check error: {error}")
            return status

        status.ga4_measurement_id = ga4_id
        status.facebook_pixel_id = pixel_id

        # Check if configured (not None and not placeholder)
        status.ga4_configured = (
            ga4_id is not None and
            ga4_id.strip() != '' and
            ga4_id != 'YOUR_GA4_MEASUREMENT_ID' and
            ga4_id.startswith('G-')
        )
        status.pixel_configured = (
            pixel_id is not None and
            pixel_id.strip() != '' and
            pixel_id != 'YOUR_FACEBOOK_PIXEL_ID' and
            pixel_id.isdigit() and len(pixel_id) >= 15
        )

        # Skip if validate-ready-only and not configured
        if validate_ready_only and not (status.ga4_configured and status.pixel_configured):
            status.status = "missing"
            status.issues.append("Not ready for validation - IDs not configured")
            return status

        # Check live tracking if configured
        if status.ga4_configured and status.pixel_configured:
            status.tracking_verified = self.check_live_tracking(site_name, ga4_id, pixel_id)

        # Determine status and issues
        if not status.ga4_configured:
            status.issues.append("GA4 Measurement ID not configured or invalid")
        if not status.pixel_configured:
            status.issues.append("Facebook Pixel ID not configured or invalid")
        if status.ga4_configured and status.pixel_configured and not status.tracking_verified:
            status.issues.append("Analytics tracking not detected on live site")

        # Set overall status
        if status.issues:
            if "Configuration check error" in str(status.issues):
                status.status = "error"
            elif "Not ready for validation" in str(status.issues):
                status.status = "missing"
            else:
                status.status = "configured"  # Configured but has issues
        else:
            status.status = "ready"  # Fully validated

        return status

    def check_all_sites(self, validate_ready_only: bool = False) -> Dict[str, SiteAnalyticsStatus]:
        """Check analytics status for all P0 sites."""
        results = {}
        for site in self.p0_sites:
            results[site] = self.validate_site(site, validate_ready_only)
        return results

    def calculate_summary(self, sites: Dict[str, SiteAnalyticsStatus]) -> Dict[str, int]:
        """Calculate summary statistics."""
        return {
            "ready": sum(1 for s in sites.values() if s.status == "ready"),
            "configured": sum(1 for s in sites.values() if s.status == "configured"),
            "missing": sum(1 for s in sites.values() if s.status == "missing"),
            "error": sum(1 for s in sites.values() if s.status == "error"),
            "total": len(sites)
        }

    def create_snapshot(self, validate_ready_only: bool = False) -> AnalyticsSnapshot:
        """Create a new analytics validation snapshot."""
        sites = self.check_all_sites(validate_ready_only)
        summary = self.calculate_summary(sites)
        timestamp = datetime.now().isoformat()

        return AnalyticsSnapshot(
            timestamp=timestamp,
            sites=sites,
            summary=summary
        )

    def detect_changes(self, current: AnalyticsSnapshot, previous: Optional[AnalyticsSnapshot]) -> List[str]:
        """Detect changes between snapshots."""
        if not previous:
            return ["Initial snapshot - no previous state to compare"]

        changes = []

        # Check summary changes
        for key in ["ready", "configured", "missing", "error"]:
            if current.summary[key] != previous.summary[key]:
                changes.append(
                    f"Summary {key}: {previous.summary[key]} → {current.summary[key]}"
                )

        # Check individual site changes
        for site_name in self.p0_sites:
            if site_name not in current.sites or site_name not in previous.sites:
                continue

            curr = current.sites[site_name]
            prev = previous.sites[site_name]

            # Status change
            if curr.status != prev.status:
                changes.append(
                    f"{site_name}: Status {prev.status} → {curr.status}"
                )

            # Configuration changes
            if curr.ga4_measurement_id != prev.ga4_measurement_id:
                changes.append(
                    f"{site_name}: GA4 ID {prev.ga4_measurement_id} → {curr.ga4_measurement_id}"
                )
            if curr.facebook_pixel_id != prev.facebook_pixel_id:
                changes.append(
                    f"{site_name}: Pixel ID {prev.facebook_pixel_id} → {curr.facebook_pixel_id}"
                )

            # New issues
            new_issues = set(curr.issues) - set(prev.issues)
            for issue in new_issues:
                changes.append(f"{site_name}: New issue - {issue}")

            # Resolved issues
            resolved_issues = set(prev.issues) - set(curr.issues)
            for issue in resolved_issues:
                changes.append(f"{site_name}: Resolved - {issue}")

        return changes

    def generate_report(self, snapshot: AnalyticsSnapshot, changes: List[str] = None) -> str:
        """Generate markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""# Analytics Validation Health Check Report
**Generated:** {timestamp}
**Tool:** tools/analytics_validation_scheduler.py

## Executive Summary
- **✅ Ready:** {snapshot.summary['ready']}/{snapshot.summary['total']} sites fully validated
- **⚠️ Configured:** {snapshot.summary['configured']}/{snapshot.summary['total']} sites configured with issues
- **❌ Missing:** {snapshot.summary['missing']}/{snapshot.summary['total']} sites not configured
- **🔴 Error:** {snapshot.summary['error']}/{snapshot.summary['total']} sites with errors

"""

        if changes:
            report += "## Changes Since Last Check\n"
            for change in changes:
                report += f"- {change}\n"
            report += "\n"

        report += "## Site Status Details\n\n"

        for site_name, status in snapshot.sites.items():
            report += f"### {site_name}\n"
            report += f"**Status:** {status.status.upper()}\n"
            report += f"**Last Checked:** {status.last_checked or 'Never'}\n\n"

            # Configuration status
            ga4_status = "✅" if status.ga4_configured else "❌"
            pixel_status = "✅" if status.pixel_configured else "❌"
            tracking_status = "✅" if status.tracking_verified else "❌"

            report += "**Configuration:**\n"
            report += f"- {ga4_status} GA4: {status.ga4_measurement_id or 'NOT SET'}\n"
            report += f"- {pixel_status} Pixel: {status.facebook_pixel_id or 'NOT SET'}\n"
            report += f"- {tracking_status} Live Tracking: {'Verified' if status.tracking_verified else 'Not verified'}\n"

            if status.issues:
                report += "\n**Issues:**\n"
                for issue in status.issues:
                    report += f"- ❌ {issue}\n"

            report += "\n"

        # Recommendations
        if snapshot.summary['ready'] == snapshot.summary['total']:
            report += "## ✅ All Clear\nAll P0 sites have analytics properly configured and tracking.\n"
        else:
            report += "## ⚠️ Action Required\n"
            if snapshot.summary['error'] > 0:
                report += f"- {snapshot.summary['error']} site(s) have configuration errors that need immediate attention\n"
            if snapshot.summary['missing'] > 0:
                report += f"- {snapshot.summary['missing']} site(s) need analytics IDs configured\n"
            if snapshot.summary['configured'] > 0:
                report += f"- {snapshot.summary['configured']} site(s) have configuration issues to resolve\n"

        return report

    def save_report(self, report: str, output_file: Optional[str] = None) -> Path:
        """Save report to file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reports/analytics_health_check_{timestamp}.md"

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return output_path

    def run_once(self, validate_ready_only: bool = False, save_report: bool = True) -> AnalyticsSnapshot:
        """Run a single validation check."""
        current = self.create_snapshot(validate_ready_only)
        previous = self.load_last_snapshot()

        changes = self.detect_changes(current, previous) if previous else None

        # Save current state
        self.save_snapshot(current)

        if save_report:
            report = self.generate_report(current, changes)
            report_path = self.save_report(report)
            print(f"Report saved: {report_path}")

        return current

    def watch_mode(self, interval: int = 300, validate_ready_only: bool = False) -> None:
        """Run in watch mode with periodic checks."""
        print(f"Starting watch mode - checking every {interval} seconds...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking analytics status...")
                snapshot = self.run_once(validate_ready_only, save_report=True)

                ready = snapshot.summary['ready']
                total = snapshot.summary['total']

                if ready == total:
                    print(f"✅ All {total} sites ready")
                else:
                    print(f"⚠️ {ready}/{total} sites ready - {total - ready} need attention")

                print(f"Next check in {interval} seconds...\n")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nWatch mode stopped by user")

    def print_status(self, snapshot: AnalyticsSnapshot) -> None:
        """Print current status to console."""
        print("Analytics Validation Status:")
        print("=" * 50)

        for site_name, status in snapshot.sites.items():
            print(f"\n{site_name}:")
            print(f"  Status: {status.status.upper()}")

            ga4_status = "✅" if status.ga4_configured else "❌"
            pixel_status = "✅" if status.pixel_configured else "❌"
            tracking_status = "✅" if status.tracking_verified else "❌"

            print(f"  {ga4_status} GA4: {status.ga4_measurement_id or 'NOT SET'}")
            print(f"  {pixel_status} Pixel: {status.facebook_pixel_id or 'NOT SET'}")
            print(f"  {tracking_status} Tracking: {'Verified' if status.tracking_verified else 'Not verified'}")

            if status.issues:
                print("  Issues:")
                for issue in status.issues:
                    print(f"    - {issue}")

        print(f"\nSummary: {snapshot.summary['ready']}/{snapshot.summary['total']} sites ready")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analytics validation scheduler and health check tool"
    )
    parser.add_argument(
        "--validate-on-ready",
        action="store_true",
        help="Validate only sites with IDs configured"
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Run in watch mode (continuous monitoring)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Watch mode interval in seconds (default: 300)"
    )
    parser.add_argument(
        "--site",
        help="Check specific site only"
    )
    parser.add_argument(
        "--output",
        help="Output file path (default: auto-generated)"
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip generating markdown report"
    )

    args = parser.parse_args()

    scheduler = AnalyticsValidationScheduler()

    if args.watch:
        # Watch mode
        scheduler.watch_mode(args.interval, args.validate_on_ready)

    elif args.site:
        # Single site check
        status = scheduler.validate_site(args.site, args.validate_ready_only)
        print(f"Analytics Status for {args.site}:")
        print(f"  Status: {status.status.upper()}")
        print(f"  GA4 Configured: {'✅' if status.ga4_configured else '❌'} ({status.ga4_measurement_id or 'NOT SET'})")
        print(f"  Pixel Configured: {'✅' if status.pixel_configured else '❌'} ({status.facebook_pixel_id or 'NOT SET'})")
        print(f"  Tracking Verified: {'✅' if status.tracking_verified else '❌'}")
        if status.issues:
            print("  Issues:")
            for issue in status.issues:
                print(f"    - {issue}")

    else:
        # Full check
        snapshot = scheduler.run_once(args.validate_on_ready, save_report=not args.no_report)
        scheduler.print_status(snapshot)


if __name__ == "__main__":
    main()