#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

OBS Caption Listener
===================

Real-time OBS caption capture via WebSocket.
Listens for caption events and emits them for processing.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Callable, Optional

try:
    import websockets
    WEBSOCKETS_AVAILABLE = True
except ImportError:
    WEBSOCKETS_AVAILABLE = False

logger = logging.getLogger(__name__)


class OBSCaptionListener:
    """
    Listens to OBS WebSocket for real-time captions.

    OBS Setup:
    1. OBS → Tools → Scripts → Add WebSocket Server
    2. Enable WebSocket server on localhost:4455 (default)
    3. Configure caption output to WebSocket
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 4455,
        password: Optional[str] = None,
        on_caption: Optional[Callable[[dict], None]] = None,
    ):
        """
        Initialize OBS caption listener.

        Args:
            host: OBS WebSocket host (default: localhost)
            port: OBS WebSocket port (default: 4455)
            password: OBS WebSocket password (if required)
            on_caption: Callback function for caption events
        """
        if not WEBSOCKETS_AVAILABLE:
            raise ImportError(
                "websockets library required. Install with: pip install websockets"
            )

        self.host = host
        self.port = port
        self.password = password
        self.on_caption = on_caption
        self.websocket = None
        self.running = False
        self.reconnect_delay = 5.0
        self.max_reconnect_delay = 60.0

    async def connect(self) -> bool:
        """
        Connect to OBS WebSocket.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            uri = f"ws://{self.host}:{self.port}"
            logger.info(f"🔌 Connecting to OBS WebSocket: {uri}")

            self.websocket = await websockets.connect(uri)

            # Authenticate if password required
            if self.password:
                auth_message = {"request-type": "Authenticate", "auth": self.password}
                await self.websocket.send(json.dumps(auth_message))
                response = await self.websocket.recv()
                auth_result = json.loads(response)
                if auth_result.get("status") != "ok":
                    logger.error("❌ OBS authentication failed")
                    return False

            logger.info("✅ Connected to OBS WebSocket")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to OBS: {e}")
            return False

    async def listen(self) -> None:
        """
        Start listening for caption events.

        Continuously listens for messages and processes caption events.
        """
        if not await self.connect():
            logger.error("Failed to establish OBS connection")
            return

        self.running = True
        logger.info("👂 Listening for OBS captions...")

        try:
            while self.running:
                try:
                    from src.core.config.timeout_constants import TimeoutConstants
                    message = await asyncio.wait_for(
                        self.websocket.recv(), timeout=TimeoutConstants.HTTP_QUICK
                    )
                    await self._process_message(message)

                except asyncio.TimeoutError:
                    # Send ping to keep connection alive
                    await self._send_ping()
                    continue

                except websockets.exceptions.ConnectionClosed:
                    logger.warning("⚠️ OBS connection closed, reconnecting...")
                    if self.running:
                        await self._reconnect()
                    break

        except KeyboardInterrupt:
            logger.info("🛑 Stopping OBS caption listener")
        except Exception as e:
            logger.error(f"❌ Error in listen loop: {e}", exc_info=True)
        finally:
            await self.disconnect()

    async def _process_message(self, message: str) -> None:
        """
        Process incoming WebSocket message.

        Args:
            message: Raw WebSocket message
        """
        try:
            data = json.loads(message)

            # Check if this is a caption event
            if self._is_caption_event(data):
                caption_data = self._extract_caption(data)
                if caption_data:
                    await self._handle_caption(caption_data)

        except json.JSONDecodeError:
            logger.debug(f"Non-JSON message received: {message[:100]}")
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)

    def _is_caption_event(self, data: dict) -> bool:
        """
        Check if message is a caption event.

        Args:
            data: Parsed JSON data

        Returns:
            True if this is a caption event
        """
        # OBS caption events typically have these fields
        return (
            data.get("update-type") == "Caption"
            or "caption" in str(data).lower()
            or "text" in data
            and "timestamp" in data
        )

    def _extract_caption(self, data: dict) -> Optional[dict]:
        """
        Extract caption data from event.

        Args:
            data: Event data

        Returns:
            Caption data dict or None
        """
        try:
            # OBS caption format varies, handle common patterns
            text = data.get("text") or data.get("caption") or data.get("content", "")
            timestamp = data.get("timestamp") or datetime.now().isoformat()

            if not text or not text.strip():
                return None

            return {
                "text": text.strip(),
                "timestamp": timestamp,
                "raw_data": data,
            }

        except Exception as e:
            logger.error(f"Error extracting caption: {e}")
            return None

    async def _handle_caption(self, caption_data: dict) -> None:
        """
        Handle caption event.

        Args:
            caption_data: Caption data dictionary
        """
        logger.info(f"📝 Caption received: {caption_data['text'][:50]}...")

        # Call callback if provided
        if self.on_caption:
            try:
                if asyncio.iscoroutinefunction(self.on_caption):
                    await self.on_caption(caption_data)
                else:
                    self.on_caption(caption_data)
            except Exception as e:
                logger.error(f"Error in caption callback: {e}", exc_info=True)

    async def _send_ping(self) -> None:
        """Send ping to keep connection alive."""
        try:
            if self.websocket:
                ping_message = {"request-type": "GetVersion"}
                await self.websocket.send(json.dumps(ping_message))
        except Exception:
            pass  # Ignore ping errors

    async def _reconnect(self) -> None:
        """Attempt to reconnect to OBS."""
        delay = self.reconnect_delay
        while self.running:
            logger.info(f"🔄 Reconnecting in {delay}s...")
            await asyncio.sleep(delay)

            if await self.connect():
                await self.listen()
                break

            delay = min(delay * 2, self.max_reconnect_delay)

    async def disconnect(self) -> None:
        """Disconnect from OBS WebSocket."""
        self.running = False
        if self.websocket:
            try:
                await self.websocket.close()
                logger.info("🔌 Disconnected from OBS")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")

    async def start(self) -> None:
        """Start listening (convenience method)."""
        await self.listen()


