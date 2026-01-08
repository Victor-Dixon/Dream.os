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
    """Application lifespan manager."""
    # Startup
    logger.info("Starting FastAPI application...")
    validate_configuration()

    yield

    # Shutdown
    logger.info("Shutting down FastAPI application...")

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

# Static files (if templates directory exists)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

logger.info("✅ FastAPI application initialized with modular architecture")

__all__ = ["app", "templates"]