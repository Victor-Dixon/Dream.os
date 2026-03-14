#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: robinhood_auth_test module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-development-robinhood-auth-test-py
# @registry docs/recovery/recovery_registry.yaml#tools-development-robinhood-auth-test-py

"""
Robinhood Authentication Test Tool
===================================

Interactive tool to test Robinhood authentication and approval flow.

Usage:
    python tools/robinhood_auth_test.py

This will:
1. Attempt to authenticate with Robinhood
2. Guide you through manual 2FA approval if needed
3. Test basic API functionality
4. Show your account balance

Environment Variables Required:
    ROBINHOOD_USERNAME=your_username
    ROBINHOOD_PASSWORD=your_password
    ROBINHOOD_TOTP_SECRET=your_totp_secret (optional)
"""

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.trading_robot.core.robinhood_broker import RobinhoodBroker


def main():
    """Interactive Robinhood authentication test"""
    print("🔐 Robinhood Authentication Test")
    print("=" * 40)

    # Check credentials
    username = os.getenv('ROBINHOOD_USERNAME')
    password = os.getenv('ROBINHOOD_PASSWORD')

    if not username or not password:
        print("❌ Missing credentials!")
        print("Please set ROBINHOOD_USERNAME and ROBINHOOD_PASSWORD environment variables")
        return 1

    print(f"📧 Username: {username}")
    print("🔑 Password: [HIDDEN]")

    totp = os.getenv('ROBINHOOD_TOTP_SECRET')
    if totp:
        print("🔐 TOTP: Configured (automatic 2FA)")
    else:
        print("⚠️  TOTP: Not configured (manual 2FA required)")

    print("\n🚀 Starting authentication...")

    # Create broker instance
    broker = RobinhoodBroker()

    if broker.is_authenticated:
        print("\n✅ SUCCESS: Authenticated with Robinhood!")
        print("\n📊 Testing basic functionality...")

        # Test balance
        balance = broker.get_balance()
        if "error" not in balance:
            print("💰 Account Balance Retrieved Successfully")
            print(f"💵 Cash Balance: ${balance['cash']:.2f}")
            print(f"📊 Portfolio Value: ${balance['portfolio_value']:.2f}")
        else:
            print(f"❌ Balance error: {balance.get('error', 'Unknown error')}")

        # Test positions
        positions = broker.get_options_positions()
        if isinstance(positions, list) and len(positions) > 0:
            print(f"📊 Options Positions: {len(positions)} found")
        else:
            print("📊 Options Positions: None found or error")

        # Logout
        print("\n🔐 Logging out...")
        broker.logout()

        print("\n🎉 Robinhood integration test completed successfully!")
        return 0

    else:
        print("\n❌ Authentication failed")
        print("\n🔧 Troubleshooting:")
        print("1. Check your username and password")
        print("2. If using manual 2FA, make sure you approved the login request")
        print("3. Try again in a few minutes (Robinhood may have rate limits)")
        print("4. Log into robinhood.com manually first to ensure account is active")

        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
