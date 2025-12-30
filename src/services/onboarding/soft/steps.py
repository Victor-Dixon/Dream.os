"""
<!-- SSOT Domain: integration -->

Soft Onboarding Protocol Steps
================================

Extracted protocol steps for soft onboarding service.
Uses shared operations and coordinates for consistency.

V2 Compliant: < 300 lines
"""

import logging
import time
from typing import Optional

from ..shared.coordinates import OnboardingCoordinates
from ..shared.operations import PyAutoGUIOperations
from .messaging_fallback import OnboardingMessagingFallback

logger = logging.getLogger(__name__)


class SoftOnboardingSteps:
    """Soft onboarding protocol steps."""
    
    def __init__(
        self,
        operations: PyAutoGUIOperations,
        coordinates: OnboardingCoordinates,
        messaging_fallback: OnboardingMessagingFallback,
    ):
        """Initialize soft onboarding steps."""
        self.ops = operations
        self.coords = coordinates
        self.messaging = messaging_fallback
    
    def step_1_click_chat_input(self, agent_id: str) -> bool:
        """
        Step 1: Click chat input to get agent's attention.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping step 1")
            return True  # Non-blocking
        
        try:
            chat_coords, _ = self.coords.load_coordinates(agent_id)
            if not chat_coords:
                logger.error(f"❌ No chat coordinates for {agent_id}")
                return False
            
            x, y = chat_coords
            logger.info(f"👆 Step 1: Clicking chat input for {agent_id} at {chat_coords}")
            
            # Click chat input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            logger.info(f"✅ Chat input clicked for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to click chat input: {e}")
            return False
    
    def step_2_save_session(self) -> bool:
        """
        Step 2: Save session (Ctrl+Enter).
        
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping step 2")
            return True  # Non-blocking
        
        try:
            logger.info("💾 Step 2: Saving session (Ctrl+Enter)")
            if not self.ops.send_hotkey("ctrl", "enter", wait=0.8):
                return False
            logger.info("✅ Session saved")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to save session: {e}")
            return False
    
    def step_3_send_cleanup_prompt(self, agent_id: str, custom_cleanup_message: Optional[str] = None) -> bool:
        """
        Step 3: Send cleanup prompt (passdown message).
        
        Args:
            agent_id: Target agent ID
            custom_cleanup_message: Optional custom cleanup message (defaults to A++ session closure prompt)
            
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - using messaging system for step 3")
            return self.messaging.send_cleanup_via_messaging(agent_id, custom_cleanup_message)
        
        try:
            from .cleanup_defaults import DEFAULT_SESSION_CLOSURE_PROMPT
            cleanup_message = (
                custom_cleanup_message.strip() 
                if custom_cleanup_message and custom_cleanup_message.strip() 
                else DEFAULT_SESSION_CLOSURE_PROMPT
            )
            logger.info(f"📝 Step 3: Sending cleanup prompt to {agent_id}")
            
            # Clear input first
            if not self.ops.clear_input(wait=0.3):
                return False
            
            # Paste and send cleanup message
            if not self.ops.paste_text(cleanup_message, wait=0.3):
                return False
            
            # Press Enter
            if not self.ops.press_key("enter", wait=1.0):
                return False
            
            logger.info(f"✅ Cleanup prompt sent to {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send cleanup prompt: {e}")
            return False
    
    def step_4_open_new_tab(self) -> bool:
        """
        Step 4: Open new tab (Ctrl+T).
        
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping step 4")
            return True  # Non-blocking
        
        try:
            logger.info("🆕 Step 4: Opening new tab (Ctrl+T)")
            if not self.ops.send_hotkey("ctrl", "t", wait=2.0):
                return False
            logger.info("✅ New tab opened")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to open new tab: {e}")
            return False
    
    def step_5_navigate_to_onboarding(self, agent_id: str) -> bool:
        """
        Step 5: Navigate to onboarding coordinates.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping step 5")
            return True  # Non-blocking
        
        try:
            _, onboarding_coords = self.coords.load_coordinates(agent_id)
            if not onboarding_coords:
                logger.error(f"❌ No onboarding coordinates for {agent_id}")
                return False
            
            x, y = onboarding_coords
            logger.info(f"🎯 Step 5: Navigating to onboarding coords for {agent_id} at {onboarding_coords}")
            
            # Click onboarding input
            if not self.ops.click_at_coords(x, y, duration=0.5):
                return False
            time.sleep(1.0)  # Wait for app to respond
            
            logger.info(f"✅ Navigated to onboarding input for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to navigate to onboarding: {e}")
            return False
    
    def step_6_paste_onboarding_message(
        self,
        agent_id: str,
        message: Optional[str] = None,
        context_override: Optional[str] = None,
    ) -> bool:
        """
        Step 6: Paste and send onboarding message using unified S2A ONBOARDING template.
        
        Args:
            agent_id: Target agent ID
            message: Onboarding message (if provided, used as actions; otherwise uses default)
            context_override: Optional custom context (if provided, used instead of default context)
            
        Returns:
            True if successful
        """
        if not self.ops.available:
            logger.warning("⚠️ PyAutoGUI not available - using messaging system for step 6")
            return self.messaging.send_onboarding_via_messaging(agent_id, message)
        
        try:
            from pathlib import Path
            from src.core.messaging_models import (
                MessageCategory,
                UnifiedMessage,
                UnifiedMessagePriority,
                UnifiedMessageTag,
                UnifiedMessageType,
            )
            from src.core.messaging_templates import render_message
            from .default_message import get_default_soft_onboarding_message
            
            # Use default message if none provided, otherwise use provided message as actions
            if message and message.strip():
                actions = message
                context = (
                    context_override.strip()
                    if context_override and context_override.strip()
                    else (
                        "## 🛰️ S2A ACTIVATION DIRECTIVE — CUSTOM\n"
                        f"Agent: {agent_id}\n"
                        "Mode: Autonomous Execution\n"
                    )
                )
            else:
                context, actions = get_default_soft_onboarding_message(agent_id)
                # Override context if provided
                if context_override and context_override.strip():
                    context = context_override.strip()
            
            # Create S2A message with proper category and tags
            msg = UnifiedMessage(
                content=actions,  # Content used for message body
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.SYSTEM],  # Use SYSTEM tag for S2A
                category=MessageCategory.S2A,
            )
            
            # Render using unified S2A ONBOARDING template with SOFT mode
            rendered = render_message(
                msg,
                template_key="ONBOARDING",
                context=context,
                actions=actions,
                fallback="If blocked: 1 blocker + fix + owner.",
                mode="SOFT",
                footer="",
            )
            
            # Length guard: Save full message to artifact if too long
            MAX_CHARS = 8000  # Conservative for chat UI stability; tune as needed
            if len(rendered) > MAX_CHARS:
                # Save full content (artifact) and send truncated + pointer
                out_dir = Path(f"agent_workspaces/{agent_id}/inbox")
                out_dir.mkdir(parents=True, exist_ok=True)
                full_path = out_dir / "soft_onboarding_message_full.txt"
                full_path.write_text(rendered, encoding="utf-8")
                
                truncated = (
                    rendered[:MAX_CHARS - 300]
                    + "\n\n[TRUNCATED]\n"
                    + f"Full message saved: {full_path.as_posix()}\n"
                    + "Action: open file and follow instructions.\n"
                )
                rendered = truncated
                logger.info(f"⚠️  Message truncated ({len(rendered)} chars), full content saved to {full_path}")
            
            logger.info(f"📝 Step 6: Pasting S2A ONBOARDING (SOFT) message for {agent_id}")
            
            # Clear input first
            if not self.ops.clear_input(wait=0.3):
                return False
            
            # Paste and send rendered template message
            if not self.ops.paste_text(rendered, wait=0.5):
                return False
            
            # Press Enter
            if not self.ops.press_key("enter", wait=0.8):
                return False
            
            logger.info(f"✅ S2A ONBOARDING (SOFT) message sent to {agent_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to paste onboarding message: {e}")
            return False

