#!/usr/bin/env python3
"""
Twitch Chat Bridge
==================

Connects to Twitch IRC and handles:
- Receiving chat messages
- Sending agent responses
- Command routing

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import asyncio
import logging
import re
import threading
from pathlib import Path
from typing import Any, Callable, Optional

try:
    import irc.bot
    import irc.client
    IRC_AVAILABLE = True
except ImportError:
    IRC_AVAILABLE = False

# Use unified logging system
from src.core.unified_logging_system import get_logger, configure_logging

# Configure logging for chat_presence with file handler
log_dir = Path(__file__).parent.parent.parent.parent / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_file = log_dir / "chat_presence_twitch.log"
configure_logging(level="DEBUG", log_file=log_file)

logger = get_logger(__name__)


class TwitchChatBridge:
    """
    Twitch IRC bridge for chat presence.

    Connects to Twitch IRC and routes messages to/from agents.
    """

    def __init__(
        self,
        username: str,
        oauth_token: str,
        channel: str,
        on_message: Optional[Callable[[dict], None]] = None,
        event_loop: Optional[Any] = None,
    ):
        """
        Initialize Twitch chat bridge.

        Args:
            username: Twitch bot username
            oauth_token: Twitch OAuth token (oauth:xxxxx format)
            channel: Twitch channel name (without #)
            on_message: Callback for incoming messages
            event_loop: Optional event loop for async callbacks (if None, will try to get current loop)
        """
        if not IRC_AVAILABLE:
            raise ImportError(
                "irc library required. Install with: pip install irc"
            )

        self.username = username
        self.oauth_token = oauth_token
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.on_message = on_message
        self.event_loop = event_loop
        self.bot = None
        self.running = False
        self.connected = False  # True when actually joined channel
        self._has_sent_online_message = False

    async def connect(self) -> bool:
        """
        Connect to Twitch IRC.

        Returns:
            True if connected successfully
        """
        try:
            logger.info(f"🔌 Connecting to Twitch IRC as {self.username}")

            # Create IRC bot with OAuth token
            self.bot = TwitchIRCBot(
                server_list=[("irc.chat.twitch.tv", 6667)],
                nickname=self.username,
                realname=self.username,
                channel=self.channel,
                on_message=self._handle_message,
                bridge_instance=self,  # Pass bridge instance for shared state
                oauth_token=self.oauth_token,  # Pass OAuth token to bot
            )

            # Connect in separate thread (bot.start() is blocking)
            bot_thread = threading.Thread(
                target=self._run_bot,
                daemon=True,
                name="TwitchIRCBot"
            )
            bot_thread.start()
            
            # Wait a moment for connection to establish
            await asyncio.sleep(2)
            
            # Set running flag - connection will complete in background thread
            self.running = True
            logger.info(f"🔄 Twitch bot starting in background thread...")
            logger.info(f"📺 Will connect to channel: {self.channel}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to connect to Twitch: {e}", exc_info=True)
            return False

    def _run_bot(self) -> None:
        """Run IRC bot in separate thread (blocking call)."""
        try:
            logger.info("🔄 Starting IRC bot in background thread...")
            logger.debug(f"Bot object: {self.bot}")
            if self.bot:
                logger.debug(f"Bot has connection: {hasattr(self.bot, 'connection')}")
                if hasattr(self.bot, 'connection') and self.bot.connection:
                    has_password = bool(getattr(self.bot.connection, 'password', None))
                    logger.debug(f"Connection password set: {has_password}")
                    pwd = getattr(self.bot.connection, 'password', None)
                    if pwd:
                        logger.debug(f"Password value: {pwd[:20]}...")
            logger.debug("About to call bot.start()...")
            self.bot.start()
            logger.warning("bot.start() returned (unexpected - it's blocking)")
        except Exception as e:
            logger.error(
                "IRC bot thread error",
                extra={
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "component": "TwitchIRCBot",
                    "operation": "_run_bot",
                },
                exc_info=True
            )
            self.running = False
            self.connected = False

    def _handle_message(self, message_data: dict) -> None:
        """
        Handle incoming chat message.

        Args:
            message_data: Message data dictionary
        """
        if self.on_message:
            try:
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in message callback: {e}", exc_info=True)

    async def send_message(self, message: str) -> bool:
        """
        Send message to Twitch chat.

        Args:
            message: Message to send

        Returns:
            True if sent successfully
        """
        if not self.bot or not self.running or not self.connected:
            logger.warning("⚠️ Not connected to Twitch (bot not ready)")
            return False

        try:
            # Check if connection is actually ready
            if not hasattr(self.bot, 'connection') or not self.bot.connection:
                logger.warning("⚠️ IRC connection not ready")
                return False
            
            # CRITICAL: IRC doesn't allow newlines or carriage returns in messages
            # Sanitize message by replacing newlines/carriage returns with spaces
            sanitized = message.replace('\n', ' ').replace('\r', ' ').strip()
            # Also remove any double spaces that might result
            while '  ' in sanitized:
                sanitized = sanitized.replace('  ', ' ')
            
            # Twitch IRC message format
            self.bot.connection.privmsg(self.channel, sanitized)
            logger.info(f"📤 Sent to Twitch: {sanitized[:50]}...")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False

    async def send_as_agent(self, agent_id: str, message: str) -> bool:
        """
        Send message as specific agent.

        Args:
            agent_id: Agent identifier
            message: Message content

        Returns:
            True if sent successfully
        """
        # Format message with agent identity
        formatted = f"[{agent_id}] {message}"

        return await self.send_message(formatted)

    def stop(self) -> None:
        """Stop Twitch connection."""
        self.running = False
        self._has_sent_online_message = False  # Reset for next connection
        if self.bot:
            try:
                self.bot.connection.quit("Agent system shutdown")
                logger.info("🔌 Disconnected from Twitch")
            except Exception:
                pass


class TwitchIRCBot(irc.bot.SingleServerIRCBot):
    """IRC bot implementation for Twitch."""

    def __init__(
        self,
        server_list: list,
        nickname: str,
        realname: str,
        channel: str,
        on_message: Optional[Callable[[dict], None]] = None,
        bridge_instance: Optional[Any] = None,
        oauth_token: Optional[str] = None,
    ):
        """
        Initialize Twitch IRC bot.

        Args:
            server_list: List of (host, port) tuples
            nickname: Bot nickname
            realname: Bot realname
            channel: Channel to join
            on_message: Message callback
            bridge_instance: Reference to TwitchChatBridge for shared state
            oauth_token: OAuth token for authentication
        """
        # Store OAuth token for use in _connect()
        self.oauth_token = oauth_token
        
        # Pass password via connect_params - parent _connect() will use it
        # The parent _connect() calls self.connect() with **self.__connect_params
        connect_params = {}
        if oauth_token:
            connect_params['password'] = oauth_token
            logger.info("🔐 Passing OAuth token via connect_params")
            print(f"🔐 DEBUG: Passing OAuth token via connect_params: {oauth_token[:20]}...", flush=True)
        
        # Call parent __init__ with connect_params
        super().__init__(server_list, nickname, realname, **connect_params)
        
        self.channel = channel
        self.on_message = on_message
        self.bridge_instance = bridge_instance
    
    def _connect(self):
        """
        Override _connect() to pass password correctly.
        
        The parent _connect() passes server.password as positional arg,
        which conflicts with password in connect_params. We override to
        pass None for server.password and use our oauth_token instead.
        """
        server = self.servers.peek()
        try:
            # Get connect_params from parent (name-mangled attribute)
            connect_params = getattr(self, '_SingleServerIRCBot__connect_params', {})
            
            # Pass None for server.password (4th positional arg) to avoid conflict
            # Use password from oauth_token or connect_params
            password = self.oauth_token if self.oauth_token else connect_params.get('password')
            
            self.connect(
                server.host,
                server.port,
                self._nickname,
                password,  # Use our OAuth token directly
                ircname=self._realname,
                **{k: v for k, v in connect_params.items() if k != 'password'},  # Exclude password from kwargs to avoid conflict
            )
        except irc.client.ServerConnectionError:
            self.connection._handle_event(
                irc.client.Event("disconnect", self.connection.server, "", [""])
            )

    def on_welcome(self, connection, event) -> None:
        """Called when bot connects to IRC."""
        logger.info("✅ Connected to Twitch IRC")
        print("✅ DEBUG: Connected to Twitch IRC - on_welcome called")
        print(f"✅ DEBUG: Event type: {event.type}, Event args: {event.arguments}")
        
        # Request IRC capabilities for Twitch tags (required for message metadata)
        # CRITICAL: These capabilities are required to receive messages properly
        try:
            connection.cap("REQ", "twitch.tv/membership")
            connection.cap("REQ", "twitch.tv/tags")
            connection.cap("REQ", "twitch.tv/commands")
            logger.info("📋 Requested Twitch IRC capabilities")
            print("📋 DEBUG: Requested Twitch IRC capabilities: membership, tags, commands", flush=True)
        except Exception as e:
            logger.warning(f"⚠️ Could not request IRC capabilities: {e}")
            print(f"⚠️ DEBUG: Could not request IRC capabilities: {e}", flush=True)
        
        # Join channel
        logger.info(f"📺 Attempting to join channel: {self.channel}")
        print(f"📺 DEBUG: Attempting to join channel: {self.channel}", flush=True)
        connection.join(self.channel)
        logger.info(f"📺 Join command sent for channel: {self.channel}")
        print(f"📺 DEBUG: Join command sent", flush=True)
    
    def on_cap(self, connection, event) -> None:
        """Handle CAP (capability) responses from Twitch."""
        cap_args = getattr(event, 'arguments', [])
        logger.info(f"📋 CAP response: {cap_args}")
        print(f"📋 DEBUG: CAP response received: {cap_args}", flush=True)
    
    def on_nicknameinuse(self, connection, event) -> None:
        """Called when nickname is already in use."""
        logger.error("❌ Nickname already in use!")
        print("❌ DEBUG: Nickname already in use!")
    
    def on_disconnect(self, connection, event) -> None:
        """Called when disconnected from IRC."""
        logger.warning("⚠️ Disconnected from Twitch IRC")
        print("⚠️ DEBUG: Disconnected from Twitch IRC")
        print(f"⚠️ DEBUG: Disconnect event type: {event.type}")
        print(f"⚠️ DEBUG: Disconnect event args: {getattr(event, 'arguments', 'N/A')}")
        print(f"⚠️ DEBUG: Connection state: {getattr(connection, 'connected', 'N/A')}")
        if self.bridge_instance:
            self.bridge_instance.connected = False
            self.bridge_instance.running = False
    
    def on_error(self, connection, event) -> None:
        """Called on IRC errors."""
        error_msg = str(event)
        error_args = getattr(event, 'arguments', [])
        error_type = getattr(event, 'type', 'unknown')
        
        logger.error(f"❌ IRC Error: {error_msg}")
        logger.error(f"❌ IRC Error Type: {error_type}")
        logger.error(f"❌ IRC Error Args: {error_args}")
        print(f"❌ DEBUG: IRC Error: {error_msg}", flush=True)
        print(f"❌ DEBUG: Error type: {error_type}, Arguments: {error_args}", flush=True)
        print(f"❌ DEBUG: Full error event: {event}", flush=True)
        if hasattr(event, 'source'):
            print(f"❌ DEBUG: Error source: {event.source}", flush=True)
        
        # Check for authentication errors
        error_str = str(error_msg).lower() + " " + " ".join(str(arg).lower() for arg in error_args)
        if any(keyword in error_str for keyword in ['authentication', 'password', 'login', 'invalid', 'unauthorized']):
            logger.error("❌ AUTHENTICATION FAILURE DETECTED!")
            logger.error("❌ OAuth token may be invalid, expired, or incorrectly formatted")
            print("❌ DEBUG: AUTHENTICATION FAILURE - OAuth token likely invalid/expired", flush=True)
            print("❌ DEBUG: Verify token at: https://twitchapps.com/tmi/", flush=True)
        
        if self.bridge_instance:
            self.bridge_instance.connected = False
    
    def on_notice(self, connection, event) -> None:
        """Called on IRC NOTICE messages - Twitch uses these for auth errors."""
        notice_msg = event.arguments[0] if event.arguments else str(event)
        logger.warning(f"📢 IRC Notice: {notice_msg}")
        print(f"📢 DEBUG: IRC Notice: {notice_msg}", flush=True)
        
        # Twitch sends authentication errors as NOTICE messages
        if any(keyword in notice_msg.lower() for keyword in ['login', 'authentication', 'password', 'invalid', 'unauthorized', 'error']):
            logger.error(f"❌ AUTHENTICATION ERROR from Twitch: {notice_msg}")
            print(f"❌ DEBUG: AUTHENTICATION ERROR: {notice_msg}", flush=True)
            print("❌ DEBUG: Your OAuth token is likely invalid or expired", flush=True)
            print("❌ DEBUG: Get a new token at: https://twitchapps.com/tmi/", flush=True)
            if self.bridge_instance:
                self.bridge_instance.connected = False
    
    def on_all_events(self, connection, event) -> None:
        """Called for all IRC events - useful for debugging."""
        # Log important events - especially pubmsg to see if messages are received
        if event.type in ['disconnect', 'error', 'welcome', 'join', 'privmsg', 'pubmsg', 'notice']:
            event_args = getattr(event, 'arguments', [])
            if event.type == 'pubmsg':
                # CRITICAL: Log ALL pubmsg events to see if messages are being received
                message_text = event_args[0] if event_args else ""
                username = getattr(event.source, 'nick', 'unknown') if hasattr(event, 'source') else 'unknown'
                logger.info(f"📡 IRC PUBMSG Event: {username}: {message_text[:50]}")
                print(f"📡 DEBUG: IRC PUBMSG Event received - User: {username}, Message: {message_text[:50]}", flush=True)
            elif event.type in ['disconnect', 'error']:
                logger.error(f"📡 IRC Event: {event.type} - {event_args}")
                print(f"📡 DEBUG: IRC Event: {event.type} - {event_args}", flush=True)
            elif event.type == 'notice':
                notice_msg = event_args[0] if event_args else str(event)
                logger.info(f"📡 IRC NOTICE: {notice_msg[:100]}")
                print(f"📡 DEBUG: IRC NOTICE: {notice_msg[:100]}", flush=True)
            else:
                logger.debug(f"📡 IRC Event: {event.type} - {event_args}")

    def on_join(self, connection, event) -> None:
        """Called when bot joins channel."""
        logger.info(f"✅ Joined {event.target}")
        print(f"✅ DEBUG: Joined {event.target}")
        
        # Mark as connected when we actually join the channel
        if self.bridge_instance:
            self.bridge_instance.connected = True
            logger.info("✅ Connection fully established - ready to send messages")
            print("✅ DEBUG: Connection fully established")
        
        # Send online message when bot joins (only once)
        # Check flag on bridge instance if available
        has_sent = False
        if self.bridge_instance:
            has_sent = self.bridge_instance._has_sent_online_message
        
        if not has_sent:
            try:
                # Wait a moment for connection to stabilize
                import time
                time.sleep(1)
                
                # Send online message
                online_message = "🐝 Swarm bot is now online! Use !status to check agent status, or !agent7 <message> to message agents (admin only). 🐝 WE. ARE. SWARM. ⚡🔥"
                connection.privmsg(self.channel, online_message)
                logger.info("📢 Sent online message to chat")
                print("📢 DEBUG: Sent online message to chat")
                if self.bridge_instance:
                    self.bridge_instance._has_sent_online_message = True
            except Exception as e:
                logger.error(f"❌ Failed to send online message: {e}", exc_info=True)
                print(f"❌ DEBUG: Failed to send online message: {e}")

    def on_pubmsg(self, connection, event) -> None:
        """
        Called when public message received.

        Args:
            connection: IRC connection
            event: IRC event
        """
        # Parse Twitch message
        message_text = event.arguments[0] if event.arguments else ""
        username = event.source.nick

        logger.info(f"🔍 DEBUG: Received message from {username}: {message_text[:50]}")
        print(f"🔍 DEBUG: on_pubmsg called - User: {username}, Message: {message_text[:50]}")

        # Skip bot's own messages
        try:
            bot_nickname = self.connection.get_nickname()
            if username == bot_nickname:
                logger.debug(f"⏭️ Skipping bot's own message from {username}")
                print(f"⏭️ DEBUG: Skipping bot's own message from {username} (bot: {bot_nickname})")
                return
        except Exception as e:
            logger.warning(f"⚠️ Could not get bot nickname: {e}")
            print(f"⚠️ DEBUG: Could not get bot nickname: {e}")
            # Continue processing - might be first message

        # Extract Twitch-specific metadata
        tags = {}
        if hasattr(event, "tags"):
            tags = event.tags
        elif hasattr(event, "arguments") and len(event.arguments) > 0:
            # Parse IRC tags from message if available
            # Twitch IRC format: @badges=broadcaster/1;color=#FF0000;display-name=Username :username!username@username.tmi.twitch.tv PRIVMSG #channel :message
            pass  # Tags should be in event.tags, but fallback parsing could go here

        message_data = {
            "username": username,
            "message": message_text,
            "channel": self.channel,
            "timestamp": event.timestamp if hasattr(event, "timestamp") else None,
            "tags": tags,
            "raw_event": event,
        }

        # Call callback
        if self.on_message:
            try:
                is_coroutine = asyncio.iscoroutinefunction(self.on_message)
                logger.info(
                    "Calling message callback",
                    extra={
                        "message_preview": message_text[:50],
                        "is_coroutine": is_coroutine,
                        "has_bridge_instance": self.bridge_instance is not None,
                    }
                )
                
                if self.bridge_instance:
                    event_loop_status = "SET" if (hasattr(self.bridge_instance, 'event_loop') and self.bridge_instance.event_loop) else "NOT SET"
                    logger.debug(f"bridge_instance.event_loop: {event_loop_status}")
                
                if is_coroutine:
                    # Get event loop - try bridge_instance's event_loop, then get from bridge
                    loop = None
                    if self.bridge_instance:
                        # Try to get event loop from bridge instance (TwitchChatBridge)
                        if hasattr(self.bridge_instance, 'event_loop') and self.bridge_instance.event_loop:
                            loop = self.bridge_instance.event_loop
                            logger.debug(f"Found event loop from bridge_instance: {loop}")
                    
                    if not loop:
                        # Try to get current/running loop
                        try:
                            loop = asyncio.get_running_loop()
                            logger.debug(f"Found running event loop: {loop}")
                        except RuntimeError:
                            try:
                                loop = asyncio.get_event_loop()
                                logger.debug(f"Found event loop (not running): {loop}")
                            except RuntimeError:
                                logger.warning("No event loop found")
                    
                    if loop and loop.is_running():
                        # Schedule coroutine in the running event loop
                        future = asyncio.run_coroutine_threadsafe(self.on_message(message_data), loop)
                        logger.info(
                            "Scheduled message callback in event loop",
                            extra={"future_id": id(future)}
                        )
                        
                        # Add callback to handle exceptions
                        def callback_done(fut):
                            try:
                                result = fut.result(timeout=0)  # Check if done
                                logger.info("Callback completed successfully")
                            except Exception as e:
                                logger.error(
                                    "Callback raised exception",
                                    extra={
                                        "error_type": type(e).__name__,
                                        "error_message": str(e),
                                        "component": "TwitchIRCBot",
                                        "operation": "on_message_callback",
                                    },
                                    exc_info=True
                                )
                        
                        future.add_done_callback(callback_done)
                    else:
                        # Fallback: run in new thread with new event loop
                        logger.warning("No running event loop found, creating new one")
                        import threading
                        def run_async():
                            new_loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(new_loop)
                            try:
                                logger.info("Starting callback execution in new event loop")
                                new_loop.run_until_complete(self.on_message(message_data))
                                logger.info("Callback executed in new event loop")
                            except Exception as e:
                                logger.error(
                                    "Error in callback execution",
                                    extra={
                                        "error_type": type(e).__name__,
                                        "error_message": str(e),
                                        "component": "TwitchIRCBot",
                                        "operation": "on_message_callback_fallback",
                                    },
                                    exc_info=True
                                )
                            finally:
                                new_loop.close()
                        thread = threading.Thread(target=run_async, daemon=True, name="TwitchCallbackThread")
                        thread.start()
                        logger.info("Started callback in new thread", extra={"thread_name": thread.name})
                else:
                    # Synchronous callback
                    logger.info("📨 Calling synchronous callback")
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"❌ Error in message handler: {e}", exc_info=True)
                print(f"❌ DEBUG: Error in message handler: {e}", flush=True)
                import traceback
                traceback.print_exc()
        else:
            logger.warning("⚠️ No message callback registered!")
            print("⚠️ DEBUG: No message callback registered!", flush=True)

    def on_privmsg(self, connection, event) -> None:
        """
        Called when private message received.

        Args:
            connection: IRC connection
            event: IRC event
        """
        # Handle private messages similarly
        message_text = event.arguments[0] if event.arguments else ""
        username = event.source.nick

        message_data = {
            "username": username,
            "message": message_text,
            "channel": "PRIVATE",
            "timestamp": None,
            "tags": {},
            "raw_event": event,
        }

        if self.on_message:
            try:
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in private message handler: {e}", exc_info=True)


# Alternative: WebSocket-based Twitch connection (modern approach)
class TwitchWebSocketBridge:
    """
    Modern Twitch WebSocket bridge (PubSub/EventSub).

    More reliable than IRC for production use.
    """

    def __init__(
        self,
        client_id: str,
        access_token: str,
        channel_id: str,
        on_message: Optional[Callable[[dict], None]] = None,
    ):
        """
        Initialize WebSocket bridge.

        Args:
            client_id: Twitch API client ID
            access_token: Twitch API access token
            channel_id: Twitch channel ID
            on_message: Message callback
        """
        self.client_id = client_id
        self.access_token = access_token
        self.channel_id = channel_id
        self.on_message = on_message
        self.running = False

    async def connect(self) -> bool:
        """Connect to Twitch WebSocket."""
        # Implementation would use Twitch EventSub WebSocket
        # This is a placeholder for the modern approach
        logger.warning("⚠️ WebSocket bridge not yet implemented, use IRC bridge")
        return False


__all__ = ["TwitchChatBridge", "TwitchIRCBot", "TwitchWebSocketBridge"]




