#!/usr/bin/env python3
"""
Check .htaccess File for freerideinvestor.com
==============================================

Examines .htaccess file for syntax errors or issues that could cause HTTP 500.

Author: Agent-7 (Web Development Specialist)
V2 Compliant: <300 lines
"""

import sys
import json
import paramiko
import re
from pathlib import Path
from typing import List, Dict

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def check_htaccess(site_key: str = "freerideinvestor") -> Dict:
    """Check .htaccess file for issues."""
    # Load site config
    config_file = project_root / ".deploy_credentials" / "sites.json"
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        return {}

    with open(config_file) as f:
        sites = json.load(f)
        config = sites.get(site_key, {})

    if not config:
        print(f"❌ Site '{site_key}' not found in config")
        return {}

    host = config.get("host")
    port = config.get("port", 65002)
    username = config.get("username")
    password = config.get("password")
    remote_path = config.get("remote_path", "")

    if not all([host, username, password]):
        print(f"❌ Missing SFTP credentials for {site_key}")
        return {}

    # Connect to SFTP
    try:
        transport = paramiko.Transport((host, port))
        transport.banner_timeout = 10
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print(f"✅ Connected to SFTP: {host}:{port}")
    except Exception as e:
        print(f"❌ SFTP connection failed: {e}")
        return {}

    # Find .htaccess
    htaccess_paths = [
        f"{remote_path}/.htaccess".lstrip('/'),
        ".htaccess",
        "public_html/.htaccess",
        f"domains/{site_key}.com/public_html/.htaccess"
    ]

    htaccess_path = None
    for path in htaccess_paths:
        try:
            sftp.stat(path)
            htaccess_path = path
            print(f"✅ Found .htaccess: {path}")
            break
        except FileNotFoundError:
            continue

    if not htaccess_path:
        print("⚠️  .htaccess not found (may be normal)")
        sftp.close()
        transport.close()
        return {"found": False}

    # Read .htaccess
    try:
        with sftp.open(htaccess_path, 'r') as f:
            content = f.read().decode('utf-8')
    except Exception as e:
        print(f"❌ Error reading .htaccess: {e}")
        sftp.close()
        transport.close()
        return {"error": str(e)}

    sftp.close()
    transport.close()

    # Analyze .htaccess
    issues = []
    warnings = []

    # Check for common syntax issues
    lines = content.split('\n')
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        # Check for unclosed directives
        if re.match(r'^<IfModule', stripped) and '</IfModule>' not in content[content.find(line):]:
            issues.append(f"Line {i}: Potentially unclosed <IfModule> directive")

        # Check for malformed RewriteRule
        if stripped.startswith('RewriteRule') and not re.match(r'^RewriteRule\s+\S+\s+\S+', stripped):
            issues.append(f"Line {i}: Malformed RewriteRule: {stripped[:50]}")

        # Check for php_value/php_flag (may not work on shared hosting)
        if 'php_value' in stripped or 'php_flag' in stripped:
            warnings.append(f"Line {i}: php_value/php_flag may not work on shared hosting: {stripped[:50]}")

    # Check for WordPress standard structure
    if "# BEGIN WordPress" not in content:
        warnings.append("Missing WordPress BEGIN marker - may be custom .htaccess")

    if "# END WordPress" not in content:
        warnings.append("Missing WordPress END marker - may be custom .htaccess")

    result = {
        "found": True,
        "path": htaccess_path,
        "content": content,
        "line_count": len(lines),
        "issues": issues,
        "warnings": warnings,
        "size_bytes": len(content.encode('utf-8'))
    }

    print(f"\n📊 .htaccess Analysis:")
    print(f"   Lines: {result['line_count']}")
    print(f"   Size: {result['size_bytes']} bytes")
    print(f"   Issues: {len(issues)}")
    print(f"   Warnings: {len(warnings)}")

    if issues:
        print(f"\n⚠️  Issues Found:")
        for issue in issues:
            print(f"   - {issue}")

    if warnings:
        print(f"\n💡 Warnings:")
        for warning in warnings:
            print(f"   - {warning}")

    if not issues and not warnings:
        print("\n✅ No obvious syntax issues found in .htaccess")

    return result


def main():
    """Main execution."""
    print("🔍 Checking .htaccess for freerideinvestor.com")
    print("=" * 60)
    
    result = check_htaccess("freerideinvestor")
    
    if result.get("issues"):
        print("\n💡 Recommendation: Temporarily rename .htaccess to test if it's causing the 500 error")
        print("   If site works without .htaccess, there's a syntax error in the file")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

