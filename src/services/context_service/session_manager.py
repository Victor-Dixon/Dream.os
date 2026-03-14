#!/usr/bin/env python3
"""
Session Manager - Phase 6 Context Management Service
====================================================

In-memory session management for context service operations.

<!-- SSOT Domain: context_service_session_manager -->
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import uuid4

from .models import ContextSession, ContextType, SessionStatus

logger = logging.getLogger(__name__)


class SessionManager:
    """Manage context sessions in memory with simple cleanup."""

    def __init__(self, session_ttl_hours: int = 24, cleanup_interval: int = 300):
        self.session_ttl = timedelta(hours=session_ttl_hours)
        self.cleanup_interval = cleanup_interval
        self.sessions: Dict[str, ContextSession] = {}
        self._cleanup_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """Initialize background cleanup task."""
        if not self._cleanup_task:
            self._cleanup_task = asyncio.create_task(self._background_cleanup())

    async def cleanup(self) -> None:
        """Stop background cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            self._cleanup_task = None

    async def create_session(
        self,
        user_id: str,
        context_type: ContextType,
        context_data: Optional[Dict[str, Any]] = None,
    ) -> ContextSession:
        """Create a new session and return it."""
        session_id = str(uuid4())
        session = ContextSession(
            session_id=session_id,
            user_id=user_id,
            context_type=context_type,
            status=SessionStatus.ACTIVE,
            context_data=context_data or {},
        )
        self.sessions[session_id] = session
        return session

    async def get_session(self, session_id: str) -> Optional[ContextSession]:
        """Fetch a session by ID."""
        return self.sessions.get(session_id)

    async def update_session_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any],
    ) -> Optional[ContextSession]:
        """Update context data for a session."""
        session = self.sessions.get(session_id)
        if not session:
            return None
        session.context_data.update(context_updates)
        session.last_updated = datetime.now()
        session.update_count += 1
        return session

    async def close_session(self, session_id: str) -> bool:
        """Mark a session as completed and remove it from memory."""
        session = self.sessions.get(session_id)
        if not session:
            return False
        session.status = SessionStatus.COMPLETED
        self.sessions.pop(session_id, None)
        return True

    async def _background_cleanup(self) -> None:
        while True:
            await asyncio.sleep(self.cleanup_interval)
            self._cleanup_expired_sessions()

    def _cleanup_expired_sessions(self) -> None:
        now = datetime.now()
        expired = [
            session_id
            for session_id, session in self.sessions.items()
            if now - session.last_updated > self.session_ttl
        ]
        for session_id in expired:
            self.sessions.pop(session_id, None)
            logger.info("Expired session cleaned up: %s", session_id)
