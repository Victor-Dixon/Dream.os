#!/usr/bin/env python3
"""
<!-- SSOT Domain: infrastructure -->
SFTP Connection Validation Tool for Swarm Websites

Validates SFTP connections and paths for all swarm websites to ensure
WordPress deployment infrastructure is working correctly.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional

try:
    import paramiko
    HAS_PARAMIKO = True
except ImportError:
    HAS_PARAMIKO = False
    print("ERROR: paramiko not installed. Install with: pip install paramiko")
    sys.exit(1)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SFTPValidator:
    """Validates SFTP connections and paths for swarm websites"""

    def __init__(self, creds_file: str = "D:/Agent_Cellphone_V2_Repository/.deploy_credentials/sites.json"):
        self.creds_file = Path(creds_file)
        self.credentials = {}
        self.load_credentials()

    def load_credentials(self):
        """Load credentials from sites.json"""
        if not self.creds_file.exists():
            logger.error(f"Credentials file not found: {self.creds_file}")
            return

        try:
            with open(self.creds_file, 'r') as f:
                self.credentials = json.load(f)
            logger.info(f"Loaded credentials for {len(self.credentials)} sites")
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")

    def validate_connection(self, site_key: str) -> Dict:
        """Validate SFTP connection for a specific site"""
        if site_key not in self.credentials:
            return {
                "site": site_key,
                "status": "ERROR",
                "error": f"No credentials found for {site_key}"
            }

        creds = self.credentials[site_key]
        logger.info(f"Testing connection to {site_key}...")

        try:
            # Create SSH client
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect
            client.connect(
                hostname=creds["host"],
                username=creds["username"],
                password=creds["password"],
                port=creds.get("port", 22),
                timeout=10
            )

            # Test SFTP
            sftp = client.open_sftp()

            # Test directory access
            remote_path = creds.get("remote_path", "")
            if remote_path:
                try:
                    sftp.listdir(remote_path)
                    dir_exists = True
                except IOError:
                    dir_exists = False

                # Test file creation (safe test)
                test_file = f"{remote_path}/sftp_test.tmp"
                try:
                    with sftp.file(test_file, 'w') as f:
                        f.write("test")
                    sftp.remove(test_file)  # Clean up
                    write_access = True
                except Exception:
                    write_access = False
            else:
                dir_exists = False
                write_access = False

            client.close()

            return {
                "site": site_key,
                "status": "SUCCESS" if dir_exists and write_access else "WARNING",
                "connection": True,
                "directory_exists": dir_exists,
                "write_access": write_access,
                "remote_path": remote_path,
                "details": f"Dir: {'✓' if dir_exists else '✗'}, Write: {'✓' if write_access else '✗'}"
            }

        except Exception as e:
            return {
                "site": site_key,
                "status": "ERROR",
                "connection": False,
                "error": str(e)
            }

    def validate_all_sites(self) -> List[Dict]:
        """Validate all sites in credentials file"""
        results = []
        target_sites = [
            "southwestsecret.com", "prismblossom.online", "freerideinvestor",
            "ariajet.site", "weareswarm.online", "weareswarm.site"
        ]

        for site in target_sites:
            if site in self.credentials:
                result = self.validate_connection(site)
                results.append(result)
                logger.info(f"{site}: {result['status']} - {result.get('details', result.get('error', ''))}")
            else:
                results.append({
                    "site": site,
                    "status": "ERROR",
                    "error": "No credentials configured"
                })
                logger.error(f"{site}: ERROR - No credentials configured")

        return results

    def generate_report(self, results: List[Dict]) -> str:
        """Generate a comprehensive validation report"""
        report = "# 🐝 SFTP Connection Validation Report\n\n"
        report += f"**Validation Time:** {json.dumps(results[0].get('timestamp', 'N/A'), indent=2) if results else 'N/A'}\n\n"

        success_count = sum(1 for r in results if r["status"] == "SUCCESS")
        warning_count = sum(1 for r in results if r["status"] == "WARNING")
        error_count = sum(1 for r in results if r["status"] == "ERROR")

        report += f"**Summary:** {success_count} ✓, {warning_count} ⚠️, {error_count} ❌\n\n"

        for result in results:
            status_emoji = {"SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌"}.get(result["status"], "❓")
            report += f"## {status_emoji} {result['site']}\n"
            report += f"**Status:** {result['status']}\n"

            if result["status"] == "SUCCESS":
                report += f"**Connection:** ✅\n"
                report += f"**Directory Access:** {'✅' if result.get('directory_exists') else '❌'}\n"
                report += f"**Write Access:** {'✅' if result.get('write_access') else '❌'}\n"
                report += f"**Remote Path:** {result.get('remote_path', 'N/A')}\n"
            elif result["status"] == "WARNING":
                report += f"**Connection:** ✅\n"
                report += f"**Directory Access:** {'✅' if result.get('directory_exists') else '❌'}\n"
                report += f"**Write Access:** {'✅' if result.get('write_access') else '❌'}\n"
                report += f"**Issue:** Limited permissions or missing directories\n"
            else:
                report += f"**Error:** {result.get('error', 'Unknown error')}\n"

            report += "\n"

        # Recommendations
        report += "## 📋 Recommendations\n\n"
        if error_count > 0:
            report += "❌ **Critical Issues to Fix:**\n"
            for result in results:
                if result["status"] == "ERROR":
                    report += f"- {result['site']}: {result.get('error', 'Connection failed')}\n"
            report += "\n"

        if warning_count > 0:
            report += "⚠️ **Permission Issues to Address:**\n"
            for result in results:
                if result["status"] == "WARNING":
                    report += f"- {result['site']}: Check directory permissions and ownership\n"
            report += "\n"

        if success_count == len(results):
            report += "✅ **All sites validated successfully!**\n"
            report += "WordPress deployment infrastructure is ready.\n"

        return report

def main():
    """CLI interface for SFTP validation"""
    import argparse

    parser = argparse.ArgumentParser(description="🐝 SFTP Connection Validator for Swarm Websites")
    parser.add_argument("--site", help="Validate specific site")
    parser.add_argument("--all", action="store_true", help="Validate all sites")
    parser.add_argument("--report", action="store_true", help="Generate detailed report")
    parser.add_argument("--creds", default="D:/Agent_Cellphone_V2_Repository/.deploy_credentials/sites.json",
                       help="Path to credentials file")

    args = parser.parse_args()

    validator = SFTPValidator(args.creds)

    if args.site:
        result = validator.validate_connection(args.site)
        print(json.dumps(result, indent=2))
    elif args.all or args.report:
        results = validator.validate_all_sites()
        if args.report:
            print(validator.generate_report(results))
        else:
            print(json.dumps(results, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
