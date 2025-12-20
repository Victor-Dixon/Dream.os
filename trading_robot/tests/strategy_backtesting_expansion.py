#!/usr/bin/env python3
"""
Strategy Backtesting Expansion
==============================

Comprehensive backtesting for all trading strategies:
- TSLA Improved Strategy plugin
- Built-in strategies (Trend Following, Mean Reversion)
- Performance comparison and analysis

V2 Compliant: < 400 lines
"""

import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
from loguru import logger

# Add trading_robot to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backtesting.backtester import Backtester, BacktestResult
from strategies.strategy_implementations import TrendFollowingStrategy, MeanReversionStrategy
from plugins.robots.tsla_improved_strategy.tsla_improved_strategy import TslaImprovedStrategy
from plugins.plugin_metadata import PluginMetadata
from core.alpaca_client import AlpacaClient
from config.settings import config


class StrategyBacktestingExpansion:
    """Expanded backtesting for all trading strategies."""
    
    def __init__(self):
        """Initialize backtesting expansion."""
        self.results: Dict[str, BacktestResult] = {}
        self.comparison_report: Dict[str, Any] = {
            "backtest_date": datetime.now().isoformat(),
            "strategies": {},
            "comparison": {},
            "recommendations": []
        }
    
    def get_historical_data(self, symbol: str, days: int = 365) -> Optional[pd.DataFrame]:
        """Get historical data for backtesting."""
        try:
            broker = AlpacaClient()
            broker.connect()
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            data = broker.get_historical_data(
                symbol=symbol,
                timeframe="1Day",
                start=start_date,
                end=end_date,
                limit=days
            )
            
            if data is None or data.empty:
                logger.error(f"❌ Failed to get historical data for {symbol}")
                return None
            
            logger.info(f"✅ Retrieved {len(data)} days of historical data for {symbol}")
            return data
            
        except Exception as e:
            logger.error(f"❌ Error getting historical data: {e}")
            return None
    
    def backtest_tsla_improved_strategy(self, data: pd.DataFrame) -> Optional[BacktestResult]:
        """Backtest TSLA Improved Strategy plugin."""
        logger.info("📊 Backtesting TSLA Improved Strategy...")
        
        try:
            # Create strategy instance (PluginBase extends BaseStrategy, so compatible)
            metadata = PluginMetadata(
                name="TSLA Improved Strategy",
                version="1.0.0",
                author="Trading Robot",
                description="Risk-based TSLA trading strategy"
            )
            strategy = TslaImprovedStrategy(metadata)
            
            # Create backtester
            backtester = Backtester(initial_balance=config.backtest_initial_balance)
            
            # Run backtest
            result = backtester.run_backtest(
                strategy=strategy,
                data=data,
                symbol="TSLA"
            )
            
            if result:
                result.calculate_metrics()
                logger.info(f"✅ TSLA Improved Strategy backtest complete: {result.total_trades} trades, {result.win_rate:.1%} win rate")
                return result
            else:
                logger.error("❌ TSLA Improved Strategy backtest failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ TSLA Improved Strategy backtest error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def backtest_trend_following(self, data: pd.DataFrame, symbol: str = "AAPL") -> Optional[BacktestResult]:
        """Backtest Trend Following strategy."""
        logger.info("📊 Backtesting Trend Following Strategy...")
        
        try:
            strategy = TrendFollowingStrategy()
            backtester = Backtester(initial_balance=config.backtest_initial_balance)
            
            result = backtester.run_backtest(
                strategy=strategy,
                data=data,
                symbol=symbol
            )
            
            if result:
                result.calculate_metrics()
                logger.info(f"✅ Trend Following backtest complete: {result.total_trades} trades, {result.win_rate:.1%} win rate")
                return result
            else:
                logger.error("❌ Trend Following backtest failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ Trend Following backtest error: {e}")
            return None
    
    def backtest_mean_reversion(self, data: pd.DataFrame, symbol: str = "AAPL") -> Optional[BacktestResult]:
        """Backtest Mean Reversion strategy."""
        logger.info("📊 Backtesting Mean Reversion Strategy...")
        
        try:
            strategy = MeanReversionStrategy()
            backtester = Backtester(initial_balance=config.backtest_initial_balance)
            
            result = backtester.run_backtest(
                strategy=strategy,
                data=data,
                symbol=symbol
            )
            
            if result:
                result.calculate_metrics()
                logger.info(f"✅ Mean Reversion backtest complete: {result.total_trades} trades, {result.win_rate:.1%} win rate")
                return result
            else:
                logger.error("❌ Mean Reversion backtest failed")
                return None
                
        except Exception as e:
            logger.error(f"❌ Mean Reversion backtest error: {e}")
            return None
    
    def compare_strategies(self) -> Dict[str, Any]:
        """Compare all backtested strategies."""
        logger.info("📊 Comparing strategies...")
        
        comparison = {
            "best_win_rate": None,
            "best_profit_factor": None,
            "best_sharpe_ratio": None,
            "best_total_return": None,
            "lowest_drawdown": None,
            "strategy_rankings": []
        }
        
        # Find best performers
        for strategy_name, result in self.results.items():
            if result is None:
                continue
            
            # Track best performers
            if comparison["best_win_rate"] is None or result.win_rate > comparison["best_win_rate"][1]:
                comparison["best_win_rate"] = (strategy_name, result.win_rate)
            
            if comparison["best_profit_factor"] is None or result.profit_factor > comparison["best_profit_factor"][1]:
                comparison["best_profit_factor"] = (strategy_name, result.profit_factor)
            
            if comparison["best_sharpe_ratio"] is None or result.sharpe_ratio > comparison["best_sharpe_ratio"][1]:
                comparison["best_sharpe_ratio"] = (strategy_name, result.sharpe_ratio)
            
            if comparison["best_total_return"] is None or result.total_return > comparison["best_total_return"][1]:
                comparison["best_total_return"] = (strategy_name, result.total_return)
            
            if comparison["lowest_drawdown"] is None or result.max_drawdown < comparison["lowest_drawdown"][1]:
                comparison["lowest_drawdown"] = (strategy_name, result.max_drawdown)
        
        # Create strategy rankings (by total return)
        rankings = []
        for strategy_name, result in self.results.items():
            if result is None:
                continue
            rankings.append({
                "strategy": strategy_name,
                "total_return": result.total_return,
                "win_rate": result.win_rate,
                "profit_factor": result.profit_factor,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "total_trades": result.total_trades
            })
        
        rankings.sort(key=lambda x: x["total_return"], reverse=True)
        comparison["strategy_rankings"] = rankings
        
        return comparison
    
    def generate_recommendations(self, comparison: Dict[str, Any]) -> List[str]:
        """Generate strategy recommendations based on backtest results."""
        recommendations = []
        
        if not comparison.get("strategy_rankings"):
            recommendations.append("⚠️ No valid backtest results to generate recommendations")
            return recommendations
        
        # Get top strategy
        top_strategy = comparison["strategy_rankings"][0]
        
        recommendations.append(f"🏆 Top Performing Strategy: {top_strategy['strategy']}")
        recommendations.append(f"   - Total Return: {top_strategy['total_return']:.2f}%")
        recommendations.append(f"   - Win Rate: {top_strategy['win_rate']:.1%}")
        recommendations.append(f"   - Profit Factor: {top_strategy['profit_factor']:.2f}")
        recommendations.append(f"   - Sharpe Ratio: {top_strategy['sharpe_ratio']:.2f}")
        
        # Risk assessment
        if top_strategy['max_drawdown'] > 20:
            recommendations.append(f"⚠️ High drawdown warning: {top_strategy['max_drawdown']:.2f}%")
        
        # Compare strategies
        if len(comparison["strategy_rankings"]) > 1:
            second_strategy = comparison["strategy_rankings"][1]
            recommendations.append(f"\n📊 Comparison:")
            recommendations.append(f"   - {top_strategy['strategy']}: {top_strategy['total_return']:.2f}% return")
            recommendations.append(f"   - {second_strategy['strategy']}: {second_strategy['total_return']:.2f}% return")
            recommendations.append(f"   - Difference: {top_strategy['total_return'] - second_strategy['total_return']:.2f}%")
        
        return recommendations
    
    def run_all_backtests(self) -> Dict[str, Any]:
        """Run backtests for all strategies."""
        logger.info("🚀 Starting strategy backtesting expansion...")
        
        # Get historical data (use TSLA for TSLA strategy, AAPL for others)
        tsla_data = self.get_historical_data("TSLA", days=365)
        aapl_data = self.get_historical_data("AAPL", days=365)
        
        if tsla_data is None or aapl_data is None:
            logger.error("❌ Failed to get historical data")
            return self.comparison_report
        
        # Backtest TSLA Improved Strategy
        self.results["TSLA Improved Strategy"] = self.backtest_tsla_improved_strategy(tsla_data)
        
        # Backtest built-in strategies
        self.results["Trend Following"] = self.backtest_trend_following(aapl_data)
        self.results["Mean Reversion"] = self.backtest_mean_reversion(aapl_data)
        
        # Store results in comparison report
        for strategy_name, result in self.results.items():
            if result:
                self.comparison_report["strategies"][strategy_name] = {
                    "total_trades": result.total_trades,
                    "win_rate": result.win_rate,
                    "profit_factor": result.profit_factor,
                    "sharpe_ratio": result.sharpe_ratio,
                    "total_return": result.total_return,
                    "max_drawdown": result.max_drawdown,
                    "avg_win": result.avg_win,
                    "avg_loss": result.avg_loss
                }
        
        # Compare strategies
        comparison = self.compare_strategies()
        self.comparison_report["comparison"] = comparison
        
        # Generate recommendations
        recommendations = self.generate_recommendations(comparison)
        self.comparison_report["recommendations"] = recommendations
        
        return self.comparison_report
    
    def print_report(self):
        """Print backtesting report."""
        print("\n" + "=" * 60)
        print("📊 STRATEGY BACKTESTING EXPANSION REPORT")
        print("=" * 60)
        
        # Strategy results
        print("\n📈 Strategy Performance:")
        for strategy_name, result in self.results.items():
            if result:
                print(f"\n{strategy_name}:")
                print(f"  Total Trades: {result.total_trades}")
                print(f"  Win Rate: {result.win_rate:.1%}")
                print(f"  Total Return: {result.total_return:.2f}%")
                print(f"  Profit Factor: {result.profit_factor:.2f}")
                print(f"  Sharpe Ratio: {result.sharpe_ratio:.2f}")
                print(f"  Max Drawdown: {result.max_drawdown:.2f}%")
        
        # Comparison
        if self.comparison_report.get("comparison"):
            comp = self.comparison_report["comparison"]
            print("\n🏆 Best Performers:")
            if comp.get("best_total_return"):
                print(f"  Best Return: {comp['best_total_return'][0]} ({comp['best_total_return'][1]:.2f}%)")
            if comp.get("best_win_rate"):
                print(f"  Best Win Rate: {comp['best_win_rate'][0]} ({comp['best_win_rate'][1]:.1%})")
            if comp.get("best_sharpe_ratio"):
                print(f"  Best Sharpe: {comp['best_sharpe_ratio'][0]} ({comp['best_sharpe_ratio'][1]:.2f})")
        
        # Recommendations
        if self.comparison_report.get("recommendations"):
            print("\n💡 Recommendations:")
            for rec in self.comparison_report["recommendations"]:
                print(f"  {rec}")
        
        print("\n" + "=" * 60)
    
    def save_report(self, output_file: Optional[Path] = None):
        """Save backtesting report to file."""
        if output_file is None:
            output_file = Path(__file__).parent.parent / "docs" / "trading_robot" / "strategy_backtesting_results.json"
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(self.comparison_report, f, indent=2, default=str)
        
        logger.info(f"📄 Report saved to: {output_file}")


def main():
    """Main execution."""
    expansion = StrategyBacktestingExpansion()
    
    try:
        # Run all backtests
        report = expansion.run_all_backtests()
        
        # Print report
        expansion.print_report()
        
        # Save report
        expansion.save_report()
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Backtesting expansion failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

