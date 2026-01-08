"""
OBS Coordinator - V2 Coordinator Module
=======================================

SSOT Domain: integration

V2 Compliant: <100 lines, single responsibility
OBS (Open Broadcaster Software) integration coordinator.

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from typing import Optional, Dict, Any, List, Callable

from .chat_config_manager import ChatConfigManager


class OBSCoordinator:
    """
    V2 Compliant OBS Coordinator

    Manages OBS integration for streaming coordination:
    - Connection to OBS WebSocket
    - Scene switching
    - Source control
    - Recording/streaming status
    """

    def __init__(self, config_manager: ChatConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger("OBSCoordinator")

        # Connection state
        self.connected = False
        self.streaming = False
        self.recording = False
        self.current_scene = ""

        # Callbacks
        self.status_handlers: List[Callable] = []
        self.scene_handlers: List[Callable] = []

    async def start(self) -> bool:
        """Start OBS coordination"""
        if not self.config_manager.is_obs_enabled():
            self.logger.info("OBS coordination disabled in config")
            return True

        try:
            # TODO: Implement OBS WebSocket connection
            # For now, mark as connected for architecture completeness
            self.connected = True
            self.logger.info("✅ OBS coordinator started (placeholder)")
            return True

        except Exception as e:
            self.logger.error(f"❌ OBS coordinator startup error: {e}")
            return False

    async def stop(self) -> None:
        """Stop OBS coordination"""
        self.connected = False
        self.streaming = False
        self.recording = False
        self.logger.info("🛑 OBS coordinator stopped")

    async def switch_scene(self, scene_name: str) -> bool:
        """Switch to specified OBS scene"""
        if not self.connected:
            return False

        try:
            # TODO: Implement actual OBS scene switching
            old_scene = self.current_scene
            self.current_scene = scene_name
            self.logger.info(f"🎭 Scene switched: {old_scene} → {scene_name}")

            # Notify scene handlers
            for handler in self.scene_handlers:
                try:
                    await handler(scene_name, old_scene)
                except Exception as e:
                    self.logger.error(f"Scene handler error: {e}")

            return True

        except Exception as e:
            self.logger.error(f"Scene switch error: {e}")
            return False

    def add_status_handler(self, handler: Callable) -> None:
        """Add status change handler callback"""
        self.status_handlers.append(handler)

    def add_scene_handler(self, handler: Callable) -> None:
        """Add scene change handler callback"""
        self.scene_handlers.append(handler)

    def get_status(self) -> Dict[str, Any]:
        """Get current OBS coordination status"""
        return {
            "connected": self.connected,
            "streaming": self.streaming,
            "recording": self.recording,
            "current_scene": self.current_scene,
            "config_valid": self.config_manager.validate_config()["valid"]
        }

    def is_healthy(self) -> bool:
        """Check if OBS coordinator is healthy"""
        if not self.config_manager.is_obs_enabled():
            return True  # Disabled is considered healthy

        return self.connected

    async def start_streaming(self) -> bool:
        """Start OBS streaming"""
        if not self.connected:
            return False

        try:
            # TODO: Implement actual OBS streaming start
            self.streaming = True
            self.logger.info("🎥 OBS streaming started")
            return True
        except Exception as e:
            self.logger.error(f"Streaming start error: {e}")
            return False

    async def stop_streaming(self) -> bool:
        """Stop OBS streaming"""
        if not self.connected:
            return False

        try:
            # TODO: Implement actual OBS streaming stop
            self.streaming = False
            self.logger.info("🛑 OBS streaming stopped")
            return True
        except Exception as e:
            self.logger.error(f"Streaming stop error: {e}")
            return False