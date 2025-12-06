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
from typing import Any, Callable, Optional

try:
    import irc.bot
    import irc.client
    IRC_AVAILABLE = True
except ImportError:
    IRC_AVAILABLE = False

logger = logging.getLogger(__name__)


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
    ):
        """
        Initialize Twitch chat bridge.

        Args:
            username: Twitch bot username
            oauth_token: Twitch OAuth token (oauth:xxxxx format)
            channel: Twitch channel name (without #)
            on_message: Callback for incoming messages
        """
        if not IRC_AVAILABLE:
            raise ImportError(
                "irc library required. Install with: pip install irc"
            )

        self.username = username
        self.oauth_token = oauth_token
        self.channel = channel if channel.startswith("#") else f"#{channel}"
        self.on_message = on_message
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
            print("🔄 DEBUG: Starting IRC bot in background thread...", flush=True)
            print(f"🔄 DEBUG: Bot object: {self.bot}", flush=True)
            if self.bot:
                print(f"🔄 DEBUG: Bot has connection: {hasattr(self.bot, 'connection')}", flush=True)
                if hasattr(self.bot, 'connection') and self.bot.connection:
                    print(f"🔄 DEBUG: Connection password set: {bool(getattr(self.bot.connection, 'password', None))}", flush=True)
                    pwd = getattr(self.bot.connection, 'password', None)
                    if pwd:
                        print(f"🔄 DEBUG: Password value: {pwd[:20]}...", flush=True)
            print("🔄 DEBUG: About to call bot.start()...", flush=True)
            self.bot.start()
            print("🔄 DEBUG: bot.start() returned (unexpected - it's blocking)", flush=True)
        except Exception as e:
            logger.error(f"❌ IRC bot thread error: {e}", exc_info=True)
            print(f"❌ DEBUG: IRC bot thread error: {e}", flush=True)
            import traceback
            traceback.print_exc()
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
                
            # Twitch IRC message format
            self.bot.connection.privmsg(self.channel, message)
            logger.info(f"📤 Sent to Twitch: {message[:50]}...")
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
        # Store OAuth token BEFORE calling super().__init__()
        # We'll set it on the connection after it's created
        self.oauth_token = oauth_token
        
        super().__init__(server_list, nickname, realname)
        self.channel = channel
        self.on_message = on_message
        self.bridge_instance = bridge_instance
        
        # Set OAuth token immediately after parent __init__ creates connection
        # The connection object exists after super().__init__()
        if self.oauth_token and hasattr(self, 'connection') and self.connection:
            try:
                self.connection.password = self.oauth_token
                logger.info("🔐 Set OAuth token on connection (in __init__)")
            except Exception as e:
                logger.error(f"❌ Failed to set password: {e}", exc_info=True)
        else:
            logger.warning("⚠️ Could not set OAuth token in __init__ - connection or token missing")
    
    def _connect(self):
        """
        Override connection method to ensure password is set BEFORE connecting.
        
        CRITICAL: Password must be set BEFORE super()._connect() is called,
        because that's when the IRC handshake (PASS/NICK/USER) begins.
        """
        # CRITICAL: Set password BEFORE calling parent _connect()
        # The parent _connect() starts the IRC handshake, and the password
        # must be sent as the first command (PASS <password>)
        if self.oauth_token and hasattr(self, 'connection') and self.connection:
            try:
                self.connection.password = self.oauth_token
                logger.info("🔐 Set OAuth token BEFORE connection (in _connect)")
                print(f"🔐 DEBUG: Set OAuth token BEFORE _connect(): {self.oauth_token[:20]}...", flush=True)
                print(f"🔐 DEBUG: Connection password verified: {getattr(self.connection, 'password', 'NOT SET')[:20] if getattr(self.connection, 'password', None) else 'NOT SET'}...", flush=True)
            except Exception as e:
                logger.error(f"❌ CRITICAL: Failed to set password before _connect: {e}", exc_info=True)
                print(f"❌ DEBUG: Failed to set password: {e}", flush=True)
                import traceback
                traceback.print_exc()
        else:
            logger.error("❌ CRITICAL: Cannot set password - token or connection missing!")
            print("❌ DEBUG: Cannot set password!", flush=True)
            if not self.oauth_token:
                print("   ❌ OAuth token is None!", flush=True)
            if not hasattr(self, 'connection'):
                print("   ❌ Connection attribute missing!", flush=True)
            elif not self.connection:
                print("   ❌ Connection object is None!", flush=True)
        
        # NOW call parent _connect() - this will use the password we just set
        logger.info("🔌 Calling parent _connect() - handshake will use password above")
        print("🔌 DEBUG: Calling parent _connect() now...", flush=True)
        return super()._connect()

    def on_welcome(self, connection, event) -> None:
        """Called when bot connects to IRC."""
        logger.info("✅ Connected to Twitch IRC")
        print("✅ DEBUG: Connected to Twitch IRC - on_welcome called")
        print(f"✅ DEBUG: Event type: {event.type}, Event args: {event.arguments}")
        
        # Request IRC capabilities for Twitch tags (required for message metadata)
        try:
            connection.cap("REQ", "twitch.tv/membership")
            connection.cap("REQ", "twitch.tv/tags")
            connection.cap("REQ", "twitch.tv/commands")
            logger.info("📋 Requested Twitch IRC capabilities")
            print("📋 DEBUG: Requested Twitch IRC capabilities")
        except Exception as e:
            logger.warning(f"⚠️ Could not request IRC capabilities: {e}")
            print(f"⚠️ DEBUG: Could not request IRC capabilities: {e}")
        
        # Join channel
        logger.info(f"📺 Attempting to join channel: {self.channel}")
        print(f"📺 DEBUG: Attempting to join channel: {self.channel}")
        connection.join(self.channel)
        logger.info(f"📺 Join command sent for channel: {self.channel}")
        print(f"📺 DEBUG: Join command sent")
    
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
        
        # Log authentication failure details if available
        if hasattr(event, 'arguments') and event.arguments:
            error_msg = ' '.join(event.arguments) if isinstance(event.arguments, list) else str(event.arguments)
            if any(keyword in error_msg.lower() for keyword in ['authentication', 'password', 'login', 'invalid', 'bad']):
                logger.error(f"❌ AUTHENTICATION FAILURE DETECTED: {error_msg}")
                print(f"❌ DEBUG: AUTHENTICATION FAILURE: {error_msg}", flush=True)
                print(f"❌ DEBUG: OAuth token was: {self.oauth_token[:20] if self.oauth_token else 'MISSING'}...", flush=True)
        
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
        
        # Check for authentication-related errors
        error_str = f"{error_msg} {error_args}".lower()
        if any(keyword in error_str for keyword in ['authentication', 'password', 'login', 'invalid', 'bad', 'incorrect']):
            logger.error("❌ AUTHENTICATION ERROR DETECTED!")
            print("❌ DEBUG: This appears to be an AUTHENTICATION ERROR!", flush=True)
            print(f"❌ DEBUG: OAuth token was: {self.oauth_token[:20] if self.oauth_token else 'MISSING'}...", flush=True)
            print(f"❌ DEBUG: Check if OAuth token is valid and not expired", flush=True)
        
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
        # Only log important events to avoid spam
        if event.type in ['disconnect', 'error', 'welcome', 'join', 'privmsg', 'pubmsg']:
            logger.debug(f"📡 IRC Event: {event.type} - {getattr(event, 'arguments', '')}")
            if event.type in ['disconnect', 'error']:
                print(f"📡 DEBUG: IRC Event: {event.type} - {getattr(event, 'arguments', '')}")

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
                if asyncio.iscoroutinefunction(self.on_message):
                    asyncio.create_task(self.on_message(message_data))
                else:
                    self.on_message(message_data)
            except Exception as e:
                logger.error(f"Error in message handler: {e}", exc_info=True)

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




