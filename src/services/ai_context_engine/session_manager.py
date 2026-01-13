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
<<<<<<< HEAD
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import asdict
import json

from .models import ContextSession, validate_session_data
=======
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import asdict

from .models import ContextSession
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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
<<<<<<< HEAD
        Initialize session manager with enhanced configuration.
=======
        Initialize session manager.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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

<<<<<<< HEAD
        # Statistics and monitoring
        self.stats = {
            'total_sessions_created': 0,
            'sessions_cleaned_up': 0,
            'active_sessions_peak': 0,
            'errors_encountered': 0,
            'last_cleanup_time': None,
            'performance_metrics': {}
        }

        logger.info(f"SessionManager initialized with timeout={session_timeout_hours}h, max_sessions={max_sessions}")

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
        Create a new context processing session with validation and error handling.
=======
        Create a new context processing session.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        Navigation:
        ├── Used by: AIContextEngine.create_session()
        ├── Creates: ContextSession instance
        └── Related: session limit enforcement, ID generation
        """
<<<<<<< HEAD
        try:
            # Validate inputs
            if not user_id or not isinstance(user_id, str):
                raise ValueError("user_id must be a non-empty string")

            if not context_type or not isinstance(context_type, str):
                raise ValueError("context_type must be a non-empty string")

            if not isinstance(initial_context, dict):
                logger.warning("initial_context is not a dict, converting to empty dict")
                initial_context = {}

            # Generate session ID
            session_id = f"{user_id}_{context_type}_{int(datetime.now().timestamp())}"

            # Create session with error handling
            session = ContextSession(
                session_id=session_id,
                user_id=user_id,
                context_type=context_type,
                start_time=datetime.now(),
                last_activity=datetime.now(),
                context_data=initial_context.copy()
            )

            # Validate session data
            validation_errors = validate_session_data(session)
            if validation_errors:
                logger.error(f"Session validation failed: {validation_errors}")
                raise ValueError(f"Invalid session data: {', '.join(validation_errors)}")

            # Enforce session limit with intelligent cleanup
            if len(self.active_sessions) >= self.max_sessions:
                cleaned = await self._cleanup_expired_sessions(force=True)
                if len(self.active_sessions) >= self.max_sessions:
                    # If still at limit, remove oldest session
                    oldest_session_id = min(
                        self.active_sessions.keys(),
                        key=lambda sid: self.active_sessions[sid].last_activity
                    )
                    await self.end_session(oldest_session_id)
                    logger.warning(f"Removed oldest session {oldest_session_id} due to session limit")

            # Store session
            self.active_sessions[session_id] = session
            self.stats['total_sessions_created'] += 1
            self.stats['active_sessions_peak'] = max(self.stats['active_sessions_peak'], len(self.active_sessions))

            logger.info(f"Created session {session_id} for user {user_id} (active: {len(self.active_sessions)})")
            return session_id

        except Exception as e:
            self.stats['errors_encountered'] += 1
            logger.error(f"Failed to create session for user {user_id}: {e}")
            raise
=======
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
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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

<<<<<<< HEAD
    async def end_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        End a session and return final statistics.

        Navigation:
        ├── Used by: AIContextEngine.end_session()
        ├── Removes: session from active_sessions
        └── Returns: session summary data
        """
        session = self.active_sessions.pop(session_id, None)
        if not session:
            return None

        # Calculate final statistics
        duration = datetime.now() - session.start_time
        summary = {
            'session_id': session_id,
            'user_id': session.user_id,
            'context_type': session.context_type,
            'duration_seconds': duration.total_seconds(),
            'suggestions_generated': len(session.ai_suggestions),
            'suggestions_applied': sum(1 for s in session.ai_suggestions if s.get('applied', False)),
            'final_status': session.status,
            'end_time': datetime.now().isoformat()
        }

        logger.info(f"Ended session {session_id} after {duration.total_seconds():.1f}s")
        return summary

    def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get context data for a session with enhanced error handling.
