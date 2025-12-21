#!/usr/bin/env python3
"""
Gas Pipeline - Main Pipeline Orchestrator
==========================================

Main pipeline orchestrator using Pipeline Pattern.
Coordinates stages: progress monitoring → gas decision → gas delivery.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from src.swarm_brain.swarm_memory import SwarmMemory

from ..core.models import AgentState, PipelineAgent
from ..core.pipeline_config import get_default_pipeline_config, setup_pipeline_agents
from ..stages.progress_monitor import calculate_progress
from ..stages.gas_decision import update_fsm_state, should_send_gas
from ..stages.gas_delivery import build_gas_message, send_gas_message, mark_gas_sent
from ..handlers.error_handler import handle_pipeline_error


class AutoGasPipelineSystem:
    """
    🚀 AUTOMATED GAS DELIVERY SYSTEM

    Monitors all agents → Detects progress → Sends gas automatically → Perpetual motion!
    """

    def __init__(self):
        self.agents: Dict[str, PipelineAgent] = {}
        self.swarm_memory = SwarmMemory(agent_id='AutoGasPipeline')
        self.workspace_path = Path("agent_workspaces")
        self.monitoring_active = False

        # Setup pipeline with default configuration
        config = get_default_pipeline_config()
        self.agents = setup_pipeline_agents(config)

    def monitor_pipeline(self, check_interval: int = 60):
        """
        🔥 PERPETUAL MOTION ENGINE

        Monitors all agents every X seconds:
        1. Check status.json for progress
        2. Calculate completion percentage
        3. Update FSM state
        4. Auto-send gas at 75%, 90%, 100%
        5. Log to Swarm Brain

        Result: Agents NEVER run out of gas!
        """
        print("🚀 AUTO-GAS PIPELINE SYSTEM ACTIVATED!")
        print(f"⏱️  Monitoring interval: {check_interval} seconds")
        print("⛽ Gas will be sent automatically at 75%, 90%, 100%")
        print("🐝 PERPETUAL MOTION ENGAGED!\n")

        self.monitoring_active = True
        cycle = 0

        while self.monitoring_active:
            cycle += 1
            print(f"\n{'='*60}")
            print(f"🔄 PIPELINE MONITOR - Cycle {cycle}")
            print(f"{'='*60}\n")

            for agent_id, agent in self.agents.items():
                try:
                    # Stage 1: Monitor progress
                    progress = calculate_progress(
                        agent_id, agent, self.workspace_path)

                    # Stage 2: Update FSM state and decide on gas
                    update_fsm_state(agent, progress)
                    gas_reasons = should_send_gas(agent, progress)

                    # Display status
                    status_emoji = {
                        AgentState.IDLE: "⏸️",
                        AgentState.STARTING: "🟡",
                        AgentState.EXECUTING: "🟢",
                        AgentState.COMPLETING: "🟠",
                        AgentState.COMPLETE: "✅",
                    }

                    emoji = status_emoji.get(agent.state, "❓")
                    print(
                        f"{emoji} {agent_id}: {progress:.1f}% | State: {agent.state.value} | Repos: {agent.repos_assigned[0]}-{agent.repos_assigned[1]}")

                    # Stage 3: Send gas if needed
                    if gas_reasons:
                        for reason in gas_reasons:
                            print(f"   ⛽ AUTO-SENDING GAS: {reason}")
                            self._send_auto_gas(agent_id, reason, progress)

                except Exception as e:
                    handle_pipeline_error(agent_id, e, {
                                          "cycle": cycle, "progress": progress if 'progress' in locals() else None})

            print(f"\n{'='*60}")
            print(f"⏱️  Next check in {check_interval} seconds...")
            print(f"{'='*60}")

            time.sleep(check_interval)

    def _send_auto_gas(self, agent_id: str, reason: str, progress: float):
        """Automatically send gas to next agent in pipeline."""
        agent = self.agents[agent_id]

        if not agent.next_agent:
            print(f"✅ {agent_id} mission complete! No next agent (end of pipeline)")
            return

        next_agent_id = agent.next_agent
        next_agent = self.agents.get(next_agent_id)

        if not next_agent:
            print(f"⚠️ Next agent {next_agent_id} not in pipeline!")
            return

        # Build and send gas message
        message = build_gas_message(agent, next_agent, reason, progress)
        success = send_gas_message(next_agent_id, message)

        if success:
            # Mark gas as sent
            mark_gas_sent(agent, reason)

            # Log to Swarm Brain
            self.swarm_memory.share_learning(
                title=f'Auto-Gas Sent: {agent_id} → {next_agent_id}',
                content=f'Progress: {progress:.1f}%, Reason: {reason}, Timestamp: {agent.last_gas_sent}',
                tags=['auto-gas', 'pipeline', 'perpetual-motion']
            )

            print(
                f"⛽ AUTO-GAS SENT: {agent_id} ({progress:.1f}%) → {next_agent_id} [{reason}]")
        else:
            print(f"❌ Failed to send gas from {agent_id} to {next_agent_id}")

    def start_monitoring(self, interval: int = 60):
        """Start the perpetual motion engine."""
        try:
            self.monitor_pipeline(check_interval=interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Pipeline monitoring stopped by user")
            self.monitoring_active = False

    def get_pipeline_status(self) -> Dict:
        """Get current pipeline status for all agents."""
        from ..stages.progress_monitor import calculate_progress

        status = {
            "timestamp": datetime.now().isoformat(),
            "agents": {}
        }

        for agent_id, agent in self.agents.items():
            progress = calculate_progress(agent_id, agent, self.workspace_path)

            status["agents"][agent_id] = {
                "repos": f"{agent.repos_assigned[0]}-{agent.repos_assigned[1]}",
                "progress": f"{progress:.1f}%",
                "state": agent.state.value,
                "current_repo": agent.current_repo,
                "gas_sent_75": agent.gas_sent_at_75,
                "gas_sent_90": agent.gas_sent_at_90,
                "gas_sent_100": agent.gas_sent_at_100,
                "next_agent": agent.next_agent or "MISSION_COMPLETE"
            }

        return status

    def force_gas_send(self, agent_id: str, reason: str = "MANUAL"):
        """Manually trigger gas send (emergency use)."""
        from ..stages.progress_monitor import calculate_progress

        progress = calculate_progress(
            agent_id, self.agents[agent_id], self.workspace_path)
        self._send_auto_gas(agent_id, reason, progress)
