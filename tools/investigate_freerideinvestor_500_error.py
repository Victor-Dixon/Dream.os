#!/usr/bin/env python3
"""
Investigate freerideinvestor.com HTTP 500 Error
================================================

Diagnoses HTTP 500 error by checking:
- WordPress error logs (debug.log)
- PHP compatibility and version
- Plugin/theme conflicts
- .htaccess issues
- wp-config.php errors

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import sys
import json
import paramiko
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


class WordPress500Investigator:
    """Investigates HTTP 500 errors on WordPress sites."""

    def __init__(self, site_key: str = "freerideinvestor"):
        """Initialize investigator."""
        self.site_key = site_key
        self.config = self._load_site_config()
        self.sftp_client = None
        self.findings = {
            "site_url": f"https://{site_key}.com" if not site_key.endswith('.com') else f"https://{site_key}",
            "timestamp": datetime.now().isoformat(),
            "http_status": None,
            "debug_log": None,
            "php_version": None,
            "php_errors": [],
            "wp_config_issues": [],
            "htaccess_issues": [],
            "plugin_conflicts": [],
            "recommendations": []
        }

    def _load_site_config(self) -> Dict:
        """Load site configuration."""
        config_file = project_root / ".deploy_credentials" / "sites.json"
        if config_file.exists():
            with open(config_file) as f:
                sites = json.load(f)
                return sites.get(self.site_key, {})
        return {}

    def connect_sftp(self) -> bool:
        """Connect to SFTP server."""
        try:
            host = self.config.get("host")
            port = self.config.get("port", 65002)
            username = self.config.get("username")
            password = self.config.get("password")

            if not all([host, username, password]):
                print(f"❌ Missing SFTP credentials for {self.site_key}")
                return False

            transport = paramiko.Transport((host, port))
            transport.banner_timeout = 10
            transport.connect(username=username, password=password)
            self.sftp_client = paramiko.SFTPClient.from_transport(transport)
            print(f"✅ Connected to SFTP: {host}:{port}")
            return True

        except Exception as e:
            print(f"❌ SFTP connection failed: {e}")
            return False

    def disconnect_sftp(self):
        """Disconnect from SFTP."""
        if self.sftp_client:
            self.sftp_client.close()
            self.sftp_client = None

    def check_http_status(self) -> Dict:
        """Check current HTTP status."""
        url = self.findings["site_url"]
        try:
            response = requests.get(url, timeout=10, verify=False, allow_redirects=False)
            self.findings["http_status"] = response.status_code
            print(f"📊 HTTP Status: {response.status_code}")
            return {"status": response.status_code, "headers": dict(response.headers)}
        except Exception as e:
            print(f"❌ HTTP check failed: {e}")
            return {"status": None, "error": str(e)}

    def read_debug_log(self) -> Optional[str]:
        """Read WordPress debug.log file."""
        if not self.sftp_client:
            return None

        debug_log_paths = [
            "wp-content/debug.log",
            "public_html/wp-content/debug.log",
            f"{self.config.get('remote_path', '')}/wp-content/debug.log".lstrip('/')
        ]

        for log_path in debug_log_paths:
            try:
                with self.sftp_client.open(log_path, 'r') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    # Get last 100 lines
                    lines = content.split('\n')
                    recent_lines = '\n'.join(lines[-100:]) if len(lines) > 100 else content
                    self.findings["debug_log"] = recent_lines
                    print(f"✅ Found debug.log: {log_path}")
                    print(f"   Last {min(100, len(lines))} lines retrieved")
                    return recent_lines
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️  Error reading {log_path}: {e}")
                continue

        print("⚠️  debug.log not found (debug mode may not be enabled)")
        return None

    def check_php_errors(self) -> List[str]:
        """Check for PHP errors in debug log."""
        errors = []
        if not self.findings.get("debug_log"):
            return errors

        log_content = self.findings["debug_log"]
        error_patterns = [
            "Fatal error",
            "Parse error",
            "Warning:",
            "Notice:",
            "Call to undefined",
            "Cannot redeclare",
            "Maximum execution time",
            "Allowed memory size",
            "plugin.*error",
            "theme.*error"
        ]

        for line in log_content.split('\n'):
            for pattern in error_patterns:
                if pattern.lower() in line.lower():
                    errors.append(line.strip())
                    break

        if errors:
            print(f"⚠️  Found {len(errors)} PHP errors in debug.log")
            self.findings["php_errors"] = errors[:20]  # Limit to 20 most recent
        else:
            print("✅ No PHP errors found in debug.log")

        return errors

    def check_wp_config(self) -> List[str]:
        """Check wp-config.php for common issues."""
        if not self.sftp_client:
            return []

        issues = []
        wp_config_paths = [
            "wp-config.php",
            "public_html/wp-config.php",
            f"{self.config.get('remote_path', '')}/wp-config.php".lstrip('/')
        ]

        for config_path in wp_config_paths:
            try:
                with self.sftp_client.open(config_path, 'r') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    
                    # Check for debug mode
                    if "WP_DEBUG" not in content:
                        issues.append("WP_DEBUG not defined - debug logging disabled")
                    
                    # Check memory limit
                    if "WP_MEMORY_LIMIT" not in content:
                        issues.append("WP_MEMORY_LIMIT not set - using PHP default")
                    
                    # Check for syntax errors (basic check)
                    if content.count("<?php") != 1:
                        issues.append("Potential syntax issue: Multiple <?php tags or missing opening tag")
                    
                    print(f"✅ Read wp-config.php: {config_path}")
                    self.findings["wp_config_issues"] = issues
                    return issues

            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️  Error reading wp-config.php: {e}")
                return [f"Error reading wp-config.php: {e}"]

        print("⚠️  wp-config.php not found")
        return []

    def check_htaccess(self) -> List[str]:
        """Check .htaccess for issues."""
        if not self.sftp_client:
            return []

        issues = []
        htaccess_paths = [
            ".htaccess",
            "public_html/.htaccess",
            f"{self.config.get('remote_path', '')}/.htaccess".lstrip('/')
        ]

        for htaccess_path in htaccess_paths:
            try:
                with self.sftp_client.open(htaccess_path, 'r') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                    
                    # Check for common issues
                    if "RewriteEngine On" in content and "RewriteBase" not in content:
                        issues.append("RewriteEngine On without RewriteBase may cause issues")
                    
                    # Check for PHP version directives
                    if "php_value" in content or "php_flag" in content:
                        issues.append("php_value/php_flag directives may not work (check hosting support)")
                    
                    print(f"✅ Read .htaccess: {htaccess_path}")
                    self.findings["htaccess_issues"] = issues
                    return issues

            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"⚠️  Error reading .htaccess: {e}")
                return []

        print("⚠️  .htaccess not found (may be normal)")
        return []

    def check_php_version(self) -> Optional[str]:
        """Check PHP version via phpinfo or wp-config."""
        # Try to create a temporary phpinfo file
        if not self.sftp_client:
            return None

        # Alternative: Check via WordPress REST API or check wp-config for PHP version requirements
        # For now, return None and recommend manual check
        print("💡 PHP version check: Recommend checking via hosting control panel")
        return None

    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on findings."""
        recommendations = []

        if self.findings["http_status"] == 500:
            recommendations.append("HTTP 500 error confirmed - server-side issue")

        if self.findings.get("php_errors"):
            recommendations.append(f"Found {len(self.findings['php_errors'])} PHP errors - review debug.log")

        if not self.findings.get("debug_log"):
            recommendations.append("Enable WordPress debug mode: Add to wp-config.php:")
            recommendations.append("  define('WP_DEBUG', true);")
            recommendations.append("  define('WP_DEBUG_LOG', true);")
            recommendations.append("  define('WP_DEBUG_DISPLAY', false);")

        if self.findings.get("wp_config_issues"):
            recommendations.append("Review wp-config.php issues identified above")

        if self.findings.get("htaccess_issues"):
            recommendations.append("Review .htaccess - consider temporarily renaming to test")

        recommendations.append("Check hosting error logs in control panel")
        recommendations.append("Verify PHP version compatibility (WordPress requires PHP 7.4+)")
        recommendations.append("Check plugin/theme conflicts - disable all plugins to test")
        recommendations.append("Increase PHP memory limit if needed: define('WP_MEMORY_LIMIT', '256M');")

        self.findings["recommendations"] = recommendations
        return recommendations

    def generate_report(self) -> str:
        """Generate investigation report."""
        report = ["# 🔍 freerideinvestor.com HTTP 500 Error Investigation", ""]
        report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Site**: {self.findings['site_url']}")
        report.append("")

        report.append("## 📊 Status Check")
        report.append(f"**HTTP Status**: {self.findings.get('http_status', 'Unknown')}")
        report.append("")

        if self.findings.get("debug_log"):
            report.append("## 📝 Debug Log Analysis")
            report.append(f"**Log Found**: ✅ Yes")
            if self.findings.get("php_errors"):
                report.append(f"**PHP Errors Found**: {len(self.findings['php_errors'])}")
                report.append("")
                report.append("### Recent Errors:")
                for error in self.findings["php_errors"][:10]:
                    report.append(f"- `{error[:100]}...`")
            else:
                report.append("**PHP Errors**: None found")
            report.append("")
        else:
            report.append("## 📝 Debug Log")
            report.append("**Status**: ⚠️ Not found or debug mode disabled")
            report.append("")

        if self.findings.get("wp_config_issues"):
            report.append("## ⚙️ wp-config.php Issues")
            for issue in self.findings["wp_config_issues"]:
                report.append(f"- {issue}")
            report.append("")

        if self.findings.get("htaccess_issues"):
            report.append("## 📄 .htaccess Issues")
            for issue in self.findings["htaccess_issues"]:
                report.append(f"- {issue}")
            report.append("")

        report.append("## 💡 Recommendations")
        for rec in self.findings["recommendations"]:
            report.append(f"- {rec}")
        report.append("")

        return "\n".join(report)


