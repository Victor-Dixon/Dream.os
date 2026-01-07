#!/usr/bin/env python3
"""
Trading Journal Service - Automatic Trade Logging
================================================

<!-- SSOT Domain: trading_robot -->

Enterprise-grade trading journal that automatically logs all trades from connected brokers.
Implements comprehensive trade tracking, P&L analysis, and performance metrics.

Features:
- Automatic trade fetching from Robinhood
- Comprehensive trade logging with metadata
- P&L calculations and performance analysis
- Risk metrics and trade analytics
- Scheduled journaling with error recovery
- Integration with trading strategies

Author: Agent-2 (Architecture & Design Specialist)
Safety-First: Read-only operations only
"""

import logging
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import os
from dataclasses import dataclass, asdict

from ..core.broker_factory import BrokerFactory
from ..core.unified_logging_system import UnifiedLoggingSystem

logger = logging.getLogger(__name__)


@dataclass
class TradeEntry:
    """Comprehensive trade entry for journaling."""
    trade_id: str
    broker: str
    instrument: str
    trade_type: str  # equity, options, crypto
    side: str  # buy, sell
    quantity: int
    price: float
    timestamp: str
    commission: float = 0.0
    pnl: float = 0.0
    strategy: Optional[str] = None
    notes: Optional[str] = None

    # Options-specific fields
    option_type: Optional[str] = None  # call/put
    strike_price: Optional[float] = None
    expiration_date: Optional[str] = None

    # Metadata
    journaled_at: Optional[str] = None
    source: str = "api"  # api, manual, strategy

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TradeEntry':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class JournalSummary:
    """Trading journal summary statistics."""
    total_trades: int = 0
    total_pnl: float = 0.0
    win_rate: float = 0.0
    average_trade: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    total_commissions: float = 0.0
    date_range: Tuple[str, str] = ("", "")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class TradingJournal:
    """
    Automatic Trading Journal Service

    Automatically fetches and journals trades from connected brokers.
    Provides comprehensive trade analysis and performance metrics.
    """

    def __init__(self, journal_dir: Optional[Path] = None):
        """
        Initialize trading journal.

        Args:
            journal_dir: Directory to store journal files
        """
        self.journal_dir = journal_dir or Path("data/trading_journal")
        self.journal_dir.mkdir(parents=True, exist_ok=True)

        # Journal files (dynamic based on year)
        self.current_year = 2025  # Default to 2025
        self.trades_file = self.journal_dir / f"trades_{self.current_year}.json"
        self.summary_file = self.journal_dir / f"summary_{self.current_year}.json"
        self.last_update_file = self.journal_dir / "last_update.json"

        # Tracking
        self.trades: List[TradeEntry] = []
        self.summary = JournalSummary()
        self.last_journaled_trade_id: Optional[str] = None

        # Broker connections
        self.brokers: Dict[str, Any] = {}

        logger.info(f"Trading journal initialized at {self.journal_dir}")

    def connect_broker(self, broker_type: str, **credentials) -> bool:
        """
        Connect to a broker for trade fetching.

        Args:
            broker_type: Type of broker (robinhood, etc.)
            **credentials: Broker credentials

        Returns:
            True if connected successfully
        """
        try:
            broker = BrokerFactory.create_broker(broker_type, **credentials)
            if broker and broker.connect():
                self.brokers[broker_type] = broker
                logger.info(f"Connected to {broker_type} for journaling")
                return True
            else:
                logger.error(f"Failed to connect to {broker_type}")
                return False
        except Exception as e:
            logger.error(f"Broker connection failed: {e}")
            return False

    def load_existing_journal(self):
        """Load existing trade journal from disk."""
        try:
            if self.trades_file.exists():
                with open(self.trades_file, 'r') as f:
                    trades_data = json.load(f)
                    self.trades = [TradeEntry.from_dict(trade) for trade in trades_data]
                    logger.info(f"Loaded {len(self.trades)} existing trades")

            if self.summary_file.exists():
                with open(self.summary_file, 'r') as f:
                    summary_data = json.load(f)
                    self.summary = JournalSummary(**summary_data)

            if self.last_update_file.exists():
                with open(self.last_update_file, 'r') as f:
                    update_data = json.load(f)
                    self.last_journaled_trade_id = update_data.get('last_trade_id')

        except Exception as e:
            logger.error(f"Failed to load existing journal: {e}")

    def save_journal(self):
        """Save current journal to disk."""
        try:
            # Save trades
            trades_data = [trade.to_dict() for trade in self.trades]
            with open(self.trades_file, 'w') as f:
                json.dump(trades_data, f, indent=2, default=str)

            # Save summary
            with open(self.summary_file, 'w') as f:
                json.dump(self.summary.to_dict(), f, indent=2, default=str)

            # Save last update
            update_data = {
                'last_update': datetime.now().isoformat(),
                'total_trades': len(self.trades),
                'last_trade_id': self.last_journaled_trade_id
            }
            with open(self.last_update_file, 'w') as f:
                json.dump(update_data, f, indent=2)

            logger.info(f"Journal saved: {len(self.trades)} trades")

        except Exception as e:
            logger.error(f"Failed to save journal: {e}")

    def fetch_and_journal_trades(self, year: int = 2025) -> int:
        """
        Fetch trades from connected brokers and add to journal.

        Args:
            year: Year to fetch trades for

        Returns:
            Number of new trades journaled
        """
        new_trades_count = 0

        for broker_name, broker in self.brokers.items():
            try:
                logger.info(f"Fetching 2025 trades from {broker_name}...")

                # Get trade history for the year
                if hasattr(broker, f'get_trade_history_{year}'):
                    # Call year-specific method
                    method_name = f'get_trade_history_{year}'
                    trades_data = getattr(broker, method_name)()
                elif hasattr(broker, 'get_trade_history'):
                    # Generic trade history method
                    start_date = f"{year}-01-01"
                    end_date = f"{year}-12-31"
                    trades_data = broker.get_trade_history(start_date, end_date)
                else:
                    logger.warning(f"Broker {broker_name} doesn't support trade history")
                    continue

                if isinstance(trades_data, dict) and 'error' in trades_data:
                    logger.error(f"Error fetching trades from {broker_name}: {trades_data['error']}")
                    continue

                # Process trades
                for trade_data in trades_data:
                    if isinstance(trade_data, dict) and 'error' not in trade_data:
                        trade_entry = self._create_trade_entry(trade_data, broker_name)
                        if trade_entry and self._is_new_trade(trade_entry):
                            self.trades.append(trade_entry)
                            new_trades_count += 1
                            self.last_journaled_trade_id = trade_entry.trade_id

                logger.info(f"Added {new_trades_count} new trades from {broker_name}")

            except Exception as e:
                logger.error(f"Failed to fetch trades from {broker_name}: {e}")

        # Update summary after adding trades
        self._update_summary()
        self.save_journal()

        return new_trades_count

    def _create_trade_entry(self, trade_data: Dict[str, Any], broker_name: str) -> Optional[TradeEntry]:
        """Create a TradeEntry from broker trade data."""
        try:
            trade_entry = TradeEntry(
                trade_id=trade_data.get('trade_id') or trade_data.get('id') or f"{broker_name}_{int(time.time())}",
                broker=broker_name,
                instrument=trade_data.get('instrument') or trade_data.get('symbol', 'Unknown'),
                trade_type=trade_data.get('type', 'equity'),
                side=trade_data.get('side', 'buy'),
                quantity=int(trade_data.get('quantity', 0)),
                price=float(trade_data.get('price') or trade_data.get('average_price', 0)),
                timestamp=trade_data.get('timestamp') or trade_data.get('created_at', datetime.now().isoformat()),
                commission=float(trade_data.get('commission') or trade_data.get('fees', 0)),
                pnl=float(trade_data.get('pnl', 0)),
                strategy=trade_data.get('strategy'),
                notes=f"Auto-journaled from {broker_name} API"
            )

            # Options-specific fields
            if trade_data.get('option_type'):
                trade_entry.option_type = trade_data['option_type']
                trade_entry.strike_price = float(trade_data.get('strike_price', 0))
                trade_entry.expiration_date = trade_data.get('expiration_date')

            trade_entry.journaled_at = datetime.now().isoformat()

            return trade_entry

        except Exception as e:
            logger.error(f"Failed to create trade entry: {e}")
            return None

    def _is_new_trade(self, trade_entry: TradeEntry) -> bool:
        """Check if this is a new trade not already in the journal."""
        return not any(t.trade_id == trade_entry.trade_id for t in self.trades)

    def _update_summary(self):
        """Update journal summary statistics."""
        if not self.trades:
            return

        # Calculate metrics
        total_trades = len(self.trades)
        total_pnl = sum(t.pnl for t in self.trades)
        winning_trades = sum(1 for t in self.trades if t.pnl > 0)
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        average_trade = total_pnl / total_trades if total_trades > 0 else 0
        largest_win = max((t.pnl for t in self.trades), default=0)
        largest_loss = min((t.pnl for t in self.trades), default=0)
        total_commissions = sum(t.commission for t in self.trades)

        # Date range
        timestamps = [t.timestamp for t in self.trades if t.timestamp]
        if timestamps:
            sorted_times = sorted(timestamps)
            date_range = (sorted_times[0], sorted_times[-1])
        else:
            date_range = ("", "")

        # Update summary
        self.summary = JournalSummary(
            total_trades=total_trades,
            total_pnl=total_pnl,
            win_rate=win_rate,
            average_trade=average_trade,
            largest_win=largest_win,
            largest_loss=largest_loss,
            total_commissions=total_commissions,
            date_range=date_range
        )

    def get_journal_summary(self) -> Dict[str, Any]:
        """Get comprehensive journal summary."""
        return {
            'summary': self.summary.to_dict(),
            'total_trades': len(self.trades),
            'last_update': datetime.now().isoformat(),
            'brokers_connected': list(self.brokers.keys()),
            'journal_file': str(self.trades_file),
            'summary_file': str(self.summary_file)
        }

    def export_journal_to_csv(self, filename: Optional[str] = None) -> str:
        """Export journal to CSV format."""
        import csv

        if not filename:
            filename = f"trading_journal_2025_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        filepath = self.journal_dir / filename

        try:
            with open(filepath, 'w', newline='') as csvfile:
                fieldnames = ['trade_id', 'broker', 'instrument', 'trade_type', 'side',
                            'quantity', 'price', 'timestamp', 'commission', 'pnl',
                            'strategy', 'option_type', 'strike_price', 'expiration_date', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for trade in self.trades:
                    row = trade.to_dict()
                    # Remove metadata fields not needed in CSV
                    row.pop('journaled_at', None)
                    row.pop('source', None)
                    writer.writerow(row)

            logger.info(f"Journal exported to {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Failed to export journal: {e}")
            return ""

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics."""
        if not self.trades:
            return {"error": "No trades in journal"}

        # Group by month
        monthly_pnl = {}
        for trade in self.trades:
            try:
                trade_date = datetime.fromisoformat(trade.timestamp.replace('Z', '+00:00'))
                month_key = trade_date.strftime('%Y-%m')
                monthly_pnl[month_key] = monthly_pnl.get(month_key, 0) + trade.pnl
            except:
                continue

        # Calculate Sharpe-like ratio (simplified)
        if len(self.trades) > 1:
            returns = [t.pnl for t in self.trades]
            avg_return = sum(returns) / len(returns)
            variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
            sharpe_ratio = avg_return / (variance ** 0.5) if variance > 0 else 0
        else:
            sharpe_ratio = 0

        return {
            'total_return': self.summary.total_pnl,
            'sharpe_ratio': sharpe_ratio,
            'monthly_performance': monthly_pnl,
            'best_month': max(monthly_pnl.values()) if monthly_pnl else 0,
            'worst_month': min(monthly_pnl.values()) if monthly_pnl else 0,
            'consistency_score': self._calculate_consistency_score()
        }

    def _calculate_consistency_score(self) -> float:
        """Calculate trading consistency score (0-100)."""
        if not self.trades:
            return 0.0

        # Factors: win rate, profit factor, max drawdown
        win_rate_score = min(self.summary.win_rate, 100) * 0.4
        profit_factor = abs(self.summary.total_pnl) / max(sum(t.commission for t in self.trades), 1)
        profit_score = min(profit_factor * 10, 40)  # 40% weight

        # Drawdown score (simplified)
        peak = 0
        max_drawdown = 0
        running_pnl = 0

        for trade in sorted(self.trades, key=lambda x: x.timestamp):
            running_pnl += trade.pnl
            if running_pnl > peak:
                peak = running_pnl
            drawdown = peak - running_pnl
            max_drawdown = max(max_drawdown, drawdown)

        drawdown_score = max(0, 20 - (max_drawdown / max(abs(self.summary.total_pnl), 1)) * 20)

        return win_rate_score + profit_score + drawdown_score

    def run_automatic_journaling(self, interval_hours: int = 24):
        """
        Run automatic journaling service.

        Args:
            interval_hours: Hours between journaling runs
        """
        logger.info(f"Starting automatic journaling service (every {interval_hours} hours)")

        while True:
            try:
                # Fetch and journal new trades
                new_trades = self.fetch_and_journal_trades(2025)

                if new_trades > 0:
                    logger.info(f"Auto-journaled {new_trades} new trades")
                    self._send_journal_notification(new_trades)
                else:
                    logger.info("No new trades to journal")

                # Wait for next interval
                time.sleep(interval_hours * 3600)

            except KeyboardInterrupt:
                logger.info("Automatic journaling stopped by user")
                break
            except Exception as e:
                logger.error(f"Automatic journaling error: {e}")
                time.sleep(300)  # Wait 5 minutes before retry

    def _send_journal_notification(self, new_trades: int):
        """Send notification about new journaled trades."""
        # This could integrate with Discord notifications, etc.
        logger.info(f"📊 Journaled {new_trades} new trades - Total: {len(self.trades)}")

    def emergency_disconnect_all_brokers(self):
        """Emergency disconnect from all brokers."""
        for broker_name, broker in self.brokers.items():
            try:
                broker.disconnect()
                logger.warning(f"Emergency disconnected from {broker_name}")
            except Exception as e:
                logger.error(f"Error disconnecting from {broker_name}: {e}")

        self.brokers.clear()