#!/usr/bin/env python3
"""
Test script for validation audit server wordpress health check
"""

import sys
import asyncio
sys.path.insert(0, '.')

from mcp_servers.validation_audit_server import ValidationAuditServer

async def test_wordpress_health_check():
    server = ValidationAuditServer()

    print("🔍 Testing WordPress Health Check for freerideinvestor.com")
    print("=" * 60)

    result = server._wordpress_health_check('freerideinvestor.com')

    print(f"Status: {'PASSED' if result.success else 'FAILED'}")
    print(f"Message: {result.message}")
    print()

    if result.details:
        print("Details:")
        for key, value in result.details.items():
            print(f"  {key}: {value}")
        print()

    if result.recommendations:
        print("Recommendations:")
        for rec in result.recommendations:
            print(f"  - {rec}")
        print()

    print("🔍 Testing P0 Sites Validation")
    print("=" * 60)

    report = await server.validate_p0_sites()
    print(report)

if __name__ == "__main__":
    asyncio.run(test_wordpress_health_check())