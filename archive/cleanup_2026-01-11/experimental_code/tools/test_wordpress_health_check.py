#!/usr/bin/env python3
"""
Test WordPress Health Check Integration
=======================================

Test script to validate wordpress_health_check integration in validation-audit MCP server.
Tests the tool with configured P0 sites as required by Agent-5 assignment.

Author: Agent-5 (Business Intelligence)
Date: 2026-01-10
"""

import sys
import os
from pathlib import Path

# Add repository root to path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root))

from mcp_servers.validation_audit_server import ValidationAuditServer

def test_wordpress_health_check():
    """Test wordpress_health_check functionality on P0 sites."""
    print("🩺 Testing WordPress Health Check Integration")
    print("=" * 50)

    server = ValidationAuditServer()

    # Test each P0 site
    for site in server.p0_sites:
        print(f"\n🔍 Testing {site}...")
        result = server._wordpress_health_check(site)

        status = "✅" if result.success else "❌"
        print(f"   {status} {result.message}")

        if result.details:
            for key, value in result.details.items():
                print(f"   • {key}: {value}")

        if result.recommendations:
            print("   📋 Recommendations:")
            for rec in result.recommendations:
                print(f"   • {rec}")

    print("\n" + "=" * 50)
    print("🩺 WordPress Health Check Integration Test Complete")

if __name__ == "__main__":
    test_wordpress_health_check()