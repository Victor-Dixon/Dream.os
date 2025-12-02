#!/usr/bin/env python3
"""
Refresh Thea Cookies
====================

Quick tool to refresh Thea authentication cookies.

Author: Agent-1
Date: 2025-01-27
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.thea.thea_service import TheaService


def main():
    """Refresh Thea cookies."""
    print("🔄 THEA COOKIE REFRESH")
    print("=" * 70)
    print()
    
    thea = TheaService()
    
    print("🍪 Checking current cookie status...")
    if thea.are_cookies_fresh():
        print("✅ Cookies are fresh")
        
        if thea.validate_cookies():
            print("✅ Cookies are valid")
            print("\n✅ No refresh needed!")
            return 0
        else:
            print("⚠️ Cookies exist but are invalid")
    else:
        print("⚠️ Cookies are stale or missing")
    
    print("\n🔄 Refreshing cookies...")
    print("⏳ Browser will open - please log in manually if needed...")
    print()
    
    if thea.refresh_cookies():
        print("\n✅ Cookies refreshed successfully!")
        print("✅ Ready for Thea code reviews")
        return 0
    else:
        print("\n❌ Failed to refresh cookies")
        print("💡 Try running: python tools/thea/setup_thea_cookies.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())

