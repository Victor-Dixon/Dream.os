"""
Replay Engine - Dream.OS Trading Replay Journal
===============================================

Core logic for candle-by-candle replay simulation.
Deterministic, testable replay system with state management.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from src.core.unified_logging_system import get_logger

from .models import Candle, ReplaySession, ReplaySessionStatus

logger = get_logger(__name__)


@dataclass
class ReplayState:
    """Current replay state."""

    session_id: int
    current_index: int
    is_playing: bool
    playback_speed: float  # 1.0 = normal, 2.0 = 2x, etc.
    visible_candles: List[Candle]
    total_candles: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        from src.core.utils.serialization_utils import to_dict
        result = to_dict(self)
        # Ensure visible_candles are serialized
        if "visible_candles" in result:
            result["visible_candles"] = [c.to_dict() if hasattr(c, 'to_dict') else to_dict(c) for c in self.visible_candles]
        return result


class ReplayEngine:
    """
    Manages replay session lifecycle and state.

    Handles:
    - Session creation and loading
    - Candle-by-candle progression
    - State management
    - Database operations
    """

    def __init__(self, db_path: Path):
        """
        Initialize replay engine.

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_database()

        # Active replay sessions (in-memory state)
        self._active_sessions: Dict[int, "ReplaySessionState"] = {}

        logger.info(f"ReplayEngine initialized (db: {db_path})")

    def _ensure_database(self) -> None:
        """Create database and tables if they don't exist."""
        schema_path = Path(__file__).parent / "schema.sql"
        if schema_path.exists():
            conn = sqlite3.connect(self.db_path)
            with open(schema_path, "r") as f:
                conn.executescript(f.read())
            conn.commit()
            conn.close()
            logger.debug("Database schema initialized")

    def create_session(
        self,
        symbol: str,
        session_date: str,
        timeframe: str = "1m",
        candles: Optional[List[Dict[str, Any]]] = None,
    ) -> int:
        """
        Create a new replay session.

        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            session_date: Session date (YYYY-MM-DD)
            timeframe: Candle timeframe (default: '1m')
            candles: List of candle data (optional)

        Returns:
            Session ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get or create symbol
            cursor.execute("SELECT id FROM symbols WHERE symbol = ?", (symbol,))
            symbol_row = cursor.fetchone()
            if not symbol_row:
                cursor.execute(
                    "INSERT INTO symbols (symbol, asset_type) VALUES (?, ?)",
                    (symbol, "stock"),
                )
                symbol_id = cursor.lastrowid
            else:
                symbol_id = symbol_row[0]

            # Create session
            cursor.execute(
                """
                INSERT OR IGNORE INTO sessions (symbol_id, session_date, timeframe, candle_count, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    symbol_id,
                    session_date,
                    timeframe,
                    len(candles) if candles else 0,
                    ReplaySessionStatus.READY.value,
                ),
            )

            cursor.execute(
                """
                SELECT id FROM sessions
                WHERE symbol_id = ? AND session_date = ? AND timeframe = ?
                """,
                (symbol_id, session_date, timeframe),
            )

            session_row = cursor.fetchone()
            session_id = session_row[0] if session_row else cursor.lastrowid

            # Insert candles if provided
            if candles:
                for idx, candle in enumerate(candles):
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO candles
                        (session_id, timestamp, open, high, low, close, volume, candle_index)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            session_id,
                            candle["timestamp"],
                            candle["open"],
                            candle["high"],
                            candle["low"],
                            candle["close"],
                            candle.get("volume", 0),
                            idx,
                        ),
                    )

                # Update candle count
                cursor.execute(
                    "UPDATE sessions SET candle_count = ? WHERE id = ?",
                    (len(candles), session_id),
                )

            conn.commit()
            logger.info(
                f"Created replay session {session_id} for {symbol} on {session_date}"
            )
            return session_id

        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to create session: {e}", exc_info=True)
            raise
        finally:
            conn.close()

    def get_session_info(self, session_id: int) -> Dict[str, Any]:
        """
        Get session information.

        Args:
            session_id: Session ID

        Returns:
            Session info dictionary
        """
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
                return {}

            return {
                "session_id": row[0],
                "session_date": row[1],
                "timeframe": row[2],
                "candle_count": row[3],
                "status": row[4],
                "symbol": row[5],
            }
        finally:
            conn.close()

    def get_replay_state(self, session_id: int) -> ReplayState:
        """
        Get current replay state for a session.

        Args:
            session_id: Session ID

        Returns:
            ReplayState object
        """
        if session_id not in self._active_sessions:
            # Load session into memory
            session_state = ReplaySessionState(self.db_path, session_id)
            self._active_sessions[session_id] = session_state

        return self._active_sessions[session_id].get_state()

    def step_replay(self, session_id: int, direction: str = "forward") -> ReplayState:
        """
        Step replay forward or backward.

        Args:
            session_id: Session ID
            direction: 'forward' or 'backward'

        Returns:
            Updated ReplayState
        """
        if session_id not in self._active_sessions:
            self._active_sessions[session_id] = ReplaySessionState(
                self.db_path, session_id
            )

        session = self._active_sessions[session_id]
        if direction == "forward":
            session.step()
        else:
            session.step_back()

        return session.get_state()

    def pause_replay(self, session_id: int) -> None:
        """Pause replay session."""
        if session_id in self._active_sessions:
            self._active_sessions[session_id].pause()
        else:
            self._active_sessions[session_id] = ReplaySessionState(
                self.db_path, session_id
            )
            self._active_sessions[session_id].pause()


