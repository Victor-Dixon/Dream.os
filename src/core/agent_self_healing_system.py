#!/usr/bin/env python3
"""
Agent Self-Healing System - Proactive Stall Detection & Recovery
================================================================

Automatically detects and recovers stalled agents without manual intervention.
Runs continuously to prevent agent stalls from accumulating.

PROGRESSIVE RECOVERY TIMELINE:
- 5 minutes: Cancel terminal operations (SHIFT+BACKSPACE)
- 8 minutes: Rescue message + Clear tasks + Reset status
- 10 minutes: Hard onboard agent

V2 Compliance: <400 lines, single responsibility
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
Priority: CRITICAL - Prevents 2XX stalled agents
"""

from __future__ import annotations

import logging
import time
import json
import asyncio
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Progressive recovery thresholds
TERMINAL_CANCEL_THRESHOLD = 300  # 5 minutes
RESCUE_THRESHOLD = 480  # 8 minutes (5 + 3)
HARD_ONBOARD_THRESHOLD = 600  # 10 minutes


@dataclass
class HealingAction:
    """Represents a healing action taken on an agent."""
    agent_id: str
    action_type: str  # "cancel_terminal", "rescue", "reset", "force_update", "clear_stuck", "hard_onboard"
    timestamp: datetime
    reason: str
    success: bool
    error: Optional[str] = None


@dataclass
class SelfHealingConfig:
    """Configuration for self-healing system."""
    check_interval_seconds: int = 30  # Check every 30 seconds
    stall_threshold_seconds: int = 120  # 2 minutes = initial detection
    recovery_attempts_max: int = 3  # Max recovery attempts before escalation
    auto_reset_enabled: bool = True  # Enable automatic status.json reset
    force_update_enabled: bool = True  # Force status.json update
    clear_stuck_tasks: bool = True  # Clear stuck tasks
    healing_history_limit: int = 100  # Keep last 100 healing actions
    terminal_cancel_enabled: bool = True  # Enable terminal cancellation
    hard_onboard_enabled: bool = True  # Enable hard onboarding


