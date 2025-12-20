#!/usr/bin/env python3
"""
Daily Automation Runner
========================

Runs daily trading plan automation for trading robot plugins.
"""

from config.settings import config
from core.trading_engine import TradingEngine
from plugins.daily_automation import DailyAutomation
from plugins.plugin_manager import PluginManager
import asyncio
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))


async def main():
    """Main entry point for daily automation."""
    logger.info("🤖 Starting Daily Trading Robot Automation")

    try:
        # Initialize components
        plugin_manager = PluginManager(plugins_directory="plugins/robots")
        trading_engine = TradingEngine()
        # Skip preflight for paper trading
        await trading_engine.initialize(skip_preflight=True)

        daily_automation = DailyAutomation(
            plugin_manager=plugin_manager,
            trading_engine=trading_engine,
            data_directory="data/plugins",
        )

        # Load TSLA Improved Strategy plugin
        plugin_id = "tsla_improved_strategy"
        logger.info(f"📦 Loading plugin: {plugin_id}")

        plugin = await daily_automation.load_plugin_for_trading(plugin_id)
        if not plugin:
            logger.error(f"Failed to load plugin {plugin_id}")
            return

        # Execute daily plan
        logger.info("📅 Executing daily trading plan...")
        result = await daily_automation.execute_daily_plan(plugin_id, symbol="TSLA")

        if result:
            logger.info(
                f"✅ Daily plan executed: {result.get('action', 'UNKNOWN')}")
            if result.get("action") == "TRADE":
                logger.info(
                    f"   📝 Trade: {result['side']} {result['quantity']} {result['symbol']} "
                    f"@ ${result['entry_price']:.2f}"
                )

        # Update trade exits (check if any open trades should be closed)
        logger.info("🔄 Checking for trade exits...")
        await daily_automation.update_trade_exits(plugin_id)

        # Get performance report
        logger.info("📊 Generating performance report...")
        performance = await daily_automation.get_performance_report(plugin_id)
        if performance:
            logger.info(f"   Total Trades: {performance['total_trades']}")
            logger.info(f"   Win Rate: {performance['win_rate']}%")
            logger.info(f"   Total P&L: ${performance['total_pnl']:.2f}")
            logger.info(
                f"   Profit Factor: {performance['profit_factor']:.2f}")

        logger.info("✅ Daily automation complete")

    except Exception as e:
        logger.error(f"❌ Error in daily automation: {e}")
        raise

    finally:
        if trading_engine:
            await trading_engine.stop()


if __name__ == "__main__":
    # Setup logging
    logger.add(
        f"logs/daily_automation_{datetime.now().date()}.log",
        rotation="1 day",
        retention="30 days",
        level="INFO",
    )

    # Run daily automation
    asyncio.run(main())

    print()
    print("🐝 WE. ARE. SWARM. ⚡🔥")

