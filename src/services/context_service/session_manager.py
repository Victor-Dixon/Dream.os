#!/usr/bin/env python3
"""
Session Manager - Phase 6 Context Management Service
====================================================

Core business logic for session lifecycle management and context operations.

<!-- SSOT Domain: context_service_session_manager -->

Navigation References:
├── Service Main → src/services/context_service/main.py
├── Data Models → src/services/context_service/models.py
├── Event Bus → src/core/infrastructure/event_bus.py

Features:
- Session CRUD operations with persistence
- Context data management and validation
- User preference handling
- Session statistics and monitoring
- Automatic cleanup and expiration
- Redis caching for performance
- Event-driven updates

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6.2 - Microservices Decomposition
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
import asyncpg
import redis.asyncio as redis

from .models import (
    ContextSession, UserPreferences, ContextEvent, SessionStatistics,
    SessionStatus, ContextType, validate_session_data,
    CONTEXT_SESSIONS_SCHEMA, USER_PREFERENCES_SCHEMA,
    CONTEXT_EVENTS_SCHEMA, SESSION_STATISTICS_SCHEMA,
    PERFORMANCE_INDEXES_SQL, CREATE_ALL_TABLES_SQL
)
from src.core.infrastructure.event_bus import EventBus

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages context sessions with database persistence and Redis caching.

    Handles session lifecycle, context updates, user preferences, and statistics.
    Provides high-performance operations with caching and event-driven updates.
    """

    def __init__(self,
                 db_pool: asyncpg.Pool,
                 redis_client: redis.Redis,
                 event_bus: EventBus):
        self.db_pool = db_pool
        self.redis = redis_client
        self.event_bus = event_bus

        # Configuration
        self.session_ttl = 3600 * 24  # 24 hours
        self.cache_ttl = 3600  # 1 hour
        self.cleanup_interval = 300  # 5 minutes
        self.max_sessions_per_user = 50

        # Statistics
        self.stats = {
            'total_sessions_created': 0,
            'active_sessions': 0,
            'total_updates': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': 0
        }

        # Background tasks
        self._cleanup_task: Optional[asyncio.Task] = None
        self._initialized = False

    async def initialize(self):
        """Initialize the session manager and start background tasks."""
        if self._initialized:
            return

        try:
            # Ensure database tables exist
            await self._ensure_tables()

            # Start background cleanup task
            self._cleanup_task = asyncio.create_task(self._background_cleanup())
            logger.info("Session manager background cleanup started")

            self._initialized = True
            logger.info("✅ Session Manager initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Session Manager: {e}")
            raise

    async def cleanup(self):
        """Clean up resources and stop background tasks."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

        # Clear caches
        await self._clear_all_caches()

        logger.info("Session Manager cleanup completed")

    async def _ensure_tables(self):
        """Ensure all required database tables exist."""
        async with self.db_pool.acquire() as conn:
            # Create tables if they don't exist
            for table_sql in [
                CONTEXT_SESSIONS_SCHEMA,
                USER_PREFERENCES_SCHEMA,
                CONTEXT_EVENTS_SCHEMA,
                SESSION_STATISTICS_SCHEMA
            ]:
                await conn.execute(table_sql)

            # Create performance indexes
            await conn.execute(PERFORMANCE_INDEXES_SQL)

            logger.info("Database tables verified/created")

    async def create_session(self,
                           user_id: str,
                           context_type: ContextType,
                           initial_context: Optional[Dict[str, Any]] = None,
                           user_preferences: Optional[Dict[str, Any]] = None) -> ContextSession:
        """
        Create a new context session.

        Args:
            user_id: User identifier
            context_type: Type of context session
            initial_context: Initial context data
            user_preferences: User preferences for this session

        Returns:
            Created ContextSession object
        """
        session_id = f"{user_id}_{context_type.value}_{int(datetime.now().timestamp())}"

        # Check user session limit
        user_sessions = await self._count_user_sessions(user_id)
        if user_sessions >= self.max_sessions_per_user:
            await self._cleanup_old_user_sessions(user_id)

        # Get user preferences if not provided
        if user_preferences is None:
            user_prefs = await self.get_user_preferences(user_id)
            user_preferences = user_prefs.dict() if user_prefs else {}

        # Create session object
        session = ContextSession(
            session_id=session_id,
            user_id=user_id,
            context_type=context_type,
            context_data=initial_context or {},
            user_preferences=user_preferences
        )

        # Persist to database
        await self._save_session(session)

        # Cache session
        await self._cache_session(session)

        # Update statistics
        self.stats['total_sessions_created'] += 1
        self.stats['active_sessions'] += 1

        # Publish session creation event
        await self._publish_session_event("session_created", session)

        logger.info(f"📝 Created session {session_id} for user {user_id}")
        return session

    async def get_session(self, session_id: str) -> Optional[ContextSession]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session identifier

        Returns:
            ContextSession object or None if not found
        """
        # Try cache first
        cached_session = await self._get_cached_session(session_id)
        if cached_session:
            self.stats['cache_hits'] += 1
            return cached_session

        self.stats['cache_misses'] += 1

        # Load from database
        session_data = await self._load_session(session_id)
        if session_data:
            session = ContextSession.from_dict(session_data)
            # Cache for future use
            await self._cache_session(session)
            return session

        return None

    async def update_context(self,
                           session_id: str,
                           context_updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update session context data.

        Args:
            session_id: Session identifier
            context_updates: Context data to update

        Returns:
            Update result with success status and suggestions
        """
        try:
            # Get current session
            session = await self.get_session(session_id)
            if not session:
                return {"success": False, "error": "Session not found"}

            if session.status != SessionStatus.ACTIVE:
                return {"success": False, "error": f"Session is {session.status.value}"}

            # Update context data
            session.context_data.update(context_updates)
            session.update_timestamp()

            # Persist changes
            await self._update_session(session)

            # Update cache
            await self._cache_session(session)

            # Update statistics
            self.stats['total_updates'] += 1

            # Generate suggestions based on context changes
            suggestions = await self._generate_context_suggestions(session, context_updates)

            # Publish context update event
            await self._publish_context_event("context_updated", session, context_updates, suggestions)

            logger.info(f"📊 Updated context for session {session_id}")

            return {
                "success": True,
                "session_id": session_id,
                "updates_applied": len(context_updates),
                "new_suggestions": suggestions
            }

        except Exception as e:
            logger.error(f"Failed to update context for session {session_id}: {e}")
            self.stats['errors'] += 1
            return {"success": False, "error": str(e)}

    async def end_session(self, session_id: str) -> Dict[str, Any]:
        """
        End a context session.

        Args:
            session_id: Session identifier

        Returns:
            Session end result with statistics
        """
        try:
            # Get session
            session = await self.get_session(session_id)
            if not session:
                return {"success": False, "error": "Session not found"}

            # Calculate session statistics
            duration = (datetime.now() - session.created_at).total_seconds()
            statistics = SessionStatistics(
                session_id=session_id,
                total_updates=session.update_count,
                total_events=session.event_count,
                ai_interactions=session.ai_interactions,
                duration_seconds=duration
            )

            # Update session status
            session.status = SessionStatus.COMPLETED
            session.update_timestamp()

            # Persist final state
            await self._update_session(session)
            await self._save_session_statistics(statistics)

            # Clear cache
            await self._clear_session_cache(session_id)

            # Update statistics
            self.stats['active_sessions'] -= 1

            # Publish session end event
            await self._publish_session_end_event(session, statistics)

            logger.info(f"🏁 Ended session {session_id}")

            return {
                "success": True,
                "session_id": session_id,
                "duration_seconds": duration,
                "statistics": statistics.to_dict()
            }

        except Exception as e:
            logger.error(f"Failed to end session {session_id}: {e}")
            self.stats['errors'] += 1
            return {"success": False, "error": str(e)}

    async def list_user_sessions(self,
                               user_id: str,
                               limit: int = 10,
                               offset: int = 0) -> List[ContextSession]:
        """
        List sessions for a specific user.

        Args:
            user_id: User identifier
            limit: Maximum number of sessions to return
            offset: Pagination offset

        Returns:
            List of ContextSession objects
        """
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM context_sessions
                WHERE user_id = $1
                ORDER BY last_updated DESC
                LIMIT $2 OFFSET $3
            """, user_id, limit, offset)

            sessions = []
            for row in rows:
                session_data = dict(row)
                session = ContextSession.from_dict(session_data)
                sessions.append(session)

            return sessions

    async def get_user_preferences(self, user_id: str) -> Optional[UserPreferences]:
        """
        Get user preferences.

        Args:
            user_id: User identifier

        Returns:
            UserPreferences object or None
        """
        # Try cache first
        cache_key = f"user_prefs:{user_id}"
        cached_prefs = await self.redis.get(cache_key)
        if cached_prefs:
            return UserPreferences.from_dict(json.loads(cached_prefs))

        # Load from database
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM user_preferences WHERE user_id = $1
            """, user_id)

            if row:
                prefs_data = dict(row)
                prefs = UserPreferences.from_dict(prefs_data)

                # Cache preferences
                await self.redis.set(cache_key, json.dumps(prefs.to_dict()), ex=self.cache_ttl)

                return prefs

        return None

    async def update_user_preferences(self,
                                    user_id: str,
                                    preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user preferences.

        Args:
            user_id: User identifier
            preferences: Preferences to update

        Returns:
            Update result
        """
        try:
            # Get current preferences
            current_prefs = await self.get_user_preferences(user_id)

            if current_prefs:
                # Update existing preferences
                for key, value in preferences.items():
                    if hasattr(current_prefs, key):
                        setattr(current_prefs, key, value)
                current_prefs.update_timestamp()
                prefs = current_prefs
            else:
                # Create new preferences
                prefs = UserPreferences(user_id=user_id, **preferences)

            # Persist to database
            await self._save_user_preferences(prefs)

            # Update cache
            cache_key = f"user_prefs:{user_id}"
            await self.redis.set(cache_key, json.dumps(prefs.to_dict()), ex=self.cache_ttl)

            logger.info(f"⚙️ Updated preferences for user {user_id}")

            return {
                "success": True,
                "user_id": user_id,
                "updated_fields": list(preferences.keys())
            }

        except Exception as e:
            logger.error(f"Failed to update preferences for user {user_id}: {e}")
            return {"success": False, "error": str(e)}

    async def update_session_suggestions(self,
                                       session_id: str,
                                       suggestions: List[Dict[str, Any]]) -> bool:
        """
        Update AI suggestions for a session.

        Args:
            session_id: Session identifier
            suggestions: List of suggestion objects

        Returns:
            Success status
        """
        try:
            session = await self.get_session(session_id)
            if not session:
                return False

            # Update session with suggestions
            session.ai_interactions += 1
            session.update_timestamp()

            # Persist updates
            await self._update_session(session)

            # Update cache
            await self._cache_session(session)

            return True

        except Exception as e:
            logger.error(f"Failed to update suggestions for session {session_id}: {e}")
            return False

    async def update_user_activity(self,
                                 user_id: str,
                                 activity_type: str,
                                 activity_data: Dict[str, Any]):
        """
        Update user activity information.

        Args:
            user_id: User identifier
            activity_type: Type of activity
            activity_data: Activity details
        """
        try:
            # Store activity in user preferences or session metadata
            # This can be used for personalization and context awareness
            cache_key = f"user_activity:{user_id}"
            activity_record = {
                "activity_type": activity_type,
                "timestamp": datetime.now().isoformat(),
                "data": activity_data
            }

            # Store recent activities (keep last 10)
            existing_activities = await self.redis.lrange(cache_key, 0, 9)
            activities = [activity_record] + [json.loads(a) for a in existing_activities[:9]]

            # Clear and repopulate list
            await self.redis.delete(cache_key)
            for activity in activities:
                await self.redis.lpush(cache_key, json.dumps(activity))

            # Set expiration
            await self.redis.expire(cache_key, 3600 * 24)  # 24 hours

        except Exception as e:
            logger.error(f"Failed to update activity for user {user_id}: {e}")

    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get session manager statistics.

        Returns:
            Statistics dictionary
        """
        # Get database statistics
        async with self.db_pool.acquire() as conn:
            db_stats = await conn.fetchrow("""
                SELECT
                    COUNT(*) as total_sessions,
                    COUNT(*) FILTER (WHERE status = 'active') as active_sessions,
                    COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '24 hours') as sessions_24h,
                    AVG(EXTRACT(EPOCH FROM (last_updated - created_at))) as avg_session_duration
                FROM context_sessions
            """)

        stats_dict = self.stats.copy()
        if db_stats:
            stats_dict.update(dict(db_stats))
        stats_dict["timestamp"] = datetime.now().isoformat()
        return stats_dict

    # Private helper methods

    async def _save_session(self, session: ContextSession):
        """Save session to database."""
        session_data = session.to_dict()
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO context_sessions (
                    session_id, user_id, context_type, status, context_data,
                    user_preferences, metadata, created_at, last_updated,
                    expires_at, update_count, event_count, ai_interactions
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13
                )
                ON CONFLICT (session_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    context_data = EXCLUDED.context_data,
                    user_preferences = EXCLUDED.user_preferences,
                    metadata = EXCLUDED.metadata,
                    last_updated = EXCLUDED.last_updated,
                    expires_at = EXCLUDED.expires_at,
                    update_count = EXCLUDED.update_count,
                    event_count = EXCLUDED.event_count,
                    ai_interactions = EXCLUDED.ai_interactions
            """,
            session.session_id, session.user_id, session.context_type.value,
            session.status.value, json.dumps(session.context_data),
            json.dumps(session.user_preferences), json.dumps(session.metadata),
            session.created_at, session.last_updated, session.expires_at,
            session.update_count, session.event_count, session.ai_interactions
            )

    async def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from database."""
        async with self.db_pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT * FROM context_sessions WHERE session_id = $1
            """, session_id)

            return dict(row) if row else None

    async def _update_session(self, session: ContextSession):
        """Update session in database."""
        session_data = session.to_dict()
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE context_sessions SET
                    status = $2, context_data = $3, user_preferences = $4,
                    metadata = $5, last_updated = $6, expires_at = $7,
                    update_count = $8, event_count = $9, ai_interactions = $10
                WHERE session_id = $1
            """,
            session.session_id, session.status.value, json.dumps(session.context_data),
            json.dumps(session.user_preferences), json.dumps(session.metadata),
            session.last_updated, session.expires_at, session.update_count,
            session.event_count, session.ai_interactions
            )

    async def _save_user_preferences(self, preferences: UserPreferences):
        """Save user preferences to database."""
        prefs_data = preferences.to_dict()
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO user_preferences (
                    user_id, theme, language, timezone, notifications,
                    ai_settings, privacy_settings, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (user_id) DO UPDATE SET
                    theme = EXCLUDED.theme,
                    language = EXCLUDED.language,
                    timezone = EXCLUDED.timezone,
                    notifications = EXCLUDED.notifications,
                    ai_settings = EXCLUDED.ai_settings,
                    privacy_settings = EXCLUDED.privacy_settings,
                    updated_at = EXCLUDED.updated_at
            """,
            preferences.user_id, preferences.theme, preferences.language,
            preferences.timezone, json.dumps(preferences.notifications),
            json.dumps(preferences.ai_settings), json.dumps(preferences.privacy_settings),
            preferences.created_at, preferences.updated_at
            )

    async def _save_session_statistics(self, stats: SessionStatistics):
        """Save session statistics to database."""
        stats_data = stats.to_dict()
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO session_statistics (
                    session_id, total_updates, total_events, ai_interactions,
                    duration_seconds, average_response_time, peak_memory_usage,
                    error_count, last_activity
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                ON CONFLICT (session_id) DO UPDATE SET
                    total_updates = EXCLUDED.total_updates,
                    total_events = EXCLUDED.total_events,
                    ai_interactions = EXCLUDED.ai_interactions,
                    duration_seconds = EXCLUDED.duration_seconds,
                    average_response_time = EXCLUDED.average_response_time,
                    peak_memory_usage = EXCLUDED.peak_memory_usage,
                    error_count = EXCLUDED.error_count,
                    last_activity = EXCLUDED.last_activity
            """,
            stats.session_id, stats.total_updates, stats.total_events,
            stats.ai_interactions, stats.duration_seconds, stats.average_response_time,
            stats.peak_memory_usage, stats.error_count, stats.last_activity
            )

    async def _cache_session(self, session: ContextSession):
        """Cache session in Redis."""
        cache_key = f"session:{session.session_id}"
        session_data = json.dumps(session.to_dict())
        await self.redis.set(cache_key, session_data, ex=self.cache_ttl)

    async def _get_cached_session(self, session_id: str) -> Optional[ContextSession]:
        """Get session from Redis cache."""
        cache_key = f"session:{session_id}"
        cached_data = await self.redis.get(cache_key)
        if cached_data:
            session_data = json.loads(cached_data)
            return ContextSession.from_dict(session_data)
        return None

    async def _clear_session_cache(self, session_id: str):
        """Clear session from Redis cache."""
        cache_key = f"session:{session_id}"
        await self.redis.delete(cache_key)

    async def _clear_all_caches(self):
        """Clear all Redis caches."""
        try:
            await self.redis.flushdb()
        except Exception as e:
            logger.error(f"Failed to clear caches: {e}")

    async def _count_user_sessions(self, user_id: str) -> int:
        """Count active sessions for a user."""
        async with self.db_pool.acquire() as conn:
            result = await conn.fetchval("""
                SELECT COUNT(*) FROM context_sessions
                WHERE user_id = $1 AND status = 'active'
            """, user_id)
            return result or 0

    async def _cleanup_old_user_sessions(self, user_id: str):
        """Clean up old sessions for a user to stay within limits."""
        async with self.db_pool.acquire() as conn:
            # Mark oldest sessions as expired
            await conn.execute("""
                UPDATE context_sessions
                SET status = 'expired', last_updated = NOW()
                WHERE user_id = $1 AND status = 'active'
                ORDER BY last_updated ASC
                LIMIT (
                    SELECT GREATEST(0, COUNT(*) - $2 + 1)
                    FROM context_sessions
                    WHERE user_id = $1 AND status = 'active'
                )
            """, user_id, self.max_sessions_per_user)

    async def _background_cleanup(self):
        """Background task for cleaning up expired sessions."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)

                # Clean up expired sessions
                async with self.db_pool.acquire() as conn:
                    expired_count = await conn.fetchval("""
                        UPDATE context_sessions
                        SET status = 'expired', last_updated = NOW()
                        WHERE status = 'active' AND expires_at < NOW()
                        RETURNING COUNT(*)
                    """)

                    if expired_count and expired_count > 0:
                        logger.info(f"Cleaned up {expired_count} expired sessions")

                # Clean up old cache entries
                # Note: Redis TTL handles most cache cleanup automatically

            except Exception as e:
                logger.error(f"Background cleanup failed: {e}")
                await asyncio.sleep(60)  # Wait before retrying

    async def _generate_context_suggestions(self,
                                          session: ContextSession,
                                          updates: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI suggestions based on context changes."""
        # This is a simplified implementation
        # In a full implementation, this would call an AI service
        suggestions = []

        # Generate basic suggestions based on context patterns
        if 'portfolio_value' in updates:
            suggestions.append({
                "suggestion_id": f"sugg_{uuid.uuid4().hex[:8]}",
                "suggestion_type": "risk_analysis",
                "confidence_score": 0.85,
                "content": {
                    "action": "analyze_portfolio_risk",
                    "message": "Portfolio value changed significantly. Consider risk analysis."
                },
                "reasoning": "Portfolio value updates often indicate need for risk assessment"
            })

        if 'market_data' in updates:
            suggestions.append({
                "suggestion_id": f"sugg_{uuid.uuid4().hex[:8]}",
                "suggestion_type": "market_insight",
                "confidence_score": 0.75,
                "content": {
                    "action": "review_market_conditions",
                    "message": "Market data updated. Review current conditions."
                },
                "reasoning": "Market data changes may require strategy adjustments"
            })

        return suggestions

    async def _publish_session_event(self, event_type: str, session: ContextSession):
        """Publish session lifecycle event."""
        if self.event_bus:
            event = self.event_bus.create_event(
                event_type=event_type,
                source_service="context_service",
                data={
                    "session_id": session.session_id,
                    "user_id": session.user_id,
                    "context_type": session.context_type.value,
                    "status": session.status.value
                },
                correlation_id=session.session_id
            )
            await self.event_bus.publish_event(event)

    async def _publish_context_event(self,
                                   event_type: str,
                                   session: ContextSession,
                                   updates: Dict[str, Any],
                                   suggestions: List[Dict[str, Any]]):
        """Publish context update event."""
        if self.event_bus:
            event = self.event_bus.create_event(
                event_type=event_type,
                source_service="context_service",
                data={
                    "session_id": session.session_id,
                    "user_id": session.user_id,
                    "updates": updates,
                    "new_suggestions": suggestions
                },
                correlation_id=session.session_id
            )
            await self.event_bus.publish_event(event)

    async def _publish_session_end_event(self,
                                       session: ContextSession,
                                       statistics: SessionStatistics):
        """Publish session end event with statistics."""
        if self.event_bus:
            duration = (datetime.now() - session.created_at).total_seconds()
            event = self.event_bus.create_event(
                event_type="session_ended",
                source_service="context_service",
                data={
                    "session_id": session.session_id,
                    "user_id": session.user_id,
                    "duration_seconds": duration,
                    "total_updates": statistics.total_updates,
                    "statistics": statistics.to_dict()
                },
                correlation_id=session.session_id
            )
            await self.event_bus.publish_event(event)