class ReplaySessionState:
    """
    Manages state for a single replay session.

    Handles:
    - Candle loading and indexing
    - Playback control
    - State progression
    """

    def __init__(self, db_path: Path, session_id: int):
        """Initialize replay session state."""
        self.db_path = db_path
        self.session_id = session_id
        self.candles: List[Candle] = []
        self.current_index = 0
        self.is_playing = False
        self.playback_speed = 1.0

        self._load_candles()

    def _load_candles(self) -> None:
        """Load all candles for this session from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT timestamp, open, high, low, close, volume, candle_index
                FROM candles
                WHERE session_id = ?
                ORDER BY candle_index ASC
                """,
                (self.session_id,),
            )

            rows = cursor.fetchall()
            self.candles = [
                Candle(
                    timestamp=datetime.fromisoformat(row[0]),
                    open=float(row[1]),
                    high=float(row[2]),
                    low=float(row[3]),
                    close=float(row[4]),
                    volume=int(row[5]),
                    candle_index=int(row[6]),
                )
                for row in rows
            ]

            logger.debug(
                f"Loaded {len(self.candles)} candles for session {self.session_id}"
            )
        finally:
            conn.close()

    def get_state(self) -> ReplayState:
        """Get current replay state."""
        return ReplayState(
            session_id=self.session_id,
            current_index=self.current_index,
            is_playing=self.is_playing,
            playback_speed=self.playback_speed,
            visible_candles=self.candles[: self.current_index + 1],
            total_candles=len(self.candles),
        )

    def step(self) -> List[Candle]:
        """Move forward one candle."""
        if self.current_index < len(self.candles) - 1:
            self.current_index += 1
        return self.candles[: self.current_index + 1]

    def step_back(self) -> List[Candle]:
        """Move backward one candle."""
        if self.current_index > 0:
            self.current_index -= 1
        return self.candles[: self.current_index + 1]

    def jump_to_time(self, target_time: datetime) -> List[Candle]:
        """Jump to specific timestamp."""
        for i, candle in enumerate(self.candles):
            if candle.timestamp >= target_time:
                self.current_index = i
                break
        else:
            self.current_index = len(self.candles) - 1

        return self.candles[: self.current_index + 1]

    def play(self) -> None:
        """Start playing."""
        self.is_playing = True

    def pause(self) -> None:
        """Pause playing."""
        self.is_playing = False

    def set_speed(self, speed: float) -> None:
        """Set playback speed (1.0 = normal, 2.0 = 2x, etc.)."""
        self.playback_speed = max(0.1, min(10.0, speed))

    def reset(self) -> List[Candle]:
        """Reset to beginning."""
        self.current_index = 0
        self.is_playing = False
        return self.candles[:1] if self.candles else []

    def get_progress(self) -> float:
        """Get replay progress (0.0 to 1.0)."""
        if not self.candles:
            return 0.0
        return (self.current_index + 1) / len(self.candles)

    def is_complete(self) -> bool:
        """Check if replay is complete."""
        return self.current_index >= len(self.candles) - 1



