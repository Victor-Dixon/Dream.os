#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Trading Commands
========================

Commands for trading reports and analysis.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-01-27
"""

import logging
from datetime import datetime
from typing import Dict, List, Any

import discord
from discord.ext import commands

from .trading_data_service import TradingDataService

logger = logging.getLogger(__name__)


class TradingCommands(commands.Cog):
    """Commands for trading reports and analysis."""

    def __init__(self, bot):
        """Initialize trading commands."""
        self.bot = bot
        self.trading_service = TradingDataService()
        logger.info("✅ Trading commands initialized")

    @commands.command(
        name="tbow",
        aliases=["trading_report", "daily_setups"],
        description="Generate daily trading report with all possible setups"
    )
    async def tbow(self, ctx: commands.Context):
        """Generate comprehensive daily trading report."""
        try:
            # Show thinking message
            await ctx.send("🤔 Analyzing market data and generating report...")

            # Generate report
            report = self._generate_trading_report()

            # Create embed
            embed = self._create_trading_report_embed(report)

            await ctx.send(embed=embed)
            logger.info(f"✅ Trading report generated for {ctx.author}")

        except Exception as e:
            logger.error(
                f"❌ Error generating trading report: {e}", exc_info=True)
            await ctx.send(f"❌ Error generating trading report: {str(e)}")

    def _generate_trading_report(self) -> Dict[str, Any]:
        """Generate comprehensive trading report."""
        report = {
            "timestamp": datetime.now(),
            "tsla_analysis": self._analyze_tsla(),
            "other_setups": self._get_other_setups(),
            "market_conditions": self.trading_service.get_market_conditions()
        }
        return report

    def _analyze_tsla(self) -> Dict[str, Any]:
        """Analyze TSLA for call/put day determination."""
        try:
            analysis = self.trading_service.analyze_symbol("TSLA")

            # Determine call/put day
            signal = analysis.get("signal", "UNKNOWN")
            confidence = analysis.get("confidence", 0.0)
            price = analysis.get("price")

            if signal == "CALL":
                day_type = "CALL DAY"
                reasoning = analysis.get("reason", "Bullish signals detected")
            elif signal == "PUT":
                day_type = "PUT DAY"
                reasoning = analysis.get("reason", "Bearish signals detected")
            else:
                day_type = "NEUTRAL"
                reasoning = "Mixed or unclear signals"

            return {
                "day_type": day_type,
                "confidence": confidence,
                "reasoning": reasoning,
                "price": price,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"⚠️ TSLA analysis failed: {e}")
            return {
                "day_type": "UNKNOWN",
                "confidence": 0.0,
                "reasoning": f"Analysis unavailable: {str(e)}",
                "price": None,
                "timestamp": datetime.now().isoformat()
            }

    def _get_other_setups(self) -> List[Dict[str, Any]]:
        """Get other trading setups."""
        setups = []

        # Analyze common symbols
        symbols = ["AAPL", "MSFT", "NVDA", "SPY"]
        setup_types = ["Breakout", "Pullback", "Momentum", "Trend Following"]

        for symbol, setup_type in zip(symbols, setup_types):
            try:
                analysis = self.trading_service.analyze_symbol(symbol)
                price = analysis.get("price")
                confidence = analysis.get("confidence", 0.0)

                if price and confidence > 0.3:
                    setups.append({
                        "symbol": symbol,
                        "setup_type": setup_type,
                        "signal": analysis.get("signal", "UNKNOWN"),
                        "entry": price * 0.99,  # Approximate entry
                        "exit": price * 1.02,   # Approximate exit
                        "confidence": confidence,
                        "notes": analysis.get("reason", "Analysis complete")
                    })
            except Exception as e:
                logger.warning(f"⚠️ Analysis failed for {symbol}: {e}")
                continue

        return setups

    def _create_trading_report_embed(self, report: Dict[str, Any]) -> discord.Embed:
        """Create Discord embed for trading report."""
        embed = discord.Embed(
            title="📊 Daily Trading Report",
            description="**All Possible Setups for Today**",
            color=discord.Color.gold(),
            timestamp=report["timestamp"]
        )

        # TSLA Analysis
        tsla = report["tsla_analysis"]
        tsla_value = f"**{tsla['day_type']}**"
        if tsla['price']:
            tsla_value += f"\n💰 Price: ${tsla['price']:.2f}"
        tsla_value += f"\n🎯 Confidence: {tsla['confidence']:.0%}"
        tsla_value += f"\n📝 Reasoning: {tsla['reasoning']}"

        embed.add_field(
            name="🚗 TSLA Analysis",
            value=tsla_value,
            inline=False
        )

        # Other Setups
        if report["other_setups"]:
            setups_text = ""
            for setup in report["other_setups"][:5]:  # Limit to 5
                setups_text += f"**{setup['symbol']}** - {setup['setup_type']}\n"
                setups_text += f"Signal: {setup['signal']} | "
                setups_text += f"Confidence: {setup['confidence']:.0%}\n"
                if setup.get('entry'):
                    setups_text += f"Entry: ${setup['entry']:.2f} | Exit: ${setup['exit']:.2f}\n"
                setups_text += f"*{setup['notes']}*\n\n"

            embed.add_field(
                name="📈 Other Trading Setups",
                value=setups_text or "No setups found",
                inline=False
            )

        # Market Conditions
        conditions = report["market_conditions"]
        market_text = f"**Status**: {conditions['market_status']}\n"
        if conditions.get('vix'):
            market_text += f"**VIX**: {conditions['vix']}\n"
        market_text += f"**SPY Trend**: {conditions['spy_trend']}\n"
        market_text += f"**Risk Level**: {conditions['risk_level']}"

        embed.add_field(
            name="🌍 Market Conditions",
            value=market_text,
            inline=False
        )

        embed.set_footer(text="Generated by Agent-1 Trading System")

        return embed
