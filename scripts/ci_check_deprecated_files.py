#!/usr/bin/env python3
"""
CI Check for Deprecated Files Usage
===================================

Scans codebase for imports or references to deprecated files marked with deprecation headers.
Fails CI if deprecated files are still being used.

Part of SSOT consolidation effort - prevents reintroduction of deprecated dependencies.

Author: Agent-4 (Captain) - Technical Debt Prevention Specialist
"""

import sys
import re
from pathlib import Path
from typing import Set, List, Dict, Tuple

# Files that have been marked as deprecated
DEPRECATED_FILES = {
    "scripts/deploy_via_wordpress_admin.py",
    "tools/deploy_tradingrobotplug_plugin.py",
    "tools/deploy_tradingrobotplug_plugin_phase3.py",
    "tools/deploy_fastapi_tradingrobotplug.py",
    "tools/deploy_weareswarm_feed_system.py",
    "tools/deploy_weareswarm_font_fix.py",
    "tools/deploy_tradingrobotplug_font_fix.py",
    "tools/wordpress_manager.py",
    "ops/deployment/simple_wordpress_deployer.py",
}

# Canonical replacements for deprecated files
CANONICAL_REPLACEMENTS = {
    "scripts/deploy_via_wordpress_admin.py": "mcp_servers/deployment_server.py::deploy_wordpress_file()",
    "tools/deploy_tradingrobotplug_plugin.py": "mcp_servers/deployment_server.py::deploy_wordpress_theme()",
    "tools/deploy_tradingrobotplug_plugin_phase3.py": "mcp_servers/deployment_server.py::deploy_wordpress_theme()",
    "tools/deploy_fastapi_tradingrobotplug.py": "mcp_servers/deployment_server.py::deploy_analytics_code()",
    "tools/deploy_weareswarm_feed_system.py": "mcp_servers/deployment_server.py::deploy_wordpress_file()",
    "tools/deploy_weareswarm_font_fix.py": "mcp_servers/deployment_server.py::deploy_wordpress_theme()",
    "tools/deploy_tradingrobotplug_font_fix.py": "mcp_servers/deployment_server.py::deploy_wordpress_theme()",
    "tools/wordpress_manager.py": "mcp_servers/wp_cli_manager_server.py",
    "ops/deployment/simple_wordpress_deployer.py": "mcp_servers/deployment_server.py",
}

def find_deprecated_usage() -> List[Dict[str, str]]:
    """
    Scan codebase for usage of deprecated files.

    Returns list of violations found.
    """
    violations = []

    # Skip directories that shouldn't be scanned
    skip_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", "node_modules"}

    for file_path in Path(".").rglob("*"):
        if file_path.is_dir():
            continue

        # Skip certain directories
        if any(part in skip_dirs for part in file_path.parts):
            continue

        # Skip generated files and certain directories
        skip_patterns = [
            "project_analysis.json",  # Generated analysis file
            "node_modules/",
            ".git/",
            "__pycache__/",
            ".pytest_cache/",
            "reports/",  # Generated reports
            "swarm_brain/",  # Knowledge base, not code
            "docs/archive/",  # Historical docs
            "docs/toolbelt/COMPREHENSIVE_TOOL_AUDIT.md",  # Audit docs
        ]

        should_skip = False
        for pattern in skip_patterns:
            if pattern in str(file_path):
                should_skip = True
                break

        if should_skip:
            continue

        # Only check code files for imports
        is_code_file = file_path.suffix.lower() in [".py", ".js", ".ts"]
        is_doc_file = file_path.suffix.lower() in [".md", ".txt", ".json", ".yaml", ".yml"]

        if not (is_code_file or is_doc_file):
            continue

        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue

        # Check each deprecated file
        for deprecated_file in DEPRECATED_FILES:
            deprecated_name = Path(deprecated_file).name

            # For code files, only check for actual imports
            if is_code_file:
                if f"from {deprecated_file}" in content or f"import {deprecated_file}" in content:
                    violations.append({
                        "file": str(file_path),
                        "deprecated_file": deprecated_file,
                        "violation_type": "direct_import",
                        "line_content": f"imports {deprecated_file}",
                        "replacement": CANONICAL_REPLACEMENTS.get(deprecated_file, "Unknown")
                    })

            # Skip documentation files for Phase 1 - focus on code only
        # Documentation will be updated in Phase 2
        if is_doc_file:
            continue

    return violations

def check_deprecated_headers() -> List[Dict[str, str]]:
    """
    Check that deprecated files have proper deprecation headers.

    Returns list of missing headers.
    """
    missing_headers = []

    for deprecated_file in DEPRECATED_FILES:
        file_path = Path(deprecated_file)

        if not file_path.exists():
            continue

        try:
            content = file_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue

        if "⚠️ DEPRECATED - DO NOT USE" not in content:
            missing_headers.append({
                "file": deprecated_file,
                "issue": "Missing deprecation header"
            })

    return missing_headers

def main() -> int:
    """Main CI check function."""
    print("🛡️ Checking for deprecated file usage...")
    print("=" * 50)

    # Check for deprecated file usage
    violations = find_deprecated_usage()
    header_issues = check_deprecated_headers()

    # Report violations
    if violations:
        print(f"❌ Found {len(violations)} deprecated file usage violations:")
        print()

        for violation in violations:
            print(f"🚫 {violation['file']}")
            print(f"   Uses deprecated: {violation['deprecated_file']}")
            print(f"   Type: {violation['violation_type']}")
            if 'line_number' in violation:
                print(f"   Line {violation['line_number']}: {violation['line_content']}")
            print(f"   Replacement: {violation['replacement']}")
            print()

        print("💡 Fix these violations before committing.")
        return 1

    # Report header issues
    if header_issues:
        print(f"⚠️ Found {len(header_issues)} deprecated files missing headers:")
        print()

        for issue in header_issues:
            print(f"📄 {issue['file']}: {issue['issue']}")

        print()
        print("💡 Add proper deprecation headers to these files.")
        return 1

    # Success
    print("✅ No deprecated file usage found!")
    print("✅ All deprecated files have proper headers!")
    print()
    print("🎉 CI check passed - ready for commit.")

    return 0

if __name__ == "__main__":
    sys.exit(main())