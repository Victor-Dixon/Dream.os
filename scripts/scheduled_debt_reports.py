#!/usr/bin/env python3
"""
Scheduled Technical Debt Reports
=================================

Automatically generates and distributes technical debt reports.
Can be run as a cron job or scheduled task.

Usage:
    python scripts/scheduled_debt_reports.py --daily
    python scripts/scheduled_debt_reports.py --weekly
    python scripts/scheduled_debt_reports.py --all
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from systems.technical_debt.daily_report_generator import DailyReportGenerator
from systems.technical_debt.weekly_report_generator import WeeklyReportGenerator

# Optional Discord integration
try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ScheduledDebtReports:
    """Handles scheduled technical debt report generation and distribution."""

    def __init__(self):
        """Initialize scheduled reports."""
        self.daily_generator = DailyReportGenerator()
        self.weekly_generator = WeeklyReportGenerator()
        self.discord_bot = None

        # Initialize Discord bot if available
        if DISCORD_AVAILABLE:
            self._init_discord_bot()

    def _init_discord_bot(self):
        """Initialize Discord bot for report distribution."""
        try:
            discord_token = self._get_discord_token()
            if discord_token:
                intents = discord.Intents.default()
                self.discord_bot = commands.Bot(command_prefix='!', intents=intents)
                logger.info("✅ Discord bot initialized for report distribution")
            else:
                logger.warning("⚠️ Discord token not found, reports will be local only")
        except Exception as e:
            logger.warning(f"⚠️ Discord bot initialization failed: {e}")

    def _get_discord_token(self) -> str:
        """Get Discord bot token from environment or config."""
        import os
        return os.getenv("DISCORD_BOT_TOKEN", "")

    async def send_discord_report(self, report_path: Path, channel_id: str = None):
        """Send report to Discord channel."""
        if not self.discord_bot or not DISCORD_AVAILABLE:
            logger.warning("Discord bot not available for report distribution")
            return

        try:
            # Default channel ID if not specified
            if not channel_id:
                channel_id = "1234567890123456789"  # Replace with actual channel ID

            channel = self.discord_bot.get_channel(int(channel_id))
            if not channel:
                logger.error(f"Could not find Discord channel: {channel_id}")
                return

            # Read report content
            if report_path.exists():
                content = report_path.read_text(encoding='utf-8')

                # Create embed
                embed = discord.Embed(
                    title=f"📋 Scheduled {report_path.stem.replace('_', ' ').title()}",
                    description=f"```{content[:1900] if len(content) > 1900 else content}```",
                    color=0x00FF00,
                    timestamp=datetime.now()
                )

                await channel.send(embed=embed)
                logger.info(f"✅ Report sent to Discord channel {channel_id}")
            else:
                logger.error(f"Report file not found: {report_path}")

        except Exception as e:
            logger.error(f"Failed to send Discord report: {e}")

    def generate_daily_report(self) -> Path:
        """Generate daily technical debt report."""
        logger.info("📊 Generating daily technical debt report...")
        try:
            report_path = self.daily_generator.generate_report()
            if report_path:
                logger.info(f"✅ Daily report generated: {report_path}")
                return report_path
            else:
                logger.error("❌ Daily report generation failed")
                return None
        except Exception as e:
            logger.error(f"❌ Error generating daily report: {e}")
            return None

    def generate_weekly_report(self) -> Path:
        """Generate weekly technical debt report."""
        logger.info("📊 Generating weekly technical debt report...")
        try:
            report_path = self.weekly_generator.generate_report()
            if report_path:
                logger.info(f"✅ Weekly report generated: {report_path}")
                return report_path
            else:
                logger.error("❌ Weekly report generation failed")
                return None
        except Exception as e:
            logger.error(f"❌ Error generating weekly report: {e}")
            return None

    def run_daily_schedule(self):
        """Run daily scheduled reports."""
        logger.info("🕐 Running daily scheduled debt reports...")

        report_path = self.generate_daily_report()
        if report_path:
            logger.info(f"📄 Daily report available at: {report_path}")

            # Send to Discord if available
            if self.discord_bot:
                import asyncio
                asyncio.run(self.send_discord_report(report_path))

        logger.info("✅ Daily schedule completed")

    def run_weekly_schedule(self):
        """Run weekly scheduled reports."""
        logger.info("🕐 Running weekly scheduled debt reports...")

        report_path = self.generate_weekly_report()
        if report_path:
            logger.info(f"📄 Weekly report available at: {report_path}")

            # Send to Discord if available
            if self.discord_bot:
                import asyncio
                asyncio.run(self.send_discord_report(report_path))

        logger.info("✅ Weekly schedule completed")

    def run_all_reports(self):
        """Run all available reports."""
        logger.info("🕐 Running all technical debt reports...")

        daily_path = self.generate_daily_report()
        weekly_path = self.generate_weekly_report()

        if daily_path:
            logger.info(f"📄 Daily report: {daily_path}")
        if weekly_path:
            logger.info(f"📄 Weekly report: {weekly_path}")

        # Send reports to Discord if available
        if self.discord_bot:
            import asyncio
            if daily_path:
                asyncio.run(self.send_discord_report(daily_path))
            if weekly_path:
                asyncio.run(self.send_discord_report(weekly_path))

        logger.info("✅ All reports completed")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Scheduled Technical Debt Reports")
    parser.add_argument("--daily", action="store_true", help="Generate daily report")
    parser.add_argument("--weekly", action="store_true", help="Generate weekly report")
    parser.add_argument("--all", action="store_true", help="Generate all reports")

    args = parser.parse_args()

    # Default to daily if no args specified
    if not any([args.daily, args.weekly, args.all]):
        args.daily = True

    try:
        scheduler = ScheduledDebtReports()

        if args.all:
            scheduler.run_all_reports()
        elif args.weekly:
            scheduler.run_weekly_schedule()
        elif args.daily:
            scheduler.run_daily_schedule()

    except Exception as e:
        logger.error(f"❌ Scheduled reports failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()