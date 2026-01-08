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

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Configure middleware
setup_all_middleware(app)

# Include API routes
app.include_router(api_router)

# Static files (if templates directory exists)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

logger.info("✅ FastAPI application initialized with modular architecture")

__all__ = ["app", "templates"]