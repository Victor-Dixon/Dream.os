#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Pipeline Monitor Integration - Integration Layer
===============================================

Integration layer combining pipeline, optimizer, and monitoring.
@registry docs/recovery/recovery_registry.yaml#src-core-gas-pipeline-core-integration
"""

from datetime import datetime
from src.swarm_brain.swarm_memory import SwarmMemory

from .pipeline import AutoGasPipelineSystem
from .optimizer import JetFuelOptimizer


class PipelineMonitorIntegration:
    """
    🔥 THE SOPHISTICATED SOLUTION - UNLIMITED GAS!

    Integrates:
    1. Status.json monitoring → Detect progress
    2. FSM state tracking → Agent lifecycle
    3. Messaging system → Auto-gas delivery
    4. Swarm Brain → Learning and logging
    5. Jet Fuel Optimizer → Smart timing + rich context

    Result: NOTHING BUT JET FUEL - Agents never run out, always have context!
    """

    def __init__(self):
        self.pipeline = AutoGasPipelineSystem()
        self.optimizer = JetFuelOptimizer(self.pipeline)
        self.swarm_memory = SwarmMemory(agent_id='PipelineMonitor')

    def start_perpetual_motion(self, interval: int = 60):
        """
        🚀 START THE PERPETUAL MOTION ENGINE!

        This runs FOREVER:
        - Monitors status.json every X seconds
        - Detects 75%, 90%, 100% completion
        - Auto-sends JET FUEL (not just gas!)
        - Logs to Swarm Brain
        - Updates FSM states

        Agents NEVER run out of fuel!
        Pipeline NEVER breaks!
        Swarm NEVER stalls!

        THIS IS THE SOLUTION! ⚡
        """
        print("🔥🔥🔥 PERPETUAL MOTION ENGINE STARTING! 🔥🔥🔥")
        print("⛽ Unlimited gas mode activated!")
        print("🚀 Jet fuel optimization enabled!")
        print("🐝 SWARM WILL NEVER STOP!\n")

        # Log to Swarm Brain
        self.swarm_memory.share_learning(
            title='Perpetual Motion Engine Activated',
            content=f'Auto-gas pipeline started at {datetime.now().isoformat()}. Monitoring all agents, sending jet fuel automatically. Swarm perpetual motion engaged!',
            tags=['pipeline', 'auto-gas', 'perpetual-motion', 'system']
        )

        # Start monitoring
        self.pipeline.start_monitoring(interval=interval)

    def get_status_dashboard(self) -> str:
        """Get formatted dashboard of pipeline status."""
        status = self.pipeline.get_pipeline_status()

        dashboard = f"""
╔══════════════════════════════════════════════════════════════╗
║  🚀 AUTO-GAS PIPELINE SYSTEM - STATUS DASHBOARD             ║
╚══════════════════════════════════════════════════════════════╝

Timestamp: {status['timestamp']}

AGENT STATUS:
"""

        for agent_id, agent_status in status['agents'].items():
            dashboard += f"""
{agent_id}:
  Repos: {agent_status['repos']}
  Progress: {agent_status['progress']}
  State: {agent_status['state']}
  Gas Sent: 75%={agent_status['gas_sent_75']} | 90%={agent_status['gas_sent_90']} | 100%={agent_status['gas_sent_100']}
  Next: {agent_status['next_agent']}
"""

        return dashboard
