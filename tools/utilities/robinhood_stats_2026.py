#!/usr/bin/env python3
# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: robinhood_stats_2026 module.
# SSOT: docs/recovery/recovery_registry.yaml#tools-utilities-robinhood-stats-2026-py
# @registry docs/recovery/recovery_registry.yaml#tools-utilities-robinhood-stats-2026-py

"""
Robinhood 2026 Options Statistics Tool
=======================================

Get real 2026 options trading statistics and account balance from Robinhood.

Usage:
    python tools/robinhood_stats_2026.py

Environment Variables Required:
    ROBINHOOD_USERNAME=your_username
    ROBINHOOD_PASSWORD=your_password
    ROBINHOOD_TOTP_SECRET=your_totp_secret (optional)

Safety Features:
- Read-only access (no trading)
- Emergency stop mechanisms
- Daily loss limit monitoring
- Position size caps

Author: Agent-2 (dream.os)
Date: 2026-01-07
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.trading_robot.core.robinhood_broker import (
    RobinhoodBroker,
    format_balance,
    format_options_stats
)
from src.core.config.config_manager import UnifiedConfigManager


def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['ROBINHOOD_USERNAME', 'ROBINHOOD_PASSWORD']
    optional_vars = ['ROBINHOOD_TOTP_SECRET']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var, '').strip():
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Set these in your .env file or environment")
        print("\nExample .env entries:")
        print("ROBINHOOD_USERNAME=your_email@example.com")
        print("ROBINHOOD_PASSWORD=your_password")
        print("ROBINHOOD_TOTP_SECRET=your_totp_secret_from_authenticator_app  # Recommended")
        print("\n🔐 If you don't set ROBINHOOD_TOTP_SECRET, you'll need to manually")
        print("   approve login requests in your Robinhood app/browser.")
        return False

    # Show optional vars status
    totp_set = bool(os.getenv('ROBINHOOD_TOTP_SECRET', '').strip())
    if totp_set:
        print("✅ TOTP secret configured (automatic 2FA)")
    else:
        print("⚠️  TOTP secret not set (manual 2FA required)")

    return True


def main():
    """Main function to get Robinhood statistics"""
    print("🚀 Robinhood 2026 Options Statistics Tool")
    print("=" * 50)

    setup_logging()

    # Check environment
    if not check_environment():
        return 1

    # Check if running interactively
    import sys
    if not sys.stdin.isatty():
        print("❌ INTERACTIVE MODE REQUIRED")
        print("   This tool requires manual 2FA approval from Robinhood app.")
        print("   Please run directly in your terminal:")
        print(f"   python {sys.argv[0]}")
        print("   Or:")
        print("   cd D:\\Agent_Cellphone_V2_Repository")
        print("   python tools/robinhood_stats_2026.py")
        return 1

    try:
        # Create Robinhood broker
        print("🔐 Connecting to Robinhood...")
        broker = RobinhoodBroker()

        # Manual approval flow for 2FA
        if not broker.is_authenticated:
            print("\n🔐 MANUAL 2FA APPROVAL REQUIRED:")
            print("   1. Open your Robinhood app on your phone")
            print("   2. Look for a 'Device Approval' or 'Login Request' notification")
            print("   3. Approve the login request in the app")
            print("   4. Press Enter here after you've approved the login...")

            try:
                input("\nPress Enter after approving login in Robinhood app: ")
                print("   ✅ Approval confirmed, checking login status...")

                # Try to connect again after approval
                if broker._initialize_connection():
                    print("✅ Connected successfully after manual approval")
                else:
                    print("❌ Still failed to authenticate after manual approval")
                    print("   Check your credentials and try again")
                    return 1

            except KeyboardInterrupt:
                print("\n⚠️  Manual approval cancelled by user")
                return 1

        print("✅ Connected successfully")

        # Get account balance
        print("\n📊 Retrieving account balance...")
        balance = broker.get_balance()

        if "error" in balance:
            print(f"❌ Balance retrieval failed: {balance['error']}")
            return 1

        print(format_balance(balance))

        # Get 2025 options statistics
        print("📈 Retrieving 2025 options statistics...")
        stats = broker.get_2025_options_statistics()

        print(format_options_stats(stats))

        # Get current options positions
        print("📊 Retrieving current options positions...")
        positions = broker.get_options_positions()

        if positions and isinstance(positions[0], dict) and "error" not in positions[0]:
            print(f"\n📊 Current Options Positions: {len(positions)}")
            for pos in positions[:10]:  # Show first 10
                print(f"   {pos.get('instrument', '')} {pos.get('type', '').upper()} "
                      f"${pos.get('strike_price', 0):.2f} {pos.get('expiration_date', '')} "
                      f"Qty: {pos.get('quantity', 0)} P&L: ${pos.get('unrealized_pnl', 0):+,.2f}")
        else:
            print("📊 No active options positions found")

        # Safety status
        print("\n🛡️  Safety Status:")
        is_safe, reason = broker.check_safety_limits()
        status_emoji = "✅" if is_safe else "❌"
        print(f"   {status_emoji} {reason}")

        # Logout
        print("\n🔐 Logging out...")
        broker.logout()

        print("\n✅ Statistics retrieval complete")
        return 0

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        logging.exception("Unexpected error in robinhood_stats_2026")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
