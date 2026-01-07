#!/usr/bin/env python3
"""
Context Management Service - Phase 6 Microservices Architecture
================================================================

Standalone FastAPI service for session lifecycle and context data management.

<!-- SSOT Domain: context_service -->

Navigation References:
├── Phase 6 Architecture → PHASE6_INFRASTRUCTURE_OPTIMIZATION_ROADMAP.md
├── Event Bus Integration → src/core/infrastructure/event_bus.py
├── Database Models → src/services/context_service/models.py
├── API Endpoints → src/services/context_service/api.py
├── Session Management → src/services/context_service/session_manager.py

Features:
- Session lifecycle management (create, update, end)
- Context data persistence and retrieval
- User preference storage and synchronization
- Event-driven context updates
- Health monitoring and metrics
- Database connection pooling

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6.2 - Microservices Decomposition
"""

import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any
import uvicorn
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, Field
import redis.asyncio as redis
import asyncpg
from datetime import datetime, timedelta

from src.core.infrastructure.event_bus import EventBus, get_event_bus
from src.services.context_service.session_manager import SessionManager
from src.services.context_service.models import ContextSession, UserPreferences
from src.core.config.config_manager import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
logger = logging.getLogger(__name__)

# Service configuration
SERVICE_NAME = "context-service"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = int(os.getenv("CONTEXT_SERVICE_PORT", "8001"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/context")
HEALTH_CHECK_INTERVAL = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))

# Global service instances
event_bus: Optional[EventBus] = None
session_manager: Optional[SessionManager] = None
db_pool: Optional[asyncpg.Pool] = None


