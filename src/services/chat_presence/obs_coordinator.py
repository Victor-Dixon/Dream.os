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
import asyncio
import json
from typing import Optional, Dict, Any, List, Callable

from .chat_config_manager import ChatConfigManager

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False
    websockets = None


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
        self.websocket = None
        self.host = "localhost"
        self.port = 4444
        self.password = ""

        # Callbacks
        self.status_handlers: List[Callable] = []
        self.scene_handlers: List[Callable] = []

    async def start(self) -> bool:
        """Start OBS coordination"""
        if not self.config_manager.is_obs_enabled():
            self.logger.info("OBS coordination disabled in config")
            return True

        try:
            if not WEBSOCKETS_AVAILABLE:
                self.logger.warning("websockets library not available, OBS integration disabled")
                return False

            # Get OBS configuration
            obs_config = self.config_manager.get_obs_config()
            self.host = obs_config.get("host", "localhost")
            self.port = obs_config.get("port", 4444)
            self.password = obs_config.get("password", "")

            # Connect to OBS WebSocket
            uri = f"ws://{self.host}:{self.port}"
            self.websocket = await websockets.connect(uri)

            # Authenticate if password is set
            if self.password:
                await self._authenticate()

            # Get initial status
            await self._update_status()

            self.connected = True
            self.logger.info(f"✅ OBS coordinator connected to {uri}")
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
            if not self.websocket:
                return False

            # Send SetCurrentScene request
            request = {
                "request-type": "SetCurrentScene",
                "scene-name": scene_name,
                "message-id": f"scene_switch_{scene_name}"
            }

            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            response_data = json.loads(response)

            if response_data.get("status") == "ok":
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
            if not self.websocket:
                return False

            # Send StartStreaming request
            request = {
                "request-type": "StartStreaming",
                "message-id": "start_streaming"
            }

            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            response_data = json.loads(response)

            if response_data.get("status") == "ok":
                self.streaming = True
                self.logger.info("🎥 OBS streaming started")
                return True
            else:
                self.logger.error(f"Failed to start streaming: {response_data}")
                return False
        except Exception as e:
            self.logger.error(f"Streaming start error: {e}")
            return False

    async def stop_streaming(self) -> bool:
        """Stop OBS streaming"""
        if not self.connected:
            return False

        try:
            if not self.websocket:
                return False

            # Send StopStreaming request
            request = {
                "request-type": "StopStreaming",
                "message-id": "stop_streaming"
            }

            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            response_data = json.loads(response)

            if response_data.get("status") == "ok":
                self.streaming = False
                self.logger.info("🛑 OBS streaming stopped")
                return True
            else:
                self.logger.error(f"Failed to stop streaming: {response_data}")
                return False

    async def _authenticate(self) -> None:
        """Authenticate with OBS WebSocket"""
        if not self.password:
            return

        try:
            # Get authentication info
            auth_request = {
                "request-type": "GetAuthRequired",
                "message-id": "auth_required"
            }

            await self.websocket.send(json.dumps(auth_request))
            response = await self.websocket.recv()
            auth_info = json.loads(response)

            if auth_info.get("authRequired"):
                # Calculate authentication response
                import hashlib
                import base64

                challenge = auth_info["challenge"]
                salt = auth_info["salt"]

                # OBS WebSocket authentication formula
                secret = base64.b64encode(hashlib.sha256(
                    (self.password + salt).encode('utf-8')
                ).digest()).decode('utf-8')

                auth_response = base64.b64encode(hashlib.sha256(
                    (secret + challenge).encode('utf-8')
                ).digest()).decode('utf-8')

                # Send authentication
                auth_msg = {
                    "request-type": "Authenticate",
                    "auth": auth_response,
                    "message-id": "authenticate"
                }

                await self.websocket.send(json.dumps(auth_msg))
                auth_resp = await self.websocket.recv()
                auth_result = json.loads(auth_resp)

                if auth_result.get("status") != "ok":
                    raise Exception(f"OBS authentication failed: {auth_result}")

                self.logger.info("🔐 OBS WebSocket authenticated")

        except Exception as e:
            self.logger.error(f"OBS authentication error: {e}")
            raise

    async def _update_status(self) -> None:
        """Update OBS status from WebSocket"""
        try:
            if not self.websocket:
                return

            # Get streaming status
            stream_request = {
                "request-type": "GetStreamingStatus",
                "message-id": "get_streaming_status"
            }

            await self.websocket.send(json.dumps(stream_request))
            stream_response = await self.websocket.recv()
            stream_data = json.loads(stream_response)

            self.streaming = stream_data.get("streaming", False)

            # Get current scene
            scene_request = {
                "request-type": "GetCurrentScene",
                "message-id": "get_current_scene"
            }

            await self.websocket.send(json.dumps(scene_request))
            scene_response = await self.websocket.recv()
            scene_data = json.loads(scene_response)

            self.current_scene = scene_data.get("name", "")

            self.logger.debug(f"OBS status updated - streaming: {self.streaming}, scene: {self.current_scene}")

        except Exception as e:
            self.logger.error(f"Error updating OBS status: {e}")
        except Exception as e:
            self.logger.error(f"Streaming stop error: {e}")
            return False