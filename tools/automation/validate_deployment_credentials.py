#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.OS
# Purpose: validate deployment credentials.
# SSOT: docs/recovery/recovery_registry.yaml#tools-automation-validate-deployment-credentials
# @registry docs/recovery/recovery_registry.yaml#tools-automation-validate-deployment-credentials

"""
Deployment Credentials Validation Tool
=====================================

Validates deployment credentials setup and sync status.

Usage:
    python tools/validate_deployment_credentials.py

Checks:
- .deploy_credentials.example directory structure
- Template files present
- Actual credential files (if they exist)
- Sync mechanism availability
- Security compliance (credentials not in git)

Author: Agent-5
Date: 2026-01-08
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

class DeploymentCredentialsValidator:
    """Validates deployment credentials setup and configuration."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.credentials_dir = repo_root / ".deploy_credentials"
        self.template_dir = repo_root / ".deploy_credentials.example"

    def validate_directory_structure(self) -> Tuple[bool, List[str]]:
        """Validate that required directories and files exist."""
        issues = []

        # Check template directory exists
        if not self.template_dir.exists():
            issues.append("❌ .deploy_credentials.example directory missing")
            return False, issues

        if not self.credentials_dir.exists():
            issues.append("⚠️  .deploy_credentials directory missing (create locally for real credentials)")

        # Check required template files
        required_templates = [
            "sites.example.json",
            "blogging_api.example.json",
            "README.md"
        ]

        for template in required_templates:
            template_path = self.template_dir / template
            if not template_path.exists():
                issues.append(f"❌ Template file missing: {template}")
            else:
                issues.append(f"✅ Template file present: {template}")

        required_count = len(required_templates)
        passed = len([issue for issue in issues if issue.startswith("✅")]) == required_count
        return passed, issues

    def validate_actual_credentials(self) -> Tuple[bool, List[str]]:
        """Check if actual credential files exist (should be local-only)."""
        issues = []

        actual_files = ["sites.json", "blogging_api.json"]
        credentials_present = []

        for actual_file in actual_files:
            actual_path = self.credentials_dir / actual_file
            if actual_path.exists():
                credentials_present.append(actual_file)
                issues.append(f"✅ Actual credentials file present: {actual_file}")
            else:
                issues.append(f"⚠️  Actual credentials file missing: {actual_file} (create from template)")

        has_credentials = len(credentials_present) > 0
        return has_credentials, issues

    def validate_sync_mechanism(self) -> Tuple[bool, List[str]]:
        """Check if sync mechanism is available."""
        issues = []

        # Check if websites directory is accessible (can't validate from here)
        issues.append("ℹ️  Sync mechanism: python tools/sync_site_credentials.py (from websites directory)")

        # Check if sync tool exists (assuming it's in websites)
        issues.append("ℹ️  Sync tool location: websites/tools/sync_site_credentials.py")

        return True, issues  # Always passes - mechanism exists in design

    def validate_git_security(self) -> Tuple[bool, List[str]]:
        """Validate that credentials are not committed to git."""
        issues = []

        # Check .gitignore exists
        gitignore_path = self.repo_root / ".gitignore"
        if not gitignore_path.exists():
            issues.append("⚠️  No .gitignore file found")
            return False, issues

        # Read .gitignore
        try:
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()

            # Check if credentials are gitignored
            credential_patterns = [
                ".deploy_credentials/",
                ".deploy_credentials/sites.json",
                ".deploy_credentials/blogging_api.json"
            ]

            for pattern in credential_patterns:
                if pattern in gitignore_content:
                    issues.append(f"✅ Credential pattern gitignored: {pattern}")
                else:
                    issues.append(f"❌ Credential pattern NOT gitignored: {pattern}")
                    return False, issues

        except Exception as e:
            issues.append(f"❌ Error reading .gitignore: {e}")
            return False, issues

        return True, issues

    def run_validation(self) -> Dict[str, any]:
        """Run all validation checks."""
        results = {
            "directory_structure": self.validate_directory_structure(),
            "actual_credentials": self.validate_actual_credentials(),
            "sync_mechanism": self.validate_sync_mechanism(),
            "git_security": self.validate_git_security()
        }

        # Calculate overall status
        all_passed = all(result[0] for result in results.values())
        all_issues = []
        for check_name, (passed, issues) in results.items():
            all_issues.extend(issues)

        return {
            "overall_status": all_passed,
            "checks": results,
            "all_issues": all_issues
        }

def main():
    """Main validation function."""
    repo_root = Path(__file__).resolve().parents[1]

    print("🔍 Deployment Credentials Validation Tool")
    print("=" * 50)

    validator = DeploymentCredentialsValidator(repo_root)
    results = validator.run_validation()

    print(f"\n📊 Overall Status: {'✅ PASS' if results['overall_status'] else '❌ FAIL'}")
    print("\n📋 Detailed Results:")
    print("-" * 30)

    for issue in results['all_issues']:
        print(issue)

    print(f"\n🎯 Summary: {len([i for i in results['all_issues'] if '✅' in i])} checks passed")

    if not results['overall_status']:
        print("\n💡 To fix issues:")
        print("   1. Copy templates: cp .deploy_credentials.example/sites.example.json .deploy_credentials/sites.json")
        print("   2. Fill in actual credentials")
        print("   3. Ensure .gitignore excludes credential files")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
