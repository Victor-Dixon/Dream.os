#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery
Sends messages to agent chat input coordinates using PyAutoGUI

<!-- SSOT Domain: communication -->

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
from typing import Dict, List, Callable, Any, Optional, Union, Tuple, Set


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
        Validate coordinates before sending with comprehensive checks.

        Args:
            agent_id: Agent identifier
            coords: Coordinate tuple (x, y)

        Returns:
            True if coordinates are valid
        """
        if not coords or len(coords) != 2:
            logger.error(f"❌ Invalid coordinates for {agent_id}: {coords}")
            return False

        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"❌ Coordinates must be numeric for {agent_id}: ({x}, {y})")
            return False

        # Validate against bounds from cursor_agent_coords.json
        try:
            from .coordinate_loader import get_coordinate_loader
            coord_loader = get_coordinate_loader()
            
            # Get expected coordinates for this agent
            expected_chat_coords = coord_loader.get_chat_coordinates(agent_id)
            expected_onboarding_coords = coord_loader.get_onboarding_coordinates(agent_id)
            
            # Check if coords match expected (within tolerance for screen variations)
            coords_match = (
                coords == expected_chat_coords or 
                coords == expected_onboarding_coords or
                (abs(x - expected_chat_coords[0]) <= 5 and abs(y - expected_chat_coords[1]) <= 5) or
                (abs(x - expected_onboarding_coords[0]) <= 5 and abs(y - expected_onboarding_coords[1]) <= 5)
            )
            
            if not coords_match:
                logger.warning(
                    f"⚠️ Coordinate mismatch for {agent_id}: got {coords}, "
                    f"expected chat={expected_chat_coords} or onboarding={expected_onboarding_coords}"
                )
                # Don't fail - allow with warning (screen resolution differences)
            
            # Validate bounds from cursor_agent_coords.json validation_rules
            # Default bounds: min_x=-2000, max_x=2000, min_y=0, max_y=1500
            if x < -2000 or x > 2000:
                logger.error(f"❌ X coordinate out of bounds for {agent_id}: {x} (expected -2000 to 2000)")
                return False
            if y < 0 or y > 1500:
                logger.error(f"❌ Y coordinate out of bounds for {agent_id}: {y} (expected 0 to 1500)")
                return False
            
            logger.debug(f"✅ Coordinates validated for {agent_id}: {coords}")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not validate coordinates against SSOT: {e}, using basic validation")
            # Fallback to basic validation if SSOT check fails
            return True

    def send_message(self, message) -> bool:
        """
        Send message to agent chat input coordinates.
        
        RACE CONDITION FIXES:
        - Clipboard locking (prevents concurrent overwrites)
        - Increased delays (1.0s for slow systems)
        - 3-attempt retry mechanism
        
        CRITICAL FIX: Handles both dict and UnifiedMessage object formats.
        """
        # Extract recipient for logging (handles both dict and object)
        recipient = None
        if isinstance(message, dict):
            recipient = message.get('recipient') or message.get('to', 'UNKNOWN')
        elif hasattr(message, 'recipient'):
            recipient = message.recipient
        else:
            recipient = 'UNKNOWN'
        
        # RACE CONDITION FIX #3: Retry mechanism (3 attempts)
        for attempt in range(3):
            try:
                success = self._send_message_attempt(message, attempt + 1)
                if success:
                    return True
                
                # Wait before retry
                if attempt < 2:
                    logger.warning(f"⚠️ Retry {attempt + 1}/3 for {recipient}")
                    time.sleep(1.0)
            
            except Exception as e:
                logger.error(
                    f"❌ Attempt {attempt + 1} failed for {recipient}: {e}",
                    exc_info=True
                )
                if attempt < 2:
                    time.sleep(1.0)
        
        logger.error(
            f"❌ All 3 attempts failed for {recipient} - message not delivered",
            exc_info=False
        )
        return False
    
    def _send_message_attempt(self, message, attempt_num: int) -> bool:
        """Single message delivery attempt with all race condition fixes."""
        # CRITICAL FIX: Handle both dict and UnifiedMessage object formats
        # Queue messages are normalized to dicts, but delivery expects UnifiedMessage objects
        if isinstance(message, dict):
            # Convert dict to UnifiedMessage-like object for compatibility
            from .messaging_models_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
            
            # Extract recipient from dict (CRITICAL for routing)
            recipient = message.get('recipient') or message.get('to')
            if not recipient:
                logger.error(f"❌ Message dict missing recipient: {message.keys()}")
                return False
            
            # Convert message_type string to enum if needed
            message_type_str = message.get('message_type', 'text')
            if isinstance(message_type_str, str):
                try:
                    message_type = UnifiedMessageType(message_type_str)
                except (ValueError, AttributeError):
                    # Fallback to TEXT if invalid
                    message_type = UnifiedMessageType.TEXT
            else:
                message_type = message_type_str
            
            # Convert priority string to enum if needed
            priority_str = message.get('priority', 'regular')
            if isinstance(priority_str, str):
                try:
                    priority = UnifiedMessagePriority(priority_str)
                except (ValueError, AttributeError):
                    priority = UnifiedMessagePriority.REGULAR
            else:
                priority = priority_str
            
            # Convert tags list to enums if needed
            tags_list = message.get('tags', [])
            tags = []
            for tag in tags_list:
                if isinstance(tag, str):
                    try:
                        tags.append(UnifiedMessageTag(tag))
                    except (ValueError, AttributeError):
                        pass
                else:
                    tags.append(tag)
            
            # Extract category from metadata if present
            category = None
            metadata_dict = message.get('metadata', {})
            if isinstance(metadata_dict, dict):
                category_str = metadata_dict.get('message_category')
                if category_str:
                    try:
                        from .messaging_models_core import MessageCategory
                        category = MessageCategory(category_str.lower())
                    except (ValueError, AttributeError):
                        pass
            
            # Create UnifiedMessage object from dict
            message = UnifiedMessage(
                content=message.get('content', ''),
                sender=message.get('sender', 'CAPTAIN'),
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                tags=tags if tags else [UnifiedMessageTag.SYSTEM],
                metadata=metadata_dict,
                category=category if category else None  # Preserve category from metadata
            )
        
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
            # CRITICAL: Check if message already has a template header (e.g., [HEADER] S2A STALL RECOVERY, [HEADER] D2A DISCORD INTAKE)
            # Also check metadata for message_category to detect D2A/C2A/A2A/S2A templates
            # If it does, don't add another prefix - the template is already complete
            metadata = message.metadata if isinstance(message.metadata, dict) else {}
            message_category = metadata.get("message_category") or getattr(message, "category", None)
            
            # Log for debugging
            logger.info(f"🔍 Template detection for {message.recipient}: content_length={len(message.content)}, category={message_category}, content_preview={message.content[:100]}")
            
            # Check if content has template header (D2A, S2A, C2A, A2A templates all start with [HEADER])
            # CRITICAL: Check anywhere in content, not just start, because prefix may have been added
            content_has_template_header = (
                message.content.startswith("[HEADER]") or 
                "[HEADER]" in message.content or  # Check entire content for template headers
                "[HEADER] D2A" in message.content or
                "[HEADER] S2A" in message.content or
                "[HEADER] C2A" in message.content or
                "[HEADER] A2A" in message.content
            )
            
            # Also check if metadata indicates this is a templated message (D2A, C2A, A2A, S2A)
            # Handle both string values and MessageCategory enum values
            category_value = None
            if message_category:
                if isinstance(message_category, str):
                    category_value = message_category.lower()
                elif hasattr(message_category, 'value'):
                    category_value = message_category.value.lower()
                elif hasattr(message_category, 'name'):
                    category_value = message_category.name.lower()
            
            is_templated_message = (
                category_value in ["d2a", "c2a", "a2a", "s2a"] or
                content_has_template_header
            )
            
            logger.info(f"🔍 Template check result: has_header={content_has_template_header}, category={category_value}, is_templated={is_templated_message}")
            
            # #region agent log
            import json
            from pathlib import Path
            from datetime import datetime
            log_path = Path(r"d:\Agent_Cellphone_V2_Repository\.cursor\debug.log")
            try:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_pyautogui_before", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_pyautogui.py:575", "message": "PyAutoGUI before content selection", "data": {"is_templated": is_templated_message, "content_length": len(message.content), "content_preview": message.content[:200], "has_header": content_has_template_header}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "E"}) + "\n")
            except: pass
            # #endregion
            if is_templated_message:
                # Message already has template applied - use content as-is
                # CRITICAL: If content has prefix but also has template header, extract just the template part
                # This handles cases where format_c2a_message was called before template detection
                content_to_use = message.content
                
                # If content has both prefix AND template header, extract template part
                if "[HEADER]" in content_to_use and not content_to_use.startswith("[HEADER]"):
                    # Find where template actually starts
                    header_index = content_to_use.find("[HEADER]")
                    if header_index > 0:
                        # Extract template part (everything from [HEADER] onwards)
                        original_length = len(content_to_use)
                        content_to_use = content_to_use[header_index:]
                        logger.info(f"🔧 Extracted template content: removed {header_index} chars prefix, template length: {len(content_to_use)} (was {original_length})")
                
                # Don't add any prefix - template is complete as-is
                msg_content = content_to_use
                logger.info(f"✅ Using pre-rendered template content (category: {category_value}, has_header: {content_has_template_header}, final_length: {len(msg_content)})")
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_pyautogui_templated", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_pyautogui.py:592", "message": "PyAutoGUI using templated content", "data": {"msg_content_length": len(msg_content), "msg_content_preview": msg_content[:200]}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "E"}) + "\n")
                except: pass
                # #endregion
            else:
                # No template header - format with prefix
                logger.info(f"📝 No template detected - formatting with prefix (category: {category_value}, has_header: {content_has_template_header})")
                msg_content_before = message.content
                msg_content = format_c2a_message(
                    recipient=message.recipient,
                    content=message.content,
                    priority=message.priority.value,
                    sender=sender  # Pass sender for correct tagging
                )
                # #region agent log
                try:
                    with open(log_path, "a", encoding="utf-8") as f:
                        f.write(json.dumps({"id": f"log_{int(datetime.now().timestamp() * 1000)}_pyautogui_formatted", "timestamp": int(datetime.now().timestamp() * 1000), "location": "messaging_pyautogui.py:602", "message": "PyAutoGUI after format_c2a_message", "data": {"before_length": len(msg_content_before), "after_length": len(msg_content), "after_preview": msg_content[:200]}, "sessionId": "debug-session", "runId": "run1", "hypothesisId": "E"}) + "\n")
                except: pass
                # #endregion

            # Click agent chat input - ensure proper focus
            logger.debug(f"📍 Moving to coordinates: ({x}, {y})")
            self.pyautogui.moveTo(x, y, duration=0.5)
            
            # CRITICAL: Validate coordinates AFTER moveTo but BEFORE paste
            # This ensures we're at the correct location before attempting paste
            current_mouse_pos = self.pyautogui.position()
            coords_valid = self.validate_coordinates(message.recipient, (x, y))
            
            # Verify mouse actually moved to target coordinates (within tolerance)
            distance = ((current_mouse_pos[0] - x) ** 2 + (current_mouse_pos[1] - y) ** 2) ** 0.5
            if distance > 10:  # Allow 10px tolerance for screen variations
                logger.warning(
                    f"⚠️ Mouse position mismatch for {message.recipient}: "
                    f"expected ({x}, {y}), got {current_mouse_pos}, distance={distance:.1f}px"
                )
                # Retry moveTo if too far off
                self.pyautogui.moveTo(x, y, duration=0.3)
                time.sleep(0.2)
                current_mouse_pos = self.pyautogui.position()
                distance = ((current_mouse_pos[0] - x) ** 2 + (current_mouse_pos[1] - y) ** 2) ** 0.5
                if distance > 10:
                    logger.error(
                        f"❌ Failed to move to coordinates for {message.recipient}: "
                        f"expected ({x}, {y}), still at {current_mouse_pos}"
                    )
                    return False
            
            if not coords_valid:
                logger.error(f"❌ Coordinate validation failed for {message.recipient} at ({x}, {y})")
                return False
            
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

            # CRITICAL: Final coordinate validation RIGHT BEFORE paste
            # This is the last chance to catch coordinate issues before pasting
            final_mouse_pos = self.pyautogui.position()
            final_distance = ((final_mouse_pos[0] - x) ** 2 + (final_mouse_pos[1] - y) ** 2) ** 0.5
            if final_distance > 10:
                logger.error(
                    f"❌ CRITICAL: Mouse moved away before paste for {message.recipient}: "
                    f"expected ({x}, {y}), got {final_mouse_pos}"
                )
                # Re-position before paste
                self.pyautogui.moveTo(x, y, duration=0.2)
                time.sleep(0.2)
                self.pyautogui.click()  # Re-focus
                time.sleep(0.3)

            # RACE CONDITION FIX #1: Clipboard lock (prevents concurrent overwrites!)
            with _clipboard_lock:
                # Paste message (clipboard locked during this entire block!)
                logger.debug(f"📋 Copying message to clipboard: {msg_content[:50]}...")
                pyperclip.copy(msg_content)
                time.sleep(0.5)  # Wait for clipboard to be ready
                
                # CRITICAL: One final coordinate check before paste
                pre_paste_pos = self.pyautogui.position()
                if abs(pre_paste_pos[0] - x) > 10 or abs(pre_paste_pos[1] - y) > 10:
                    logger.error(
                        f"❌ CRITICAL: Mouse position invalid before paste for {message.recipient}: "
                        f"expected ({x}, {y}), got {pre_paste_pos}"
                    )
                    return False
                
                logger.debug("📥 Pasting message")
                self.pyautogui.hotkey("ctrl", "v")
                time.sleep(1.0)  # Wait for paste to complete
                
                # Verify paste worked by checking clipboard still matches
                # (This is a sanity check, not a guarantee)
                try:
                    clipboard_check = pyperclip.paste()
                    if clipboard_check == msg_content:
                        logger.debug("✅ Clipboard verified")
                    else:
                        logger.warning(
                            f"⚠️ Clipboard mismatch after paste for {message.recipient}: "
                            f"expected {len(msg_content)} chars, got {len(clipboard_check)} chars"
                        )
                except Exception:
                    pass  # Non-critical check

            # CRITICAL: Send message (use Ctrl+Enter for stalled flag, regular enter for all others)
            send_mode = None
            is_stalled = False
            if isinstance(message.metadata, dict):
                send_mode = message.metadata.get("send_mode")
                is_stalled = message.metadata.get("stalled", False)
            
            logger.debug(f"📤 Sending message (stalled={is_stalled}, send_mode={send_mode})")
            # Priority: explicit send_mode -> stalled flag -> default enter
            if send_mode == "ctrl_enter" or (send_mode is None and is_stalled):
                logger.debug("⚠️ Using Ctrl+Enter send")
                self.pyautogui.hotkey("ctrl", "enter")
            else:
                logger.debug("✅ Using Enter send")
                self.pyautogui.press("enter")
            time.sleep(1.0)  # Wait for message to be sent
            
            # CRITICAL: Verify message was sent and UI has settled
            # This ensures the full sequence completed before returning
            try:
                # #region agent log
                import json
                from pathlib import Path
                log_path = Path("d:\\Agent_Cellphone_V2_Repository\\.cursor\\debug.log")
                settlement_start = time.time()
                recipient = message.get('recipient') if isinstance(message, dict) else getattr(message, 'recipient', 'unknown')
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "D", "location": "messaging_pyautogui.py:744", "message": "Before UI settlement delay", "data": {"recipient": recipient, "delay_seconds": 3.0}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                # Additional delay to allow UI to fully process and coordinate validation to complete
                # Increased to 3.0s to prevent routing race conditions between agents
                time.sleep(3.0)  # Increased from 2.0s to 3.0s for routing stability
                # #region agent log
                settlement_end = time.time()
                actual_delay = settlement_end - settlement_start
                try:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps({"sessionId": "debug-session", "runId": "run1", "hypothesisId": "D", "location": "messaging_pyautogui.py:751", "message": "After UI settlement delay", "data": {"recipient": recipient, "expected_delay": 3.0, "actual_delay": round(actual_delay, 2)}, "timestamp": int(time.time() * 1000)}) + "\n")
                except: pass
                # #endregion
                
                # Verify mouse is still at correct coordinates (confirms UI is stable)
                final_verify_pos = self.pyautogui.position()
                verify_distance = ((final_verify_pos[0] - x) ** 2 + (final_verify_pos[1] - y) ** 2) ** 0.5
                if verify_distance > 20:  # Allow some movement tolerance
                    logger.warning(
                        f"⚠️ Mouse moved significantly after send for {message.recipient}: "
                        f"distance={verify_distance:.1f}px (may indicate UI interaction)"
                    )
                else:
                    logger.debug(f"✅ Mouse position stable after send (distance={verify_distance:.1f}px)")
                
                logger.debug("✅ Message send sequence completed and UI settled")
            except Exception as e:
                logger.warning(f"⚠️ Could not verify message send completion: {e}")

            logger.info(f"✅ Message sent to {message.recipient} at {coords} (attempt {attempt_num}) - UI settled")
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


def send_message_to_agent(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Alias for send_message_pyautogui for backward compatibility."""
    return send_message_pyautogui(agent_id, message, timeout)
