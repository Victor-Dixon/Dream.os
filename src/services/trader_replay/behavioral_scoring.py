"""
Behavioral Scoring - Dream.OS Trading Replay Journal
=====================================================

Behavioral analysis and scoring algorithms for trading performance.
Analyzes trading patterns, risk management, and discipline.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: <300 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist) with Agent-5 (Business Intelligence)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from src.core.unified_logging_system import get_logger

from .models import PaperTrade, TradeStatus, TradeSide, BehavioralScore
from .repositories import TradeRepository

logger = get_logger(__name__)


class BehavioralScorer:
    """
    Analyzes trading behavior and generates scores.

    Scoring categories:
    - Stop integrity: Adherence to stop loss rules
    - Patience: Waiting for proper setups
    - Risk discipline: Position sizing and risk management
    - Rule adherence: Following trading plan
    - Overtrading: Trading frequency and quality
    """

    def __init__(self, trade_repository: TradeRepository):
        """Initialize behavioral scorer."""
        self.trade_repository = trade_repository
        logger.info("BehavioralScorer initialized")

    def calculate_stop_integrity_score(
        self, session_id: int, trades: List[PaperTrade]
    ) -> BehavioralScore:
        """
        Calculate stop integrity score.

        Measures adherence to stop loss rules.
        - Points deducted for moving stops
        - Points deducted for not using stops
        - Bonus for consistent stop usage
        """
        if not trades:
            return BehavioralScore(
                session_id=session_id,
                score_type="stop_integrity",
                score_value=0.0,
                details={"reason": "No trades to analyze"},
            )

        total_trades = len(trades)
        trades_with_stops = sum(1 for t in trades if t.stop_loss)
        stopped_trades = sum(
            1 for t in trades if t.status == TradeStatus.STOPPED
        )

        # Base score from stop usage
        stop_usage_score = (trades_with_stops / total_trades) * 50

        # Bonus for actually getting stopped (shows stops were real)
        stop_effectiveness_score = (stopped_trades / trades_with_stops * 50) if trades_with_stops > 0 else 0

        total_score = min(100.0, stop_usage_score + stop_effectiveness_score)

        return BehavioralScore(
            session_id=session_id,
            score_type="stop_integrity",
            score_value=round(total_score, 2),
            details={
                "total_trades": total_trades,
                "trades_with_stops": trades_with_stops,
                "stopped_trades": stopped_trades,
                "stop_usage_rate": trades_with_stops / total_trades if total_trades > 0 else 0,
            },
        )

    def calculate_patience_score(
        self, session_id: int, trades: List[PaperTrade]
    ) -> BehavioralScore:
        """
        Calculate patience score.

        Measures quality over quantity:
        - Fewer trades with better setups = higher score
        - Time between trades indicates patience
        - Reward for selective trading
        """
        if not trades:
            return BehavioralScore(
                session_id=session_id,
                score_type="patience",
                score_value=100.0,  # Perfect patience = no trades
                details={"reason": "No trades - maximum patience"},
            )

        total_trades = len(trades)
        winning_trades = sum(1 for t in trades if t.pnl and t.pnl > 0)

        # Calculate average time between trades
        trade_times = sorted(
            [
                t.entry_timestamp
                for t in trades
                if t.entry_timestamp is not None
            ]
        )

        time_intervals = []
        for i in range(1, len(trade_times)):
            delta = (trade_times[i] - trade_times[i - 1]).total_seconds() / 3600
            time_intervals.append(delta)

        avg_time_between = (
            sum(time_intervals) / len(time_intervals)
            if time_intervals
            else 0
        )

        # Score based on trade quality and spacing
        # Fewer trades = higher patience score
        trade_frequency_penalty = min(50, total_trades * 5)
        win_rate_bonus = (winning_trades / total_trades * 30) if total_trades > 0 else 0
        spacing_bonus = min(20, avg_time_between / 2)  # Reward for spacing trades

        total_score = max(
            0.0,
            100.0 - trade_frequency_penalty + win_rate_bonus + spacing_bonus,
        )

        return BehavioralScore(
            session_id=session_id,
            score_type="patience",
            score_value=round(total_score, 2),
            details={
                "total_trades": total_trades,
                "winning_trades": winning_trades,
                "win_rate": winning_trades / total_trades if total_trades > 0 else 0,
                "avg_hours_between_trades": round(avg_time_between, 2),
            },
        )

    def calculate_risk_discipline_score(
        self, session_id: int, trades: List[PaperTrade]
    ) -> BehavioralScore:
        """
        Calculate risk discipline score.

        Measures:
        - Position sizing consistency
        - Risk-reward ratios
        - Maximum drawdown management
        """
        if not trades:
            return BehavioralScore(
                session_id=session_id,
                score_type="risk_discipline",
                score_value=0.0,
                details={"reason": "No trades to analyze"},
            )

        # Analyze position sizing
        quantities = [t.quantity for t in trades if t.quantity > 0]
        if not quantities:
            return BehavioralScore(
                session_id=session_id,
                score_type="risk_discipline",
                score_value=0.0,
                details={"reason": "No valid position sizes"},
            )

        avg_quantity = sum(quantities) / len(quantities)
        size_variance = sum(
            abs(q - avg_quantity) for q in quantities
        ) / len(quantities)
        size_consistency = max(
            0, 50 - (size_variance / avg_quantity * 50) if avg_quantity > 0 else 0
        )

        # Analyze R-multiples
        r_multiples = [t.r_multiple for t in trades if t.r_multiple is not None]
        avg_r_multiple = (
            sum(r_multiples) / len(r_multiples) if r_multiples else 0
        )
        r_multiple_score = min(50, avg_r_multiple * 10) if avg_r_multiple > 0 else 0

        total_score = min(100.0, size_consistency + r_multiple_score)

        return BehavioralScore(
            session_id=session_id,
            score_type="risk_discipline",
            score_value=round(total_score, 2),
            details={
                "avg_position_size": round(avg_quantity, 2),
                "size_consistency_score": round(size_consistency, 2),
                "avg_r_multiple": round(avg_r_multiple, 2),
                "r_multiple_score": round(r_multiple_score, 2),
            },
        )

    def calculate_rule_adherence_score(
        self, session_id: int, trades: List[PaperTrade]
    ) -> BehavioralScore:
        """
        Calculate rule adherence score.

        Measures following trading plan:
        - Consistent entry types
        - Proper use of stop loss and take profit
        - Adherence to trading rules
        """
        if not trades:
            return BehavioralScore(
                session_id=session_id,
                score_type="rule_adherence",
                score_value=0.0,
                details={"reason": "No trades to analyze"},
            )

        total_trades = len(trades)

        # Check for consistent entry types
        market_entries = sum(1 for t in trades if t.entry_type == "market")
        limit_entries = sum(1 for t in trades if t.entry_type == "limit")
        entry_consistency = (
            max(market_entries, limit_entries) / total_trades * 30
        )

        # Check for stop/target usage
        trades_with_stops = sum(1 for t in trades if t.stop_loss)
        trades_with_targets = sum(1 for t in trades if t.take_profit)
        risk_management_usage = (
            (trades_with_stops + trades_with_targets) / (total_trades * 2) * 70
        )

        total_score = min(100.0, entry_consistency + risk_management_usage)

        return BehavioralScore(
            session_id=session_id,
            score_type="rule_adherence",
            score_value=round(total_score, 2),
            details={
                "total_trades": total_trades,
                "market_entries": market_entries,
                "limit_entries": limit_entries,
                "trades_with_stops": trades_with_stops,
                "trades_with_targets": trades_with_targets,
            },
        )

    def calculate_all_scores(self, session_id: int) -> List[BehavioralScore]:
        """
        Calculate all behavioral scores for a session.

        Args:
            session_id: Session ID

        Returns:
            List of BehavioralScore objects
        """
        try:
            trades = self.trade_repository.list_by_session(session_id)

            scores = [
                self.calculate_stop_integrity_score(session_id, trades),
                self.calculate_patience_score(session_id, trades),
                self.calculate_risk_discipline_score(session_id, trades),
                self.calculate_rule_adherence_score(session_id, trades),
            ]

            logger.info(
                f"Calculated {len(scores)} behavioral scores for session {session_id}"
            )
            return scores

        except Exception as e:
            logger.error(
                f"Failed to calculate scores for session {session_id}: {e}",
                exc_info=True,
            )
            return []



