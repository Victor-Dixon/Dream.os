#!/usr/bin/env python3
"""
Safe Automated Trading Tool - Prevent Account Blowups
====================================================

Command-line tool for ultra-conservative automated trading.
Implements multiple safety layers to prevent account losses.

Features:
- Ultra-conservative risk management (0.25% risk per trade)
- Daily loss limits (0.5% maximum loss)
- Emergency stop mechanisms
- Manual override capabilities
- Real-time monitoring and alerts

Usage:
    python tools/safe_automated_trading.py --help

Author: Agent-2 (Architecture & Design Specialist)
Mission: Prevent trading losses through automated safety controls
"""

import argparse
import logging
import sys
import time
import signal
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.trading_robot.strategies.conservative_automated_strategy import ConservativeAutomatedStrategy
from src.trading_robot.services.risk_management_service import RiskLevel

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SafeAutomatedTradingTool:
    """Safe automated trading tool with comprehensive risk controls."""

    def __init__(self):
        self.strategy = None
        self.running = False

    def run(self):
        """Run the safe automated trading tool."""
        parser = argparse.ArgumentParser(
            description="Safe Automated Trading Tool - Prevent account blowups through conservative automation"
        )

        # Main commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Connect command
        connect_parser = subparsers.add_parser('connect', help='Connect to broker safely')
        connect_parser.add_argument('--broker', default='robinhood', help='Broker type (default: robinhood)')
        connect_parser.add_argument('--username', help='Broker username')
        connect_parser.add_argument('--password', help='Broker password (prompt if not provided)')
        connect_parser.add_argument('--risk-level', choices=['ultra_conservative', 'conservative'],
                                  default='ultra_conservative', help='Risk tolerance level')

        # Start command
        start_parser = subparsers.add_parser('start', help='Start automated trading')
        start_parser.add_argument('--cycle-interval', type=int, default=60,
                                help='Seconds between strategy cycles (default: 60)')

        # Status command
        subparsers.add_parser('status', help='Show trading status and P&L')

        # Stop command
        subparsers.add_parser('stop', help='Safely stop automated trading')

        # Manual override commands
        manual_parser = subparsers.add_parser('manual', help='Manual override commands')
        manual_parser.add_argument('action', choices=['emergency_stop', 'reset_daily', 'close_position'],
                                 help='Manual action to perform')
        manual_parser.add_argument('--symbol', help='Symbol for position actions')

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        try:
            if args.command == 'connect':
                self.connect_broker(args)
            elif args.command == 'start':
                self.start_automated_trading(args)
            elif args.command == 'status':
                self.show_status()
            elif args.command == 'stop':
                self.stop_trading()
            elif args.command == 'manual':
                self.manual_override(args)

        except KeyboardInterrupt:
            logger.info("Operation cancelled by user")
            self.stop_trading()
        except Exception as e:
            logger.error(f"Command failed: {e}")
            self.stop_trading()
            sys.exit(1)

    def connect_broker(self, args):
        """Safely connect to broker with validation."""
        print("🔐 Safe Broker Connection")
        print("=" * 50)
        print("⚠️  SAFETY FIRST: This tool implements ultra-conservative risk controls")
        print("📊 Risk per trade: 0.25% of portfolio")
        print("🛑 Daily loss limit: 0.5% of portfolio")
        print("⏱️  Max 3 trades per day")
        print("🚫 NO trading permissions initially - read-only connection")
        print()

        # Get risk level
        risk_level_map = {
            'ultra_conservative': RiskLevel.ULTRA_CONSERVATIVE,
            'conservative': RiskLevel.CONSERVATIVE
        }
        risk_level = risk_level_map[args.risk_level]

        print(f"🛡️  Risk Level: {risk_level.value.upper()}")

        # Initialize strategy
        self.strategy = ConservativeAutomatedStrategy(risk_level)

        # Get credentials
        username = args.username
        if not username:
            username = input("Broker username: ")

        password = args.password
        if not password:
            from getpass import getpass
            password = getpass("Broker password: ")

        print("\n⏳ Connecting to broker with safety protocols...")

        if self.strategy.connect_broker(args.broker, username=username, password=password):
            print("✅ Connected successfully!")
            print("🔒 Safety Status: Read-only access (trading disabled)")
            print("📊 Ready for safe automated monitoring")
            print()
            print("Next steps:")
            print("1. Run 'status' to check account and risk status")
            print("2. Run 'start' to begin automated monitoring (no trading)")
            print("3. Use manual controls for emergency actions")
        else:
            print("❌ Connection failed")
            print("💡 Check credentials and ensure MFA is configured")
            sys.exit(1)

    def start_automated_trading(self, args):
        """Start safe automated trading with monitoring."""
        if not self.strategy:
            print("❌ No broker connection. Run 'connect' first.")
            sys.exit(1)

        print("🚀 Safe Automated Trading System")
        print("=" * 50)
        print("⚠️  SAFETY PROTOCOLS ACTIVE:")
        print("   🛑 Emergency stop available (Ctrl+C)")
        print("   📊 Real-time risk monitoring")
        print("   🚫 No actual trading (monitoring only)")
        print("   📝 All actions logged and auditable")
        print()

        # Start the strategy
        if not self.strategy.start_strategy():
            print("❌ Failed to start strategy")
            sys.exit(1)

        print("✅ Safe automated system started")
        print(f"⏱️  Monitoring cycle: every {args.cycle_interval} seconds")
        print("🎯 Looking for ultra-safe entry opportunities...")
        print()
        print("Press Ctrl+C to stop safely")

        # Set up signal handling for safe shutdown
        def signal_handler(signum, frame):
            print("\n🛑 Safe shutdown initiated...")
            self.stop_trading()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        self.running = True
        cycle_count = 0

        try:
            while self.running:
                cycle_count += 1

                # Run strategy cycle
                result = self.strategy.run_strategy_cycle()

                # Report cycle results
                print(f"🔄 Cycle {cycle_count}: {result.get('status', 'unknown')}")

                if result.get('status') == 'signal_found':
                    signal_data = result.get('signal', {})
                    print(f"   🎯 Signal: {signal_data.get('symbol')} {signal_data.get('direction')} "
                          f"(confidence: {signal_data.get('confidence', 0):.1%})")
                    print("   📊 Signal validated but trading DISABLED for safety")

                elif result.get('status') == 'emergency_stop':
                    print("   🚨 EMERGENCY STOP ACTIVATED")
                    break

                elif result.get('status') == 'error':
                    print(f"   ❌ Error: {result.get('message', 'Unknown error')}")

                # Wait for next cycle
                time.sleep(args.cycle_interval)

        except Exception as e:
            logger.error(f"Automated trading error: {e}")
            self.stop_trading()

    def show_status(self):
        """Show comprehensive trading status."""
        print("📊 Trading System Status")
        print("=" * 50)

        if not self.strategy:
            print("❌ No strategy initialized. Run 'connect' first.")
            return

        try:
            # Get strategy status
            strategy_status = self.strategy.get_strategy_status()
            risk_status = strategy_status.get('risk_limits', {})

            print(f"🤖 Strategy State: {strategy_status['state'].upper()}")
            print(f"📊 Open Positions: {strategy_status['open_positions']}")
            print(f"📈 Daily Trades: {strategy_status['daily_trades']}")
            print(f"💰 Daily P&L: ${strategy_status['daily_pnl']:.2f}")
            print(f"🛑 Emergency Stop: {'ACTIVE' if strategy_status['emergency_stop'] else 'Inactive'}")
            print(f"⚡ Circuit Breaker: {'TRIPPED' if strategy_status.get('circuit_breaker', False) else 'Normal'}")
            print()

            # Risk limits
            limits = risk_status.get('limits', {})
            print("🛡️  Risk Limits:")
            print(".1f"            print(".1f"            print(f"   Max Daily Trades: {limits.get('max_daily_trades', 'N/A')}")
            print(f"   Max Open Positions: {limits.get('max_open_positions', 'N/A')}")
            print()

            # Account info (if available)
            if hasattr(self.strategy, 'broker') and self.strategy.broker:
                account_info = self.strategy.broker.get_account_info()
                if not account_info.get('error'):
                    print("🏦 Account Status:")
                    print(".2f"                    print(".2f"                    print(".2f"                    print(".2f"                    print(f"   Account Type: {account_info.get('account_type', 'N/A')}")
                    print(f"   Status: {account_info.get('status', 'N/A')}")
                else:
                    print(f"🏦 Account Status: {account_info.get('error')}")

        except Exception as e:
            print(f"❌ Status check failed: {e}")

    def stop_trading(self):
        """Safely stop automated trading."""
        print("\n🛑 Safe Shutdown Protocol")
        print("=" * 50)

        if self.strategy:
            print("⏳ Stopping strategy safely...")
            self.strategy.stop_strategy()
            print("✅ Strategy stopped")

        self.running = False
        print("✅ All systems safely shut down")
        print("📝 All actions logged and auditable")

    def manual_override(self, args):
        """Execute manual override commands."""
        print("🔧 Manual Override System")
        print("=" * 50)

        if not self.strategy:
            print("❌ No strategy active. Run 'connect' first.")
            return

        print(f"⚠️  Executing manual override: {args.action.upper()}")

        try:
            if args.action == 'emergency_stop':
                print("🚨 ACTIVATING EMERGENCY STOP")
                self.strategy.manual_override('emergency_stop')
                print("✅ Emergency stop activated - all trading halted")

            elif args.action == 'reset_daily':
                print("🔄 Resetting daily counters")
                self.strategy.manual_override('reset_daily')
                print("✅ Daily counters reset")

            elif args.action == 'close_position':
                if not args.symbol:
                    print("❌ Symbol required for position close")
                    return
                print(f"📤 Closing position: {args.symbol}")
                self.strategy.manual_override('close_position', symbol=args.symbol)
                print("✅ Position close initiated")

        except Exception as e:
            print(f"❌ Manual override failed: {e}")


def main():
    """Main entry point."""
    print("🛡️  Safe Automated Trading Tool")
    print("Prevents account blowups through ultra-conservative risk controls")
    print("=" * 70)
    print()

    tool = SafeAutomatedTradingTool()
    tool.run()


if __name__ == "__main__":
    main()