# Alternative: File-based caption listener (fallback)
class OBSCaptionFileListener:
    """
    Fallback: Listen to OBS caption file output.

    OBS Setup:
    1. OBS → Settings → Output → Recording
    2. Enable "Caption Output" → Select file path
    3. This listener watches that file for changes
    """

    def __init__(
        self,
        caption_file_path: str,
        on_caption: Optional[Callable[[dict], None]] = None,
        poll_interval: float = 0.5,
    ):
        """
        Initialize file-based caption listener.

        Args:
            caption_file_path: Path to OBS caption output file
            on_caption: Callback for caption events
            poll_interval: File polling interval in seconds
        """
        self.caption_file_path = caption_file_path
        self.on_caption = on_caption
        self.poll_interval = poll_interval
        self.running = False
        self.last_position = 0

    async def listen(self) -> None:
        """Start listening for file changes."""
        from pathlib import Path

        caption_file = Path(self.caption_file_path)
        if not caption_file.exists():
            logger.warning(f"⚠️ Caption file not found: {self.caption_file_path}")
            return

        self.running = True
        logger.info(f"👂 Watching caption file: {self.caption_file_path}")

        try:
            while self.running:
                await self._check_file(caption_file)
                await asyncio.sleep(self.poll_interval)

        except KeyboardInterrupt:
            logger.info("🛑 Stopping file caption listener")
        finally:
            self.running = False

    async def _check_file(self, file_path) -> None:
        """Check file for new captions."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                f.seek(self.last_position)
                new_content = f.read()
                self.last_position = f.tell()

                if new_content.strip():
                    lines = new_content.strip().split("\n")
                    for line in lines:
                        if line.strip():
                            caption_data = {
                                "text": line.strip(),
                                "timestamp": datetime.now().isoformat(),
                                "source": "file",
                            }

                            if self.on_caption:
                                try:
                                    if asyncio.iscoroutinefunction(self.on_caption):
                                        await self.on_caption(caption_data)
                                    else:
                                        self.on_caption(caption_data)
                                except Exception as e:
                                    logger.error(f"Error in caption callback: {e}")

        except Exception as e:
            logger.error(f"Error reading caption file: {e}")

    def stop(self) -> None:
        """Stop listening."""
        self.running = False


__all__ = ["OBSCaptionListener", "OBSCaptionFileListener"]