=======
    def get_session_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get context data for a session.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

        Navigation:
        ├── Used by: AIContextEngine.get_session_context()
        ├── Returns: formatted context data with risk metrics and suggestions
        └── Related: ContextSession data serialization
        """
<<<<<<< HEAD
        try:
            session = self.get_session(session_id)
            if not session:
                return None

            # Safely serialize risk metrics
            risk_metrics_data = None
            if session.risk_metrics:
                try:
                    risk_metrics_data = asdict(session.risk_metrics)
                except Exception as e:
                    logger.warning(f"Failed to serialize risk metrics for session {session_id}: {e}")

            return {
                'session_id': session.session_id,
                'user_id': session.user_id,
                'context_type': session.context_type,
                'context_data': session.context_data.copy(),  # Return copy to prevent external modification
                'risk_metrics': risk_metrics_data,
                'ai_suggestions': session.ai_suggestions.copy() if session.ai_suggestions else [],
                'performance_metrics': session.performance_metrics.copy() if session.performance_metrics else {},
                'last_activity': session.last_activity.isoformat(),
                'status': session.status
            }

        except Exception as e:
            logger.error(f"Error getting session context for {session_id}: {e}")
            return None

    def list_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List all active sessions for a user.

        Args:
            user_id: User identifier

        Returns:
            List of session summaries
        """
        user_sessions = [
            {
                'session_id': session.session_id,
                'context_type': session.context_type,
                'last_activity': session.last_activity.isoformat(),
                'status': session.status,
                'suggestion_count': len(session.ai_suggestions)
            }
            for session in self.active_sessions.values()
            if session.user_id == user_id
        ]
        return user_sessions

    def get_system_stats(self) -> Dict[str, Any]:
        """
        Get system-wide session statistics.

        Returns:
            Dictionary with session system statistics
        """
        current_time = datetime.now()
        active_count = len(self.active_sessions)

        # Calculate average session age
        if active_count > 0:
            total_age = sum((current_time - session.last_activity).total_seconds()
                          for session in self.active_sessions.values())
            avg_age_seconds = total_age / active_count
        else:
            avg_age_seconds = 0

        return {
            **self.stats,
            'active_sessions': active_count,
            'average_session_age_seconds': avg_age_seconds,
            'uptime_seconds': (current_time - datetime.fromtimestamp(asyncio.get_event_loop().time())).total_seconds() if hasattr(asyncio, 'get_event_loop') else 0,
            'timestamp': current_time.isoformat()
        }
=======
        session = self.get_session(session_id)
        if not session:
            return None

        return {
            'session_id': session.session_id,
            'context_data': session.context_data,
            'risk_metrics': asdict(session.risk_metrics) if session.risk_metrics else None,
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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

<<<<<<< HEAD
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Get detailed performance statistics.

        Returns:
            Dictionary with performance metrics
        """
        current_time = datetime.now()
        active_count = len(self.active_sessions)

        # Calculate session type distribution
        type_distribution = {}
        for session in self.active_sessions.values():
            session_type = session.context_type
            type_distribution[session_type] = type_distribution.get(session_type, 0) + 1

        # Calculate suggestion statistics
        total_suggestions = sum(len(session.ai_suggestions) for session in self.active_sessions.values())
        applied_suggestions = sum(
            sum(1 for s in session.ai_suggestions if s.get('applied', False))
            for session in self.active_sessions.values()
        )

        return {
            'active_sessions': active_count,
            'session_types': type_distribution,
            'total_suggestions': total_suggestions,
            'applied_suggestions': applied_suggestions,
            'suggestion_application_rate': applied_suggestions / max(total_suggestions, 1),
            'system_stats': self.stats.copy(),
            'timestamp': current_time.isoformat()
        }

    async def force_cleanup(self) -> int:
        """
        Force cleanup of all expired sessions.

        Returns:
            Number of sessions cleaned up
        """
        initial_count = len(self.active_sessions)
        await self._cleanup_expired_sessions(force=True)
        final_count = len(self.active_sessions)
        cleaned_count = initial_count - final_count

        self.stats['sessions_cleaned_up'] += cleaned_count
        logger.info(f"🧹 Force cleaned up {cleaned_count} sessions")
        return cleaned_count

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
                logger.info(f"📊 Session Manager Performance: active={stats['active_sessions']}, suggestions={stats['total_suggestions']}")
=======
                logger.info(f"📊 Session Manager Performance: {stats}")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

                await asyncio.sleep(3600)  # Log every hour
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(300)