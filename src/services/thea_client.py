#!/usr/bin/env python3
"""
Thea Client - Integration with Thea AI for guidance
==================================================

<!-- SSOT Domain: integration -->

Provides clean interface to Thea AI for project guidance and recommendations.

V2 Compliance: <300 lines, SOLID principles, async support
Author: Agent-4 (Captain - Strategic Coordination)
"""

import json
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TheaClient:
    """Client for Thea AI guidance integration."""

    def __init__(self, base_url: str = "http://localhost:8002", timeout: int = 30):
        """
        Initialize Thea client.

        Args:
            base_url: Base URL for Thea service
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()

    async def initialize(self):
        """Initialize the client session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        logger.info("Thea client initialized")

    async def cleanup(self):
        """Clean up the client session."""
        if self.session:
            await self.session.close()
            self.session = None
        logger.info("Thea client cleaned up")

    async def get_guidance(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Get guidance from Thea AI.

        Args:
            prompt: The guidance request prompt
            context: Additional context information

        Returns:
            Dictionary containing guidance recommendations or None if failed
        """
        if not self.session:
            await self.initialize()

        try:
            payload = {
                "prompt": prompt,
                "timestamp": datetime.now().isoformat(),
                "context": context or {},
                "request_type": "project_guidance"
            }

            url = f"{self.base_url}/guidance"
            logger.info(f"Requesting Thea guidance from {url}")

            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ Thea guidance received successfully")
                    return result
                else:
                    logger.warning(f"⚠️ Thea guidance request failed with status {response.status}")
                    error_text = await response.text()
                    logger.warning(f"Error response: {error_text}")
                    return None

        except aiohttp.ClientError as e:
            logger.error(f"Network error communicating with Thea: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting Thea guidance: {e}")
            return None

    async def get_health_status(self) -> Dict[str, Any]:
        """Get Thea service health status."""
        if not self.session:
            await self.initialize()

        try:
            url = f"{self.base_url}/health"
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status}",
                        "timestamp": datetime.now().isoformat()
                    }
        except Exception as e:
            return {
                "status": "unreachable",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    async def validate_connection(self) -> bool:
        """Validate connection to Thea service."""
        try:
            health = await self.get_health_status()
            return health.get("status") == "healthy"
        except Exception:
            return False

# Convenience function for simple usage
async def get_thea_guidance(prompt: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get Thea guidance with automatic cleanup.

    Args:
        prompt: The guidance request prompt
        context: Additional context information

    Returns:
        Dictionary containing guidance recommendations or None if failed
    """
    async with TheaClient() as client:
        return await client.get_guidance(prompt, context)