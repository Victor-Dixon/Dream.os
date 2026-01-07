#!/usr/bin/env python3
"""
Trading Journal Tool - Automatic Trade Logging
=============================================

Command-line tool for managing the trading journal and fetching trades from Robinhood.

Features:
- Fetch and journal 2025 trades from Robinhood
- View journal statistics and performance metrics
- Export journal to CSV
- Run automatic journaling service
- Safety-first with read-only operations

Usage:
    python tools/trading_journal_tool.py --help

Author: Agent-2 (Architecture & Design Specialist)
Safety: Read-only operations only
"""

import argparse
import logging
import sys
import os
from pathlib import Path
from getpass import getpass

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.trading_robot.services.trading_journal import TradingJournal

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradingJournalTool:
    """Command-line tool for trading journal management."""

    def __init__(self):
        self.journal = TradingJournal()

    def run(self):
        """Run the trading journal tool."""
        parser = argparse.ArgumentParser(
            description="Trading Journal Tool - Automatic trade logging from Robinhood"
        )

        # Main commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Connect command
        connect_parser = subparsers.add_parser('connect', help='Connect to Robinhood')
        connect_parser.add_argument('--username', help='Robinhood username')
        connect_parser.add_argument('--password', help='Robinhood password (prompt if not provided)')

        # Journal command
        journal_parser = subparsers.add_parser('journal', help='Fetch and journal trades')
        journal_parser.add_argument('--year', type=int, default=2025, help='Year to journal (default: 2025)')
        journal_parser.add_argument('--auto', action='store_true', help='Run automatic journaling service')

        # Status command
        status_parser = subparsers.add_parser('status', help='Show journal status and statistics')

        # Export command
        export_parser = subparsers.add_parser('export', help='Export journal to CSV')
        export_parser.add_argument('--filename', help='Output filename')

        # Performance command
        perf_parser = subparsers.add_parser('performance', help='Show performance metrics')

        # Disconnect command
        subparsers.add_parser('disconnect', help='Disconnect from all brokers')

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        try:
            if args.command == 'connect':
                self.connect_robinhood(args)
            elif args.command == 'journal':
                if args.auto:
                    self.run_automatic_journaling(args.year)
                else:
                    self.journal_trades(args.year)
            elif args.command == 'status':
                self.show_status()
            elif args.command == 'export':
                self.export_journal(args.filename)
            elif args.command == 'performance':
                self.show_performance()
            elif args.command == 'disconnect':
                self.disconnect_brokers()

        except KeyboardInterrupt:
            logger.info("Operation cancelled by user")
        except Exception as e:
            logger.error(f"Command failed: {e}")
            sys.exit(1)

    def connect_robinhood(self, args):
        """Connect to Robinhood for journaling."""
        print("🔐 Robinhood Connection (Read-Only Mode)")
        print("=" * 50)

        username = args.username or input("Robinhood username: ")
        password = args.password or getpass("Robinhood password: ")

        print("\n⏳ Connecting to Robinhood (read-only access only)...")

        if self.journal.connect_broker('robinhood', username=username, password=password):
            print("✅ Connected to Robinhood successfully!")
            print("🔒 Safety Mode: Read-only access (no trading capabilities)")
            print("📊 Ready to fetch balance and trade history")
        else:
            print("❌ Failed to connect to Robinhood")
            print("💡 Check credentials and ensure MFA is set up in Robinhood app")
            sys.exit(1)

    def journal_trades(self, year: int):
        """Fetch and journal trades for the specified year."""
        print(f"📊 Journaling {year} Trades")
        print("=" * 50)

        if not self.journal.brokers:
            print("❌ No brokers connected. Run 'connect' command first.")
            sys.exit(1)

        # Load existing journal
        self.journal.load_existing_journal()

        print(f"📂 Loaded {len(self.journal.trades)} existing trades")
        print("⏳ Fetching new trades from connected brokers...")

        new_trades = self.journal.fetch_and_journal_trades(year)

        print(f"✅ Journaled {new_trades} new trades")
        print(f"📊 Total trades in journal: {len(self.journal.trades)}")

        if new_trades > 0:
            self.show_summary()

    def show_status(self):
        """Show journal status and summary."""
        print("📊 Trading Journal Status")
        print("=" * 50)

        # Load journal
        self.journal.load_existing_journal()

        journal_info = self.journal.get_journal_summary()

        print(f"📂 Journal Location: {self.journal.journal_dir}")
        print(f"📊 Total Trades: {journal_info['total_trades']}")
        print(f"🤖 Connected Brokers: {', '.join(journal_info['brokers_connected']) or 'None'}")
        print(f"🕒 Last Update: {journal_info['last_update']}")

        if journal_info['total_trades'] > 0:
            summary = journal_info['summary']
            print("
💰 Financial Summary:"            print(".2f"            print(".1f"            print(".2f"            print(".2f"            print(".2f"
        else:
            print("\n📝 No trades in journal yet")

    def show_summary(self):
        """Show detailed journal summary."""
        summary = self.journal.get_journal_summary()['summary']

        print("
📈 Journal Summary:"        print(f"  Date Range: {summary['date_range'][0]} to {summary['date_range'][1]}")
        print(f"  Winning Trades: {int(summary['win_rate'] * summary['total_trades'] / 100)}")
        print(f"  Losing Trades: {int((100 - summary['win_rate']) * summary['total_trades'] / 100)}")
        print(".2f"        print(".2f"        print(".2f"        print(".2f"
    def show_performance(self):
        """Show detailed performance metrics."""
        print("📊 Performance Metrics")
        print("=" * 50)

        try:
            metrics = self.journal.get_performance_metrics()

            if 'error' in metrics:
                print(f"❌ {metrics['error']}")
                return

            print(".2f"            print(".2f"            print("
📅 Monthly Performance:"            for month, pnl in metrics['monthly_performance'].items():
                print(".2f"
            print("
🏆 Best Month:"            print(".2f"            print("
📉 Worst Month:"            print(".2f"            print("
🎯 Consistency Score:"            print(".1f"
        except Exception as e:
            print(f"❌ Failed to calculate performance metrics: {e}")

    def export_journal(self, filename: str = None):
        """Export journal to CSV."""
        print("📤 Exporting Journal")
        print("=" * 50)

        filepath = self.journal.export_journal_to_csv(filename)

        if filepath:
            print(f"✅ Journal exported to: {filepath}")
            print(f"📊 Total trades exported: {len(self.journal.trades)}")
        else:
            print("❌ Export failed")

    def run_automatic_journaling(self, year: int):
        """Run automatic journaling service."""
        print("🤖 Automatic Journaling Service")
        print("=" * 50)
        print("This will run continuously, journaling trades every 24 hours")
        print("Press Ctrl+C to stop")

        if not self.journal.brokers:
            print("❌ No brokers connected. Run 'connect' command first.")
            sys.exit(1)

        try:
            self.journal.run_automatic_journaling(interval_hours=24)
        except KeyboardInterrupt:
            print("\n🛑 Automatic journaling stopped")

    def disconnect_brokers(self):
        """Disconnect from all brokers."""
        print("🔌 Disconnecting from brokers")
        print("=" * 50)

        self.journal.emergency_disconnect_all_brokers()
        print("✅ All brokers disconnected")


def main():
    """Main entry point."""
    tool = TradingJournalTool()
    tool.run()


if __name__ == "__main__":
    main()