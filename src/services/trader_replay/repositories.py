"""
Trader Replay Repositories - Dream.OS Trading Replay Journal
===========================================================

Repository pattern implementation for data access layer.
Clean separation between business logic and data persistence.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: Repository pattern, <300 lines per class
Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.core.unified_logging_system import get_logger

from .models import (
    ReplaySession,
    ReplaySessionStatus,
    PaperTrade,
    TradeSide,
    TradeStatus,
    JournalEntry,
    JournalEntryType,
    BehavioralScore,
    Candle,
)

logger = get_logger(__name__)


class SessionRepository:
    """Repository for replay session data access."""

    def __init__(self, db_path: Path):
        """Initialize session repository."""
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get(self, session_id: int) -> Optional[ReplaySession]:
        """Get session by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT s.id, s.session_date, s.timeframe, s.candle_count, s.status, sym.symbol
                FROM sessions s
                JOIN symbols sym ON s.symbol_id = sym.id
                WHERE s.id = ?
                """,
                (session_id,),
            )

            row = cursor.fetchone()
            if not row:
                return None

            return ReplaySession(
                session_id=row[0],
                symbol=row[5],
                session_date=row[1],
                timeframe=row[2],
                status=ReplaySessionStatus(row[4]),
                total_candles=row[3],
            )
        finally:
            conn.close()

    def list_all(self, symbol: Optional[str] = None) -> List[ReplaySession]:
        """List all sessions, optionally filtered by symbol."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            if symbol:
                cursor.execute(
                    """
                    SELECT s.id, s.session_date, s.timeframe, s.candle_count, s.status, sym.symbol
                    FROM sessions s
                    JOIN symbols sym ON s.symbol_id = sym.id
                    WHERE sym.symbol = ?
                    ORDER BY s.session_date DESC
                    """,
                    (symbol,),
                )
            else:
                cursor.execute(
                    """
                    SELECT s.id, s.session_date, s.timeframe, s.candle_count, s.status, sym.symbol
                    FROM sessions s
                    JOIN symbols sym ON s.symbol_id = sym.id
                    ORDER BY s.session_date DESC
                    """
                )

            rows = cursor.fetchall()
            return [
                ReplaySession(
                    session_id=row[0],
                    symbol=row[5],
                    session_date=row[1],
                    timeframe=row[2],
                    status=ReplaySessionStatus(row[4]),
                    total_candles=row[3],
                )
                for row in rows
            ]
        finally:
            conn.close()

    def update_status(
        self, session_id: int, status: ReplaySessionStatus
    ) -> bool:
        """Update session status."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "UPDATE sessions SET status = ? WHERE id = ?",
                (status.value, session_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class TradeRepository:
    """Repository for paper trade data access."""

    def __init__(self, db_path: Path):
        """Initialize trade repository."""
        self.db_path = db_path

    def create(self, trade: PaperTrade) -> int:
        """Create a new paper trade."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO paper_trades
                (session_id, entry_timestamp, exit_timestamp, entry_price, exit_price,
                 quantity, side, entry_type, stop_loss, take_profit, pnl, r_multiple, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trade.session_id,
                    trade.entry_timestamp.isoformat() if trade.entry_timestamp else None,
                    trade.exit_timestamp.isoformat() if trade.exit_timestamp else None,
                    trade.entry_price,
                    trade.exit_price,
                    trade.quantity,
                    trade.side.value,
                    trade.entry_type,
                    trade.stop_loss,
                    trade.take_profit,
                    trade.pnl,
                    trade.r_multiple,
                    trade.status.value,
                ),
            )
            conn.commit()
            trade_id = cursor.lastrowid
            logger.info(f"Created paper trade {trade_id} for session {trade.session_id}")
            return trade_id
        finally:
            conn.close()

    def get(self, trade_id: int) -> Optional[PaperTrade]:
        """Get trade by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, session_id, entry_timestamp, exit_timestamp, entry_price,
                       exit_price, quantity, side, entry_type, stop_loss, take_profit,
                       pnl, r_multiple, status
                FROM paper_trades
                WHERE id = ?
                """,
                (trade_id,),
            )

            row = cursor.fetchone()
            if not row:
                return None

            return PaperTrade(
                trade_id=row[0],
                session_id=row[1],
                entry_timestamp=(
                    datetime.fromisoformat(row[2]) if row[2] else None
                ),
                exit_timestamp=(
                    datetime.fromisoformat(row[3]) if row[3] else None
                ),
                entry_price=row[4],
                exit_price=row[5],
                quantity=row[6],
                side=TradeSide(row[7]),
                entry_type=row[8],
                stop_loss=row[9],
                take_profit=row[10],
                pnl=row[11],
                r_multiple=row[12],
                status=TradeStatus(row[13]),
            )
        finally:
            conn.close()

    def list_by_session(self, session_id: int) -> List[PaperTrade]:
        """List all trades for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, session_id, entry_timestamp, exit_timestamp, entry_price,
                       exit_price, quantity, side, entry_type, stop_loss, take_profit,
                       pnl, r_multiple, status
                FROM paper_trades
                WHERE session_id = ?
                ORDER BY entry_timestamp ASC
                """,
                (session_id,),
            )

            rows = cursor.fetchall()
            return [
                PaperTrade(
                    trade_id=row[0],
                    session_id=row[1],
                    entry_timestamp=(
                        datetime.fromisoformat(row[2]) if row[2] else None
                    ),
                    exit_timestamp=(
                        datetime.fromisoformat(row[3]) if row[3] else None
                    ),
                    entry_price=row[4],
                    exit_price=row[5],
                    quantity=row[6],
                    side=TradeSide(row[7]),
                    entry_type=row[8],
                    stop_loss=row[9],
                    take_profit=row[10],
                    pnl=row[11],
                    r_multiple=row[12],
                    status=TradeStatus(row[13]),
                )
                for row in rows
            ]
        finally:
            conn.close()

    def update(self, trade: PaperTrade) -> bool:
        """Update an existing trade."""
        if not trade.trade_id:
            return False

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE paper_trades SET
                    exit_timestamp = ?, exit_price = ?, stop_loss = ?, take_profit = ?,
                    pnl = ?, r_multiple = ?, status = ?
                WHERE id = ?
                """,
                (
                    trade.exit_timestamp.isoformat() if trade.exit_timestamp else None,
                    trade.exit_price,
                    trade.stop_loss,
                    trade.take_profit,
                    trade.pnl,
                    trade.r_multiple,
                    trade.status.value,
                    trade.trade_id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()


class JournalRepository:
    """Repository for journal entry data access."""

    def __init__(self, db_path: Path):
        """Initialize journal repository."""
        self.db_path = db_path

    def create(self, entry: JournalEntry) -> int:
        """Create a new journal entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            template_json = (
                json.dumps(entry.template_data) if entry.template_data else None
            )

            cursor.execute(
                """
                INSERT INTO journal_entries
                (session_id, timestamp, candle_index, trade_id, entry_type,
                 content, emotion_tag, screenshot_path, template_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry.session_id,
                    entry.timestamp.isoformat() if entry.timestamp else None,
                    entry.candle_index,
                    entry.trade_id,
                    entry.entry_type.value,
                    entry.content,
                    entry.emotion_tag,
                    entry.screenshot_path,
                    template_json,
                ),
            )
            conn.commit()
            entry_id = cursor.lastrowid
            logger.info(
                f"Created journal entry {entry_id} for session {entry.session_id}"
            )
            return entry_id
        finally:
            conn.close()

    def list_by_session(self, session_id: int) -> List[JournalEntry]:
        """List all journal entries for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, session_id, timestamp, candle_index, trade_id, entry_type,
                       content, emotion_tag, screenshot_path, template_data
                FROM journal_entries
                WHERE session_id = ?
                ORDER BY timestamp ASC
                """,
                (session_id,),
            )

            rows = cursor.fetchall()
            entries = []
            for row in rows:
                template_data = None
                if row[9]:
                    try:
                        template_data = json.loads(row[9])
                    except (json.JSONDecodeError, TypeError):
                        pass

                entries.append(
                    JournalEntry(
                        entry_id=row[0],
                        session_id=row[1],
                        timestamp=(
                            datetime.fromisoformat(row[2]) if row[2] else None
                        ),
                        candle_index=row[3],
                        trade_id=row[4],
                        entry_type=JournalEntryType(row[5]),
                        content=row[6],
                        emotion_tag=row[7],
                        screenshot_path=row[8],
                        template_data=template_data,
                    )
                )
            return entries
        finally:
            conn.close()


class ScoreRepository:
    """Repository for behavioral score data access."""

    def __init__(self, db_path: Path):
        """Initialize score repository."""
        self.db_path = db_path

    def create(self, score: BehavioralScore) -> int:
        """Create a new behavioral score."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            details_json = json.dumps(score.details) if score.details else None

            cursor.execute(
                """
                INSERT OR REPLACE INTO scores
                (session_id, score_type, score_value, details)
                VALUES (?, ?, ?, ?)
                """,
                (
                    score.session_id,
                    score.score_type,
                    score.score_value,
                    details_json,
                ),
            )
            conn.commit()
            score_id = cursor.lastrowid
            logger.info(
                f"Created score {score_id} for session {score.session_id} ({score.score_type})"
            )
            return score_id
        finally:
            conn.close()

    def get_by_session(self, session_id: int) -> List[BehavioralScore]:
        """Get all scores for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, session_id, score_type, score_value, details, created_at
                FROM scores
                WHERE session_id = ?
                ORDER BY created_at DESC
                """,
                (session_id,),
            )

            rows = cursor.fetchall()
            scores = []
            for row in rows:
                details = None
                if row[4]:
                    try:
                        details = json.loads(row[4])
                    except (json.JSONDecodeError, TypeError):
                        pass

                scores.append(
                    BehavioralScore(
                        score_id=row[0],
                        session_id=row[1],
                        score_type=row[2],
                        score_value=row[3],
                        details=details,
                        created_at=(
                            datetime.fromisoformat(row[5]) if row[5] else None
                        ),
                    )
                )
            return scores
        finally:
            conn.close()



