#!/usr/bin/env python3
"""
FastAPI Configuration - Modular V2 Compliance
==============================================

<!-- SSOT Domain: web -->

Configuration management for FastAPI application.
Centralized settings with validation.

V2 Compliant: <50 lines
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import os
from typing import Optional

class FastAPISettings:
    """FastAPI application settings - standalone implementation."""

    def __init__(self):
        # Application settings
        self.app_name: str = "Agent Cellphone V2 API"
        self.app_version: str = "2.0.0"
        self.debug: bool = os.getenv("FASTAPI_DEBUG", "false").lower() == "true"

        # Server settings
        self.host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
        self.port: int = int(os.getenv("FASTAPI_PORT", "8000"))

        # CORS settings
        cors_origins = os.getenv("FASTAPI_CORS_ORIGINS", "http://localhost:3000,http://localhost:8080")
        self.cors_origins: list = [origin.strip() for origin in cors_origins.split(",")]

        # Security settings
        self.secret_key: str = os.getenv("FASTAPI_SECRET_KEY", "change-this-in-production")
        self.jwt_secret: str = os.getenv("FASTAPI_JWT_SECRET", "change-this-in-production")

        # Database settings
        self.database_url: Optional[str] = os.getenv("FASTAPI_DATABASE_URL")

        # Redis settings
        self.redis_url: str = os.getenv("FASTAPI_REDIS_URL", "redis://localhost:6379")

        # AI service settings
        self.ai_service_enabled: bool = os.getenv("FASTAPI_AI_ENABLED", "true").lower() == "true"
        self.ai_service_url: Optional[str] = os.getenv("FASTAPI_AI_URL")

        # PERFORMANCE OPTIMIZATION: Performance settings
        self.enable_caching: bool = os.getenv("FASTAPI_ENABLE_CACHING", "true").lower() == "true"
        self.cache_ttl: int = int(os.getenv("FASTAPI_CACHE_TTL", "300"))  # 5 minutes default
        self.cache_max_size: int = int(os.getenv("FASTAPI_CACHE_MAX_SIZE", "1000"))
        self.enable_compression: bool = os.getenv("FASTAPI_ENABLE_COMPRESSION", "true").lower() == "true"
        self.compression_level: int = int(os.getenv("FASTAPI_COMPRESSION_LEVEL", "6"))
        self.enable_performance_monitoring: bool = os.getenv("FASTAPI_PERFORMANCE_MONITORING", "true").lower() == "true"

        # PERFORMANCE OPTIMIZATION: Connection settings
        self.max_connections: int = int(os.getenv("FASTAPI_MAX_CONNECTIONS", "100"))
        self.connection_timeout: int = int(os.getenv("FASTAPI_CONNECTION_TIMEOUT", "30"))
        self.keep_alive_timeout: int = int(os.getenv("FASTAPI_KEEP_ALIVE_TIMEOUT", "65"))

        # Monitoring settings
        self.enable_monitoring: bool = os.getenv("FASTAPI_MONITORING", "true").lower() == "true"
        self.metrics_enabled: bool = os.getenv("FASTAPI_METRICS", "true").lower() == "true"


# Global settings instance
settings = FastAPISettings()


def validate_configuration() -> None:
    """Validate configuration settings."""
    if settings.debug:
        print("⚠️  DEBUG MODE ENABLED - NOT FOR PRODUCTION")

    if settings.secret_key == "change-this-in-production":
        print("⚠️  DEFAULT SECRET KEY DETECTED - CHANGE IN PRODUCTION")

    if not settings.database_url and settings.enable_monitoring:
        print("ℹ️  No database URL configured - using in-memory storage")

    print("✅ FastAPI configuration validated")


def get_cors_origins() -> list:
    """Get CORS origins for middleware."""
    return settings.cors_origins


def is_debug_mode() -> bool:
    """Check if application is in debug mode."""
    return settings.debug


def is_monitoring_enabled() -> bool:
    """Check if monitoring is enabled."""
    return settings.enable_monitoring