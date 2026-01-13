#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
Auto-Gas Pipeline System - UNLIMITED FUEL SOLUTION
=================================================

<!-- SSOT Domain: core -->

Automated gas/fuel delivery system for perpetual agent pipeline operation.

Features:
- Continuous status.json monitoring
- Progress-based gas delivery (75%, 90%, 100%)
- FSM state tracking
- Jet fuel optimization
- Swarm Brain integration
- Discord status reporting

V2 Consolidated: Uses SSOT base classes for standardized patterns
Author: Agent-3 (Infrastructure & DevOps Specialist)
SSOT Migration: Agent-8 (System Integration)
Date: 2026-01-12
V2 Compliance: <400 lines, SOLID principles, comprehensive error handling
"""

# SSOT Import Standardization - eliminates redundant typing imports
from src.core.base.import_standardization import (
    logging, time, threading, datetime, timedelta, Path, json, os,
    Dict, Any, List, Optional
)
from src.core.base.service_base import BaseService
from src.core.base.error_handling import ErrorHandler, error_context

# Initialize standardized logger through SSOT base
logger = logging.getLogger(__name__)

from .agent_status.aggregator import SwarmStateAggregator
from .unified_service_base import UnifiedServiceBase

logger = logging.getLogger(__name__)


class AutoGasPipelineSystem(UnifiedServiceBase):
    """
    Auto-Gas Pipeline System - Prevents pipeline stalls through automated fuel delivery.

    Monitors agent progress and automatically sends gas at optimal intervals:
    - 75%: Primary gas delivery
    - 90%: Safety gas delivery
    - 100%: Completion gas delivery
    """

    def __init__(self, workspace_root: Optional[Path] = None, monitoring_interval: int = 60):
        """Initialize the auto-gas pipeline system."""

        # Configuration schema for unified service
        config_schema = {
            'defaults': {
                'workspace_root': str(workspace_root or Path.cwd()),
                'monitoring_interval': monitoring_interval,
                'jet_fuel_enabled': False,
                'discord_reporting': True,
            },
            'types': {
                'workspace_root': str,
                'monitoring_interval': int,
                'jet_fuel_enabled': bool,
                'discord_reporting': bool,
            }
        }

        # Initialize unified service base
        super().__init__(
            service_name="AutoGasPipelineSystem",
            config_schema=config_schema,
            loop_interval=monitoring_interval
        )

        # Service-specific attributes
        self.monitor_thread = None

        # Initialize components
        self.status_aggregator = SwarmStateAggregator(Path(self.config['workspace_root']))
        self.agent_progress_cache: Dict[str, Dict[str, Any]] = {}
        self.gas_delivery_log: List[Dict[str, Any]] = []

        # Jet fuel optimization
        self.agent_velocity_history: Dict[str, List[float]] = {}
        self.adaptive_thresholds: Dict[str, Dict[str, float]] = {}

        # Legacy compatibility - map config to old attributes
        self.monitoring_interval = self.config['monitoring_interval']
        self.jet_fuel_enabled = self.config.get('jet_fuel_enabled', False)

        self.logger.info("✅ Auto-Gas Pipeline System initialized with unified patterns")

    def run_once(self) -> None:
        """Main service execution logic - monitor agents and deliver gas as needed."""
        try:
            self._monitor_agents()
        except Exception as e:
            self.logger.error(f"Error in gas pipeline run_once: {e}")

    def check_health(self) -> Dict[str, Any]:
        """Check service health."""
        return {
            "healthy": True,
            "status": "monitoring",
            "agents_monitored": len(self.agent_progress_cache),
            "gas_deliveries": len(self.gas_delivery_log),
            "jet_fuel_enabled": self.config.get('jet_fuel_enabled', False),
            "timestamp": datetime.now().isoformat()
        }

    def start(self, jet_fuel: bool = False, mode: str = "foreground") -> bool:
        """
        Start the auto-gas pipeline monitoring.

        Args:
            jet_fuel: Enable jet fuel optimization
            mode: Startup mode (foreground/background)

        Returns:
            Success status
        """
        # Update configuration with jet fuel setting
        self.set_config_value('jet_fuel_enabled', jet_fuel)

        # Use unified service base startup
        return super().start(mode)

    def stop(self) -> bool:
        """Stop the auto-gas pipeline monitoring."""
        # Use unified service base stop
        return super().stop()

    def _monitor_agents(self):
        """Monitor all agents and deliver gas as needed."""
        try:
            # Get current swarm state
            swarm_state = self.status_aggregator.aggregate_swarm_state()

            if not swarm_state or "agents" not in swarm_state:
                return

            agents = swarm_state["agents"]

            for agent_id, agent_data in agents.items():
                if agent_data.get("status") != "active":
                    continue

                # Calculate progress for this agent
                progress = self._calculate_agent_progress(agent_data)

                if progress is not None:
                    # Check if gas should be delivered
                    gas_needed = self._check_gas_requirements(agent_id, progress)

                    if gas_needed:
                        self._deliver_gas(agent_id, progress, gas_needed)

        except Exception as e:
            logger.error(f"Error monitoring agents: {e}")

    def _calculate_agent_progress(self, agent_data: Dict[str, Any]) -> Optional[float]:
        """
        Calculate agent progress percentage.

        Args:
            agent_data: Agent status data

        Returns:
            Progress percentage (0-100) or None if cannot calculate
        """
        try:
            # Get completed and total tasks from agent data
            completed_tasks = agent_data.get("completed_tasks", [])
            current_tasks = agent_data.get("current_tasks", [])

            # Parse repo completion patterns
            completed_repos = self._count_repo_completions(completed_tasks)
            total_assigned_repos = self._get_total_assigned_repos(agent_data)

            if total_assigned_repos == 0:
                return None

            progress = (completed_repos / total_assigned_repos) * 100
            return min(progress, 100.0)  # Cap at 100%

        except Exception as e:
            logger.warning(f"Could not calculate progress for agent: {e}")
            return None

    def _count_repo_completions(self, completed_tasks: List[str]) -> int:
        """Count completed repositories from task list."""
        completed_count = 0

        for task in completed_tasks:
            task_str = str(task).lower()
            # Look for repo completion patterns
            if any(pattern in task_str for pattern in [
                "repo #", "repo_", "repository", "repo complete",
                "repo done", "repo finished", "repo consolidated"
            ]):
                completed_count += 1

        return completed_count

    def _get_total_assigned_repos(self, agent_data: Dict[str, Any]) -> int:
        """Get total repositories assigned to agent."""
        # Check various fields for repo assignment info
        assignment_fields = [
            "assigned_repos", "total_repos", "repo_range",
            "repos_assigned", "mission_repos"
        ]

        for field in assignment_fields:
            if field in agent_data:
                value = agent_data[field]
                if isinstance(value, int):
                    return value
                elif isinstance(value, str):
                    # Try to parse "X-Y" range format
                    if "-" in value:
                        try:
                            start, end = map(int, value.split("-"))
                            return end - start + 1
                        except ValueError:
                            continue

        # Default: try to infer from agent ID pattern (Agent-1 = repos 1-10, etc.)
        agent_id = agent_data.get("agent_id", "")
        if agent_id.startswith("Agent-"):
            try:
                agent_num = int(agent_id.split("-")[1])
                # Simple mapping: Agent-1 = 10 repos, Agent-2 = 15 repos, etc.
                return max(10, agent_num * 5 + 5)
            except (ValueError, IndexError):
                pass

        return 10  # Default fallback

    def _check_gas_requirements(self, agent_id: str, progress: float) -> Optional[str]:
        """
        Check if gas delivery is needed based on progress.

        Args:
            agent_id: Agent identifier
            progress: Current progress percentage

        Returns:
            Gas type needed ("primary", "safety", "completion") or None
        """
        # Get adaptive thresholds for this agent
        thresholds = self._get_adaptive_thresholds(agent_id)

        # Check completion gas (100%)
        if progress >= 100.0 and not self._gas_already_sent(agent_id, "completion"):
            return "completion"

        # Check safety gas (90%)
        if progress >= thresholds["safety"] and not self._gas_already_sent(agent_id, "safety"):
            return "safety"

        # Check primary gas (75%)
        if progress >= thresholds["primary"] and not self._gas_already_sent(agent_id, "primary"):
            return "primary"

        return None

    def _get_adaptive_thresholds(self, agent_id: str) -> Dict[str, float]:
        """Get adaptive gas delivery thresholds for agent."""
        if agent_id in self.adaptive_thresholds:
            return self.adaptive_thresholds[agent_id]

        # Calculate based on agent velocity history
        velocity = self._calculate_agent_velocity(agent_id)

        if velocity > 1.5:  # Fast agent
            thresholds = {"primary": 70.0, "safety": 85.0}
        elif velocity < 0.7:  # Methodical agent
            thresholds = {"primary": 80.0, "safety": 92.0}
        else:  # Normal agent
            thresholds = {"primary": 75.0, "safety": 90.0}

        self.adaptive_thresholds[agent_id] = thresholds
        return thresholds

    def _calculate_agent_velocity(self, agent_id: str) -> float:
        """Calculate agent's repository completion velocity."""
        if agent_id not in self.agent_velocity_history:
            return 1.0  # Default velocity

        history = self.agent_velocity_history[agent_id]
        if len(history) < 2:
            return 1.0

        # Calculate repos per cycle (assuming daily cycles)
        recent_velocity = sum(history[-7:]) / len(history[-7:])  # 7-day average
        return max(0.1, recent_velocity)  # Minimum velocity

    def _gas_already_sent(self, agent_id: str, gas_type: str) -> bool:
        """Check if gas of this type was already sent to agent."""
        for delivery in self.gas_delivery_log:
            if (delivery["agent_id"] == agent_id and
                delivery["gas_type"] == gas_type and
                delivery["timestamp"] > datetime.now() - timedelta(hours=24)):  # Within last 24h
                return True
        return False

    def _deliver_gas(self, agent_id: str, progress: float, gas_type: str):
        """
        Deliver gas to agent.

        Args:
            agent_id: Target agent
            progress: Current progress
            gas_type: Type of gas ("primary", "safety", "completion")
        """
        try:
            # Create gas message
            gas_message = self._create_gas_message(agent_id, progress, gas_type)

            # Log delivery
            delivery_record = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "progress": progress,
                "gas_type": gas_type,
                "message": gas_message,
                "jet_fuel": self.jet_fuel_enabled
            }
            self.gas_delivery_log.append(delivery_record)

            # Send via messaging system
            success = self._send_gas_message(agent_id, gas_message)

            # Log to Swarm Brain
            self._log_to_swarm_brain(delivery_record, success)

            status = "✅" if success else "❌"
            logger.info(f"{status} Auto-Gas delivered to {agent_id}: {gas_type} at {progress:.1f}%")

        except Exception as e:
            logger.error(f"Failed to deliver gas to {agent_id}: {e}")

    def _create_gas_message(self, agent_id: str, progress: float, gas_type: str) -> str:
        """Create gas delivery message."""
        if not self.jet_fuel_enabled:
            # Standard gas message
            gas_messages = {
                "primary": "⛽ You're next! Execute now!",
                "safety": "⛽ Safety gas - keep pushing!",
                "completion": "⛽ Final push - complete the mission!"
            }
            return gas_messages.get(gas_type, "⛽ Gas delivered!")

        # Jet fuel message with context
        base_context = self._gather_agent_context(agent_id)

        jet_fuel_messages = {
            "primary": f"""🚀 JET FUEL DELIVERY!

LEARNINGS FROM PREVIOUS AGENT:
{base_context}

STRATEGIC PRIORITIES:
- Focus on high-impact repositories
- Maintain momentum through completion
- Coordinate with next agent

START WITH EVERYTHING YOU NEED! 🔥""",

            "safety": f"""🚀 JET FUEL SAFETY DELIVERY!

CRITICAL LEARNINGS:
{base_context}

RECOVERY PROTOCOLS:
- Assess current blockers
- Prioritize remaining high-value repos
- Request assistance if needed

SAFETY FUEL ENGAGED! 🔥""",

            "completion": f"""🚀 JET FUEL COMPLETION BURN!

FINAL PUSH CONTEXT:
{base_context}

COMPLETION OBJECTIVES:
- Finish all assigned repositories
- Document completion status
- Prepare handover for next phase

UNLIMITED FUEL FOR FINAL BURN! 🔥"""
        }

        return jet_fuel_messages.get(gas_type, "🚀 JET FUEL DELIVERED!")

    def _gather_agent_context(self, agent_id: str) -> str:
        """Gather context about agent's work for jet fuel messages."""
        try:
            # Get recent swarm brain entries for this agent
            context_items = []

            swarm_brain_path = self.workspace_root / "swarm_brain"
            if swarm_brain_path.exists():
                # Look for recent learnings
                learnings_path = swarm_brain_path / "learnings"
                if learnings_path.exists():
                    learning_files = list(learnings_path.glob("*.md"))[:3]  # Recent 3 files
                    for file_path in learning_files:
                        try:
                            content = file_path.read_text(encoding='utf-8')[:200]  # First 200 chars
                            context_items.append(f"- {file_path.stem}: {content}...")
                        except:
                            continue

            if context_items:
                return "\n".join(context_items)
            else:
                return "- Maintain high standards\n- Focus on quality over speed\n- Document key learnings"

        except Exception as e:
            logger.warning(f"Could not gather agent context: {e}")
            return "- Standard operating procedures\n- Quality assurance\n- Documentation"

    def _send_gas_message(self, agent_id: str, message: str) -> bool:
        """Send gas message via messaging system."""
        try:
            # Use the messaging CLI to send gas
            import subprocess
            import sys

            cmd = [
                sys.executable, "-m", "src.services.messaging_cli",
                "--send-message",
                f"--recipient={agent_id}",
                f"--content={message}",
                "--priority=urgent",
                "--tags=auto_gas_pipeline,system"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
                timeout=30
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to send gas message: {e}")
            return False

    def _log_to_swarm_brain(self, delivery_record: Dict[str, Any], success: bool):
        """Log gas delivery to Swarm Brain."""
        try:
            from swarm_brain import SwarmBrain

            brain = SwarmBrain()
            brain.share_learning(
                agent_id="AutoGasPipeline",
                title=f"Auto-Gas: {delivery_record['agent_id']} → {delivery_record['gas_type']}",
                content=f"""Progress: {delivery_record['progress']:.1f}%
Gas Type: {delivery_record['gas_type']}
Jet Fuel: {delivery_record['jet_fuel']}
Success: {success}
Timestamp: {delivery_record['timestamp']}

Message: {delivery_record['message'][:200]}...""",
                tags=["auto_gas", "pipeline", "automation", "system"]
            )

        except Exception as e:
            logger.warning(f"Could not log to Swarm Brain: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get current auto-gas pipeline status."""
        try:
            swarm_state = self.status_aggregator.aggregate_swarm_state()

            status = {
                "running": self.running,
                "monitoring_interval": self.monitoring_interval,
                "jet_fuel_enabled": getattr(self, 'jet_fuel_enabled', False),
                "agents_monitored": len(swarm_state.get("agents", {})),
                "gas_deliveries_today": len([
                    d for d in self.gas_delivery_log
                    if d["timestamp"].startswith(datetime.now().strftime("%Y-%m-%d"))
                ]),
                "total_gas_deliveries": len(self.gas_delivery_log),
                "last_delivery": self.gas_delivery_log[-1] if self.gas_delivery_log else None
            }

            return status

        except Exception as e:
            logger.error(f"Error getting pipeline status: {e}")
            return {"error": str(e)}

    def force_gas_delivery(self, agent_id: str, gas_type: str = "primary") -> bool:
        """
        Force immediate gas delivery to agent (emergency use).

        Args:
            agent_id: Target agent
            gas_type: Type of gas to deliver

        Returns:
            Success status
        """
        try:
            logger.info(f"🚨 Force gas delivery requested: {agent_id} ({gas_type})")

            # Create emergency gas message
            emergency_message = f"""🚨 EMERGENCY GAS DELIVERY!

FORCED {gas_type.upper()} GAS - Execute immediately!
This is an emergency fuel delivery outside normal pipeline timing.

Continue mission execution!"""

            success = self._send_gas_message(agent_id, emergency_message)

            if success:
                # Log emergency delivery
                delivery_record = {
                    "timestamp": datetime.now().isoformat(),
                    "agent_id": agent_id,
                    "progress": -1,  # Emergency delivery
                    "gas_type": f"emergency_{gas_type}",
                    "message": emergency_message,
                    "jet_fuel": False
                }
                self.gas_delivery_log.append(delivery_record)

                logger.info(f"✅ Emergency gas delivered to {agent_id}")
            else:
                logger.error(f"❌ Emergency gas delivery failed for {agent_id}")

            return success

        except Exception as e:
            logger.error(f"Error in force gas delivery: {e}")
            return False
=======
🚀 AUTOMATED GAS PIPELINE SYSTEM
=======
Auto-Gas Pipeline System - UNLIMITED FUEL SOLUTION
=================================================
>>>>>>> origin/codex/build-tsla-morning-report-system

Automated gas/fuel delivery system for perpetual agent pipeline operation.

Features:
- Continuous status.json monitoring
- Progress-based gas delivery (75%, 90%, 100%)
- FSM state tracking
- Jet fuel optimization
- Swarm Brain integration
- Discord status reporting

V2 Compliance: <400 lines, SOLID principles, comprehensive error handling
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import logging
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import os

from .agent_status.aggregator import SwarmStateAggregator

<<<<<<< HEAD
__all__ = [
    "AutoGasPipelineSystem",
    "PipelineMonitorIntegration",
    "JetFuelOptimizer",
    "AgentState",
    "PipelineAgent",
]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
logger = logging.getLogger(__name__)


class AutoGasPipelineSystem:
    """
    Auto-Gas Pipeline System - Prevents pipeline stalls through automated fuel delivery.

    Monitors agent progress and automatically sends gas at optimal intervals:
    - 75%: Primary gas delivery
    - 90%: Safety gas delivery
    - 100%: Completion gas delivery
    """

    def __init__(self, workspace_root: Optional[Path] = None, monitoring_interval: int = 60):
        """Initialize the auto-gas pipeline system."""
        self.workspace_root = workspace_root or Path.cwd()
        self.monitoring_interval = monitoring_interval  # seconds
        self.running = False
        self.monitor_thread = None

        # Initialize components
        self.status_aggregator = SwarmStateAggregator(self.workspace_root)
        self.agent_progress_cache: Dict[str, Dict[str, Any]] = {}
        self.gas_delivery_log: List[Dict[str, Any]] = []

        # Jet fuel optimization
        self.agent_velocity_history: Dict[str, List[float]] = {}
        self.adaptive_thresholds: Dict[str, Dict[str, float]] = {}

        logger.info("✅ Auto-Gas Pipeline System initialized")

    def start(self, jet_fuel: bool = False) -> bool:
        """
        Start the auto-gas pipeline monitoring.

        Args:
            jet_fuel: Enable jet fuel optimization

        Returns:
            Success status
        """
        if self.running:
            logger.warning("Auto-Gas Pipeline already running")
            return True

        try:
            self.running = True
            self.jet_fuel_enabled = jet_fuel

            # Start monitoring thread
            self.monitor_thread = threading.Thread(
                target=self._monitoring_loop,
                daemon=True,
                name="AutoGasMonitor"
            )
            self.monitor_thread.start()

            logger.info(f"🚀 Auto-Gas Pipeline started (Jet Fuel: {jet_fuel})")
            logger.info(f"   Monitoring interval: {self.monitoring_interval}s")
            logger.info("   Thresholds: 75%, 90%, 100%")

            return True

        except Exception as e:
            logger.error(f"Failed to start Auto-Gas Pipeline: {e}")
            self.running = False
            return False

    def stop(self) -> bool:
        """Stop the auto-gas pipeline monitoring."""
        if not self.running:
            return True

        try:
            self.running = False

            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=5)

            logger.info("🛑 Auto-Gas Pipeline stopped")
            return True

        except Exception as e:
            logger.error(f"Error stopping Auto-Gas Pipeline: {e}")
            return False

    def _monitoring_loop(self):
        """Main monitoring loop that runs continuously."""
        logger.info("🔄 Auto-Gas Pipeline monitoring loop started")

        while self.running:
            try:
                self._monitor_agents()
                time.sleep(self.monitoring_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.monitoring_interval)

        logger.info("🔄 Auto-Gas Pipeline monitoring loop ended")

    def _monitor_agents(self):
        """Monitor all agents and deliver gas as needed."""
        try:
            # Get current swarm state
            swarm_state = self.status_aggregator.aggregate_swarm_state()

            if not swarm_state or "agents" not in swarm_state:
                return

            agents = swarm_state["agents"]

            for agent_id, agent_data in agents.items():
                if agent_data.get("status") != "active":
                    continue

                # Calculate progress for this agent
                progress = self._calculate_agent_progress(agent_data)

                if progress is not None:
                    # Check if gas should be delivered
                    gas_needed = self._check_gas_requirements(agent_id, progress)

                    if gas_needed:
                        self._deliver_gas(agent_id, progress, gas_needed)

        except Exception as e:
            logger.error(f"Error monitoring agents: {e}")

    def _calculate_agent_progress(self, agent_data: Dict[str, Any]) -> Optional[float]:
        """
        Calculate agent progress percentage.

        Args:
            agent_data: Agent status data

        Returns:
            Progress percentage (0-100) or None if cannot calculate
        """
        try:
            # Get completed and total tasks from agent data
            completed_tasks = agent_data.get("completed_tasks", [])
            current_tasks = agent_data.get("current_tasks", [])

            # Parse repo completion patterns
            completed_repos = self._count_repo_completions(completed_tasks)
            total_assigned_repos = self._get_total_assigned_repos(agent_data)

            if total_assigned_repos == 0:
                return None

            progress = (completed_repos / total_assigned_repos) * 100
            return min(progress, 100.0)  # Cap at 100%

        except Exception as e:
            logger.warning(f"Could not calculate progress for agent: {e}")
            return None

    def _count_repo_completions(self, completed_tasks: List[str]) -> int:
        """Count completed repositories from task list."""
        completed_count = 0

        for task in completed_tasks:
            task_str = str(task).lower()
            # Look for repo completion patterns
            if any(pattern in task_str for pattern in [
                "repo #", "repo_", "repository", "repo complete",
                "repo done", "repo finished", "repo consolidated"
            ]):
                completed_count += 1

        return completed_count

    def _get_total_assigned_repos(self, agent_data: Dict[str, Any]) -> int:
        """Get total repositories assigned to agent."""
        # Check various fields for repo assignment info
        assignment_fields = [
            "assigned_repos", "total_repos", "repo_range",
            "repos_assigned", "mission_repos"
        ]

        for field in assignment_fields:
            if field in agent_data:
                value = agent_data[field]
                if isinstance(value, int):
                    return value
                elif isinstance(value, str):
                    # Try to parse "X-Y" range format
                    if "-" in value:
                        try:
                            start, end = map(int, value.split("-"))
                            return end - start + 1
                        except ValueError:
                            continue

        # Default: try to infer from agent ID pattern (Agent-1 = repos 1-10, etc.)
        agent_id = agent_data.get("agent_id", "")
        if agent_id.startswith("Agent-"):
            try:
                agent_num = int(agent_id.split("-")[1])
                # Simple mapping: Agent-1 = 10 repos, Agent-2 = 15 repos, etc.
                return max(10, agent_num * 5 + 5)
            except (ValueError, IndexError):
                pass

        return 10  # Default fallback

    def _check_gas_requirements(self, agent_id: str, progress: float) -> Optional[str]:
        """
        Check if gas delivery is needed based on progress.

        Args:
            agent_id: Agent identifier
            progress: Current progress percentage

        Returns:
            Gas type needed ("primary", "safety", "completion") or None
        """
        # Get adaptive thresholds for this agent
        thresholds = self._get_adaptive_thresholds(agent_id)

        # Check completion gas (100%)
        if progress >= 100.0 and not self._gas_already_sent(agent_id, "completion"):
            return "completion"

        # Check safety gas (90%)
        if progress >= thresholds["safety"] and not self._gas_already_sent(agent_id, "safety"):
            return "safety"

        # Check primary gas (75%)
        if progress >= thresholds["primary"] and not self._gas_already_sent(agent_id, "primary"):
            return "primary"

        return None

    def _get_adaptive_thresholds(self, agent_id: str) -> Dict[str, float]:
        """Get adaptive gas delivery thresholds for agent."""
        if agent_id in self.adaptive_thresholds:
            return self.adaptive_thresholds[agent_id]

        # Calculate based on agent velocity history
        velocity = self._calculate_agent_velocity(agent_id)

        if velocity > 1.5:  # Fast agent
            thresholds = {"primary": 70.0, "safety": 85.0}
        elif velocity < 0.7:  # Methodical agent
            thresholds = {"primary": 80.0, "safety": 92.0}
        else:  # Normal agent
            thresholds = {"primary": 75.0, "safety": 90.0}

        self.adaptive_thresholds[agent_id] = thresholds
        return thresholds

    def _calculate_agent_velocity(self, agent_id: str) -> float:
        """Calculate agent's repository completion velocity."""
        if agent_id not in self.agent_velocity_history:
            return 1.0  # Default velocity

        history = self.agent_velocity_history[agent_id]
        if len(history) < 2:
            return 1.0

        # Calculate repos per cycle (assuming daily cycles)
        recent_velocity = sum(history[-7:]) / len(history[-7:])  # 7-day average
        return max(0.1, recent_velocity)  # Minimum velocity

    def _gas_already_sent(self, agent_id: str, gas_type: str) -> bool:
        """Check if gas of this type was already sent to agent."""
        for delivery in self.gas_delivery_log:
            if (delivery["agent_id"] == agent_id and
                delivery["gas_type"] == gas_type and
                delivery["timestamp"] > datetime.now() - timedelta(hours=24)):  # Within last 24h
                return True
        return False

    def _deliver_gas(self, agent_id: str, progress: float, gas_type: str):
        """
        Deliver gas to agent.

        Args:
            agent_id: Target agent
            progress: Current progress
            gas_type: Type of gas ("primary", "safety", "completion")
        """
        try:
            # Create gas message
            gas_message = self._create_gas_message(agent_id, progress, gas_type)

            # Log delivery
            delivery_record = {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "progress": progress,
                "gas_type": gas_type,
                "message": gas_message,
                "jet_fuel": self.jet_fuel_enabled
            }
            self.gas_delivery_log.append(delivery_record)

            # Send via messaging system
            success = self._send_gas_message(agent_id, gas_message)

            # Log to Swarm Brain
            self._log_to_swarm_brain(delivery_record, success)

            status = "✅" if success else "❌"
            logger.info(f"{status} Auto-Gas delivered to {agent_id}: {gas_type} at {progress:.1f}%")

        except Exception as e:
            logger.error(f"Failed to deliver gas to {agent_id}: {e}")

    def _create_gas_message(self, agent_id: str, progress: float, gas_type: str) -> str:
        """Create gas delivery message."""
        if not self.jet_fuel_enabled:
            # Standard gas message
            gas_messages = {
                "primary": "⛽ You're next! Execute now!",
                "safety": "⛽ Safety gas - keep pushing!",
                "completion": "⛽ Final push - complete the mission!"
            }
            return gas_messages.get(gas_type, "⛽ Gas delivered!")

        # Jet fuel message with context
        base_context = self._gather_agent_context(agent_id)

        jet_fuel_messages = {
            "primary": f"""🚀 JET FUEL DELIVERY!

LEARNINGS FROM PREVIOUS AGENT:
{base_context}

STRATEGIC PRIORITIES:
- Focus on high-impact repositories
- Maintain momentum through completion
- Coordinate with next agent

START WITH EVERYTHING YOU NEED! 🔥""",

            "safety": f"""🚀 JET FUEL SAFETY DELIVERY!

CRITICAL LEARNINGS:
{base_context}

RECOVERY PROTOCOLS:
- Assess current blockers
- Prioritize remaining high-value repos
- Request assistance if needed

SAFETY FUEL ENGAGED! 🔥""",

            "completion": f"""🚀 JET FUEL COMPLETION BURN!

FINAL PUSH CONTEXT:
{base_context}

COMPLETION OBJECTIVES:
- Finish all assigned repositories
- Document completion status
- Prepare handover for next phase

UNLIMITED FUEL FOR FINAL BURN! 🔥"""
        }

        return jet_fuel_messages.get(gas_type, "🚀 JET FUEL DELIVERED!")

    def _gather_agent_context(self, agent_id: str) -> str:
        """Gather context about agent's work for jet fuel messages."""
        try:
            # Get recent swarm brain entries for this agent
            context_items = []

            swarm_brain_path = self.workspace_root / "swarm_brain"
            if swarm_brain_path.exists():
                # Look for recent learnings
                learnings_path = swarm_brain_path / "learnings"
                if learnings_path.exists():
                    learning_files = list(learnings_path.glob("*.md"))[:3]  # Recent 3 files
                    for file_path in learning_files:
                        try:
                            content = file_path.read_text(encoding='utf-8')[:200]  # First 200 chars
                            context_items.append(f"- {file_path.stem}: {content}...")
                        except:
                            continue

            if context_items:
                return "\n".join(context_items)
            else:
                return "- Maintain high standards\n- Focus on quality over speed\n- Document key learnings"

        except Exception as e:
            logger.warning(f"Could not gather agent context: {e}")
            return "- Standard operating procedures\n- Quality assurance\n- Documentation"

    def _send_gas_message(self, agent_id: str, message: str) -> bool:
        """Send gas message via messaging system."""
        try:
            # Use the messaging CLI to send gas
            import subprocess
            import sys

            cmd = [
                sys.executable, "-m", "src.services.messaging_cli",
                "--send-message",
                f"--recipient={agent_id}",
                f"--content={message}",
                "--priority=urgent",
                "--tags=auto_gas_pipeline,system"
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.workspace_root,
                timeout=30
            )

            return result.returncode == 0

        except Exception as e:
            logger.error(f"Failed to send gas message: {e}")
            return False

    def _log_to_swarm_brain(self, delivery_record: Dict[str, Any], success: bool):
        """Log gas delivery to Swarm Brain."""
        try:
            from swarm_brain import SwarmBrain

            brain = SwarmBrain()
            brain.share_learning(
                agent_id="AutoGasPipeline",
                title=f"Auto-Gas: {delivery_record['agent_id']} → {delivery_record['gas_type']}",
                content=f"""Progress: {delivery_record['progress']:.1f}%
Gas Type: {delivery_record['gas_type']}
Jet Fuel: {delivery_record['jet_fuel']}
Success: {success}
Timestamp: {delivery_record['timestamp']}

Message: {delivery_record['message'][:200]}...""",
                tags=["auto_gas", "pipeline", "automation", "system"]
            )

        except Exception as e:
            logger.warning(f"Could not log to Swarm Brain: {e}")

    def get_status(self) -> Dict[str, Any]:
        """Get current auto-gas pipeline status."""
        try:
            swarm_state = self.status_aggregator.aggregate_swarm_state()

            status = {
                "running": self.running,
                "monitoring_interval": self.monitoring_interval,
                "jet_fuel_enabled": getattr(self, 'jet_fuel_enabled', False),
                "agents_monitored": len(swarm_state.get("agents", {})),
                "gas_deliveries_today": len([
                    d for d in self.gas_delivery_log
                    if d["timestamp"].startswith(datetime.now().strftime("%Y-%m-%d"))
                ]),
                "total_gas_deliveries": len(self.gas_delivery_log),
                "last_delivery": self.gas_delivery_log[-1] if self.gas_delivery_log else None
            }

            return status

        except Exception as e:
            logger.error(f"Error getting pipeline status: {e}")
            return {"error": str(e)}

    def force_gas_delivery(self, agent_id: str, gas_type: str = "primary") -> bool:
        """
        Force immediate gas delivery to agent (emergency use).

        Args:
            agent_id: Target agent
            gas_type: Type of gas to deliver

        Returns:
            Success status
        """
        try:
            logger.info(f"🚨 Force gas delivery requested: {agent_id} ({gas_type})")

            # Create emergency gas message
            emergency_message = f"""🚨 EMERGENCY GAS DELIVERY!

FORCED {gas_type.upper()} GAS - Execute immediately!
This is an emergency fuel delivery outside normal pipeline timing.

Continue mission execution!"""

            success = self._send_gas_message(agent_id, emergency_message)

            if success:
                # Log emergency delivery
                delivery_record = {
                    "timestamp": datetime.now().isoformat(),
                    "agent_id": agent_id,
                    "progress": -1,  # Emergency delivery
                    "gas_type": f"emergency_{gas_type}",
                    "message": emergency_message,
                    "jet_fuel": False
                }
                self.gas_delivery_log.append(delivery_record)

                logger.info(f"✅ Emergency gas delivered to {agent_id}")
            else:
                logger.error(f"❌ Emergency gas delivery failed for {agent_id}")

            return success

        except Exception as e:
            logger.error(f"Error in force gas delivery: {e}")
            return False
>>>>>>> origin/codex/build-tsla-morning-report-system


# CLI Interface
def main():
<<<<<<< HEAD
<<<<<<< HEAD
    """CLI interface for auto-gas pipeline system."""
    import argparse

    parser = argparse.ArgumentParser(description="Auto-Gas Pipeline System")
    parser.add_argument("action", choices=["start", "stop", "status", "force-gas"],
                       help="Action to perform")
    parser.add_argument("--interval", type=int, default=60,
                       help="Monitoring interval in seconds (default: 60)")
    parser.add_argument("--jet-fuel", action="store_true",
                       help="Enable jet fuel optimization")
    parser.add_argument("--agent", help="Agent ID for force-gas action")
    parser.add_argument("--gas-type", choices=["primary", "safety", "completion"],
                       default="primary", help="Gas type for force-gas action")

    args = parser.parse_args()

    system = AutoGasPipelineSystem(monitoring_interval=args.interval)

    if args.action == "start":
        success = system.start(jet_fuel=args.jet_fuel)
        if success:
            print("✅ Auto-Gas Pipeline started")
            print(f"   Jet Fuel: {args.jet_fuel}")
            print(f"   Monitoring: {args.interval}s intervals")
            print("   Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                system.stop()
        else:
            print("❌ Failed to start Auto-Gas Pipeline")
            exit(1)

    elif args.action == "stop":
        success = system.stop()
        print("✅ Auto-Gas Pipeline stopped" if success else "❌ Failed to stop")

    elif args.action == "status":
        status = system.get_status()
        if "error" in status:
            print(f"❌ Error: {status['error']}")
            exit(1)

        print("🚀 Auto-Gas Pipeline Status")
        print("=" * 40)
        print(f"Running: {'✅' if status['running'] else '❌'}")
        print(f"Monitoring Interval: {status['monitoring_interval']}s")
        print(f"Jet Fuel: {'✅' if status['jet_fuel_enabled'] else '❌'}")
        print(f"Agents Monitored: {status['agents_monitored']}")
        print(f"Deliveries Today: {status['gas_deliveries_today']}")
        print(f"Total Deliveries: {status['total_gas_deliveries']}")

        if status['last_delivery']:
            last = status['last_delivery']
            print(f"Last Delivery: {last['agent_id']} ({last['gas_type']}) at {last['progress']:.1f}%")

    elif args.action == "force-gas":
        if not args.agent:
            print("❌ --agent required for force-gas action")
            exit(1)

        success = system.force_gas_delivery(args.agent, args.gas_type)
        print(f"✅ Emergency gas delivered to {args.agent}" if success
              else f"❌ Failed to deliver emergency gas to {args.agent}")


if __name__ == "__main__":
    main()
=======
    """Run the auto-gas pipeline system."""
    import sys
=======
    """CLI interface for auto-gas pipeline system."""
    import argparse
>>>>>>> origin/codex/build-tsla-morning-report-system

    parser = argparse.ArgumentParser(description="Auto-Gas Pipeline System")
    parser.add_argument("action", choices=["start", "stop", "status", "force-gas"],
                       help="Action to perform")
    parser.add_argument("--interval", type=int, default=60,
                       help="Monitoring interval in seconds (default: 60)")
    parser.add_argument("--jet-fuel", action="store_true",
                       help="Enable jet fuel optimization")
    parser.add_argument("--agent", help="Agent ID for force-gas action")
    parser.add_argument("--gas-type", choices=["primary", "safety", "completion"],
                       default="primary", help="Gas type for force-gas action")

    args = parser.parse_args()

    system = AutoGasPipelineSystem(monitoring_interval=args.interval)

    if args.action == "start":
        success = system.start(jet_fuel=args.jet_fuel)
        if success:
            print("✅ Auto-Gas Pipeline started")
            print(f"   Jet Fuel: {args.jet_fuel}")
            print(f"   Monitoring: {args.interval}s intervals")
            print("   Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                system.stop()
        else:
            print("❌ Failed to start Auto-Gas Pipeline")
            exit(1)

    elif args.action == "stop":
        success = system.stop()
        print("✅ Auto-Gas Pipeline stopped" if success else "❌ Failed to stop")

    elif args.action == "status":
        status = system.get_status()
        if "error" in status:
            print(f"❌ Error: {status['error']}")
            exit(1)

        print("🚀 Auto-Gas Pipeline Status")
        print("=" * 40)
        print(f"Running: {'✅' if status['running'] else '❌'}")
        print(f"Monitoring Interval: {status['monitoring_interval']}s")
        print(f"Jet Fuel: {'✅' if status['jet_fuel_enabled'] else '❌'}")
        print(f"Agents Monitored: {status['agents_monitored']}")
        print(f"Deliveries Today: {status['gas_deliveries_today']}")
        print(f"Total Deliveries: {status['total_gas_deliveries']}")

        if status['last_delivery']:
            last = status['last_delivery']
            print(f"Last Delivery: {last['agent_id']} ({last['gas_type']}) at {last['progress']:.1f}%")

    elif args.action == "force-gas":
        if not args.agent:
            print("❌ --agent required for force-gas action")
            exit(1)

        success = system.force_gas_delivery(args.agent, args.gas_type)
        print(f"✅ Emergency gas delivered to {args.agent}" if success
              else f"❌ Failed to deliver emergency gas to {args.agent}")


if __name__ == "__main__":
<<<<<<< HEAD
    main()
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
    main()
>>>>>>> origin/codex/build-tsla-morning-report-system
