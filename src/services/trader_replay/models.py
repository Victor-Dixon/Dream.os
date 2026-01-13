"""
Trader Replay Models - Dream.OS Trading Replay Journal
======================================================

Data models for trading replay and journaling system.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: Models with dataclasses, enums, <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List

from src.core.utils.serialization_utils import to_dict


class ReplaySessionStatus(Enum):
    """Replay session status enumeration."""

    READY = "ready"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class TradeSide(Enum):
    """Trade side enumeration."""

    LONG = "long"
    SHORT = "short"


class TradeStatus(Enum):
    """Trade status enumeration."""

    OPEN = "open"
    CLOSED = "closed"
    STOPPED = "stopped"


class JournalEntryType(Enum):
    """Journal entry type enumeration."""

    NOTE = "note"
    SETUP = "setup"
    TRIGGER = "trigger"
    RISK = "risk"
    RESULT = "result"
    LESSON = "lesson"


@dataclass
class Candle:
    """Single OHLCV candle."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    candle_index: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candle":
        """Create from dictionary."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            open=float(data["open"]),
            high=float(data["high"]),
            low=float(data["low"]),
            close=float(data["close"]),
            volume=int(data.get("volume", 0)),
            candle_index=int(data.get("candle_index", 0)),
        )


@dataclass
class ReplaySession:
    """Replay session data model."""

    session_id: int
    symbol: str
    session_date: str
    timeframe: str
    status: ReplaySessionStatus
    current_index: int = 0
    total_candles: int = 0
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplaySession":
        """Create from dictionary."""
        return cls(
            session_id=int(data["session_id"]),
            symbol=str(data["symbol"]),
            session_date=str(data["session_date"]),
            timeframe=str(data.get("timeframe", "1m")),
            status=ReplaySessionStatus(data.get("status", "ready")),
            current_index=int(data.get("current_index", 0)),
            total_candles=int(data.get("total_candles", 0)),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
        )


@dataclass
class PaperTrade:
    """Paper trade data model."""

    trade_id: Optional[int] = None
    session_id: int = 0
    entry_timestamp: Optional[datetime] = None
    exit_timestamp: Optional[datetime] = None
    entry_price: float = 0.0
    exit_price: Optional[float] = None
    quantity: int = 0
    side: TradeSide = TradeSide.LONG
    entry_type: str = "market"
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    pnl: Optional[float] = None
    r_multiple: Optional[float] = None
    status: TradeStatus = TradeStatus.OPEN

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PaperTrade":
        """Create from dictionary."""
        return cls(
            trade_id=data.get("trade_id"),
            session_id=int(data["session_id"]),
            entry_timestamp=(
                datetime.fromisoformat(data["entry_timestamp"])
                if data.get("entry_timestamp")
                else None
            ),
            exit_timestamp=(
                datetime.fromisoformat(data["exit_timestamp"])
                if data.get("exit_timestamp")
                else None
            ),
            entry_price=float(data["entry_price"]),
            exit_price=(
                float(data["exit_price"])
                if data.get("exit_price")
                else None
            ),
            quantity=int(data["quantity"]),
            side=TradeSide(data.get("side", "long")),
            entry_type=str(data.get("entry_type", "market")),
            stop_loss=(
                float(data["stop_loss"]) if data.get("stop_loss") else None
            ),
            take_profit=(
                float(data["take_profit"]) if data.get("take_profit") else None
            ),
            pnl=float(data["pnl"]) if data.get("pnl") else None,
            r_multiple=(
                float(data["r_multiple"]) if data.get("r_multiple") else None
            ),
            status=TradeStatus(data.get("status", "open")),
        )


@dataclass
class JournalEntry:
    """Journal entry data model."""

    entry_id: Optional[int] = None
    session_id: int = 0
    timestamp: Optional[datetime] = None
    candle_index: Optional[int] = None
    trade_id: Optional[int] = None
    entry_type: JournalEntryType = JournalEntryType.NOTE
    content: str = ""
    emotion_tag: Optional[str] = None
    screenshot_path: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JournalEntry":
        """Create from dictionary."""
        return cls(
            entry_id=data.get("entry_id"),
            session_id=int(data["session_id"]),
            timestamp=(
                datetime.fromisoformat(data["timestamp"])
                if data.get("timestamp")
                else None
            ),
            candle_index=data.get("candle_index"),
            trade_id=data.get("trade_id"),
            entry_type=JournalEntryType(
                data.get("entry_type", "note")
            ),
            content=str(data.get("content", "")),
            emotion_tag=data.get("emotion_tag"),
            screenshot_path=data.get("screenshot_path"),
            template_data=data.get("template_data"),
        )


@dataclass
class BehavioralScore:
    """Behavioral score data model."""

    score_id: Optional[int] = None
    session_id: int = 0
    score_type: str = ""
    score_value: float = 0.0
    details: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BehavioralScore":
        """Create from dictionary."""
        return cls(
            score_id=data.get("score_id"),
            session_id=int(data["session_id"]),
            score_type=str(data["score_type"]),
            score_value=float(data.get("score_value", 0.0)),
            details=data.get("details"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
        )



