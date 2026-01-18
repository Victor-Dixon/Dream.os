#!/usr/bin/env python3
"""
AI Context Engine Session Manager
================================

Session management and background tasks for the AI Context Engine.

<!-- SSOT Domain: ai_context -->
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import uuid4

from .models import ContextSession

logger = logging.getLogger(__name__)


class SessionManager:
    """Manage context sessions and background maintenance tasks."""

    def __init__(self, session_timeout_hours: int = 2, max_sessions: int = 1000):
        self.active_sessions: Dict[str, ContextSession] = {}
        self.session_contexts: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=session_timeout_hours)
        self.max_sessions = max_sessions
        self.cleanup_task: Optional[asyncio.Task] = None
        self.performance_monitor_task: Optional[asyncio.Task] = None

    async def start_background_tasks(self) -> None:
        """Start background tasks for session cleanup and monitoring."""
        if not self.cleanup_task:
            self.cleanup_task = asyncio.create_task(self._session_cleanup_loop())
        if not self.performance_monitor_task:
            self.performance_monitor_task = asyncio.create_task(self._performance_monitor_loop())

    async def stop_background_tasks(self) -> None:
        """Stop background tasks."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            self.cleanup_task = None
        if self.performance_monitor_task:
            self.performance_monitor_task.cancel()
            self.performance_monitor_task = None

    async def create_session(
        self,
        user_id: str,
        context_type: str,
        initial_context: Dict[str, Any],
    ) -> str:
        """Create a new context session and return its ID."""
        if len(self.active_sessions) >= self.max_sessions:
            raise ValueError("Maximum number of sessions reached")

        session_id = str(uuid4())
        now = datetime.now()
        self.active_sessions[session_id] = ContextSession(
            session_id=session_id,
            user_id=user_id,
            context_type=context_type,
            start_time=now,
            last_activity=now,
        )
        self.session_contexts[session_id] = dict(initial_context)
        return session_id

    async def update_session_activity(self, session_id: str) -> None:
        """Update last activity timestamp for a session."""
        session = self.active_sessions.get(session_id)
        if session:
            session.last_activity = datetime.now()

    def get_session(self, session_id: str) -> Optional[ContextSession]:
        """Get a session by ID."""
        return self.active_sessions.get(session_id)

    def get_session_context(self, session_id: str) -> Dict[str, Any]:
        """Return stored context for a session, if available."""
        return self.session_contexts.get(session_id, {})

    def update_session_context(self, session_id: str, context: Dict[str, Any]) -> None:
        """Update stored context for a session."""
        if session_id in self.session_contexts:
            self.session_contexts[session_id].update(context)

    async def _session_cleanup_loop(self) -> None:
        while True:
            await asyncio.sleep(60)
            self._cleanup_expired_sessions()

    def _cleanup_expired_sessions(self) -> None:
        now = datetime.now()
        expired_sessions = [
            session_id
            for session_id, session in self.active_sessions.items()
            if now - session.last_activity > self.session_timeout
        ]
        for session_id in expired_sessions:
            self.active_sessions.pop(session_id, None)
            self.session_contexts.pop(session_id, None)

    async def _performance_monitor_loop(self) -> None:
        while True:
            await asyncio.sleep(300)
            logger.debug("Active sessions: %s", len(self.active_sessions))
