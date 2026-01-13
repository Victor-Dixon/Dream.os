"""
<!-- SSOT Domain: integration -->

Hard Onboarding Service - Refactored
=====================================

Main service orchestrator for hard onboarding protocol.
Uses extracted steps for maintainability.

V2 Compliant: < 300 lines
"""

import logging
import time
from typing import Optional

from src.core.base.base_service import BaseService
from ..shared.coordinates import OnboardingCoordinates
from ..shared.operations import PyAutoGUIOperations
from .steps import HardOnboardingSteps

logger = logging.getLogger(__name__)


class HardOnboardingService(BaseService):
    """Handles hard onboarding with complete reset protocol."""
    
    def __init__(self):
        """Initialize hard onboarding service."""
        super().__init__("HardOnboardingService")
        
        # Initialize shared components
        self.operations = PyAutoGUIOperations()
        if not self.operations.available:
            raise ImportError("PyAutoGUI required for hard onboarding")
        
        self.coordinates = OnboardingCoordinates()
        self.steps = HardOnboardingSteps(self.operations, self.coordinates)
    
    def execute_hard_onboarding(
        self,
        agent_id: str,
        onboarding_message: Optional[str] = None,
        role: Optional[str] = None,
    ) -> bool:
        """
        Execute complete hard onboarding protocol (5 steps).
        
        Args:
            agent_id: Target agent ID
            onboarding_message: Onboarding message for new session (if None, uses default)
            role: Optional role assignment
            
        Returns:
            True if all steps completed successfully
        """
        logger.info(f"🚨 Starting HARD ONBOARDING for {agent_id}")
        
        # Step 1: Clear chat (Ctrl+Shift+Backspace)
        if not self.steps.step_1_clear_chat(agent_id):
            logger.error("❌ Step 1 failed: Clear chat")
            return False
        
        # Step 2: Send/Execute (Ctrl+Enter)
        if not self.steps.step_2_send_execute():
            logger.error("❌ Step 2 failed: Send/Execute")
            return False
        
        # Step 3: New window (Ctrl+N)
        if not self.steps.step_3_new_window():
            logger.error("❌ Step 3 failed: New window")
            return False
        
        # Step 4: Navigate to onboarding input
        if not self.steps.step_4_navigate_to_onboarding(agent_id):
            logger.error("❌ Step 4 failed: Navigate to onboarding input")
            return False
        
        # Step 5: Send onboarding message (Enter)
        if not self.steps.step_5_send_onboarding_message(agent_id, onboarding_message, role=role):
            logger.error("❌ Step 5 failed: Send onboarding message")
            return False
        
        logger.info(f"🎉 Hard onboarding complete for {agent_id}!")
        return True


def hard_onboard_agent(agent_id: str, onboarding_message: Optional[str] = None, role: Optional[str] = None) -> bool:
    """
    Convenience function for hard onboarding single agent.
    
    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message (if None, uses default S2A HARD_ONBOARDING message)
        role: Optional role assignment
        
    Returns:
        True if onboarding successful
    """
    try:
        service = HardOnboardingService()
        return service.execute_hard_onboarding(agent_id, onboarding_message, role)
    except Exception as e:
        logger.error(f"❌ Hard onboarding failed: {e}")
        return False


def hard_onboard_multiple_agents(
    agents: list[tuple[str, Optional[str]]], role: Optional[str] = None
) -> dict[str, bool]:
    """
    Hard onboard multiple agents sequentially.
    
    Args:
        agents: List of (agent_id, onboarding_message) tuples
        role: Optional role assignment for all agents
        
    Returns:
        Dictionary of {agent_id: success_status}
    """
    results = {}
    service = HardOnboardingService()
    
    for agent_id, onboarding_message in agents:
        logger.info(f"🚨 Processing {agent_id}...")
        success = service.execute_hard_onboarding(agent_id, onboarding_message, role)
        results[agent_id] = success
        
        if success:
            logger.info(f"✅ {agent_id} hard onboarded successfully")
        else:
            logger.error(f"❌ {agent_id} hard onboarding failed")
        
        # Wait between agents
        time.sleep(2.0)
    
    return results


def execute_hard_onboarding(
    agent_id: str,
    onboarding_message: Optional[str] = None,
    role: Optional[str] = None,
) -> bool:
    """
    Execute hard onboarding protocol.
    
    Args:
        agent_id: Target agent ID
        onboarding_message: Onboarding message (if None, uses default S2A HARD_ONBOARDING message)
        role: Optional role assignment
        
    Returns:
        True if successful
    """
    return hard_onboard_agent(agent_id, onboarding_message, role)

