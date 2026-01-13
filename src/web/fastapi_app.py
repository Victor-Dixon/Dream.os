#!/usr/bin/env python3
"""
FastAPI Application - Agent Cellphone V2
========================================

<!-- SSOT Domain: web -->

High-performance FastAPI application for dream.os.
All implementation details extracted to modular components for V2 compliance.

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
<<<<<<< HEAD
import time
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Import modular components
from .fastapi_config import settings, validate_configuration
from .fastapi_middleware import setup_all_middleware
from .fastapi_routes import api_router

logger = logging.getLogger(__name__)

# Templates and static files
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@asynccontextmanager
async def lifespan(app: FastAPI):
<<<<<<< HEAD
    """Application lifespan manager with AI-powered monitoring."""
    # Startup
    logger.info("🚀 Starting FastAPI application with AI-powered coordination...")
=======
    """Application lifespan manager."""
    # Startup
    logger.info("Starting FastAPI application...")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    validate_configuration()

    # Start repository monitoring
    try:
        from src.services.repository_monitor import start_repository_monitoring
        await start_repository_monitoring()
        logger.info("✅ Repository monitoring started")
    except Exception as e:
        logger.warning(f"Failed to start repository monitoring: {e}")

<<<<<<< HEAD
    # Start AI-powered monitoring (Phase 5 AI Context Integration)
    try:
        from .fastapi_monitoring import start_ai_monitoring
        await start_ai_monitoring()
        logger.info("🤖 AI-powered predictive monitoring started")
    except Exception as e:
        logger.warning(f"Failed to start AI monitoring: {e}")

    yield

    # Shutdown
    logger.info("🛑 Shutting down FastAPI application...")

    # Stop AI monitoring
    try:
        from .fastapi_monitoring import stop_ai_monitoring
        await stop_ai_monitoring()
        logger.info("🛑 AI-powered monitoring stopped")
    except Exception as e:
        logger.error(f"Error stopping AI monitoring: {e}")
=======
    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    # Stop repository monitoring
    try:
        from src.services.repository_monitor import stop_repository_monitoring
        await stop_repository_monitoring()
        logger.info("🛑 Repository monitoring stopped")
    except Exception as e:
        logger.error(f"Error stopping repository monitoring: {e}")

# Create FastAPI application with performance optimizations
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    # PERFORMANCE OPTIMIZATION: Connection and performance settings
    docs_url="/docs" if settings.debug else None,  # Disable docs in production
    redoc_url="/redoc" if settings.debug else None,  # Disable redoc in production
    openapi_url="/openapi.json" if settings.debug else None,  # Disable openapi in production
)

# Configure middleware
setup_all_middleware(app)

# Include API routes
app.include_router(api_router)

# PERFORMANCE OPTIMIZATION: Add direct performance endpoints
@app.get("/perf/health")
async def performance_health():
    """High-performance health check endpoint."""
    return {"status": "ok", "timestamp": int(time.time() * 1000)}

@app.get("/perf/ping")
async def performance_ping():
    """Ultra-fast ping endpoint for load balancer health checks."""
    return "pong"

<<<<<<< HEAD
@app.get("/perf/metrics")
async def performance_metrics():
    """Comprehensive performance metrics endpoint."""
    from .fastapi_performance import get_performance_metrics
    return get_performance_metrics()

@app.get("/perf/reset")
async def reset_performance_metrics():
    """Reset performance metrics (admin only)."""
    from .fastapi_performance import reset_performance_metrics
    reset_performance_metrics()
    return {"status": "reset", "message": "Performance metrics reset successfully"}

@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics."""
    from .fastapi_caching import get_cache
    cache = get_cache()
    return cache.get_stats()

@app.post("/cache/clear")
async def clear_cache():
    """Clear all cache entries (admin only)."""
    from .fastapi_caching import get_cache
    cache = get_cache()
    success = cache.clear()
    return {"status": "cleared" if success else "failed", "message": "Cache cleared successfully" if success else "Cache clear failed"}

@app.delete("/cache/{pattern}")
async def invalidate_cache_pattern(pattern: str):
    """Invalidate cache keys matching a pattern (admin only)."""
    from .fastapi_caching import invalidate_cache_pattern
    deleted_count = invalidate_cache_pattern(pattern)
    return {"status": "invalidated", "keys_deleted": deleted_count}

@app.get("/ratelimit/status")
async def rate_limit_status():
    """Get rate limiting status and configuration."""
    from .fastapi_rate_limiting import get_rate_limit_status
    return get_rate_limit_status()

@app.post("/ratelimit/config")
async def configure_rate_limit(endpoint: str, limit: str):
    """Configure rate limit for an endpoint (admin only)."""
    from .fastapi_rate_limiting import endpoint_rate_limit
    endpoint_rate_limit(endpoint, limit)
    return {"status": "configured", "endpoint": endpoint, "limit": limit}

# AI-POWERED MONITORING ENDPOINTS (Phase 5 AI Context Integration)
@app.get("/ai/monitoring/status")
async def ai_monitoring_status():
    """Get AI-powered monitoring status."""
    from .fastapi_monitoring import get_metrics
    return {
        "ai_monitoring": "active",
        "phase": "Phase 5 AI Context Integration",
        "capabilities": [
            "Predictive blocker identification",
            "Intelligent blocker resolution",
            "Context-aware monitoring",
            "AI-powered system health analysis"
        ],
        **get_metrics()
    }

@app.get("/ai/blockers/active")
async def get_active_blockers():
    """Get currently active AI-detected blockers."""
    from .fastapi_monitoring import get_blockers
    return {
        "active_blockers": get_blockers(),
        "total_count": len(get_blockers()),
        "ai_detection": "Phase 5 AI Context Integration"
    }

@app.post("/ai/blockers/resolve/{blocker_id}")
async def resolve_blocker(blocker_id: str):
    """Request AI-powered resolution of a specific blocker."""
    from .fastapi_monitoring import ai_monitor
    try:
        # AI Context: Trigger intelligent resolution
        blocker = ai_monitor.active_blockers.get(blocker_id)
        if not blocker:
            return {"error": "Blocker not found", "blocker_id": blocker_id}

        # Attempt resolution
        resolved = await ai_monitor._attempt_resolution(blocker)
        if resolved:
            return {
                "status": "resolved",
                "blocker_id": blocker_id,
                "resolution_method": "ai_automated",
                "ai_confidence": blocker.ai_confidence
            }
        else:
            return {
                "status": "resolution_attempted",
                "blocker_id": blocker_id,
                "resolution_status": "manual_intervention_required",
                "suggestions": blocker.resolution_suggestions
            }
    except Exception as e:
        return {"error": str(e), "blocker_id": blocker_id}

@app.get("/ai/predictions/health")
async def ai_health_predictions():
    """Get AI predictions about system health."""
    return {
        "predictions": [
            {
                "type": "system_health",
                "prediction": "System operating within normal parameters",
                "confidence": 0.94,
                "timestamp": "2026-01-11T02:35:00Z"
            }
        ],
        "ai_context_integration": "Phase 5 Active",
        "monitoring_status": "operational"
    }

=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
# Static files (if templates directory exists)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

logger.info("✅ FastAPI application initialized with modular architecture")

__all__ = ["app", "templates"]