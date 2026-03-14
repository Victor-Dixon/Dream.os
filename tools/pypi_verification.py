#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: pypi_verification module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-pypi-verification-py
# @registry docs/recovery/recovery_registry.yaml#tools-pypi-verification-py

"""
PyPI Package Verification Tool
==============================

Automated verification tool for PyPI package publishing success.

Usage:
    python tools/pypi_verification.py --package agent-cellphone-v2 --version 2.1.0

Author: Agent-4 (QA & Verification Specialist)
Date: 2026-01-12
"""

import argparse
import json
import sys
import time
from typing import Dict, Any, Optional
import urllib.request
import urllib.error


class PyPIVerificationTool:
    """Tool for verifying PyPI package publishing success."""

    def __init__(self):
        self.pypi_api_base = "https://pypi.org/pypi"
        self.max_retries = 10
        self.retry_delay = 30  # seconds

    def verify_package_exists(self, package_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """
        Verify that a package exists on PyPI.

        Args:
            package_name: Name of the package to verify
            version: Specific version to check (optional)

        Returns:
            Dictionary with verification results
        """
        url = f"{self.pypi_api_base}/{package_name}/json"
        if version:
            url = f"{self.pypi_api_base}/{package_name}/{version}/json"

        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

            return {
                'status': 'success',
                'package': package_name,
                'version': data['info']['version'],
                'url': f"https://pypi.org/project/{package_name}/",
                'data': data
            }

        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {
                    'status': 'not_found',
                    'package': package_name,
                    'version': version,
                    'error': 'Package/version not found on PyPI'
                }
            else:
                return {
                    'status': 'error',
                    'package': package_name,
                    'version': version,
                    'error': f'HTTP {e.code}: {e.reason}'
                }

        except Exception as e:
            return {
                'status': 'error',
                'package': package_name,
                'version': version,
                'error': str(e)
            }

    def wait_for_publishing(self, package_name: str, version: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Wait for package publishing to complete.

        Args:
            package_name: Name of the package
            version: Version to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Verification results
        """
        start_time = time.time()
        attempts = 0

        print(f"🔍 Waiting for {package_name} v{version} to appear on PyPI...")
        print(f"⏱️  Timeout: {timeout} seconds")

        while time.time() - start_time < timeout:
            attempts += 1
            result = self.verify_package_exists(package_name, version)

            if result['status'] == 'success':
                elapsed = time.time() - start_time
                print(f"✅ SUCCESS: {package_name} v{version} found on PyPI after {elapsed:.1f} seconds")
                return result

            elif attempts % 5 == 0:  # Log progress every 5 attempts
                elapsed = time.time() - start_time
                print(f"⏳ Still waiting... ({elapsed:.1f}s elapsed, attempt {attempts})")

            time.sleep(self.retry_delay)

        elapsed = time.time() - start_time
        print(f"❌ TIMEOUT: {package_name} v{version} not found within {elapsed:.1f} seconds")
        return {
            'status': 'timeout',
            'package': package_name,
            'version': version,
            'error': f'Publishing verification timed out after {elapsed:.1f} seconds'
        }

    def generate_verification_report(self, result: Dict[str, Any]) -> str:
        """Generate a human-readable verification report."""
        if result['status'] == 'success':
            return f"""
🎉 PyPI PUBLISHING VERIFICATION SUCCESS!

📦 Package: {result['package']}
🏷️  Version: {result['version']}
🔗 URL: {result['url']}

✅ Package successfully published and available for installation
   pip install {result['package']}=={result['version']}
"""
        else:
            return f"""
❌ PyPI PUBLISHING VERIFICATION FAILED!

📦 Package: {result.get('package', 'Unknown')}
🏷️  Version: {result.get('version', 'Unknown')}
❌ Status: {result['status']}
💥 Error: {result.get('error', 'Unknown error')}

🔍 Check PyPI credentials and publishing process
"""


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="PyPI Package Verification Tool")
    parser.add_argument('--package', required=True, help='Package name to verify')
    parser.add_argument('--version', help='Specific version to check')
    parser.add_argument('--wait', action='store_true', help='Wait for publishing to complete')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout for waiting (seconds)')

    args = parser.parse_args()

    tool = PyPIVerificationTool()

    if args.wait and args.version:
        result = tool.wait_for_publishing(args.package, args.version, args.timeout)
    else:
        result = tool.verify_package_exists(args.package, args.version)

    report = tool.generate_verification_report(result)
    print(report)

    # Exit with appropriate code
    if result['status'] == 'success':
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
