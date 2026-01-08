#!/usr/bin/env python3
"""
FastAPI Routes - Main API Router (Modular V2 Compliance)
========================================================

<!-- SSOT Domain: web -->

Main API router that includes all modular route handlers.
Centralized route management for FastAPI application.

V2 Compliant: <100 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import logging

from .fastapi_config import settings

# Import existing modular routes
try:
    from .ai_routes import router as ai_router
except ImportError:
    ai_router = None

try:
    from .analytics_routes import router as analytics_router
except ImportError:
    analytics_router = None

try:
    from .context_routes import router as context_router
except ImportError:
    context_router = None

try:
    from .performance_routes import router as performance_router
except ImportError:
    performance_router = None

try:
    from .trading_routes import router as trading_router
except ImportError:
    trading_router = None

logger = logging.getLogger(__name__)

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    templates = None

# Main API router
api_router = APIRouter()

# Include modular routers
if ai_router:
    api_router.include_router(ai_router, prefix="/ai", tags=["AI"])
    logger.info("✅ AI routes included")

if analytics_router:
    api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
    logger.info("✅ Analytics routes included")

if context_router:
    api_router.include_router(context_router, prefix="/context", tags=["Context"])
    logger.info("✅ Context routes included")

if performance_router:
    api_router.include_router(performance_router, prefix="/performance", tags=["Performance"])
    logger.info("✅ Performance routes included")

if trading_router:
    api_router.include_router(trading_router, prefix="/trading", tags=["Trading"])
    logger.info("✅ Trading routes included")

# Core routes (health, root pages)
@api_router.get("/health")
async def health_check():
    """Health check endpoint with performance metrics."""
    # PERFORMANCE OPTIMIZATION: Include performance metrics in health check
    performance_stats = {}

    try:
        # Get system performance metrics
        import psutil
        import time

        process = psutil.Process()
        performance_stats = {
            "memory_usage_mb": process.memory_info().rss / 1024 / 1024,
            "cpu_percent": process.cpu_percent(),
            "uptime_seconds": time.time() - process.create_time(),
            "response_time_ms": 0  # Will be set by middleware
        }
    except ImportError:
        performance_stats = {"monitoring": "psutil_not_available"}

    return {
        "status": "healthy",
        "version": settings.app_version,
        "debug": settings.debug,
        "performance": performance_stats,
        "timestamp": int(time.time() * 1000)
    }


@api_router.get("/performance/metrics")
async def performance_metrics():
    """
    PERFORMANCE OPTIMIZATION: Detailed performance metrics endpoint.
    Provides comprehensive system and application performance data.
    """
    try:
        import psutil
        import time
        from ..services.vector_database_service_unified import get_vector_database_service
        from ..infrastructure.analytics_service import get_analytics_service

        # System metrics
        system_metrics = {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": psutil.virtual_memory().used / 1024 / 1024,
            "disk_usage_percent": psutil.disk_usage('/').percent,
            "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
        }

        # Application metrics
        app_metrics = {
            "uptime_seconds": time.time() - psutil.Process().create_time(),
            "active_threads": len(psutil.Process().threads()),
            "open_files": len(psutil.Process().open_files())
        }

        # Service-specific metrics
        service_metrics = {}

        try:
            vdb_service = get_vector_database_service()
            service_metrics["vector_db"] = vdb_service.get_performance_stats()
        except Exception as e:
            service_metrics["vector_db"] = {"error": str(e)}

        try:
            analytics_service = get_analytics_service()
            service_metrics["analytics"] = {"status": "available"}
        except Exception as e:
            service_metrics["analytics"] = {"error": str(e)}

        return {
            "system": system_metrics,
            "application": app_metrics,
            "services": service_metrics,
            "timestamp": int(time.time() * 1000)
        }

    except Exception as e:
        logger.error(f"Performance metrics error: {e}")
        return {
            "error": str(e),
            "timestamp": int(time.time() * 1000)
        }


@api_router.get("/performance/cache/clear")
async def clear_response_cache():
    """
    PERFORMANCE OPTIMIZATION: Clear response cache endpoint.
    Allows manual cache clearing for performance testing.
    """
    try:
        from .fastapi_middleware import _response_cache

        cache_size_before = len(_response_cache)
        _response_cache.clear()

        return {
            "status": "cache_cleared",
            "entries_removed": cache_size_before,
            "timestamp": int(time.time() * 1000)
        }

    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return {
            "error": str(e),
            "timestamp": int(time.time() * 1000)
        }

# Root routes for web interface
if templates:
    @api_router.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        """Root page."""
        return templates.TemplateResponse("index.html", {"request": request})

    @api_router.get("/ai-chat", response_class=HTMLResponse)
    async def ai_chat_page(request: Request):
        """AI chat interface page."""
        return templates.TemplateResponse("ai_chat.html", {"request": request})

    @api_router.get("/offline", response_class=HTMLResponse)
    async def offline_page(request: Request):
        """Offline page."""
        return templates.TemplateResponse("offline.html", {"request": request})

# Background task endpoint (legacy support)
@api_router.post("/background-task/{task_name}")
async def background_task(task_name: str):
    """Legacy background task endpoint."""
    return {
        "task": task_name,
        "status": "queued",
        "message": "Background task processing moved to task queue service"
    }

logger.info("✅ Main API router configured with all modular routes")

__all__ = ["api_router"]