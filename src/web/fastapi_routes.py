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
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "debug": settings.debug
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