# Pydantic models for API
class CreateSessionRequest(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    context_type: str = Field(..., description="Type of context session")
    initial_context: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Initial context data")
    user_preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User preference overrides")


class UpdateContextRequest(BaseModel):
    context_updates: Dict[str, Any] = Field(..., description="Context data to update")
    trigger_events: Optional[bool] = Field(True, description="Whether to trigger context events")


class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    context_type: str
    status: str
    created_at: str
    last_updated: str
    context_data: Dict[str, Any]


class HealthResponse(BaseModel):
    service: str
    version: str
    status: str
    uptime_seconds: float
    database_connected: bool
    redis_connected: bool
    event_bus_connected: bool
    active_sessions: int
    total_sessions_created: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup and shutdown."""
    # Startup
    await startup_event()
    yield
    # Shutdown
    await shutdown_event()


async def startup_event():
    """Initialize service dependencies on startup."""
    global event_bus, session_manager, db_pool

    logger.info("🚀 Starting Context Management Service...")

    try:
        # Initialize database connection pool
        db_pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=60
        )
        logger.info("✅ Database connection pool initialized")

        # Initialize Redis for caching
        redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        await redis_client.ping()
        logger.info("✅ Redis connection established")

        # Initialize event bus
        event_bus = await get_event_bus()
        logger.info("✅ Event bus connected")

        # Initialize session manager
        session_manager = SessionManager(db_pool, redis_client, event_bus)
        await session_manager.initialize()
        logger.info("✅ Session manager initialized")

        # Subscribe to relevant events
        await setup_event_subscriptions()

        logger.info("🎯 Context Management Service started successfully")

    except Exception as e:
        logger.error(f"❌ Failed to start Context Management Service: {e}")
        raise


async def shutdown_event():
    """Clean up service dependencies on shutdown."""
    global event_bus, session_manager, db_pool

    logger.info("🛑 Shutting down Context Management Service...")

    try:
        if session_manager:
            await session_manager.cleanup()
            logger.info("✅ Session manager cleaned up")

        if event_bus:
            await event_bus.shutdown()
            logger.info("✅ Event bus disconnected")

        if db_pool:
            await db_pool.close()
            logger.info("✅ Database connections closed")

        logger.info("🎯 Context Management Service shutdown complete")

    except Exception as e:
        logger.error(f"❌ Error during shutdown: {e}")


async def setup_event_subscriptions():
    """Set up event subscriptions for cross-service communication."""
    global event_bus

    if not event_bus:
        return

    # Subscribe to user activity events
    async def handle_user_activity(event_data):
        """Handle user activity events from other services."""
        try:
            event = event_data
            user_id = event.data.get('user_id')
            activity_type = event.data.get('activity_type', 'unknown')

            logger.info(f"📊 User activity: {user_id} - {activity_type}")

            # Update user context based on activity
            if session_manager and user_id:
                await session_manager.update_user_activity(user_id, activity_type, event.data)

        except Exception as e:
            logger.error(f"❌ Failed to handle user activity event: {e}")

    # Subscribe to context update events from AI service
    async def handle_ai_suggestions(event_data):
        """Handle AI suggestion events for context enrichment."""
        try:
            event = event_data
            session_id = event.data.get('session_id')
            suggestions = event.data.get('suggestions', [])

            logger.info(f"🤖 AI suggestions received for session {session_id}")

            # Update session with AI suggestions
            if session_manager and session_id:
                await session_manager.update_session_suggestions(session_id, suggestions)

        except Exception as e:
            logger.error(f"❌ Failed to handle AI suggestions: {e}")

    # Register event subscriptions
    await event_bus.subscribe_to_events(
        EventSubscription(
            subscription_id=f"{SERVICE_NAME}_user_activity",
            event_types=["user_activity", "user_login", "user_logout"],
            callback=handle_user_activity
        )
    )

    await event_bus.subscribe_to_events(
        EventSubscription(
            subscription_id=f"{SERVICE_NAME}_ai_suggestions",
            event_types=["ai_suggestions_generated", "context_enrichment"],
            callback=handle_ai_suggestions
        )
    )


# FastAPI application
app = FastAPI(
    title="Context Management Service",
    description="Microservice for session lifecycle and context data management",
    version=SERVICE_VERSION,
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check endpoint."""
    global session_manager, db_pool, event_bus

    try:
        # Check database connectivity
        db_connected = False
        if db_pool:
            async with db_pool.acquire() as conn:
                await conn.fetchval("SELECT 1")
                db_connected = True

        # Check Redis connectivity
        redis_connected = False
        if hasattr(session_manager, '_redis'):
            await session_manager._redis.ping()
            redis_connected = True

        # Check event bus connectivity
        event_bus_connected = event_bus is not None and event_bus._running

        # Get session statistics
        active_sessions = 0
        total_sessions = 0
        if session_manager:
            stats = await session_manager.get_statistics()
            active_sessions = stats.get('active_sessions', 0)
            total_sessions = stats.get('total_sessions_created', 0)

        return HealthResponse(
            service=SERVICE_NAME,
            version=SERVICE_VERSION,
            status="healthy" if all([db_connected, redis_connected, event_bus_connected]) else "degraded",
            uptime_seconds=(datetime.now() - getattr(app, '_start_time', datetime.now())).total_seconds(),
            database_connected=db_connected,
            redis_connected=redis_connected,
            event_bus_connected=event_bus_connected,
            active_sessions=active_sessions,
            total_sessions_created=total_sessions
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


# Session management endpoints
@app.post("/api/sessions", response_model=SessionResponse)
async def create_session(request: CreateSessionRequest, background_tasks: BackgroundTasks):
    """Create a new context session."""
    global session_manager, event_bus

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        # Create session
        session = await session_manager.create_session(
            user_id=request.user_id,
            context_type=request.context_type,
            initial_context=request.initial_context,
            user_preferences=request.user_preferences
        )

        # Publish session creation event
        if event_bus:
            event = event_bus.create_event(
                event_type="session_created",
                source_service=SERVICE_NAME,
                data={
                    "session_id": session.session_id,
                    "user_id": session.user_id,
                    "context_type": session.context_type
                },
                correlation_id=session.session_id
            )
            background_tasks.add_task(event_bus.publish_event, event)

        logger.info(f"📝 Created session {session.session_id} for user {request.user_id}")

        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            context_type=session.context_type,
            status=session.status,
            created_at=session.created_at.isoformat(),
            last_updated=session.last_updated.isoformat(),
            context_data=session.context_data
        )

    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail=f"Session creation failed: {str(e)}")


