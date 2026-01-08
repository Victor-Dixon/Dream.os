#!/usr/bin/env python3
"""
Thea HTTP Service - V2 Compliance
================================

HTTP API wrapper for Thea browser automation.
Provides REST interface that FastAPI expects.

<!-- SSOT Domain: infrastructure -->

Author: Agent-6 (Quality Assurance & Architecture)
License: MIT
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uvicorn

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.services.thea.thea_service import TheaService

logger = logging.getLogger(__name__)

# Pydantic models
class GuidanceRequest(BaseModel):
    """Guidance request model."""
    prompt: str
    context: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 120

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    service: str = "thea"
    version: str = "2.0"

class GuidanceResponse(BaseModel):
    """Guidance response model."""
    success: bool
    response: str
    timestamp: str
    processing_time: float
    error: Optional[str] = None

class TheaHTTPService:
    """
    HTTP service wrapper for Thea browser automation.

    Provides REST API that matches FastAPI expectations while
    internally using browser automation.
    """

    def __init__(self, host: str = "localhost", port: int = 8002):
        """Initialize Thea HTTP service."""
        self.host = host
        self.port = port
        self.app = FastAPI(title="Thea AI Service", version="2.0")
        self.thea_service = None
        self._setup_routes()

    def _setup_routes(self):
        """Set up FastAPI routes."""

        @self.app.get("/health")
        async def health_check() -> HealthResponse:
            """Health check endpoint."""
            return HealthResponse(
                status="healthy",
                timestamp=datetime.now().isoformat()
            )

        @self.app.post("/api/guidance")
        async def get_guidance(request: GuidanceRequest, background_tasks: BackgroundTasks) -> GuidanceResponse:
            """Get AI guidance."""
            start_time = datetime.now()

            try:
                # Initialize Thea service if needed
                if not self.thea_service:
                    await self._initialize_thea_service()

                if not self.thea_service:
                    raise HTTPException(status_code=503, detail="Thea service unavailable")

                # Get guidance
                context = request.context or {}
                context["api_call"] = True
                context["request_timestamp"] = start_time.isoformat()

                # Run in thread pool to avoid blocking
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    self._get_guidance_sync,
                    request.prompt,
                    context,
                    request.timeout
                )

                processing_time = (datetime.now() - start_time).total_seconds()

                return GuidanceResponse(
                    success=True,
                    response=response,
                    timestamp=datetime.now().isoformat(),
                    processing_time=processing_time
                )

            except Exception as e:
                processing_time = (datetime.now() - start_time).total_seconds()
                logger.error(f"Guidance request failed: {e}")

                return GuidanceResponse(
                    success=False,
                    response="",
                    timestamp=datetime.now().isoformat(),
                    processing_time=processing_time,
                    error=str(e)
                )

        @self.app.get("/api/guidance/health")
        async def guidance_health():
            """Check Thea service health."""
            try:
                if not self.thea_service:
                    await self._initialize_thea_service()

                if self.thea_service:
                    return {"status": "ready", "service": "thea"}
                else:
                    return {"status": "initializing", "service": "thea"}
            except Exception as e:
                return {"status": "error", "error": str(e)}

    async def _initialize_thea_service(self):
        """Initialize Thea service asynchronously."""
        try:
            # Run initialization in thread pool
            def init_service():
                service = TheaService()
                # Don't start browser immediately - lazy initialization
                return service

            self.thea_service = await asyncio.get_event_loop().run_in_executor(
                None, init_service
            )

            logger.info("✅ Thea HTTP service initialized")

        except Exception as e:
            logger.error(f"❌ Thea service initialization failed: {e}")
            self.thea_service = None

    def _get_guidance_sync(self, prompt: str, context: Dict[str, Any], timeout: int = 120) -> str:
        """
        Synchronous guidance retrieval.

        Args:
            prompt: Guidance prompt
            context: Additional context
            timeout: Timeout in seconds

        Returns:
            Guidance response string
        """
        if not self.thea_service:
            raise RuntimeError("Thea service not initialized")

        try:
            # Communicate with Thea
            result = self.thea_service.communicate(prompt, save=True)

            if result["success"]:
                response = result["response"]
                if response:
                    return response
                else:
                    return "I apologize, but I was unable to generate a response. Please try again."
            else:
                error = result.get("response", "Unknown error")
                raise RuntimeError(f"Thea communication failed: {error}")

        except Exception as e:
            logger.error(f"Guidance retrieval failed: {e}")
            raise

    async def start_service(self):
        """Start the HTTP service."""
        logger.info(f"🚀 Starting Thea HTTP service on {self.host}:{self.port}")

        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )

        server = uvicorn.Server(config)

        try:
            await server.serve()
        except KeyboardInterrupt:
            logger.info("🛑 Thea HTTP service stopped")
        except Exception as e:
            logger.error(f"❌ Thea HTTP service error: {e}")
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Clean up resources."""
        if self.thea_service:
            try:
                self.thea_service.cleanup()
                logger.info("✅ Thea service cleaned up")
            except Exception as e:
                logger.error(f"❌ Cleanup error: {e}")

# Factory function
def create_thea_http_service(host: str = "localhost", port: int = 8002) -> TheaHTTPService:
    """Create Thea HTTP service instance."""
    return TheaHTTPService(host, port)

# CLI runner
async def main():
    """Run Thea HTTP service."""
    import argparse

    parser = argparse.ArgumentParser(description="Thea HTTP Service")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8002, help="Port to bind to")

    args = parser.parse_args()

    service = create_thea_http_service(args.host, args.port)
    await service.start_service()

if __name__ == "__main__":
    asyncio.run(main())

__all__ = ["TheaHTTPService", "create_thea_http_service", "GuidanceRequest", "GuidanceResponse", "HealthResponse"]