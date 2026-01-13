"""
Trade Processor (T1–T5)
=======================

Transforms raw trade data from a work session into:
- trade journal context for the trade_journal template
- social-friendly trade summary context
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    symbol: str
    action: str
    quantity: float
    price: float
    timestamp: str
    profit_loss: Optional[float] = None
    notes: Optional[str] = None


def _parse_trades(source_data: Dict[str, Any]) -> List[TradeRecord]:
    trades_raw = source_data.get("trades") or []
    trades: List[TradeRecord] = []
    for item in trades_raw:
        if not isinstance(item, dict):
            continue
        try:
            trades.append(
                TradeRecord(
                    symbol=str(item.get("symbol", "")),
                    action=str(item.get("action", "buy")),
                    quantity=float(item.get("quantity", 0) or 0),
                    price=float(item.get("price", 0) or 0),
                    timestamp=str(item.get("timestamp", "")),
                    profit_loss=(
                        float(item["profit_loss"]) if "profit_loss" in item and item["profit_loss"] is not None else None
                    ),
                    notes=str(item.get("notes", "")) or None,
                )
            )
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning("Failed to parse trade record %s: %s", item, exc)
    return trades


def _compute_performance(trades: List[TradeRecord]) -> Dict[str, Any]:
    if not trades:
        return {}

    total_pnl = sum(t.profit_loss or 0.0 for t in trades)
    wins = [t for t in trades if (t.profit_loss or 0) > 0]
    losses = [t for t in trades if (t.profit_loss or 0) < 0]

    best_trade = max(trades, key=lambda t: t.profit_loss or float("-inf"))
    worst_trade = min(trades, key=lambda t: t.profit_loss or float("inf"))

    win_rate = (len(wins) / len(trades)) * 100 if trades else 0.0

    return {
        "total_pnl": round(total_pnl, 2),
        "win_rate": round(win_rate, 1),
        "best_trade": f"{best_trade.symbol} {best_trade.action} ({best_trade.profit_loss})"
        if best_trade.profit_loss is not None
        else None,
        "worst_trade": f"{worst_trade.symbol} {worst_trade.action} ({worst_trade.profit_loss})"
        if worst_trade.profit_loss is not None
        else None,
    }


def prepare_trade_journal_context(session: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare context dict for the trade_journal template.
    """
    metadata = session.get("metadata") or {}
    source_data = session.get("source_data") or {}
    trades = _parse_trades(source_data)

    duration = metadata.get("duration_minutes") or 0
    performance = _compute_performance(trades) if trades else {}

    context: Dict[str, Any] = {
        "session_id": session.get("session_id", "unknown-session"),
        "agent_id": session.get("agent_id", "Agent-?"),
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "duration_minutes": duration,
        "trades_executed": len(trades),
        "performance": performance,
        "trades": [t.__dict__ for t in trades],
        "lessons": session.get("lessons") or [],
        "market_analysis": session.get("market_analysis"),
        "what_worked": session.get("what_worked") or [],
        "what_didnt_work": session.get("what_didnt_work") or [],
        "next_goals": session.get("next_goals") or [],
        "charts": session.get("charts") or [],
    }

    logger.info(
        "Trade journal context prepared for session %s (trades=%s)",
        context["session_id"],
        len(trades),
    )
    return context


def build_social_trade_summary(context: Dict[str, Any]) -> str:
    """
    Build a one-line social summary for a trading session.
    """
    trades_executed = context.get("trades_executed", 0)
    performance = context.get("performance") or {}
    total_pnl = performance.get("total_pnl")
    win_rate = performance.get("win_rate")

    parts: List[str] = []
    parts.append(f"{trades_executed} trade(s)")
    if total_pnl is not None:
        parts.append(f"P&L: {total_pnl}")
    if win_rate is not None:
        parts.append(f"Win rate: {win_rate}%")

    return "Trading session recap: " + ", ".join(parts)


