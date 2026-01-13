#!/usr/bin/env python3
"""
Agent Self-Healing System - Proactive Stall Detection & Recovery (V2 Refactored)

<!-- SSOT Domain: infrastructure -->

Automatically detects and recovers stalled agents without manual intervention.
Runs continuously to prevent agent stalls from accumulating.

PROGRESSIVE RECOVERY TIMELINE:
- 5 minutes: Cancel terminal operations (SHIFT+BACKSPACE)
- 8 minutes: Rescue message + Clear tasks + Reset status
- 10 minutes: Hard onboard agent

Refactored to use Service+Integration pattern:
- SelfHealingOperations: Core healing operations (terminal, status, tasks)
- SelfHealingIntegration: External service integrations (messaging, onboarding)

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
Priority: CRITICAL - Prevents 2XX stalled agents
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from datetime import datetime, date
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from .self_healing_operations import SelfHealingOperations
from .self_healing_integration import SelfHealingIntegration
from .self_healing_helpers import (
    load_agent_coordinates,
    load_cancellation_tracking,
    record_cancellation,
    get_cancellation_count_today,
    calculate_healing_stats,
)

logger = logging.getLogger(__name__)

# Progressive recovery thresholds
TERMINAL_CANCEL_THRESHOLD = 300  # 5 minutes
RESCUE_THRESHOLD = 480  # 8 minutes (5 + 3)
HARD_ONBOARD_THRESHOLD = 600  # 10 minutes


@dataclass
class HealingAction:
    """Represents a healing action taken on an agent."""
    agent_id: str
    action_type: str
    timestamp: datetime
    reason: str
    success: bool
    error: Optional[str] = None


@dataclass
class SelfHealingConfig:
    """Configuration for self-healing system."""
    check_interval_seconds: int = 30
    stall_threshold_seconds: int = 120
    recovery_attempts_max: int = 3
    auto_reset_enabled: bool = True
    force_update_enabled: bool = True
    clear_stuck_tasks: bool = True
    healing_history_limit: int = 100
    terminal_cancel_enabled: bool = True
    hard_onboard_enabled: bool = True


class AgentSelfHealingSystem:
    """
    Proactive self-healing system for stalled agents (V2 refactored).

    Uses Service+Integration pattern:
    - Service: Orchestrates healing workflow
    - Operations: Core healing operations (extracted)
    - Integration: External service integrations (extracted)
    """

    AGENT_IDS = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]

    def __init__(self, config: Optional[SelfHealingConfig] = None):
        """Initialize self-healing system."""
        self.config = config or SelfHealingConfig()
        self.logger = logging.getLogger(__name__)
        self.workspace_root = Path("agent_workspaces")

        # Healing history
        self.healing_history: List[HealingAction] = []
        self.recovery_attempts: Dict[str, int] = {}

        # Terminal cancellation tracking
        self.cancellation_counts = load_cancellation_tracking()

        # Enhanced activity detector
        try:
            from src.orchestrators.overnight.enhanced_agent_activity_detector import (
                EnhancedAgentActivityDetector
            )
            self.activity_detector = EnhancedAgentActivityDetector()
        except ImportError:
            self.logger.warning(
                "Enhanced activity detector not available, using fallback")
            self.activity_detector = None

        # Load agent coordinates
        self.agent_coordinates = load_agent_coordinates()

        # Initialize PyAutoGUI for operations
        pyautogui = None
        try:
            import pyautogui as pg
            pyautogui = pg
        except ImportError:
            self.logger.warning(
                "PyAutoGUI not available for terminal cancellation")

        # Initialize extracted modules
        def record_cancel(agent_id: str) -> int:
            return record_cancellation(self.cancellation_counts, agent_id)

        self.operations = SelfHealingOperations(
            workspace_root=self.workspace_root,
            agent_coordinates=self.agent_coordinates,
            pyautogui=pyautogui,
            record_cancellation_callback=record_cancel,
        )

        self.integration = SelfHealingIntegration()

        # Running state
        self.running = False
        self._monitoring_task: Optional[asyncio.Task] = None

    def get_cancellation_count_today(self, agent_id: str) -> int:
        """Get terminal cancellation count for agent today."""
        return get_cancellation_count_today(self.cancellation_counts, agent_id)

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
                self.logger.error(
                    f"Error in monitoring loop: {e}", exc_info=True)
                await asyncio.sleep(self.config.check_interval_seconds)

    async def _check_and_heal_all_agents(self) -> None:
        """Check all agents and heal stalled ones."""
        stalled_agents = await self._detect_stalled_agents()

        if not stalled_agents:
            return

        self.logger.warning(
            f"🔍 Detected {len(stalled_agents)} stalled agents: {stalled_agents}")

        for agent_id, stall_duration in stalled_agents:
            await self._heal_stalled_agent(agent_id, stall_duration)

    async def _detect_stalled_agents(self) -> List[Tuple[str, float]]:
        """Detect stalled agents using enhanced activity detection."""
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
                file_mtime = status_file.stat().st_mtime
                age_seconds = current_time - file_mtime

                if age_seconds > self.config.stall_threshold_seconds:
                    stalled.append((agent_id, age_seconds))
            except Exception as e:
                self.logger.error(f"Error checking {agent_id} status: {e}")

        return stalled

    async def _heal_stalled_agent(self, agent_id: str, stall_duration: float) -> None:
        """Heal a stalled agent with progressive recovery based on duration."""
        self.logger.warning(
            f"🏥 Healing {agent_id} (stalled {stall_duration:.0f}s / {stall_duration/60:.1f}min)"
        )

        healing_success = False

        # Stage 1: 5 minutes - Cancel terminal operations
        if stall_duration >= TERMINAL_CANCEL_THRESHOLD and self.config.terminal_cancel_enabled:
            if await self.operations.cancel_terminal_operations(agent_id):
                healing_success = True
                cancel_count = self.get_cancellation_count_today(agent_id)
                self._record_healing(
                    agent_id, "cancel_terminal",
                    f"Cancelled terminal operations (count: {cancel_count})", True
                )
                await asyncio.sleep(30)
                if await self.operations.check_agent_recovered(agent_id):
                    return

        # Stage 2: 8 minutes - Rescue + Clear + Reset
        if stall_duration >= RESCUE_THRESHOLD and not healing_success:
            self.logger.warning(
                f"⚠️ {agent_id}: 8 minutes - Escalating to rescue protocol")

            stall_duration_minutes = stall_duration / 60.0
            if await self.integration.send_rescue_message(agent_id, stall_duration_minutes):
                healing_success = True
                self._record_healing(agent_id, "rescue",
                                     "Sent optimized rescue message", True)

            if await self.operations.clear_stuck_tasks(agent_id):
                healing_success = True
                self._record_healing(
                    agent_id, "clear_stuck", "Cleared stuck tasks", True)

            if await self.operations.reset_agent_status(agent_id):
                healing_success = True
                self._record_healing(
                    agent_id, "reset", "Reset agent status", True)

        # Stage 3: 10 minutes - Hard onboard
        if stall_duration >= HARD_ONBOARD_THRESHOLD and self.config.hard_onboard_enabled:
            self.logger.error(
                f"🚨 {agent_id}: 10 minutes - HARD ONBOARDING REQUIRED")
            if await self.integration.hard_onboard_agent(agent_id):
                healing_success = True
                self._record_healing(
                    agent_id, "hard_onboard", "Hard onboarded agent", True)
                self.recovery_attempts[agent_id] = 0
                return

        if healing_success:
            self.logger.info(f"✅ {agent_id}: Healing successful")
        else:
            self.recovery_attempts[agent_id] = self.recovery_attempts.get(
                agent_id, 0) + 1

            if self.recovery_attempts[agent_id] >= self.config.recovery_attempts_max:
                await self._escalate_agent(agent_id)

    async def _escalate_agent(self, agent_id: str) -> None:
        """Escalate agent to manual intervention."""
        self.logger.error(
            f"🚨 ESCALATION: {agent_id} requires manual intervention "
            f"({self.config.recovery_attempts_max} recovery attempts failed)"
        )

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
        """Record healing action in history."""
        action = HealingAction(
            agent_id=agent_id,
            action_type=action_type,
            timestamp=datetime.now(),
            reason=reason,
            success=success,
            error=error,
        )

        self.healing_history.append(action)

        if len(self.healing_history) > self.config.healing_history_limit:
            self.healing_history = self.healing_history[-self.config.healing_history_limit:]

    def get_healing_stats(self) -> Dict[str, Any]:
        """Get healing statistics."""
        return calculate_healing_stats(
            self.healing_history,
            self.recovery_attempts,
            self.AGENT_IDS,
            self.get_cancellation_count_today,
        )


# Global instance
_healing_system_instance: Optional[AgentSelfHealingSystem] = None


def get_self_healing_system(config: Optional[SelfHealingConfig] = None) -> AgentSelfHealingSystem:
    """Get or create global self-healing system instance."""
    global _healing_system_instance

    if _healing_system_instance is None:
        _healing_system_instance = AgentSelfHealingSystem(config)

    return _healing_system_instance


async def heal_stalled_agents_now() -> Dict[str, Any]:
    """Immediately check and heal all stalled agents."""
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

        latest_action = system.healing_history[-1] if system.healing_history else None
        if latest_action and latest_action.success:
            results["agents_healed"].append(agent_id)
        else:
            results["agents_failed"].append(agent_id)

    return results
