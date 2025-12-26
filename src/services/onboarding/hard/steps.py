"""
Hard Onboarding Protocol Steps
================================

Extracted protocol steps for hard onboarding service.
Uses shared operations and coordinates for consistency.

V2 Compliant: < 300 lines
"""

import logging
import time
from typing import Optional, Tuple

from ..shared.coordinates import OnboardingCoordinates
from ..shared.operations import PyAutoGUIOperations
from ..onboarding_helpers import validate_onboarding_coordinates

logger = logging.getLogger(__name__)

# Import template loader
try:
    from ...onboarding_template_loader import load_onboarding_template
    TEMPLATE_LOADER_AVAILABLE = True
except ImportError:
    TEMPLATE_LOADER_AVAILABLE = False
    logger.warning("⚠️ Onboarding template loader not available")


class HardOnboardingSteps:
    """Hard onboarding protocol steps."""
    
    def __init__(
        self,
        operations: PyAutoGUIOperations,
        coordinates: OnboardingCoordinates,
    ):
        """Initialize hard onboarding steps."""
        self.ops = operations
        self.coords = coordinates
    
    def step_1_clear_chat(self, agent_id: str) -> bool:
        """
        Step 1: Go to chat input area and press Ctrl+Shift+Backspace.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        try:
            # Get chat coordinates
            chat_coords, _ = self.coords.load_coordinates(agent_id)
            if not chat_coords:
                logger.error(f"❌ No chat coordinates for {agent_id}")
                return False
            
            # Validate coordinates
            if not self.coords.validate_coordinates(agent_id, chat_coords):
                logger.error(f"❌ Coordinate validation failed for {agent_id}")
                return False
            
            x, y = chat_coords
            logger.info(f"🗑️ Step 1: Clearing chat for {agent_id} at {chat_coords}")
            
            # Click chat input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            # Press Ctrl+Shift+Backspace
            if not self.ops.send_hotkey("ctrl", "shift", "backspace", wait=0.8):
                return False
            
            logger.info(f"✅ Chat cleared for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to clear chat: {e}")
            return False
    
    def step_2_send_execute(self) -> bool:
        """
        Step 2: Press Ctrl+Enter to send/execute.
        
        Returns:
            True if successful
        """
        try:
            logger.info("⚡ Step 2: Executing Ctrl+Enter")
            if not self.ops.send_hotkey("ctrl", "enter", wait=0.8):
                return False
            logger.info("✅ Ctrl+Enter executed")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to execute Ctrl+Enter: {e}")
            return False
    
    def step_3_new_window(self) -> bool:
        """
        Step 3: Press Ctrl+N to create new window/session.
        
        Returns:
            True if successful
        """
        try:
            logger.info("🆕 Step 3: Creating new window (Ctrl+N)")
            if not self.ops.send_hotkey("ctrl", "n", wait=2.0):
                return False
            logger.info("✅ New window created")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create new window: {e}")
            return False
    
    def step_4_navigate_to_onboarding(self, agent_id: str) -> bool:
        """
        Step 4: Navigate to onboarding input coordinates.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        try:
            # Get onboarding coordinates
            _, onboarding_coords = self.coords.load_coordinates(agent_id)
            if not onboarding_coords:
                logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False
            
            # Validate bounds only
            if not validate_onboarding_coordinates(agent_id, onboarding_coords):
                return False
            
            x, y = onboarding_coords
            logger.info(f"🎯 Step 4: Navigating to onboarding input for {agent_id} at {onboarding_coords}")
            
            # Move to and click onboarding input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding input: {e}")
            return False
    
    def step_5_send_onboarding_message(
        self, agent_id: str, onboarding_message: Optional[str] = None, role: Optional[str] = None
    ) -> bool:
        """
        Step 5: Send onboarding message via Enter using S2A HARD_ONBOARDING template.
        
        Args:
            agent_id: Target agent ID
            onboarding_message: Custom mission/instructions (if None, uses default)
            role: Agent role (for agent-specific instructions)
            
        Returns:
            True if successful
        """
        try:
            from src.core.messaging_models import (
                MessageCategory,
                UnifiedMessage,
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
            )
            from src.core.messaging_templates import render_message
            from .default_message import get_default_hard_onboarding_message
            from ..agent_instructions import get_agent_specific_instructions
            
            logger.info(f"📝 Step 5: Sending S2A HARD_ONBOARDING message to {agent_id}")
            
            # Use default message if none provided, otherwise use provided message as actions
            if onboarding_message and onboarding_message.strip():
                context = "## 🛰️ **S2A ACTIVATION DIRECTIVE — SWARM ONBOARDING v2.0**\n\n**Signal Type:** System → Agent (S2A)\n**Priority:** Immediate\n**Mode:** Autonomous Execution\n\n**HARD ONBOARDING**: Complete reset protocol - starting fresh session."
                actions = onboarding_message
            else:
                context, actions = get_default_hard_onboarding_message(agent_id)
            
            # Create S2A message with proper category and tags
            msg = UnifiedMessage(
                content=actions,  # Content used for message body
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT,  # Hard onboarding is urgent
                tags=[UnifiedMessageTag.SYSTEM],  # Use SYSTEM tag for S2A
                category=MessageCategory.S2A,
            )
            
            # Render using S2A HARD_ONBOARDING template
            full_message = render_message(
                msg,
                template_key="HARD_ONBOARDING",
                context=context,
                actions=actions,
                fallback="If blocked, escalate to Captain.",
            )
            
            # Get agent-specific instructions and append them
            agent_instructions = get_agent_specific_instructions(agent_id)
            if agent_instructions:
                full_message += agent_instructions
            
            # Add Jet Fuel footer for hard onboarding
            jet_fuel_footer = """

---

🔥 JET FUEL POWER:
This message is your fuel - ACT NOW!
- Don't wait for permission
- Don't ask for approval
- ACT, CREATE, MIGRATE, IMPROVE

WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀"""
            full_message += jet_fuel_footer
            
            # Small delay before pasting
            time.sleep(0.8)
            
            # Paste onboarding message
            if not self.ops.paste_text(full_message, wait=0.5):
                return False
            
            # Press Enter to send
            if not self.ops.press_key("enter", wait=0.8):
                return False
            
            logger.info(f"✅ S2A HARD_ONBOARDING message sent to {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send onboarding message: {e}")
            return False