class AgentSelfHealingSystem:
    """
    Proactive self-healing system for stalled agents.
    
    Features:
    - Continuous monitoring (every 30 seconds)
    - Progressive recovery based on stall duration
    - Terminal cancellation (5 minutes)
    - Rescue message + reset (8 minutes)
    - Hard onboarding (10 minutes)
    - Terminal cancellation tracking per day
    """
    
    AGENT_IDS = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]
    
    def __init__(self, config: Optional[SelfHealingConfig] = None):
        """Initialize self-healing system.
        
        Args:
            config: Configuration (uses defaults if None)
        """
        self.config = config or SelfHealingConfig()
        self.logger = logging.getLogger(__name__)
        self.workspace_root = Path("agent_workspaces")
        
        # Healing history
        self.healing_history: List[HealingAction] = []
        self.recovery_attempts: Dict[str, int] = {}
        
        # Terminal cancellation tracking (per agent per day)
        self._load_cancellation_tracking()
        
        # Enhanced activity detector
        try:
            from src.orchestrators.overnight.enhanced_agent_activity_detector import (
                EnhancedAgentActivityDetector
            )
            self.activity_detector = EnhancedAgentActivityDetector()
        except ImportError:
            self.logger.warning("Enhanced activity detector not available, using fallback")
            self.activity_detector = None
        
        # PyAutoGUI for terminal cancellation
        self.pyautogui_available = False
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.pyautogui_available = True
        except ImportError:
            self.logger.warning("PyAutoGUI not available for terminal cancellation")
        
        # Agent coordinates
        self._load_agent_coordinates()
        
        # Running state
        self.running = False
        self._monitoring_task: Optional[asyncio.Task] = None
    
    def _load_agent_coordinates(self) -> None:
        """Load agent chat input coordinates from SSOT."""
        self.agent_coordinates: Dict[str, Tuple[int, int]] = {}
        try:
            coord_file = Path("cursor_agent_coords.json")
            if coord_file.exists():
                data = json.loads(coord_file.read_text(encoding="utf-8"))
                for agent_id, info in data.get("agents", {}).items():
                    coords = info.get("chat_input_coordinates")
                    if coords and len(coords) == 2:
                        self.agent_coordinates[agent_id] = (coords[0], coords[1])
                self.logger.info(f"Loaded coordinates for {len(self.agent_coordinates)} agents")
            else:
                self.logger.warning("cursor_agent_coords.json not found")
        except Exception as e:
            self.logger.error(f"Error loading coordinates: {e}")
    
    def _load_cancellation_tracking(self) -> None:
        """Load terminal cancellation tracking data."""
        self.cancellation_tracking_file = Path("agent_workspaces/.terminal_cancellation_tracking.json")
        try:
            if self.cancellation_tracking_file.exists():
                with open(self.cancellation_tracking_file, 'r') as f:
                    data = json.load(f)
                    # Filter to current day only
                    today = date.today().isoformat()
                    self.cancellation_counts: Dict[str, Dict[str, int]] = {
                        agent_id: {today: counts.get(today, 0)}
                        for agent_id, counts in data.items()
                        if today in counts
                    }
            else:
                self.cancellation_counts: Dict[str, Dict[str, int]] = {}
        except Exception as e:
            self.logger.error(f"Error loading cancellation tracking: {e}")
            self.cancellation_counts: Dict[str, Dict[str, int]] = {}
    
    def _save_cancellation_tracking(self) -> None:
        """Save terminal cancellation tracking data."""
        try:
            self.cancellation_tracking_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cancellation_tracking_file, 'w') as f:
                json.dump(self.cancellation_counts, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving cancellation tracking: {e}")
    
    def _record_terminal_cancellation(self, agent_id: str) -> int:
        """Record terminal cancellation and return count for today.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Cancellation count for today
        """
        today = date.today().isoformat()
        if agent_id not in self.cancellation_counts:
            self.cancellation_counts[agent_id] = {}
        if today not in self.cancellation_counts[agent_id]:
            self.cancellation_counts[agent_id][today] = 0
        self.cancellation_counts[agent_id][today] += 1
        self._save_cancellation_tracking()
        return self.cancellation_counts[agent_id][today]
    
    def get_cancellation_count_today(self, agent_id: str) -> int:
        """Get terminal cancellation count for agent today.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Cancellation count for today
        """
        today = date.today().isoformat()
        return self.cancellation_counts.get(agent_id, {}).get(today, 0)
    
    def start(self) -> None:
        """Start continuous self-healing monitoring."""
        if self.running:
            self.logger.warning("Self-healing system already running")
            return
        
        self.running = True
        self.logger.info(
            f"🚀 Agent Self-Healing System started: "
            f"check_interval={self.config.check_interval_seconds}s, "
            f"stall_threshold={self.config.stall_threshold_seconds}s"
        )
        
        # Start monitoring loop in background
        loop = asyncio.get_event_loop()
        self._monitoring_task = loop.create_task(self._monitoring_loop())
    
    def stop(self) -> None:
        """Stop self-healing monitoring."""
        self.running = False
        if self._monitoring_task:
            self._monitoring_task.cancel()
        self.logger.info("🛑 Agent Self-Healing System stopped")
    
    async def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        while self.running:
            try:
                await self._check_and_heal_all_agents()
                await asyncio.sleep(self.config.check_interval_seconds)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}", exc_info=True)
                await asyncio.sleep(self.config.check_interval_seconds)
    
    async def _check_and_heal_all_agents(self) -> None:
        """Check all agents and heal stalled ones."""
        stalled_agents = await self._detect_stalled_agents()
        
        if not stalled_agents:
            return
        
        self.logger.warning(f"🔍 Detected {len(stalled_agents)} stalled agents: {stalled_agents}")
        
        for agent_id, stall_duration in stalled_agents:
            await self._heal_stalled_agent(agent_id, stall_duration)
    
    async def _detect_stalled_agents(self) -> List[Tuple[str, float]]:
        """Detect stalled agents using enhanced activity detection.
        
        Returns:
            List of (agent_id, stall_duration_seconds) tuples
        """
        stalled = []
        current_time = time.time()
        
        if self.activity_detector:
            try:
                stale_agents = self.activity_detector.get_stale_agents(
                    max_age_seconds=self.config.stall_threshold_seconds
                )
                return stale_agents
            except Exception as e:
                self.logger.error(f"Enhanced detection error: {e}")
        
        # Fallback: Check status.json files directly
        for agent_id in self.AGENT_IDS:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                stalled.append((agent_id, float("inf")))
                continue
            
            try:
                # Check file modification time
                file_mtime = status_file.stat().st_mtime
                age_seconds = current_time - file_mtime
                
                if age_seconds > self.config.stall_threshold_seconds:
                    stalled.append((agent_id, age_seconds))
            except Exception as e:
                self.logger.error(f"Error checking {agent_id} status: {e}")
        
        return stalled
    
    async def _heal_stalled_agent(self, agent_id: str, stall_duration: float) -> None:
        """Heal a stalled agent with progressive recovery based on duration.
        
        PROGRESSIVE RECOVERY TIMELINE:
        - 5 minutes: Cancel terminal operations (SHIFT+BACKSPACE)
        - 8 minutes: Rescue message + Clear tasks + Reset status
        - 10 minutes: Hard onboard agent
        
        Args:
            agent_id: Agent identifier
            stall_duration: How long agent has been stalled (seconds)
        """
        self.logger.warning(
            f"🏥 Healing {agent_id} (stalled {stall_duration:.0f}s / {stall_duration/60:.1f}min)"
        )
        
        healing_success = False
        
        # PROGRESSIVE RECOVERY BASED ON DURATION
        
        # Stage 1: 5 minutes - Cancel terminal operations
        if stall_duration >= TERMINAL_CANCEL_THRESHOLD and self.config.terminal_cancel_enabled:
            if await self._cancel_terminal_operations(agent_id):
                healing_success = True
                cancel_count = self.get_cancellation_count_today(agent_id)
                self.logger.info(
                    f"✅ {agent_id}: Terminal cancelled "
                    f"(cancellation #{cancel_count} today)"
                )
                self._record_healing(
                    agent_id, "cancel_terminal",
                    f"Cancelled terminal operations (count: {cancel_count})", True
                )
                # Wait a bit to see if agent recovers
                await asyncio.sleep(30)
                # Re-check status after cancellation
                if await self._check_agent_recovered(agent_id):
                    return  # Agent recovered, stop here
        
        # Stage 2: 8 minutes - Rescue + Clear + Reset
        if stall_duration >= RESCUE_THRESHOLD and not healing_success:
            self.logger.warning(f"⚠️ {agent_id}: 8 minutes - Escalating to rescue protocol")
            
            # Rescue message (with optimized prompt using FSM + Cycle Planner)
            stall_duration_minutes = stall_duration / 60.0
            if await self._send_rescue_message(agent_id, stall_duration_minutes=stall_duration_minutes):
                healing_success = True
                self._record_healing(agent_id, "rescue", "Sent optimized rescue message (FSM+Cycle Planner)", True)
            
            # Clear stuck tasks
            if await self._clear_stuck_tasks(agent_id):
                healing_success = True
                self._record_healing(agent_id, "clear_stuck", "Cleared stuck tasks", True)
            
            # Reset status
            if await self._reset_agent_status(agent_id):
                healing_success = True
                self._record_healing(agent_id, "reset", "Reset agent status", True)
        
        # Stage 3: 10 minutes - Hard onboard
        if stall_duration >= HARD_ONBOARD_THRESHOLD and self.config.hard_onboard_enabled:
            self.logger.error(f"🚨 {agent_id}: 10 minutes - HARD ONBOARDING REQUIRED")
            if await self._hard_onboard_agent(agent_id):
                healing_success = True
                self._record_healing(agent_id, "hard_onboard", "Hard onboarded agent", True)
                # Reset recovery attempts after hard onboard
                self.recovery_attempts[agent_id] = 0
                return
        
        if healing_success:
            self.logger.info(f"✅ {agent_id}: Healing successful")
        else:
            # Increment recovery attempts if no healing succeeded
            self.recovery_attempts[agent_id] = self.recovery_attempts.get(agent_id, 0) + 1
            
            if self.recovery_attempts[agent_id] >= self.config.recovery_attempts_max:
                await self._escalate_agent(agent_id)
    
    async def _cancel_terminal_operations(self, agent_id: str) -> bool:
        """Cancel terminal operations by clicking chat input and pressing SHIFT+BACKSPACE.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if successful
        """
        if not self.pyautogui_available:
            self.logger.warning(f"PyAutoGUI not available - cannot cancel terminal for {agent_id}")
            return False
        
        if agent_id not in self.agent_coordinates:
            self.logger.error(f"No coordinates found for {agent_id}")
            return False
        
        try:
            x, y = self.agent_coordinates[agent_id]
            self.logger.info(f"🛑 Cancelling terminal for {agent_id} at ({x}, {y})")
            
            # Click chat input coordinates
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            await asyncio.sleep(0.3)
            
            # Press SHIFT+BACKSPACE to cancel terminal operations
            self.pyautogui.hotkey("shift", "backspace")
            await asyncio.sleep(0.5)
            
            # Record cancellation
            cancel_count = self._record_terminal_cancellation(agent_id)
            
            self.logger.info(
                f"✅ Terminal cancelled for {agent_id} "
                f"(cancellation #{cancel_count} today)"
            )
            return True
            
        except Exception as e:
            self.logger.error(f"Error cancelling terminal for {agent_id}: {e}")
            return False
    
    async def _check_agent_recovered(self, agent_id: str) -> bool:
        """Check if agent has recovered after cancellation.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if agent status was updated recently
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            if not status_file.exists():
                return False
            
            file_mtime = status_file.stat().st_mtime
            age_seconds = time.time() - file_mtime
            
            # If status updated in last 30 seconds, agent recovered
            return age_seconds < 30
        except Exception:
            return False
    
    async def _clear_stuck_tasks(self, agent_id: str) -> bool:
        """Clear stuck tasks from agent status.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if successful
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            
            if not status_file.exists():
                return False
            
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            # Clear current_tasks
            if "current_tasks" in status:
                status["current_tasks"] = []
                if "healing_applied" not in status:
                    status["healing_applied"] = []
                status["healing_applied"].append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "clear_stuck_tasks",
                })
                
                status["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(status_file, 'w') as f:
                    json.dump(status, f, indent=2)
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error clearing stuck tasks for {agent_id}: {e}")
            return False
    
    async def _reset_agent_status(self, agent_id: str) -> bool:
        """Reset agent status.json to active state.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if successful
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            status_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Create fresh status
            reset_status = {
                "agent_id": agent_id,
                "status": "ACTIVE_AGENT_MODE",
                "current_phase": "TASK_EXECUTION",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "healing_applied": [{
                    "timestamp": datetime.now().isoformat(),
                    "action": "reset",
                    "reason": "stall_recovery",
                }],
                "current_mission": "System recovery - ready for new tasks",
                "mission_priority": "HIGH",
                "current_tasks": [],
                "next_actions": ["Awaiting task assignment"],
            }
            
            with open(status_file, 'w') as f:
                json.dump(reset_status, f, indent=2)
            
            self.logger.info(f"✅ {agent_id}: Status reset successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error resetting status for {agent_id}: {e}")
            return False
    
    async def _send_rescue_message(self, agent_id: str, stall_duration_minutes: float = 0.0) -> bool:
        """Send optimized rescue message to stalled agent with FSM and Cycle Planner integration.
        
        Args:
            agent_id: Agent identifier
            stall_duration_minutes: How long agent has been stalled (for prompt urgency)
            
        Returns:
            True if successful
        """
        try:
            # Use optimized prompt generator directly
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt
            
            # Generate optimized prompt
            rescue_message = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=None,  # Will be loaded from status.json
                last_mission=None,  # Will be loaded from status.json
                stall_duration_minutes=stall_duration_minutes
            )
            
            # Send via messaging service
            try:
                from src.core.messaging_core import send_message
                from src.core.messaging_models_core import (
                    UnifiedMessageType,
                    UnifiedMessagePriority,
                    UnifiedMessageTag
                )
                
                success = send_message(
                    content=rescue_message,
                    sender="SYSTEM",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.URGENT,
                    tags=[UnifiedMessageTag.SYSTEM]
                )
                
                if success:
                    self.logger.info(f"✅ Optimized rescue message sent to {agent_id}")
                    return True
                else:
                    self.logger.warning(f"⚠️ Rescue message send failed for {agent_id}")
                    return False
            except ImportError:
                # Fallback to recovery system
                from src.orchestrators.overnight.recovery import RecoverySystem
                recovery = RecoverySystem()
                await recovery._rescue_agent(agent_id)
                return True
        except Exception as e:
            self.logger.error(f"Error sending rescue message to {agent_id}: {e}")
            return False
    
    async def _hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard agent (complete reset).
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            True if successful
        """
        try:
            from src.services.hard_onboarding_service import HardOnboardingService
            
            service = HardOnboardingService()
            
            # Get default onboarding message
            onboarding_message = (
                f"[S2A] {agent_id}: System recovery - Hard onboarding initiated. "
                f"Status: ACTIVE_AGENT_MODE. Ready for task assignment."
            )
            
            success = service.execute_hard_onboarding(
                agent_id=agent_id,
                onboarding_message=onboarding_message,
                role=None  # Use default role
            )
            
            if success:
                self.logger.info(f"✅ {agent_id}: Hard onboarding successful")
            else:
                self.logger.error(f"❌ {agent_id}: Hard onboarding failed")
            
            return success
            
        except ImportError as e:
            self.logger.error(f"Hard onboarding service not available: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error hard onboarding {agent_id}: {e}")
            return False
    
    async def _escalate_agent(self, agent_id: str) -> None:
        """Escalate agent to manual intervention.
        
        Args:
            agent_id: Agent identifier
        """
        self.logger.error(
            f"🚨 ESCALATION: {agent_id} requires manual intervention "
            f"({self.config.recovery_attempts_max} recovery attempts failed)"
        )
        
        # Create escalation marker
        escalation_file = self.workspace_root / agent_id / ".ESCALATION_REQUIRED"
        escalation_file.write_text(
            f"Agent {agent_id} requires manual intervention.\n"
            f"Timestamp: {datetime.now().isoformat()}\n"
            f"Recovery attempts: {self.recovery_attempts.get(agent_id, 0)}\n"
        )
    
    def _record_healing(
        self,
        agent_id: str,
        action_type: str,
        reason: str,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """Record healing action in history.
        
        Args:
            agent_id: Agent identifier
            action_type: Type of healing action
            reason: Reason for healing
            success: Whether healing succeeded
            error: Error message if failed
        """
        action = HealingAction(
            agent_id=agent_id,
            action_type=action_type,
            timestamp=datetime.now(),
            reason=reason,
            success=success,
            error=error,
        )
        
        self.healing_history.append(action)
        
        # Trim history
        if len(self.healing_history) > self.config.healing_history_limit:
            self.healing_history = self.healing_history[-self.config.healing_history_limit:]
    
    def get_healing_stats(self) -> Dict[str, Any]:
        """Get healing statistics.
        
        Returns:
            Dictionary with healing statistics
        """
        successful = sum(1 for a in self.healing_history if a.success)
        failed = sum(1 for a in self.healing_history if not a.success)
        
        by_agent: Dict[str, Dict[str, int]] = {}
        for action in self.healing_history:
            if action.agent_id not in by_agent:
                by_agent[action.agent_id] = {"total": 0, "successful": 0, "failed": 0}
            by_agent[action.agent_id]["total"] += 1
            if action.success:
                by_agent[action.agent_id]["successful"] += 1
            else:
                by_agent[action.agent_id]["failed"] += 1
        
        # Add cancellation counts
        cancellation_counts = {
            agent_id: self.get_cancellation_count_today(agent_id)
            for agent_id in self.AGENT_IDS
        }
        
        return {
            "total_actions": len(self.healing_history),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(self.healing_history) * 100) if self.healing_history else 0.0,
            "by_agent": by_agent,
            "recovery_attempts": self.recovery_attempts.copy(),
            "terminal_cancellations_today": cancellation_counts,
            "recent_actions": [
                {
                    "agent_id": a.agent_id,
                    "action": a.action_type,
                    "reason": a.reason,
                    "success": a.success,
                    "timestamp": a.timestamp.isoformat(),
                }
                for a in self.healing_history[-10:]
            ],
        }


# Global instance
_healing_system_instance: Optional[AgentSelfHealingSystem] = None


def get_self_healing_system(config: Optional[SelfHealingConfig] = None) -> AgentSelfHealingSystem:
    """Get or create global self-healing system instance.
    
    Args:
        config: Configuration (only used on first call)
        
    Returns:
        Self-healing system instance
    """
    global _healing_system_instance
    
    if _healing_system_instance is None:
        _healing_system_instance = AgentSelfHealingSystem(config)
    
    return _healing_system_instance


async def heal_stalled_agents_now() -> Dict[str, Any]:
    """Immediately check and heal all stalled agents.
    
    Returns:
        Dictionary with healing results
    """
    system = get_self_healing_system()
    stalled_agents = await system._detect_stalled_agents()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "stalled_agents_found": len(stalled_agents),
        "agents_healed": [],
        "agents_failed": [],
    }
    
    for agent_id, stall_duration in stalled_agents:
        await system._heal_stalled_agent(agent_id, stall_duration)
        
        # Check if healing succeeded
        latest_action = system.healing_history[-1] if system.healing_history else None
        if latest_action and latest_action.success:
            results["agents_healed"].append(agent_id)
        else:
            results["agents_failed"].append(agent_id)
    
    return results