@app.get("/api/sessions/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Retrieve session information."""
    global session_manager

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        session = await session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        return SessionResponse(
            session_id=session.session_id,
            user_id=session.user_id,
            context_type=session.context_type,
            status=session.status,
            created_at=session.created_at.isoformat(),
            last_updated=session.last_updated.isoformat(),
            context_data=session.context_data
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Session retrieval failed: {str(e)}")


@app.put("/api/sessions/{session_id}/context")
async def update_session_context(session_id: str, request: UpdateContextRequest, background_tasks: BackgroundTasks):
    """Update session context data."""
    global session_manager, event_bus

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        # Update context
        result = await session_manager.update_context(session_id, request.context_updates)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Context update failed"))

        # Publish context update event
        if event_bus and request.trigger_events:
            event = event_bus.create_event(
                event_type="context_updated",
                source_service=SERVICE_NAME,
                data={
                    "session_id": session_id,
                    "updates": request.context_updates,
                    "new_suggestions": result.get("new_suggestions", [])
                },
                correlation_id=session_id
            )
            background_tasks.add_task(event_bus.publish_event, event)

        logger.info(f"📊 Updated context for session {session_id}")

        return {
            "success": True,
            "session_id": session_id,
            "updates_applied": len(request.context_updates),
            "new_suggestions": result.get("new_suggestions", [])
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update context for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Context update failed: {str(e)}")


@app.delete("/api/sessions/{session_id}")
async def end_session(session_id: str, background_tasks: BackgroundTasks):
    """End a context session."""
    global session_manager, event_bus

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        # End session
        result = await session_manager.end_session(session_id)

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result.get("error", "Session end failed"))

        # Publish session end event
        if event_bus:
            event = event_bus.create_event(
                event_type="session_ended",
                source_service=SERVICE_NAME,
                data={
                    "session_id": session_id,
                    "duration_seconds": result.get("duration_seconds", 0),
                    "total_updates": result.get("total_updates", 0)
                },
                correlation_id=session_id
            )
            background_tasks.add_task(event_bus.publish_event, event)

        logger.info(f"🏁 Ended session {session_id}")

        return {
            "success": True,
            "session_id": session_id,
            "message": "Session ended successfully",
            "statistics": result.get("statistics", {})
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to end session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Session end failed: {str(e)}")


@app.get("/api/sessions")
async def list_user_sessions(user_id: str, limit: int = 10, offset: int = 0):
    """List sessions for a specific user."""
    global session_manager

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        sessions = await session_manager.list_user_sessions(user_id, limit=limit, offset=offset)

        return {
            "user_id": user_id,
            "sessions": [
                {
                    "session_id": s.session_id,
                    "context_type": s.context_type,
                    "status": s.status,
                    "created_at": s.created_at.isoformat(),
                    "last_updated": s.last_updated.isoformat()
                }
                for s in sessions
            ],
            "total": len(sessions),
            "limit": limit,
            "offset": offset
        }

    except Exception as e:
        logger.error(f"Failed to list sessions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Session listing failed: {str(e)}")


@app.get("/api/statistics")
async def get_service_statistics():
    """Get service performance statistics."""
    global session_manager

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        stats = await session_manager.get_statistics()
        return {
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to get service statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")


# User preferences endpoints
@app.get("/api/users/{user_id}/preferences")
async def get_user_preferences(user_id: str):
    """Get user preferences."""
    global session_manager

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        preferences = await session_manager.get_user_preferences(user_id)
        return {
            "user_id": user_id,
            "preferences": preferences.dict() if preferences else {},
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to get preferences for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Preferences retrieval failed: {str(e)}")


@app.put("/api/users/{user_id}/preferences")
async def update_user_preferences(user_id: str, preferences: Dict[str, Any], background_tasks: BackgroundTasks):
    """Update user preferences."""
    global session_manager, event_bus

    if not session_manager:
        raise HTTPException(status_code=503, detail="Session manager not available")

    try:
        result = await session_manager.update_user_preferences(user_id, preferences)

        # Publish preferences update event
        if event_bus:
            event = event_bus.create_event(
                event_type="user_preferences_updated",
                source_service=SERVICE_NAME,
                data={
                    "user_id": user_id,
                    "updated_fields": list(preferences.keys())
                },
                correlation_id=f"user_{user_id}"
            )
            background_tasks.add_task(event_bus.publish_event, event)

        logger.info(f"⚙️ Updated preferences for user {user_id}")

        return {
            "success": True,
            "user_id": user_id,
            "updated_fields": list(preferences.keys()),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to update preferences for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Preferences update failed: {str(e)}")


if __name__ == "__main__":
    # Store startup time
    app._start_time = datetime.now()

    # Start server
    uvicorn.run(
        "src.services.context_service.main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=False,
        log_level="info"
    )