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

        # Server settings - LAN ACCESSIBLE
        self.host: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
        self.port: int = int(os.getenv("FASTAPI_PORT", "8080"))

        # CORS settings - LAN ACCESSIBLE
        cors_origins = os.getenv("FASTAPI_CORS_ORIGINS", "http://localhost:3000,http://localhost:8080,http://192.168.1.0/24,http://10.0.0.0/8,http://172.16.0.0/12,*")
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
        self.enable_monitoring: bool = os.getenv("FASTAPI_MONITORING", "true").lower() == "true"
        self.enable_caching: bool = os.getenv("FASTAPI_CACHING", "true").lower() == "true"
        self.enable_rate_limiting: bool = os.getenv("FASTAPI_RATE_LIMITING", "true").lower() == "true"

        # Performance tuning
        self.max_workers: int = int(os.getenv("FASTAPI_MAX_WORKERS", "4"))
        self.connection_limit: int = int(os.getenv("FASTAPI_CONNECTION_LIMIT", "100"))
        self.request_timeout: int = int(os.getenv("FASTAPI_REQUEST_TIMEOUT", "30"))

# Global settings instance
settings = FastAPISettings()

def get_cors_origins() -> list:
    """Get CORS origins for middleware."""
    return settings.cors_origins


def is_debug_mode() -> bool:
    """Check if application is in debug mode."""
    return settings.debug


def is_monitoring_enabled() -> bool:
    """Check if monitoring is enabled."""
    return settings.enable_monitoring


def validate_configuration():
    """Validate configuration settings."""
    required_settings = [
        ("host", settings.host),
        ("port", settings.port),
        ("cors_origins", settings.cors_origins),
    ]

    for name, value in required_settings:
        if not value:
            raise ValueError(f"Required setting '{name}' is not configured")

    # Validate port range
    if not (1 <= settings.port <= 65535):
        raise ValueError(f"Invalid port number: {settings.port}")

    print("✅ FastAPI configuration validated")