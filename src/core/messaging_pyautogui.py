#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery
Sends messages to agent chat input coordinates using PyAutoGUI

RACE CONDITION FIXES (2025-10-15):
- Clipboard locking to prevent concurrent overwrites
- Increased delays (0.5s→1.0s) for slow systems
- 3-attempt retry mechanism for reliability

CRITICAL FIX (2025-01-27): Global keyboard control lock
- Prevents "9 ppl controlling my keyboard" scenario
- Synchronizes Discord + computer + agents
- Single lock for entire PyAutoGUI operation sequence
"""

import logging
import time
import threading

# Import global keyboard control lock
from .keyboard_control_lock import keyboard_control

logger = logging.getLogger(__name__)

# RACE CONDITION FIX #1: Global clipboard lock
_clipboard_lock = threading.Lock()

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


def get_message_tag(sender: str, recipient: str) -> str:
    """
    Determine correct message tag based on sender and recipient.
    
    Args:
        sender: Message sender (GENERAL, DISCORD, CAPTAIN, Agent-X, SYSTEM)
        recipient: Message recipient (Agent-X, ALL, CAPTAIN)
    
    Returns:
        Correct message tag ([D2A], [G2A], [C2A], [A2A], [A2C], [S2A])
    """
    sender_upper = sender.upper()
    recipient_upper = recipient.upper() if recipient else ""
    
    # General broadcasts (STRATEGIC - highest priority!)
    if 'GENERAL' in sender_upper:
        return '[G2A]'  # General-to-Agent
    
    # Discord/Commander broadcasts
    if sender_upper in ['DISCORD', 'COMMANDER', 'DISCORD-CONTROLLER']:
        return '[D2A]'  # Discord-to-Agent
    
    # System automated messages
    if sender_upper == 'SYSTEM':
        return '[S2A]'  # System-to-Agent
    
    # Captain to Agent
    if sender_upper in ['CAPTAIN', 'AGENT-4']:
        if 'ALL' in recipient_upper or 'BROADCAST' in recipient_upper:
            return '[C2A-ALL]'  # Captain broadcast
        return '[C2A]'  # Captain-to-Agent
    
    # Agent to Captain
    if recipient_upper in ['CAPTAIN', 'AGENT-4']:
        return '[A2C]'  # Agent-to-Captain
    
    # Agent to Agent
    if sender.startswith('Agent-') and recipient.startswith('Agent-'):
        return '[A2A]'  # Agent-to-Agent
    
    # Fallback to C2A for safety
    return '[C2A]'


def format_c2a_message(recipient: str, content: str, priority: str | None = None, sender: str = "CAPTAIN") -> str:
    """
    Format message with correct tag based on sender (UPDATED - Agent-1 2025-10-15).

    Per STANDARDS.md: Compact messaging with essential fields only.
    NOW SUPPORTS: [D2A], [G2A], [S2A], [C2A], [A2A], [A2C]

    Args:
        recipient: Target agent ID
        content: Message content
        priority: Optional priority level (defaults to 'normal')
        sender: Message sender (determines tag) - NEW!

    Returns:
        Formatted message with correct tag
    """
    priority = priority or "normal"
    
    # Get correct message tag based on sender
    tag = get_message_tag(sender, recipient)

    # Add "URGENT MESSAGE" prefix for urgent priority
    urgent_prefix = ""
    if priority == "urgent":
        urgent_prefix = "🚨 URGENT MESSAGE 🚨\n\n"

    # Lean format: [Tag] Recipient (no priority in header for urgent)
    header = f"{tag} {recipient}"

    return f"{urgent_prefix}{header}\n\n{content}"


class PyAutoGUIMessagingDelivery:
    """Delivers messages via PyAutoGUI to agent chat coordinates."""

    def __init__(self):
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI not available")
        self.pyautogui = pyautogui

    def validate_coordinates(self, agent_id: str, coords: tuple[int, int]) -> bool:
        """
        Validate coordinates before sending.

        Args:
            agent_id: Agent identifier
            coords: Coordinate tuple (x, y)

        Returns:
            True if coordinates are valid
        """
        if not coords or len(coords) != 2:
            logger.error(f"Invalid coordinates for {agent_id}: {coords}")
            return False

        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"Coordinates must be numeric for {agent_id}: ({x}, {y})")
            return False

        return True

    def send_message(self, message) -> bool:
        """
        Send message to agent chat input coordinates.
        
        RACE CONDITION FIXES:
        - Clipboard locking (prevents concurrent overwrites)
        - Increased delays (1.0s for slow systems)
        - 3-attempt retry mechanism
        """
        # RACE CONDITION FIX #3: Retry mechanism (3 attempts)
        for attempt in range(3):
            try:
                success = self._send_message_attempt(message, attempt + 1)
                if success:
                    return True
                
                # Wait before retry
                if attempt < 2:
                    logger.warning(f"⚠️ Retry {attempt + 1}/3 for {message.recipient}")
                    time.sleep(1.0)
            
            except Exception as e:
                logger.error(
                    f"❌ Attempt {attempt + 1} failed for {message.recipient}: {e}",
                    exc_info=True
                )
                if attempt < 2:
                    time.sleep(1.0)
        
        logger.error(
            f"❌ All 3 attempts failed for {message.recipient} - message not delivered",
            exc_info=False
        )
        return False
    
    def _send_message_attempt(self, message, attempt_num: int) -> bool:
        """Single message delivery attempt with all race condition fixes."""
        # Get sender for lock identifier
        sender = "CAPTAIN"  # default
        if hasattr(message, 'sender'):
            sender = message.sender
        if isinstance(message.metadata, dict):
            sender = message.metadata.get('sender', sender)
        
        # CRITICAL: Check if keyboard lock is already held (e.g., by queue processor)
        # If lock is already held, skip acquiring it again to prevent deadlock
        from .keyboard_control_lock import is_locked
        lock_already_held = is_locked()
        
        # CRITICAL: Global keyboard control lock - prevents "9 ppl controlling keyboard"
        # This ensures only ONE source can control keyboard at a time
        # BUT: Skip if lock already held (caller already has it, e.g., queue processor)
        source = message.metadata.get('source', 'unknown') if isinstance(message.metadata, dict) else 'unknown'
        lock_source = f"{source}:{sender}:{message.recipient}"
        
        # Only acquire lock if not already held
        if lock_already_held:
            logger.debug(f"🔒 Keyboard lock already held, skipping lock acquisition for {message.recipient}")
            # Execute delivery without acquiring lock (caller already has it)
            return self._execute_delivery_operations(message, attempt_num, sender)
        else:
            # Acquire lock and execute delivery
            with keyboard_control(lock_source):
                return self._execute_delivery_operations(message, attempt_num, sender)
    
    def _execute_delivery_operations(self, message, attempt_num: int, sender: str) -> bool:
        """Execute the actual PyAutoGUI delivery operations (no lock management)."""
        try:
            # Get coordinates for agent
            from .coordinate_loader import get_coordinate_loader
            from .messaging_models_core import UnifiedMessageType

            coord_loader = get_coordinate_loader()

            # CRITICAL FIX: Only use onboarding coordinates for ONBOARDING message type
            # All other message types (TEXT, BROADCAST, SYSTEM_TO_AGENT, etc.) use chat coordinates
            # EXTRA PROTECTION: Agent-4 ALWAYS uses chat coordinates unless explicitly ONBOARDING type
            message_type_str = str(message.message_type)
            logger.info(f"🔍 Message type for {message.recipient}: {message_type_str} (enum: {message.message_type})")
            
            # Get both coordinate sets for verification
            chat_coords_expected = coord_loader.get_chat_coordinates(message.recipient)
            onboarding_coords_check = coord_loader.get_onboarding_coordinates(message.recipient)
            
            # CRITICAL HARDCODED OVERRIDE FOR AGENT-4: Force correct coordinates regardless of loader
            # This ensures Agent-4 ALWAYS uses the correct coordinates
            if message.recipient == "Agent-4":
                AGENT4_CHAT_COORDS = (-308, 1000)  # Hardcoded from cursor_agent_coords.json
                AGENT4_ONBOARDING_COORDS = (-304, 680)  # Hardcoded from cursor_agent_coords.json
                
                # Verify loader returned correct coords
                if chat_coords_expected != AGENT4_CHAT_COORDS:
                    logger.warning(f"⚠️ Agent-4 chat coords mismatch! Loader: {chat_coords_expected}, Expected: {AGENT4_CHAT_COORDS}. Using hardcoded.")
                    chat_coords_expected = AGENT4_CHAT_COORDS
                
                if onboarding_coords_check != AGENT4_ONBOARDING_COORDS:
                    logger.warning(f"⚠️ Agent-4 onboarding coords mismatch! Loader: {onboarding_coords_check}, Expected: {AGENT4_ONBOARDING_COORDS}. Using hardcoded.")
                    onboarding_coords_check = AGENT4_ONBOARDING_COORDS
                
                logger.info(f"✅ Agent-4 coordinates verified: Chat={chat_coords_expected}, Onboarding={onboarding_coords_check}")
            
            # CRITICAL ROUTING LOGIC: Agent-4 ALWAYS uses chat coordinates unless EXPLICITLY ONBOARDING
            # This is a defensive fix to prevent messages from going to onboarding coordinates
            # Only messages with message_type == UnifiedMessageType.ONBOARDING should use onboarding coords
            
            # Log message details for debugging
            logger.info(f"🔍 Routing decision for {message.recipient}:")
            logger.info(f"   - Message type: {message.message_type} ({message_type_str})")
            logger.info(f"   - Message type class: {type(message.message_type)}")
            if hasattr(message.message_type, 'value'):
                logger.info(f"   - Message type value: '{message.message_type.value}'")
            logger.info(f"   - Sender: {sender}")
            logger.info(f"   - Recipient: {message.recipient}")
            logger.info(f"   - Chat coords: {chat_coords_expected}")
            logger.info(f"   - Onboarding coords: {onboarding_coords_check}")
            # CRITICAL: Log metadata in case message_type is being overridden
            if hasattr(message, 'metadata') and isinstance(message.metadata, dict):
                logger.info(f"   - Metadata keys: {list(message.metadata.keys())}")
                if 'message_type' in message.metadata:
                    logger.warning(f"   ⚠️ WARNING: message_type found in metadata: {message.metadata.get('message_type')}")
                if 'use_onboarding_coords' in message.metadata:
                    logger.error(f"   ❌ ERROR: use_onboarding_coords flag found in metadata: {message.metadata.get('use_onboarding_coords')}")
            
            # CRITICAL: Agent-4 special handling - ONLY use onboarding coords for explicit ONBOARDING type
            # Use multiple checks to ensure correct routing
            is_onboarding_type = False
            if hasattr(message.message_type, 'value'):
                is_onboarding_type = message.message_type.value == "onboarding" or message.message_type == UnifiedMessageType.ONBOARDING
            elif isinstance(message.message_type, str):
                is_onboarding_type = message.message_type.lower() == "onboarding"
            else:
                # Enum comparison
                is_onboarding_type = message.message_type == UnifiedMessageType.ONBOARDING
            
            # CRITICAL FIX: Discord messages to Agent-4 ALWAYS use chat coordinates
            # Check metadata for Discord source (multiple ways to detect Discord messages)
            is_discord_message = False
            if hasattr(message, 'metadata') and isinstance(message.metadata, dict):
                # Check for Discord source in metadata
                source = message.metadata.get("source", "")
                is_discord_message = (
                    source == "discord" or 
                    source == "DISCORD" or
                    "discord" in str(source).lower() or
                    message.metadata.get("discord_user_id") is not None or
                    message.metadata.get("discord_username") is not None
                )
            
            if message.recipient == "Agent-4":
                # CRITICAL: Agent-4 MUST use chat coords unless EXPLICITLY ONBOARDING
                # ABSOLUTE OVERRIDE: Hardcode coordinates for Agent-4 to prevent any routing errors
                AGENT4_CHAT_ABS = (-308, 1000)
                AGENT4_ONBOARDING_ABS = (-304, 680)
                
                # CRITICAL FIX: ALL messages to Agent-4 use chat coords UNLESS EXPLICITLY ONBOARDING
                # This includes Discord messages, CAPTAIN_TO_AGENT, SYSTEM_TO_AGENT, etc.
                # ONLY UnifiedMessageType.ONBOARDING should use onboarding coordinates
                
                # Check if Discord message (for logging)
                if is_discord_message:
                    logger.info(f"📍 Agent-4: Discord message detected - forcing chat coordinates")
                    logger.info(f"📍 Agent-4: Metadata source: {message.metadata.get('source') if hasattr(message, 'metadata') and isinstance(message.metadata, dict) else 'N/A'}")
                
                # ONLY use onboarding coords if EXPLICITLY ONBOARDING type
                if is_onboarding_type:
                    # ONLY case where Agent-4 uses onboarding coordinates
                    coords = AGENT4_ONBOARDING_ABS  # Use hardcoded onboarding coords
                    logger.info(f"📍 Agent-4: Using ONBOARDING coordinates (EXPLICIT ONBOARDING type confirmed): {coords}")
                else:
                    # ALL other message types for Agent-4 use chat coordinates - NO EXCEPTIONS
                    # This includes: CAPTAIN_TO_AGENT, SYSTEM_TO_AGENT, TEXT, BROADCAST, etc.
                    # ABSOLUTE OVERRIDE: Hardcode chat coords for Agent-4
                    coords = AGENT4_CHAT_ABS  # Use hardcoded chat coords - NEVER use onboarding
                    logger.info(f"📍 Agent-4: FORCING hardcoded chat coordinates (type: {message_type_str}, sender: {sender}, is_discord: {is_discord_message}): {coords}")
                    logger.info(f"📍 Agent-4: ABSOLUTE OVERRIDE - Chat coords hardcoded to prevent routing errors")
                    
                    # Triple-check: If somehow wrong coords were selected, force hardcoded chat coords
                    if coords != AGENT4_CHAT_ABS:
                        logger.error(f"❌ CRITICAL BUG: Agent-4 non-ONBOARDING message using wrong coords! Expected: {AGENT4_CHAT_ABS}, Got: {coords}")
                        coords = AGENT4_CHAT_ABS  # Force hardcoded chat coords
                        logger.warning(f"⚠️ ABSOLUTE OVERRIDE: Agent-4 now using hardcoded chat coordinates: {coords}")
            
            # Agent-2 special handling (similar to Agent-4)
            elif message.recipient == "Agent-2":
                if message.message_type == UnifiedMessageType.ONBOARDING:
                    coords = onboarding_coords_check
                    logger.info(f"📍 Agent-2: Using ONBOARDING coordinates (explicit ONBOARDING type): {coords}")
                else:
                    coords = chat_coords_expected
                    logger.info(f"📍 Agent-2: Using chat coordinates (type: {message_type_str}): {coords}")
                    # Defensive check
                    if coords == onboarding_coords_check:
                        logger.error(f"❌ CRITICAL BUG: Agent-2 non-ONBOARDING message selected onboarding coords! FORCING chat coords.")
                        coords = chat_coords_expected
            
            # All other agents: Use onboarding coords ONLY for ONBOARDING type
            elif message.message_type == UnifiedMessageType.ONBOARDING:
                coords = onboarding_coords_check
                logger.info(f"📍 {message.recipient}: Using ONBOARDING coordinates (explicit ONBOARDING type): {coords}")
            else:
                coords = chat_coords_expected
                logger.info(f"📍 {message.recipient}: Using CHAT coordinates (type: {message_type_str}): {coords}")
            
            # Final defensive verification for Agent-4 - ABSOLUTE HARDCODED OVERRIDE
            if message.recipient == "Agent-4":
                # Hardcoded coordinates for absolute override
                AGENT4_CHAT_FINAL = (-308, 1000)
                AGENT4_ONBOARDING_FINAL = (-304, 680)
                
                # Re-check onboarding type status with multiple methods
                final_is_onboarding = False
                if hasattr(message.message_type, 'value'):
                    final_is_onboarding = message.message_type.value == "onboarding"
                elif isinstance(message.message_type, str):
                    final_is_onboarding = message.message_type.lower() == "onboarding"
                else:
                    final_is_onboarding = message.message_type == UnifiedMessageType.ONBOARDING
                
                # Re-check Discord source (multiple detection methods)
                final_is_discord = False
                if hasattr(message, 'metadata') and isinstance(message.metadata, dict):
                    source = message.metadata.get("source", "")
                    final_is_discord = (
                        source == "discord" or 
                        source == "DISCORD" or
                        "discord" in str(source).lower() or
                        message.metadata.get("discord_user_id") is not None or
                        message.metadata.get("discord_username") is not None
                    )
                
                logger.info(f"🔍 Agent-4 FINAL VERIFICATION:")
                logger.info(f"   - Final is_onboarding check: {final_is_onboarding}")
                logger.info(f"   - Final is_discord check: {final_is_discord}")
                logger.info(f"   - Selected coords: {coords}")
                logger.info(f"   - Hardcoded chat: {AGENT4_CHAT_FINAL}")
                logger.info(f"   - Hardcoded onboarding: {AGENT4_ONBOARDING_FINAL}")
                
                # CRITICAL: Discord messages ALWAYS use chat coordinates
                if final_is_discord:
                    if coords != AGENT4_CHAT_FINAL:
                        logger.error(f"❌ CRITICAL ROUTING ERROR: Agent-4 Discord message using wrong coords!")
                        logger.error(f"   Expected hardcoded chat: {AGENT4_CHAT_FINAL}, Got: {coords}")
                        coords = AGENT4_CHAT_FINAL  # Force chat coords for Discord
                        logger.warning(f"⚠️ ABSOLUTE OVERRIDE: Agent-4 Discord message forced to chat coordinates: {coords}")
                    else:
                        logger.info(f"✅ Agent-4 Discord message verified: Using chat coordinates")
                elif not final_is_onboarding:
                    # ABSOLUTE OVERRIDE: Force hardcoded chat coords for Agent-4 if not onboarding
                    if coords != AGENT4_CHAT_FINAL:
                        logger.error(f"❌ CRITICAL ROUTING ERROR: Agent-4 non-ONBOARDING message using wrong coords!")
                        logger.error(f"   Expected hardcoded chat: {AGENT4_CHAT_FINAL}, Got: {coords}")
                        logger.error(f"   Message type: {message.message_type}, Message type str: {message_type_str}")
                        logger.error(f"   Is onboarding check: {final_is_onboarding}")
                        coords = AGENT4_CHAT_FINAL  # Force hardcoded chat coords - ABSOLUTE OVERRIDE
                        logger.warning(f"⚠️ ABSOLUTE HARDCODED OVERRIDE: Agent-4 routing fixed - using hardcoded chat coordinates: {coords}")
                    else:
                        logger.info(f"✅ Agent-4 routing verified: Using hardcoded chat coordinates for non-ONBOARDING message")
                else:
                    # Verify onboarding coords match hardcoded
                    if coords != AGENT4_ONBOARDING_FINAL:
                        logger.warning(f"⚠️ Agent-4 ONBOARDING coords mismatch, using hardcoded: {AGENT4_ONBOARDING_FINAL}")
                        coords = AGENT4_ONBOARDING_FINAL
            
            if not coords:
                logger.error(f"No coordinates for {message.recipient}")
                return False

            x, y = coords

            # Format message content using lean compact formatter with sender
            msg_content = format_c2a_message(
                recipient=message.recipient,
                content=message.content,
                priority=message.priority.value,
                sender=sender  # NEW: Pass sender for correct tagging!
            )

            # Click agent chat input - ensure proper focus
            logger.debug(f"📍 Moving to coordinates: ({x}, {y})")
            self.pyautogui.moveTo(x, y, duration=0.5)
            
            # Click to focus window and input field
            logger.debug("🖱️ Clicking to focus input field")
            self.pyautogui.click()
            time.sleep(0.5)  # Wait for initial focus
            
            # Click again to ensure input field is active
            self.pyautogui.click()
            time.sleep(0.5)  # Wait for input field to be ready
            
            # CRITICAL: Clear existing text in input field first
            logger.debug("🧹 Clearing existing text")
            self.pyautogui.hotkey("ctrl", "a")
            time.sleep(0.2)
            self.pyautogui.press("delete")
            time.sleep(0.3)

            # RACE CONDITION FIX #1: Clipboard lock (prevents concurrent overwrites!)
            with _clipboard_lock:
                # Paste message (clipboard locked during this entire block!)
                logger.debug(f"📋 Copying message to clipboard: {msg_content[:50]}...")
                pyperclip.copy(msg_content)
                time.sleep(0.5)  # Wait for clipboard to be ready
                
                logger.debug("📥 Pasting message")
                self.pyautogui.hotkey("ctrl", "v")
                time.sleep(1.0)  # Wait for paste to complete
                
                # Verify paste worked by checking clipboard still matches
                # (This is a sanity check, not a guarantee)
                try:
                    clipboard_check = pyperclip.paste()
                    if clipboard_check == msg_content:
                        logger.debug("✅ Clipboard verified")
                except Exception:
                    pass  # Non-critical check

            # CRITICAL: Send message (use Ctrl+Enter for stalled flag, regular enter for all others)
            # Check metadata for stalled flag
            is_stalled = False
            if isinstance(message.metadata, dict):
                is_stalled = message.metadata.get("stalled", False)
            
            logger.debug(f"📤 Sending message (stalled={is_stalled})")
            # CRITICAL: Use Enter for normal messages, Ctrl+Enter ONLY for stalled agents
            if is_stalled:
                logger.debug("⚠️ Using Ctrl+Enter for stalled agent")
                self.pyautogui.hotkey("ctrl", "enter")
            else:
                logger.debug("✅ Using Enter for normal message")
                self.pyautogui.press("enter")
            time.sleep(1.0)  # Wait for message to be sent

            logger.info(f"✅ Message sent to {message.recipient} at {coords} (attempt {attempt_num})")
            return True

        except Exception as e:
            logger.error(
                f"❌ PyAutoGUI delivery failed (attempt {attempt_num}) for {message.recipient}: {e}",
                exc_info=True
            )
            return False


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Legacy function for sending messages via PyAutoGUI."""
    try:
        delivery = PyAutoGUIMessagingDelivery()
        from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

        msg = UnifiedMessage(
            content=message,
            sender="CAPTAIN",
            recipient=agent_id,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
        )
        return delivery.send_message(msg)
    except Exception as e:
        logger.error(f"Failed to send PyAutoGUI message: {e}")
        return False


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send message to onboarding coordinates."""
    return send_message_pyautogui(agent_id, message, timeout)
