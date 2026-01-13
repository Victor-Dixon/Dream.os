#!/usr/bin/env python3
"""
Robinhood Authentication Debug Tool
====================================

Debug tool to help troubleshoot Robinhood authentication issues.

Usage:
    python tools/robinhood_debug_auth.py

This will:
1. Check your credentials
2. Attempt authentication with detailed logging
3. Help identify why manual 2FA approval isn't working
4. Provide step-by-step troubleshooting
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.trading_robot.core.robinhood_broker import RobinhoodBroker


def check_credentials():
    """Check if credentials are configured"""
    print("🔍 Checking Credentials...")
    print("-" * 30)

    username = os.getenv('ROBINHOOD_USERNAME')
    password = os.getenv('ROBINHOOD_PASSWORD')
    totp = os.getenv('ROBINHOOD_TOTP_SECRET')

    if username:
        print(f"✅ Username: {username}")
    else:
        print("❌ Username: NOT SET")
        return False

    if password:
        print("✅ Password: SET (hidden)")
    else:
        print("❌ Password: NOT SET")
        return False

    if totp:
        print("✅ TOTP: SET (automatic 2FA)")
    else:
        print("⚠️  TOTP: NOT SET (manual 2FA required)")

    return True


def test_basic_connection():
    """Test basic API connectivity"""
    print("\n🌐 Testing Basic Connection...")
    print("-" * 35)

    try:
        import robin_stocks.robinhood as rs
        print("✅ Robinhood library imported successfully")

        # Test basic API call (doesn't require auth)
        try:
            # This should work without authentication
            markets = rs.markets.get_markets()
            if markets:
                print("✅ API connectivity: GOOD")
                return True
            else:
                print("⚠️  API connectivity: LIMITED (may work with auth)")
                return True
        except Exception as e:
            print(f"❌ API connectivity: FAILED - {e}")
            return False

    except ImportError:
        print("❌ Robinhood library not installed")
        return False


def main():
    """Main debug function"""
    print("🔧 Robinhood Authentication Debug Tool")
    print("=" * 45)
    print("This tool will help identify why authentication isn't working.")
    print()

    # Check credentials
    if not check_credentials():
        print("\n❌ Fix credential issues first, then re-run this tool.")
        return 1

    # Test basic connection
    if not test_basic_connection():
        print("\n❌ Network/library issues detected.")
        return 1

    print("\n🚀 Attempting Authentication...")
    print("-" * 32)

    # Create broker and attempt authentication
    broker = RobinhoodBroker()

    if broker.is_authenticated:
        print("\n✅ SUCCESS: Authentication worked!")
        print("🎉 You can now get your real 2025 options statistics!")

        # Quick test of data retrieval
        print("\n🧪 Testing data retrieval...")
        balance = broker.get_balance()
        if "error" not in balance:
            print("✅ Balance data retrieved successfully")
        else:
            print(f"⚠️  Balance retrieval issue: {balance.get('error')}")

        stats = broker.get_2025_options_statistics()
        print(f"✅ Options stats retrieved ({stats.total_trades} trades found)")

        broker.logout()
        return 0

    else:
        print("\n❌ Authentication failed")
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print()
        print("1️⃣  CHECK YOUR ROBINHOOD APP:")
        print("   • Make sure you're logged into the app")
        print("   • Check for any 'Device Approval' notifications")
        print("   • Try closing and reopening the app")
        print()
        print("2️⃣  TRY MANUAL WEBSITE LOGIN:")
        print("   • Go to robinhood.com in a browser")
        print("   • Try logging in manually")
        print("   • This may reset any blocking")
        print()
        print("3️⃣  WAIT AND RETRY:")
        print("   • Robinhood may temporarily block automated logins")
        print("   • Wait 15-30 minutes and try again")
        print()
        print("4️⃣  CHECK CREDENTIALS:")
        print("   • Verify username and password are correct")
        print("   • Make sure you're using the right account")
        print()
        print("5️⃣  ALTERNATIVE: SET UP TOTP")
        print("   • Run: python tools/add_totp_secret.py")
        print("   • This enables automatic 2FA")
        print()
        print("🔄 Re-run this tool after trying the above steps:")
        print("   python tools/robinhood_debug_auth.py")

        return 1


if __name__ == "__main__":
    exit(main())