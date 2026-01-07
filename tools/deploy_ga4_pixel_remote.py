#!/usr/bin/env python3
"""
GA4 and Facebook Pixel Remote Deployment Tool
============================================

Deploys GA4 Measurement ID and Facebook Pixel ID configurations to remote WordPress sites
using SSH and WP-CLI. Optimized for production deployment scenarios.

Usage:
    python tools/deploy_ga4_pixel_remote.py --site freerideinvestor.com --ga4-id G-XXXXXXXXXX --pixel-id 1234567890123456
    python tools/deploy_ga4_pixel_remote.py --all-sites --ga4-ids config/analytics_ids.json
    python tools/deploy_ga4_pixel_remote.py --site tradingrobotplug.com --backup-only
    python tools/deploy_ga4_pixel_remote.py --validate-deployment --site dadudekc.com

Features:
- Remote deployment via SSH and WP-CLI
- Batch deployment for multiple sites
- Production-ready backup and rollback
- Deployment validation and health checks
- Integration with existing analytics validation tools

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2026-01-07
Purpose: Complete remote analytics deployment automation for P0 sites
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# P0 sites SSH configuration
P0_SITES_CONFIG = {
    "freerideinvestor.com": {
        "ssh_host": "freerideinvestor.com",
        "ssh_user": "deploy",
        "ssh_key": "~/.ssh/id_rsa",  # Update with actual key path
        "wp_path": "/var/www/freerideinvestor.com",
        "wp_cli": "wp --path=/var/www/freerideinvestor.com",
        "backup_dir": "/var/backups/freerideinvestor"
    },
    "tradingrobotplug.com": {
        "ssh_host": "tradingrobotplug.com",
        "ssh_user": "deploy",
        "ssh_key": "~/.ssh/id_rsa",
        "wp_path": "/var/www/tradingrobotplug.com",
        "wp_cli": "wp --path=/var/www/tradingrobotplug.com",
        "backup_dir": "/var/backups/tradingrobotplug"
    },
    "dadudekc.com": {
        "ssh_host": "dadudekc.com",
        "ssh_user": "deploy",
        "ssh_key": "~/.ssh/id_rsa",
        "wp_path": "/var/www/dadudekc.com",
        "wp_cli": "wp --path=/var/www/dadudekc.com",
        "backup_dir": "/var/backups/dadudekc"
    },
    "crosbyultimateevents.com": {
        "ssh_host": "crosbyultimateevents.com",
        "ssh_user": "deploy",
        "ssh_key": "~/.ssh/id_rsa",
        "wp_path": "/var/www/crosbyultimateevents.com",
        "wp_cli": "wp --path=/var/www/crosbyultimateevents.com",
        "backup_dir": "/var/backups/crosbyultimateevents"
    }
}

@dataclass
class RemoteDeploymentResult:
    """Result of a remote deployment operation."""
    site_name: str
    success: bool
    ga4_deployed: bool
    pixel_deployed: bool
    backup_created: bool
    wp_cli_available: bool
    error_message: Optional[str] = None
    rollback_available: bool = False

class RemoteAnalyticsDeploymentTool:
    """Remote GA4 and Facebook Pixel deployment tool using SSH/WP-CLI."""

    def __init__(self):
        self.results: List[RemoteDeploymentResult] = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_ssh_command(self, host: str, user: str, command: str, key_path: str = None) -> Tuple[bool, str, str]:
        """Execute command via SSH."""
        ssh_cmd = ["ssh"]

        if key_path:
            ssh_cmd.extend(["-i", key_path])

        ssh_cmd.extend([f"{user}@{host}", command])

        try:
            result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "SSH command timed out"
        except Exception as e:
            return False, "", f"SSH error: {str(e)}"

    def validate_wp_cli(self, site_config: Dict[str, str]) -> bool:
        """Validate WP-CLI availability on remote server."""
        host = site_config['ssh_host']
        user = site_config['ssh_user']
        key = site_config.get('ssh_key')
        wp_cli = site_config['wp_cli']

        success, stdout, stderr = self.run_ssh_command(host, user, f"{wp_cli} --version", key)

        if success and "WP-CLI" in stdout:
            return True

        return False

    def create_remote_backup(self, site_config: Dict[str, str]) -> Tuple[bool, str]:
        """Create backup of remote wp-config.php."""
        host = site_config['ssh_host']
        user = site_config['ssh_user']
        key = site_config.get('ssh_key')
        wp_path = site_config['wp_path']
        backup_dir = site_config['backup_dir']

        # Ensure backup directory exists
        mkdir_cmd = f"mkdir -p {backup_dir}"
        success, _, stderr = self.run_ssh_command(host, user, mkdir_cmd, key)
        if not success:
            return False, f"Failed to create backup directory: {stderr}"

        # Create backup
        backup_cmd = f"cp {wp_path}/wp-config.php {backup_dir}/wp-config.php.backup.{self.timestamp}"
        success, _, stderr = self.run_ssh_command(host, user, backup_cmd, key)

        if success:
            return True, f"Backup created: {backup_dir}/wp-config.php.backup.{self.timestamp}"
        else:
            return False, f"Backup failed: {stderr}"

    def deploy_analytics_via_wp_cli(self, site_config: Dict[str, str], ga4_id: str, pixel_id: str) -> RemoteDeploymentResult:
        """Deploy analytics configuration using WP-CLI."""
        site_name = site_config['ssh_host'].replace('.com', '')
        result = RemoteDeploymentResult(
            site_name=site_name,
            success=False,
            ga4_deployed=False,
            pixel_deployed=False,
            backup_created=False,
            wp_cli_available=False
        )

        # Validate WP-CLI availability
        result.wp_cli_available = self.validate_wp_cli(site_config)
        if not result.wp_cli_available:
            result.error_message = "WP-CLI not available on remote server"
            return result

        # Create backup
        backup_success, backup_message = self.create_remote_backup(site_config)
        result.backup_created = backup_success
        result.rollback_available = backup_success

        if not backup_success:
            result.error_message = f"Backup failed: {backup_message}"
            return result

        host = site_config['ssh_host']
        user = site_config['ssh_user']
        key = site_config.get('ssh_key')
        wp_cli = site_config['wp_cli']

        # Check if analytics already configured
        check_cmd = f"{wp_cli} config get GA4_MEASUREMENT_ID 2>/dev/null || echo 'NOT_SET'"
        success, stdout, stderr = self.run_ssh_command(host, user, check_cmd, key)

        if success and stdout.strip() and stdout.strip() != "NOT_SET":
            result.error_message = "Analytics already configured (GA4_MEASUREMENT_ID exists)"
            return result

        # Deploy GA4 configuration
        ga4_cmd = f"{wp_cli} config set GA4_MEASUREMENT_ID '{ga4_id}' --type=constant"
        ga4_success, _, ga4_stderr = self.run_ssh_command(host, user, ga4_cmd, key)

        # Deploy Facebook Pixel configuration
        pixel_cmd = f"{wp_cli} config set FACEBOOK_PIXEL_ID '{pixel_id}' --type=constant"
        pixel_success, _, pixel_stderr = self.run_ssh_command(host, user, pixel_cmd, key)

        # Set analytics enabled flag
        enabled_cmd = f"{wp_cli} config set ANALYTICS_ENABLED true --type=constant"
        enabled_success, _, enabled_stderr = self.run_ssh_command(host, user, enabled_cmd, key)

        # Set debug mode
        debug_cmd = f"{wp_cli} config set ANALYTICS_DEBUG false --type=constant"
        debug_success, _, debug_stderr = self.run_ssh_command(host, user, debug_cmd, key)

        result.ga4_deployed = ga4_success
        result.pixel_deployed = pixel_success

        if ga4_success and pixel_success and enabled_success:
            result.success = True
        else:
            errors = []
            if not ga4_success:
                errors.append(f"GA4 deployment failed: {ga4_stderr}")
            if not pixel_success:
                errors.append(f"Pixel deployment failed: {pixel_stderr}")
            if not enabled_success:
                errors.append(f"Analytics enabled flag failed: {enabled_stderr}")
            result.error_message = "; ".join(errors)

        return result

    def rollback_deployment(self, site_config: Dict[str, str]) -> bool:
        """Rollback deployment using backup."""
        host = site_config['ssh_host']
        user = site_config['ssh_user']
        key = site_config.get('ssh_key')
        wp_path = site_config['wp_path']
        backup_dir = site_config['backup_dir']

        backup_file = f"{backup_dir}/wp-config.php.backup.{self.timestamp}"

        # Check if backup exists
        check_cmd = f"test -f {backup_file} && echo 'EXISTS' || echo 'NOT_EXISTS'"
        success, stdout, _ = self.run_ssh_command(host, user, check_cmd, key)

        if not success or stdout.strip() != "EXISTS":
            return False

        # Restore backup
        restore_cmd = f"cp {backup_file} {wp_path}/wp-config.php"
        success, _, stderr = self.run_ssh_command(host, user, restore_cmd, key)

        return success

    def validate_remote_deployment(self, site_config: Dict[str, str]) -> bool:
        """Validate remote deployment by checking configurations."""
        host = site_config['ssh_host']
        user = site_config['ssh_user']
        key = site_config.get('ssh_key')
        wp_cli = site_config['wp_cli']

        # Check GA4 ID
        ga4_cmd = f"{wp_cli} config get GA4_MEASUREMENT_ID 2>/dev/null || echo 'NOT_SET'"
        ga4_success, ga4_output, _ = self.run_ssh_command(host, user, ga4_cmd, key)

        # Check Pixel ID
        pixel_cmd = f"{wp_cli} config get FACEBOOK_PIXEL_ID 2>/dev/null || echo 'NOT_SET'"
        pixel_success, pixel_output, _ = self.run_ssh_command(host, user, pixel_cmd, key)

        ga4_configured = ga4_success and ga4_output.strip() and ga4_output.strip() != "NOT_SET"
        pixel_configured = pixel_success and pixel_output.strip() and pixel_output.strip() != "NOT_SET"

        return ga4_configured and pixel_configured

    def deploy_to_site(self, site_name: str, ga4_id: str = None, pixel_id: str = None,
                      backup_only: bool = False, validate_only: bool = False) -> RemoteDeploymentResult:
        """Deploy analytics to a specific remote site."""
        if site_name not in P0_SITES_CONFIG:
            return RemoteDeploymentResult(
                site_name=site_name,
                success=False,
                ga4_deployed=False,
                pixel_deployed=False,
                backup_created=False,
                wp_cli_available=False,
                error_message=f"Unknown site: {site_name}"
            )

        site_config = P0_SITES_CONFIG[site_name]

        if validate_only:
            validation_passed = self.validate_remote_deployment(site_config)
            return RemoteDeploymentResult(
                site_name=site_name,
                success=validation_passed,
                ga4_deployed=validation_passed,
                pixel_deployed=validation_passed,
                backup_created=False,
                wp_cli_available=True,
                error_message=None if validation_passed else "Validation failed"
            )

        if backup_only:
            backup_success, backup_message = self.create_remote_backup(site_config)
            return RemoteDeploymentResult(
                site_name=site_name,
                success=backup_success,
                ga4_deployed=False,
                pixel_deployed=False,
                backup_created=backup_success,
                wp_cli_available=True,
                error_message=None if backup_success else backup_message
            )

        if not ga4_id or not pixel_id:
            return RemoteDeploymentResult(
                site_name=site_name,
                success=False,
                ga4_deployed=False,
                pixel_deployed=False,
                backup_created=False,
                wp_cli_available=False,
                error_message="GA4 ID and Pixel ID required for deployment"
            )

        result = self.deploy_analytics_via_wp_cli(site_config, ga4_id, pixel_id)
        self.results.append(result)
        return result

    def deploy_batch(self, sites_config: Dict[str, Dict[str, str]]) -> List[RemoteDeploymentResult]:
        """Deploy analytics to multiple sites from configuration."""
        results = []

        for site_name, config in sites_config.items():
            ga4_id = config.get('ga4_id')
            pixel_id = config.get('pixel_id')

            if not ga4_id or not pixel_id:
                result = RemoteDeploymentResult(
                    site_name=site_name,
                    success=False,
                    ga4_deployed=False,
                    pixel_deployed=False,
                    backup_created=False,
                    wp_cli_available=False,
                    error_message="Missing GA4 ID or Pixel ID in configuration"
                )
            else:
                result = self.deploy_to_site(site_name, ga4_id, pixel_id)

            results.append(result)

        return results

    def load_analytics_ids(self, config_file: str) -> Dict[str, Dict[str, str]]:
        """Load analytics IDs from JSON configuration file."""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)

            # Validate configuration structure
            for site_name, site_config in config.items():
                if not isinstance(site_config, dict):
                    raise ValueError(f"Invalid configuration for site {site_name}")
                if 'ga4_id' not in site_config or 'pixel_id' not in site_config:
                    raise ValueError(f"Missing ga4_id or pixel_id for site {site_name}")

            return config

        except Exception as e:
            print(f"❌ Error loading analytics IDs configuration: {str(e)}")
            sys.exit(1)

    def print_results(self, results: List[RemoteDeploymentResult]):
        """Print deployment results."""
        print(f"\n🚀 Remote GA4 & Facebook Pixel Analytics Deployment Results ({self.timestamp})")
        print("=" * 80)

        successful = 0
        for result in results:
            status = "✅ SUCCESS" if result.success else "❌ FAILED"
            print(f"\n{status} {result.site_name}")

            if result.backup_created:
                print("   📦 Backup: Created"            else:
                print("   📦 Backup: Not created"

            if result.wp_cli_available:
                print("   🔧 WP-CLI: Available"            else:
                print("   🔧 WP-CLI: Not available"

            if result.ga4_deployed:
                print("   📊 GA4: Deployed"            else:
                print("   📊 GA4: Not deployed"

            if result.pixel_deployed:
                print("   📱 Pixel: Deployed"            else:
                print("   📱 Pixel: Not deployed"

            if result.rollback_available:
                print("   🔄 Rollback: Available"            else:
                print("   🔄 Rollback: Not available"

            if result.error_message:
                print(f"   ⚠️  Error: {result.error_message}")

            if result.success:
                successful += 1

        print(f"\n📈 Summary: {successful}/{len(results)} sites deployed successfully")

        if successful == len(results):
            print("🎉 All remote deployments completed successfully!")
        elif successful > 0:
            print(f"⚠️  Partial success: {successful} sites deployed, {len(results) - successful} failed")
        else:
            print("❌ All remote deployments failed")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="GA4 and Facebook Pixel Remote Deployment Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/deploy_ga4_pixel_remote.py --site freerideinvestor.com --ga4-id G-XXXXXXXXXX --pixel-id 1234567890123456
  python tools/deploy_ga4_pixel_remote.py --all-sites --ga4-ids config/analytics_ids.json
  python tools/deploy_ga4_pixel_remote.py --site tradingrobotplug.com --backup-only
  python tools/deploy_ga4_pixel_remote.py --validate-deployment --site dadudekc.com

Configuration file format (analytics_ids.json):
{
  "freerideinvestor.com": {
    "ga4_id": "G-XXXXXXXXXX",
    "pixel_id": "1234567890123456"
  },
  "tradingrobotplug.com": {
    "ga4_id": "G-YYYYYYYYYY",
    "pixel_id": "2345678901234567"
  }
}
        """
    )

    parser.add_argument('--site', help='Deploy to specific site')
    parser.add_argument('--all-sites', action='store_true', help='Deploy to all P0 sites (requires --ga4-ids)')
    parser.add_argument('--ga4-id', help='GA4 Measurement ID for single site deployment')
    parser.add_argument('--pixel-id', help='Facebook Pixel ID for single site deployment')
    parser.add_argument('--ga4-ids', help='JSON file with analytics IDs for batch deployment')
    parser.add_argument('--backup-only', action='store_true', help='Only create backups, do not deploy')
    parser.add_argument('--validate-deployment', action='store_true', help='Only validate existing deployment')
    parser.add_argument('--quiet', action='store_true', help='Suppress detailed output')

    args = parser.parse_args()

    # Validation
    if not args.site and not args.all_sites:
        parser.error("Must specify --site <sitename> or --all-sites")

    if args.site and args.all_sites:
        parser.error("Cannot specify both --site and --all-sites")

    if args.all_sites and not args.ga4_ids:
        parser.error("--all-sites requires --ga4-ids configuration file")

    if args.site and not args.all_sites and not (args.ga4_id and args.pixel_id) and not args.backup_only and not args.validate_deployment:
        parser.error("--site requires --ga4-id and --pixel-id (or --backup-only or --validate-deployment)")

    tool = RemoteAnalyticsDeploymentTool()

    try:
        if args.all_sites:
            sites_config = tool.load_analytics_ids(args.ga4_ids)
            results = tool.deploy_batch(sites_config)
        else:
            result = tool.deploy_to_site(
                args.site,
                ga4_id=args.ga4_id,
                pixel_id=args.pixel_id,
                backup_only=args.backup_only,
                validate_only=args.validate_deployment
            )
            results = [result]

        if not args.quiet:
            tool.print_results(results)

        # Exit with success/failure code
        successful_results = [r for r in results if r.success]
        sys.exit(0 if len(successful_results) == len(results) else 1)

    except KeyboardInterrupt:
        print("\n⚠️  Remote deployment interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()