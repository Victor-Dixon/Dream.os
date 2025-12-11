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


# Custom exception classes for better error handling
class TwitchBridgeError(Exception):
    """Base exception for Twitch bridge errors."""
    pass


class TwitchAuthError(TwitchBridgeError):
    """Authentication-related errors."""
    pass


class TwitchConnectionError(TwitchBridgeError):
    """Connection-related errors."""
    pass


class TwitchMessageError(TwitchBridgeError):
    """Message sending/receiving errors."""
    pass


class TwitchReconnectError(TwitchBridgeError):
    """Reconnection errors."""
    pass


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
        
        # Reconnect state management (persistent across bot instances)
        self._stop_event = threading.Event()
        self._reconnect_attempt = 0
        self._reconnect_thread = None

    @staticmethod
    def _mask_token(tok: str) -> str:
        """
        Mask OAuth token for safe logging.
        
        Args:
            tok: OAuth token string
            
        Returns:
            Masked token string (first 10 chars + ... + last 4 chars)
        """
        if not tok:
            return ""
        if len(tok) <= 14:
            return "***"
        return tok[:10] + "..." + tok[-4:]

    async def connect(self) -> bool:
        """
        Connect to Twitch IRC with automatic reconnection loop.

        Returns:
            True if connection thread started successfully
        """
        try:
            logger.info(f"🔌 Connecting to Twitch IRC as {self.username}")
            logger.info(f"🔐 Using OAuth token: {self._mask_token(self.oauth_token)}")
            logger.info(f"📺 Channel: {self.channel}")

            # Clear stop event
            self._stop_event.clear()
            self.running = True
            
            # Start single reconnect loop in separate thread
            if self._reconnect_thread is None or not self._reconnect_thread.is_alive():
                self._reconnect_thread = threading.Thread(
                    target=self._run_reconnect_loop,
                    daemon=True,
                    name="TwitchIRCReconnectLoop"
                )
                self._reconnect_thread.start()
            
            # Wait a moment for initial connection attempt
            await asyncio.sleep(2)
            
            logger.info(f"🔄 Twitch bot reconnect loop started")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to start Twitch connection: {e}", exc_info=True)
            self.running = False
            return False

    def _run_reconnect_loop(self) -> None:
        """
        Single persistent reconnect loop.
        
        Manages one bot instance at a time with exponential backoff.
        Backoff state persists across bot instances.
        """
        import time
        import irc.client
        
        while not self._stop_event.is_set():
            try:
                self._reconnect_attempt += 1
                
                logger.info(f"🔌 IRC connect attempt {self._reconnect_attempt}")
                print(f"🔌 DEBUG: IRC connect attempt {self._reconnect_attempt}", flush=True)
                
                # Create new bot instance
                self.bot = TwitchIRCBot(
                    server_list=[("irc.chat.twitch.tv", 6667)],
                    nickname=self.username,
                    realname=self.username,
                    channel=self.channel,
                    on_message=self._handle_message,
                    bridge_instance=self,
                    oauth_token=self.oauth_token,
                )
                
                # Start bot (blocks until disconnect or reactor stops)
                logger.info("🔄 Starting IRC bot...")
                print("🔄 DEBUG: Starting IRC bot...", flush=True)
                
                try:
                    # Start bot - this blocks until reactor stops
                    self.bot.start()
                    logger.warning("⚠️ bot.start() returned (reactor stopped)")
                except Exception as e:
                    logger.error(f"❌ Error in bot.start(): {e}", exc_info=True)
                finally:
                    # Stop reactor explicitly to ensure cleanup
                    try:
                        reactor = irc.client.IRC().reactor
                        if reactor.is_alive():
                            reactor.disconnect_all()
                    except Exception:
                        pass
                
                # Calculate exponential backoff (persistent across attempts)
                # Cap at 120s, max exponent of 6 (2^6 = 64s)
                backoff = min(120, 2 ** min(self._reconnect_attempt, 6))
                
                logger.warning(
                    f"⚠️ IRC disconnected. "
                    f"Reconnecting in {backoff}s... (attempt {self._reconnect_attempt})"
                )
                print(f"⚠️ DEBUG: Reconnecting in {backoff}s... (attempt {self._reconnect_attempt})", flush=True)
                
                # Reset connection state
                self.connected = False
                self.bot = None
                
                # Wait with backoff (check stop event periodically)
                for _ in range(int(backoff)):
                    if self._stop_event.is_set():
                        logger.info("🛑 Stop requested - aborting reconnect")
                        return
                    time.sleep(1)
                
                # Continue loop for next attempt
                
            except KeyboardInterrupt:
                logger.info("🛑 Reconnect loop stopped by user")
                break
                
            except Exception as e:
                logger.exception(f"❌ Reconnect loop error: {e}")
                # Calculate exponential backoff
                backoff = min(120, 2 ** min(self._reconnect_attempt, 6))
                logger.warning(f"⚠️ Error in reconnect loop. Retrying in {backoff}s...")
                
                # Reset connection state
                self.connected = False
                self.bot = None
                
                # Wait with backoff
                for _ in range(int(backoff)):
                    if self._stop_event.is_set():
                        return
                    time.sleep(1)

    def _handle_message(self, message_data: dict) -> None:
        """
        Handle incoming chat message.

        Args:
            message_data: Message data dictionary
        """
        if not self.on_message:
            return
        
        try:
            # Validate message data structure
            if not isinstance(message_data, dict):
                logger.warning(f"⚠️ Invalid message data type: {type(message_data)}")
                return
            
            if not message_data.get("message") or not message_data.get("username"):
                logger.warning(f"⚠️ Invalid message data structure: missing required fields")
                return
            
            # Handle async or sync callbacks
            if asyncio.iscoroutinefunction(self.on_message):
                try:
                    asyncio.create_task(self.on_message(message_data))
                except RuntimeError as e:
                    # Event loop not running - create new one or use sync fallback
                    logger.warning(f"⚠️ Event loop not available, using sync fallback: {e}")
                    # Try to get or create event loop
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_closed():
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        loop.run_until_complete(self.on_message(message_data))
                    except Exception as loop_error:
                        logger.error(f"❌ Failed to handle async callback: {loop_error}", exc_info=True)
            else:
                self.on_message(message_data)
                
        except TypeError as e:
            logger.error(f"❌ Type error in message callback: {e}", exc_info=True)
        except ValueError as e:
            logger.error(f"❌ Value error in message callback: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"❌ Unexpected error in message callback: {e}", exc_info=True)

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
        """Stop Twitch connection and reconnect loop."""
        self.running = False
        self._has_sent_online_message = False
        
        # Signal stop to reconnect loop
        self._stop_event.set()
        
        # Stop current bot instance
        if self.bot:
            try:
                if hasattr(self.bot, 'stop'):
                    self.bot.stop()
                if hasattr(self.bot, 'connection') and self.bot.connection:
                    self.bot.connection.quit("Agent system shutdown")
                logger.info("🔌 Disconnected from Twitch")
            except Exception:
                pass
        
        # Wait for reconnect thread to finish (with timeout)
        if self._reconnect_thread and self._reconnect_thread.is_alive():
            self._reconnect_thread.join(timeout=2.0)


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
        self.oauth_token = oauth_token
        
        # Call parent WITHOUT password in connect_params
        # We'll set password in _connect() to avoid "multiple values" error
        super().__init__(server_list, nickname, realname)
        
        self.channel = channel
        self.on_message = on_message
        self.bridge_instance = bridge_instance
        
        # Set password on connection after parent __init__ creates it
        # This will be used in _connect() when handshake begins
        if self.oauth_token and hasattr(self, 'connection') and self.connection:
            try:
                self.connection.password = self.oauth_token
                masked = self._mask_token(self.oauth_token)
                logger.info(f"🔐 Set OAuth token on connection (in __init__): {masked}")
            except Exception as e:
                logger.error(f"❌ Failed to set password: {e}", exc_info=True)
    
    @staticmethod
    def _mask_token(tok: str) -> str:
        """
        Mask OAuth token for safe logging.
        
        Args:
            tok: OAuth token string
            
        Returns:
            Masked token string (first 10 chars + ... + last 4 chars)
        """
        if not tok:
            return ""
        if len(tok) <= 14:
            return "***"
        return tok[:10] + "..." + tok[-4:]
    
    def _connect(self):
        """
        Override connection method to ensure password is set BEFORE connecting.
        
        CRITICAL: Password must be set BEFORE super()._connect() is called,
        because that's when the IRC handshake (PASS/NICK/USER) begins.
        """
        # CRITICAL: Ensure password is set BEFORE calling parent _connect()
        if self.oauth_token and hasattr(self, 'connection') and self.connection:
            try:
                # Double-check password is set (in case it was cleared)
                if not getattr(self.connection, 'password', None):
                    self.connection.password = self.oauth_token
                    masked = self._mask_token(self.oauth_token)
                    logger.info(f"🔐 Set OAuth token BEFORE connection (in _connect): {masked}")
                    print(f"🔐 DEBUG: Set OAuth token BEFORE _connect(): {masked}", flush=True)
                else:
                    logger.info("🔐 Password already set on connection")
                    masked = self._mask_token(getattr(self.connection, 'password', 'NOT SET'))
                    print(f"🔐 DEBUG: Password already set: {masked}", flush=True)
            except Exception as e:
                logger.error(f"❌ CRITICAL: Failed to set password before _connect: {e}", exc_info=True)
                print(f"❌ DEBUG: Failed to set password: {e}", flush=True)
        
        # Call parent _connect() - it will use the password we just set
        logger.info("🔌 Calling parent _connect() - password set above")
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
    
    def on_ping(self, connection, event) -> None:
        """
        Handle PING messages from Twitch IRC server.
        
        CRITICAL: Twitch sends PING every ~5 minutes. If we don't respond with PONG,
        the connection will be closed with "Connection reset by peer".
        """
        logger.debug("🏓 Received PING from Twitch IRC server")
        print("🏓 DEBUG: Received PING - responding with PONG", flush=True)
        
        # Respond with PONG (required to keep connection alive)
        # PING format: PING :server_name
        # PONG format: PONG :server_name
        try:
            # Extract server name from event arguments or target
            server_name = ""
            if hasattr(event, 'arguments') and event.arguments:
                server_name = event.arguments[0] if len(event.arguments) > 0 else ""
            elif hasattr(event, 'target') and event.target:
                server_name = event.target
            else:
                # Default Twitch server name
                server_name = "tmi.twitch.tv"
            
            # Send PONG response
            connection.pong(server_name)
            logger.debug(f"🏓 Sent PONG response to {server_name}")
            print(f"🏓 DEBUG: PONG sent successfully to {server_name}", flush=True)
        except Exception as e:
            logger.error(f"❌ Failed to send PONG: {e}", exc_info=True)
            print(f"❌ DEBUG: Failed to send PONG: {e}", flush=True)
    
    def on_cap(self, connection, event) -> None:
        """
        Handle CAP (capabilities) responses from Twitch IRC server.
        
        Twitch responds to CAP REQ with ACK (acknowledged) or NAK (not acknowledged).
        We should acknowledge the ACK before proceeding.
        """
        if len(event.arguments) >= 2:
            cap_cmd = event.arguments[0]  # ACK or NAK
            cap_name = event.arguments[1] if len(event.arguments) > 1 else ""
            
            logger.info(f"📋 CAP response: {cap_cmd} {cap_name}")
            print(f"📋 DEBUG: CAP {cap_cmd} {cap_name}", flush=True)
            
            if cap_cmd == "ACK":
                logger.info(f"✅ Capability acknowledged: {cap_name}")
                print(f"✅ DEBUG: Capability {cap_name} acknowledged", flush=True)
            elif cap_cmd == "NAK":
                logger.warning(f"⚠️ Capability not acknowledged: {cap_name}")
                print(f"⚠️ DEBUG: Capability {cap_name} NOT acknowledged", flush=True)
    
    def on_nicknameinuse(self, connection, event) -> None:
        """Called when nickname is already in use."""
        logger.error("❌ Nickname already in use!")
        print("❌ DEBUG: Nickname already in use!")
    
    def on_disconnect(self, connection, event) -> None:
        """Called when disconnected from IRC."""
        import irc.client
        
        args = getattr(event, 'arguments', [])
        error_msg = ' '.join(args) if isinstance(args, list) else str(args)
        
        logger.warning(f"⚠️ Disconnected from Twitch IRC: {error_msg}")
        print(f"⚠️ DEBUG: Disconnected from Twitch IRC: {error_msg}", flush=True)
        
        # Log authentication failure details if available
        if args:
            if any(keyword in error_msg.lower() for keyword in ['authentication', 'password', 'login', 'invalid', 'bad', 'incorrect']):
                masked = self._mask_token(self.oauth_token) if self.oauth_token else 'MISSING'
                logger.error(f"❌ AUTHENTICATION FAILURE DETECTED: {error_msg}")
                logger.error(f"❌ OAuth token: {masked}")
                logger.error("❌ Possible causes:")
                logger.error("   1. Token is for a different user than nickname")
                logger.error("   2. Token is expired or invalid")
                logger.error("   3. Token is an app token (needs user token)")
                logger.error("   4. Token missing chat:read or chat:edit scopes")
                print(f"❌ DEBUG: AUTHENTICATION FAILURE: {error_msg}", flush=True)
                print(f"❌ DEBUG: OAuth token: {masked}", flush=True)
        
        # Update bridge state (bridge loop handles reconnection)
        if self.bridge_instance:
            self.bridge_instance.connected = False
        
        # Stop reactor to allow reconnect loop to continue
        # This ensures bot.start() returns so the reconnect loop can create a new bot
        try:
            import time as time_module
            reactor = connection.reactor if hasattr(connection, 'reactor') else None
            if reactor and hasattr(reactor, 'disconnect_all'):
                # Schedule reactor stop (don't block here)
                def stop_reactor():
                    time_module.sleep(0.5)  # Brief delay to let disconnect complete
                    try:
                        reactor.disconnect_all()
                    except Exception:
                        pass
                threading.Thread(target=stop_reactor, daemon=True).start()
        except Exception as e:
            logger.debug(f"Could not stop reactor: {e}")
    
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
        if any(keyword in error_str for keyword in ['authentication', 'password', 'login', 'invalid', 'bad', 'incorrect', 'unauthorized']):
            masked = self._mask_token(self.oauth_token) if self.oauth_token else 'MISSING'
            logger.error("❌ AUTHENTICATION ERROR DETECTED!")
            logger.error(f"❌ OAuth token: {masked}")
            logger.error("❌ Possible causes:")
            logger.error("   1. Token is for a different user than nickname")
            logger.error("   2. Token is expired or invalid")
            logger.error("   3. Token is an app token (needs user token)")
            logger.error("   4. Token missing chat:read or chat:edit scopes")
            print("❌ DEBUG: This appears to be an AUTHENTICATION ERROR!", flush=True)
            print(f"❌ DEBUG: OAuth token: {masked}", flush=True)
        
        if self.bridge_instance:
            self.bridge_instance.connected = False
    
    def stop(self) -> None:
        """Stop the bot and prevent reconnection."""
        self._stop_event.set()
        self._reconnecting = False
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.disconnect()
        except Exception:
            pass
    
    def on_notice(self, connection, event) -> None:
        """Called on IRC NOTICE messages - Twitch uses these for auth errors."""
        notice_msg = event.arguments[0] if event.arguments else str(event)
        logger.warning(f"📢 IRC Notice: {notice_msg}")
        print(f"📢 DEBUG: IRC Notice: {notice_msg}", flush=True)
        
        # Twitch sends authentication errors as NOTICE messages
        if any(keyword in notice_msg.lower() for keyword in ['login', 'authentication', 'password', 'invalid', 'unauthorized', 'error']):
            masked = self._mask_token(self.oauth_token) if self.oauth_token else 'MISSING'
            logger.error(f"❌ AUTHENTICATION ERROR from Twitch: {notice_msg}")
            logger.error(f"❌ OAuth token: {masked}")
            logger.error("❌ Possible causes:")
            logger.error("   1. Token is for a different user than nickname")
            logger.error("   2. Token is expired or invalid")
            logger.error("   3. Token is an app token (needs user token)")
            logger.error("   4. Token missing chat:read or chat:edit scopes")
            print(f"❌ DEBUG: AUTHENTICATION ERROR: {notice_msg}", flush=True)
            print(f"❌ DEBUG: OAuth token: {masked}", flush=True)
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
        
        # Reset reconnect attempts on successful connection (bridge handles this)
        if self.bridge_instance:
            # Reset attempt counter on successful connection
            self.bridge_instance._reconnect_attempt = 0
            self.bridge_instance.connected = True
            logger.info("✅ Connection fully established - ready to send messages")
            logger.info(f"✅ Reconnect attempts reset to 0")
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




