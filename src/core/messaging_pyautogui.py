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

# Import service modules (Phase 2A refactoring)
from .messaging_coordinate_routing import CoordinateRoutingService
from .messaging_formatting import MessageFormattingService
from .messaging_clipboard import ClipboardService
from .messaging_pyautogui_operations import PyAutoGUIOperationsService

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
        
        # Initialize service modules (Phase 2A refactoring)
        self.coordinate_service = CoordinateRoutingService()
        self.formatting_service = MessageFormattingService()
        self.clipboard_service = ClipboardService()
        self.operations_service = PyAutoGUIOperationsService(pyautogui_module=pyautogui)

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

        # Platform-accurate bounds check: validate against the OS virtual screen bounds.
        # This prevents false positives where negative X/Y are accepted even when the machine
        # has no left/top monitor (common cause of "it rendered but never typed").
        try:
            from .utilities.validation_utilities import get_virtual_screen_bounds
            min_x, min_y, max_x, max_y = get_virtual_screen_bounds()
            if x < min_x or x > max_x:
                logger.error(
                    f"❌ X coordinate out of virtual screen bounds for {agent_id}: {x} "
                    f"(bounds: {min_x}..{max_x}). Re-capture coords in cursor_agent_coords.json."
                )
                return False
            if y < min_y or y > max_y:
                logger.error(
                    f"❌ Y coordinate out of virtual screen bounds for {agent_id}: {y} "
                    f"(bounds: {min_y}..{max_y}). Re-capture coords in cursor_agent_coords.json."
                )
                return False
        except Exception as e:
            logger.debug(f"Virtual screen bounds check unavailable: {e}")

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
            
            # Legacy coarse bounds (kept as a final backstop)
            if x < -5000 or x > 5000:
                logger.error(f"❌ X coordinate out of coarse bounds for {agent_id}: {x} (expected -5000..5000)")
                return False
            if y < -2000 or y > 5000:
                logger.error(f"❌ Y coordinate out of coarse bounds for {agent_id}: {y} (expected -2000..5000)")
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
            # Phase 2A: Get coordinates using CoordinateRoutingService
            coords = self.coordinate_service.get_coordinates_for_message(message, sender)
            
            if not coords:
                logger.error(f"No coordinates for {message.recipient}")
                return False

            x, y = coords

            # Phase 2A: Format message content using MessageFormattingService
            msg_content = self.formatting_service.format_message_content(message, sender)

            # Execute PyAutoGUI operations using PyAutoGUIOperationsService (Phase 2A refactoring)
            # Move to coordinates with validation
            if not self.operations_service.move_to_coordinates(
                (x, y), 
                message.recipient,
                validate_callback=self.validate_coordinates
            ):
                return False
            
            # Focus input field
            if not self.operations_service.focus_input_field(message.recipient, (x, y)):
                logger.warning(f"⚠️ Focus failed for {message.recipient}, continuing anyway")
            
            # Clear input field
            if not self.operations_service.clear_input_field(message.recipient):
                logger.warning(f"⚠️ Clear failed for {message.recipient}, continuing anyway")
            
            # Verify coordinates before paste
            if not self.operations_service.verify_coordinates_before_paste(message.recipient, (x, y)):
                logger.warning(f"⚠️ Coordinate verification failed for {message.recipient}, repositioning")
                # Service handles repositioning, continue
            
            # CRITICAL: Ensure input field is focused one more time before clipboard operations
            logger.info(f"🖱️ Final focus check before paste for {message.recipient} at ({x}, {y})")
            # Re-click at coordinates to ensure focus
            try:
                import pyautogui
                pyautogui.click(x, y)
                time.sleep(0.3)  # Wait for focus to stabilize
                logger.info(f"✅ Focus click completed for {message.recipient}")
            except Exception as e:
                logger.warning(f"⚠️ Final focus click failed for {message.recipient}: {e}, continuing anyway")
            
            # Copy to clipboard and paste (using ClipboardService)
            # NOTE: copy_to_clipboard() already uses internal locking, so don't wrap in another lock
            logger.info(f"📋 Copying message to clipboard for {message.recipient} ({len(msg_content)} chars)")
            try:
                copy_result = self.clipboard_service.copy_to_clipboard(msg_content)
                logger.info(f"📋 Copy result for {message.recipient}: {copy_result}")
                if not copy_result:
                    logger.error(f"❌ Failed to copy to clipboard for {message.recipient}")
                    return False
                
                logger.info(f"✅ Clipboard ready ({len(msg_content)} chars), pasting to {message.recipient}")
                
                # One final coordinate check and paste
                if not self.operations_service.paste_content(message.recipient, (x, y), self.clipboard_service):
                    logger.error(f"❌ Failed to paste message for {message.recipient}")
                    return False
                
                # Verify clipboard (optional check)
                if not self.clipboard_service.verify_clipboard(msg_content):
                    logger.warning(f"⚠️ Clipboard verification failed for {message.recipient}, but paste may have succeeded")
            except Exception as e:
                logger.error(f"❌ Exception during clipboard/paste operations for {message.recipient}: {e}", exc_info=True)
                return False
            
            # Send message
            message_metadata = message.metadata if isinstance(message.metadata, dict) else {}
            if not self.operations_service.send_message(message.recipient, message_metadata):
                return False
            
            # Verify send completion
            self.operations_service.verify_send_completion(message.recipient, (x, y))

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
