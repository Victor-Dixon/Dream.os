"""
Trader Replay Orchestrator - Dream.OS Trading Replay Journal
============================================================

Unified orchestrator for trading replay and journaling system.
Coordinates replay sessions, agent integration, and behavioral scoring.

<!-- SSOT Domain: business-intelligence -->

V2 Compliance: <400 lines, orchestrator pattern
Migrated to BaseService for consolidated initialization and error handling.
Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.core.base.base_service import BaseService
from src.core.unified_logging_system import get_logger, configure_logging
from src.services.unified_messaging_service import UnifiedMessagingService

from .models import (
    ReplaySession,
    ReplaySessionStatus,
    PaperTrade,
    JournalEntry,
    BehavioralScore,
    Candle,
)
from .replay_engine import ReplayEngine, ReplayState

# Configure logging
log_dir = Path(__file__).parent.parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "trader_replay_orchestrator.log"
configure_logging(level="DEBUG", log_file=log_file)

logger = get_logger(__name__)


class TraderReplayOrchestrator(BaseService):
    """
    Orchestrates trading replay and journaling system.

    Manages:
    - Replay session lifecycle
    - Agent workspace integration
    - Messaging system notifications
    - Behavioral scoring coordination
    """

    def __init__(
        self,
        db_path: Optional[Path] = None,
        agent_workspace_path: Optional[Path] = None,
    ):
        """
        Initialize trader replay orchestrator.

        Args:
            db_path: Path to SQLite database (default: agent_workspaces/data/trader_replay.db)
            agent_workspace_path: Base path for agent workspaces
        """
        super().__init__("TraderReplayOrchestrator")
        # Set default database path
        if db_path is None:
            base_path = (
                Path(__file__).parent.parent.parent.parent
                / "agent_workspaces"
                / "data"
            )
            base_path.mkdir(parents=True, exist_ok=True)
            db_path = base_path / "trader_replay.db"

        self.db_path = db_path
        self.agent_workspace_path = (
            agent_workspace_path
            or Path(__file__).parent.parent.parent.parent
            / "agent_workspaces"
        )

        # Initialize components
        self.replay_engine = ReplayEngine(db_path)
        self.messaging_service = UnifiedMessagingService()

        # Active replay sessions
        self.active_sessions: Dict[int, Dict[str, Any]] = {}

        self.logger.info(
            f"TraderReplayOrchestrator initialized (db: {db_path})"
        )

    def create_session(
        self,
        symbol: str,
        session_date: str,
        timeframe: str = "1m",
        candles: Optional[List[Dict[str, Any]]] = None,
        agent_id: Optional[str] = None,
    ) -> int:
        """
        Create a new replay session.

        Args:
            symbol: Trading symbol (e.g., 'AAPL')
            session_date: Session date (YYYY-MM-DD)
            timeframe: Candle timeframe (default: '1m')
            candles: List of candle data (optional)
            agent_id: Agent ID for workspace integration

        Returns:
            Session ID
        """
        try:
            session_id = self.replay_engine.create_session(
                symbol=symbol,
                session_date=session_date,
                timeframe=timeframe,
                candles=candles or [],
            )

            # Store session metadata
            self.active_sessions[session_id] = {
                "session_id": session_id,
                "symbol": symbol,
                "session_date": session_date,
                "timeframe": timeframe,
                "agent_id": agent_id,
                "status": ReplaySessionStatus.READY,
                "created_at": datetime.now(),
            }

            # Notify agent if specified
            if agent_id:
                self._notify_agent(
                    agent_id,
                    f"✅ Trading replay session created: {symbol} on {session_date} (Session ID: {session_id})",
                )

            self.logger.info(
                f"Created replay session {session_id} for {symbol} on {session_date}"
            )
            return session_id

        except Exception as e:
            self.logger.error(f"Failed to create replay session: {e}", exc_info=True)
            raise

    def start_replay(self, session_id: int) -> Dict[str, Any]:
        """
        Start a replay session.

        Args:
            session_id: Session ID

        Returns:
            Replay state dictionary
        """
        try:
            if session_id not in self.active_sessions:
                # Load session into active sessions
                session_info = self.replay_engine.get_session_info(session_id)
                if not session_info:
                    raise ValueError(f"Session {session_id} not found")

                self.active_sessions[session_id] = {
                    **session_info,
                    "status": ReplaySessionStatus.IN_PROGRESS,
                }

            replay_state = self.replay_engine.get_replay_state(session_id)
            self.active_sessions[session_id]["status"] = (
                ReplaySessionStatus.IN_PROGRESS
            )

            self.logger.info(f"Started replay session {session_id}")
            return replay_state.to_dict()

        except Exception as e:
            self.logger.error(
                f"Failed to start replay session {session_id}: {e}",
                exc_info=True,
            )
            raise

    def step_replay(
        self, session_id: int, direction: str = "forward"
    ) -> Dict[str, Any]:
        """
        Step replay forward or backward.

        Args:
            session_id: Session ID
            direction: 'forward' or 'backward'

        Returns:
            Updated replay state
        """
        try:
            replay_state = self.replay_engine.step_replay(
                session_id, direction
            )
            return replay_state.to_dict()

        except Exception as e:
            self.logger.error(
                f"Failed to step replay session {session_id}: {e}",
                exc_info=True,
            )
            raise

    def pause_replay(self, session_id: int) -> None:
        """Pause replay session."""
        try:
            self.replay_engine.pause_replay(session_id)
            if session_id in self.active_sessions:
                self.active_sessions[session_id]["status"] = (
                    ReplaySessionStatus.PAUSED
                )
            self.logger.info(f"Paused replay session {session_id}")

        except Exception as e:
            self.logger.error(
                f"Failed to pause replay session {session_id}: {e}",
                exc_info=True,
            )
            raise

    def complete_session(self, session_id: int) -> Dict[str, Any]:
        """
        Complete a replay session and generate summary.

        Args:
            session_id: Session ID

        Returns:
            Session summary dictionary
        """
        try:
            # Update session status
            if session_id in self.active_sessions:
                self.active_sessions[session_id]["status"] = (
                    ReplaySessionStatus.COMPLETED
                )

            # Generate session summary (placeholder for future implementation)
            summary = {
                "session_id": session_id,
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
            }

            # Notify agent if session has agent_id
            session = self.active_sessions.get(session_id, {})
            agent_id = session.get("agent_id")
            if agent_id:
                self._notify_agent(
                    agent_id,
                    f"✅ Trading replay session {session_id} completed. Summary available.",
                )

            self.logger.info(f"Completed replay session {session_id}")
            return summary

        except Exception as e:
            self.logger.error(
                f"Failed to complete replay session {session_id}: {e}",
                exc_info=True,
            )
            raise

    def _notify_agent(self, agent_id: str, message: str) -> None:
        """
        Notify agent via messaging system.

        Args:
            agent_id: Agent ID
            message: Notification message
        """
        try:
            self.messaging_service.send_message(
                agent=agent_id,
                message=message,
                priority="normal",
                use_pyautogui=False,
            )
            self.logger.debug(f"Sent notification to {agent_id}")

        except Exception as e:
            self.logger.warning(
                f"Failed to notify agent {agent_id}: {e}",
                exc_info=True,
            )

    def get_session_status(self, session_id: int) -> Dict[str, Any]:
        """
        Get current session status.

        Args:
            session_id: Session ID

        Returns:
            Status dictionary
        """
        try:
            if session_id in self.active_sessions:
                return self.active_sessions[session_id]

            session_info = self.replay_engine.get_session_info(session_id)
            return session_info or {}

        except Exception as e:
            self.logger.error(
                f"Failed to get session status {session_id}: {e}",
                exc_info=True,
            )
            return {}