def main():
    """Main investigation."""
    print("🔍 Investigating freerideinvestor.com HTTP 500 Error")
    print("=" * 60)
    print()

    investigator = WordPress500Investigator("freerideinvestor")

    # Step 1: Check HTTP status
    print("STEP 1: Checking HTTP Status")
    print("-" * 60)
    investigator.check_http_status()
    print()

    # Step 2: Connect SFTP
    print("STEP 2: Connecting to SFTP")
    print("-" * 60)
    if not investigator.connect_sftp():
        print("❌ Cannot proceed without SFTP connection")
        return 1
    print()

    # Step 3: Read debug log
    print("STEP 3: Reading WordPress Debug Log")
    print("-" * 60)
    investigator.read_debug_log()
    print()

    # Step 4: Check PHP errors
    if investigator.findings.get("debug_log"):
        print("STEP 4: Analyzing PHP Errors")
        print("-" * 60)
        investigator.check_php_errors()
        print()

    # Step 5: Check wp-config.php
    print("STEP 5: Checking wp-config.php")
    print("-" * 60)
    investigator.check_wp_config()
    print()

    # Step 6: Check .htaccess
    print("STEP 6: Checking .htaccess")
    print("-" * 60)
    investigator.check_htaccess()
    print()

    # Step 7: Generate recommendations
    print("STEP 7: Generating Recommendations")
    print("-" * 60)
    investigator.generate_recommendations()
    for rec in investigator.findings["recommendations"][:5]:
        print(f"   • {rec}")
    print()

    # Generate and save report
    report = investigator.generate_report()
    report_file = project_root / f"FREERIDEINVESTOR_500_ERROR_INVESTIGATION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_file, 'w') as f:
        f.write(report)

    print("=" * 60)
    print("✅ INVESTIGATION COMPLETE")
    print("=" * 60)
    print(f"📄 Report saved: {report_file}")
    print()

    investigator.disconnect_sftp()

    return 0


if __name__ == "__main__":
    sys.exit(main())

