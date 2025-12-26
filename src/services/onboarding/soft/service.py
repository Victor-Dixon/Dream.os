"""
Soft Onboarding Service - Refactored
=====================================

Main service orchestrator for soft onboarding protocol.
Uses extracted steps for maintainability.

V2 Compliant: < 300 lines
"""

import logging
import time
from typing import Optional

from src.core.base.base_service import BaseService
from ..shared.coordinates import OnboardingCoordinates
from ..shared.operations import PyAutoGUIOperations
from .steps import SoftOnboardingSteps
from .messaging_fallback import OnboardingMessagingFallback

logger = logging.getLogger(__name__)


class SoftOnboardingService(BaseService):
    """Soft onboarding service with 6-step protocol."""
    
    def __init__(self):
        """Initialize soft onboarding service."""
        super().__init__("SoftOnboardingService")
        
        # Initialize shared components
        self.operations = PyAutoGUIOperations()
        self.coordinates = OnboardingCoordinates()
        self.messaging_fallback = OnboardingMessagingFallback()
        self.steps = SoftOnboardingSteps(
            self.operations,
            self.coordinates,
            self.messaging_fallback
        )
    
    def execute_soft_onboarding(
        self,
        agent_id: str,
        onboarding_message: Optional[str] = None,
        role: Optional[str] = None,
        custom_cleanup_message: Optional[str] = None,
    ) -> bool:
        """
        Execute full soft onboarding protocol (6 steps with animations).
        
        NOTE: Lock handling is done by caller (soft_onboard_agent or soft_onboard_multiple_agents).
        This method should NOT acquire the lock itself to avoid double-locking.
        
        Args:
            agent_id: Target agent ID
            onboarding_message: Onboarding message (if None, uses default S2A SOFT_ONBOARDING message)
            role: Optional role assignment
            custom_cleanup_message: Optional custom cleanup message
            
        Returns:
            True if all steps completed successfully
        """
        try:
            logger.info(f"🚀 Starting 6-step soft onboarding for {agent_id}")
            
            # Step 1: Click chat input
            if not self.steps.step_1_click_chat_input(agent_id):
                logger.error("❌ Step 1 failed: Click chat input")
                return False
            
            # Step 2: Save session
            if not self.steps.step_2_save_session():
                logger.error("❌ Step 2 failed: Save session")
                return False
            
            # Step 3: Send cleanup prompt
            if not self.steps.step_3_send_cleanup_prompt(agent_id, custom_cleanup_message):
                logger.error("❌ Step 3 failed: Send cleanup prompt")
                return False
            
            # Step 4: Open new tab
            if not self.steps.step_4_open_new_tab():
                logger.error("❌ Step 4 failed: Open new tab")
                return False
            
            # Step 5: Navigate to onboarding
            if not self.steps.step_5_navigate_to_onboarding(agent_id):
                logger.error("❌ Step 5 failed: Navigate to onboarding")
                return False
            
            # Step 6: Paste onboarding message
            if not self.steps.step_6_paste_onboarding_message(agent_id, onboarding_message):
                logger.error("❌ Step 6 failed: Paste onboarding message")
                return False
            
            logger.info(f"🎉 Soft onboarding complete for {agent_id}!")
            return True
        except Exception as e:
            logger.error(f"Soft onboarding execution failed: {e}")
            return False


def soft_onboard_agent(agent_id: str, message: Optional[str] = None, **kwargs) -> bool:
    """
    Convenience function for soft onboarding.
    
    CRITICAL: Wrapped in keyboard_control to block other sends during operation.
    All 6 steps must complete before allowing new sends.
    
    Args:
        agent_id: Target agent ID
        message: Onboarding message (if None, uses default S2A SOFT_ONBOARDING message)
        **kwargs: Additional options
        
    Returns:
        True if successful
    """
    from src.core.keyboard_control_lock import keyboard_control, is_locked
    
    service = SoftOnboardingService()
    
    # Check if keyboard lock is already held
    lock_already_held = is_locked()
    
    if lock_already_held:
        logger.debug(f"🔒 Keyboard lock already held, skipping lock acquisition for {agent_id}")
        return service.execute_soft_onboarding(agent_id, message, **kwargs)
    else:
        # Wrap ENTIRE operation in keyboard lock
        with keyboard_control(f"soft_onboard_{agent_id}"):
            return service.execute_soft_onboarding(agent_id, message, **kwargs)


def soft_onboard_multiple_agents(
    agents: list[tuple[str, Optional[str]]], role: Optional[str] = None, generate_cycle_report: bool = True
) -> dict[str, bool]:
    """
    Soft onboard multiple agents sequentially.
    
    CRITICAL: Wrapped in keyboard_control to block other sends during entire operation.
    All agents must complete before allowing new sends.
    
    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents
        generate_cycle_report: Whether to generate cycle accomplishments report after onboarding
        
    Returns:
        Dictionary of {agent_id: success_status}
    """
    from src.core.keyboard_control_lock import keyboard_control
    from src.core.config.timeout_constants import TimeoutConstants
    
    results = {}
    
    # Wrap ENTIRE operation in keyboard lock
    with keyboard_control("soft_onboard_multiple"):
        for agent_id, onboarding_message in agents:
            logger.info(f"🚀 Processing {agent_id}...")
            success = soft_onboard_agent(agent_id, onboarding_message, role=role)
            results[agent_id] = success
            
            if success:
                logger.info(f"✅ {agent_id} soft onboarded successfully")
            else:
                logger.error(f"❌ {agent_id} soft onboarding failed")
            
            # Small delay between agents for stability
            time.sleep(2.0)
        
        # Generate cycle accomplishments report after onboarding all agents
        if generate_cycle_report:
            try:
                logger.info("📊 Generating cycle accomplishments report...")
                from pathlib import Path
                import subprocess
                import sys
                
                report_script = Path(__file__).parent.parent.parent.parent / \
                    "tools" / "generate_cycle_accomplishments_report.py"
                if report_script.exists():
                    result = subprocess.run(
                        [sys.executable, str(report_script)],
                        capture_output=True,
                        text=True,
                        timeout=TimeoutConstants.HTTP_DEFAULT
                    )
                    if result.returncode == 0:
                        logger.info("✅ Cycle accomplishments report generated")
                        for line in result.stdout.split('\n'):
                            if 'Report generated:' in line:
                                logger.info(f"   {line.strip()}")
                    else:
                        logger.warning(f"⚠️  Cycle report generation failed: {result.stderr[:200]}")
                else:
                    logger.warning(f"⚠️  Cycle report script not found: {report_script}")
            except Exception as e:
                logger.warning(f"⚠️  Failed to generate cycle report: {e}")
    
    return results


def execute_soft_onboarding(
    agent_id: str,
    onboarding_message: Optional[str] = None,
    role: Optional[str] = None,
    custom_cleanup_message: Optional[str] = None,
) -> bool:
    """
    Execute soft onboarding protocol.
    
    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message (if None, uses default S2A SOFT_ONBOARDING message)
        role: Optional role assignment
        custom_cleanup_message: Optional custom cleanup message
        
    Returns:
        True if successful
    """
    service = SoftOnboardingService()
    return service.execute_soft_onboarding(agent_id, onboarding_message, role, custom_cleanup_message)

