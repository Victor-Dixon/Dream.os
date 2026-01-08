#!/usr/bin/env python3
"""
AI Context Engine Session Manager
================================

Session management and background tasks for the AI Context Engine.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Main Engine → ai_context_engine.py
│   ├── Data Models → models.py
│   └── Context Processors → context_processors.py
├── Documentation:
│   └── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Classes:
- SessionManager: Handles session lifecycle and background tasks
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import asdict

from .models import ContextSession

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages context processing sessions and background tasks.

    Navigation:
    ├── Used by: AIContextEngine
    ├── Manages: ContextSession lifecycle
    └── Related: background task management, session cleanup policies
    """

    def __init__(self, session_timeout_hours: int = 2, max_sessions: int = 1000):
        """
        Initialize session manager.

        Navigation:
        ├── Configures: session_timeout, max_sessions limits
        └── Related: AIContextEngine initialization parameters
        """
        self.active_sessions: Dict[str, ContextSession] = {}
        self.session_timeout = timedelta(hours=session_timeout_hours)
        self.max_sessions = max_sessions

        # Background tasks
        self.cleanup_task: Optional[asyncio.Task] = None
        self.performance_monitor_task: Optional[asyncio.Task] = None

    async def start_background_tasks(self):
        """
        Start background tasks for session management.

        Navigation:
        ├── Creates: cleanup_task, performance_monitor_task
        └── Related: AIContextEngine.start_engine()
        """
        self.cleanup_task = asyncio.create_task(self._session_cleanup_loop())
        self.performance_monitor_task = asyncio.create_task(self._performance_monitor_loop())

    async def stop_background_tasks(self):
        """
        Stop background tasks.

        Navigation:
        ├── Cancels: cleanup_task, performance_monitor_task
        └── Related: AIContextEngine.stop_engine()
        """
        if self.cleanup_task:
            self.cleanup_task.cancel()
        if self.performance_monitor_task:
            self.performance_monitor_task.cancel()

    async def create_session(self, user_id: str, context_type: str,
                           initial_context: Dict[str, Any]) -> str:
        """
        Create a new context processing session.

        Navigation:
        ├── Used by: AIContextEngine.create_session()
        ├── Creates: ContextSession instance
        └── Related: session limit enforcement, ID generation
        """
        session_id = f"{user_id}_{context_type}_{int(time.time())}"

        session = ContextSession(
            session_id=session_id,
            user_id=user_id,
            context_type=context_type,
            start_time=datetime.now(),
            last_activity=datetime.now(),
            context_data=initial_context.copy()
        )

        # Enforce session limit
        if len(self.active_sessions) >= self.max_sessions:
            await self._cleanup_expired_sessions(force=True)

        self.active_sessions[session_id] = session
        return session_id

    async def update_session_activity(self, session_id: str):
        """
        Update last activity timestamp for a session.

        Navigation:
        ├── Used by: AIContextEngine.update_session_context()
        └── Related: session timeout calculations
        """
        if session_id in self.active_sessions:
            self.active_sessions[session_id].last_activity = datetime.now()

    def get_session(self, session_id: str) -> Optional[ContextSession]:
        """
        Get a session by ID.

        Navigation:
        ├── Used by: AIContextEngine methods
        └── Returns: ContextSession or None if not found
        """
        return self.active_sessions.get(session_id)

    def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get context data for a session.

        Navigation:
        ├── Used by: AIContextEngine.get_session_context()
        ├── Returns: formatted context data with risk metrics and suggestions
        └── Related: ContextSession data serialization
        """
        session = self.get_session(session_id)
        if not session:
            return None

        return {
            'session_id': session.session_id,
            'context_data': session.context_data,
            'risk_metrics': asdict(session.risk_metrics) if session.risk_metrics else None,
            'ai_suggestions': session.ai_suggestions,
            'performance_metrics': session.performance_metrics
        }

    async def end_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        End a session and return final metrics.

        Navigation:
        ├── Used by: AIContextEngine.end_session()
        ├── Removes: session from active_sessions
        └── Returns: session summary with duration and suggestion metrics
        """
        session = self.active_sessions.pop(session_id, None)
        if not session:
            return None

        # Calculate session summary
        duration = datetime.now() - session.start_time
        suggestions_applied = sum(1 for s in session.ai_suggestions if s.get('applied', False))

        session_summary = {
            'session_id': session_id,
            'duration_seconds': duration.total_seconds(),
            'total_suggestions': len(session.ai_suggestions),
            'suggestions_applied': suggestions_applied,
            'context_type': session.context_type,
            'final_context': session.context_data,
            'performance_metrics': session.performance_metrics
        }

        logger.info(f"🏁 Ended session {session_id}: {suggestions_applied}/{len(session.ai_suggestions)} suggestions applied")
        return session_summary

    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics.

        Navigation:
        ├── Used by: AIContextEngine.get_performance_stats()
        ├── Returns: session counts, types, and activity metrics
        └── Related: performance monitoring requirements
        """
        return {
            'active_sessions_count': len(self.active_sessions),
            'session_types': list(set(s.context_type for s in self.active_sessions.values())),
            'session_capacity_utilization': len(self.active_sessions) / self.max_sessions
        }

    async def _session_cleanup_loop(self):
        """
        Background task to cleanup expired sessions.

        Navigation:
        ├── Runs: every 5 minutes
        ├── Calls: _cleanup_expired_sessions()
        └── Related: session timeout policy enforcement
        """
        while True:
            try:
                await self._cleanup_expired_sessions()
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Session cleanup error: {e}")
                await asyncio.sleep(60)

    async def _cleanup_expired_sessions(self, force: bool = False):
        """
        Cleanup expired sessions.

        Navigation:
        ├── Used by: _session_cleanup_loop, create_session (when at capacity)
        ├── Removes: sessions exceeding timeout
        └── Related: session_timeout configuration
        """
        now = datetime.now()
        expired_sessions = []

        for session_id, session in self.active_sessions.items():
            if force or (now - session.last_activity) > self.session_timeout:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            self.active_sessions.pop(session_id, None)

        if expired_sessions:
            logger.info(f"🧹 Cleaned up {len(expired_sessions)} expired sessions")

    async def _performance_monitor_loop(self):
        """
        Background task to monitor and log performance.

        Navigation:
        ├── Runs: every hour
        ├── Logs: session performance metrics
        └── Related: monitoring and observability requirements
        """
        while True:
            try:
                # Log current performance stats
                stats = self.get_performance_stats()
                logger.info(f"📊 Session Manager Performance: {stats}")

                await asyncio.sleep(3600)  # Log every hour
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)