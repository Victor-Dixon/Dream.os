#!/usr/bin/env python3
<!-- SSOT Domain: core -->
"""
🚀 AUTOMATED GAS PIPELINE SYSTEM
Monitors status.json + FSM → Auto-sends gas at 75-80% → UNLIMITED FUEL!

Backward compatibility shim for auto_gas_pipeline_system refactoring.
Maintains existing import paths while using new modular structure.

V2 Compliance: <50 lines (shim only)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-19
License: MIT
"""

from __future__ import annotations

# Import from new modular structure
from .gas_pipeline.core.pipeline import AutoGasPipelineSystem
from .gas_pipeline.core.integration import PipelineMonitorIntegration
from .gas_pipeline.core.optimizer import JetFuelOptimizer
from .gas_pipeline.core.models import AgentState, PipelineAgent

__all__ = [
    "AutoGasPipelineSystem",
    "PipelineMonitorIntegration",
    "JetFuelOptimizer",
    "AgentState",
    "PipelineAgent",
]


# CLI Interface
def main():
    """Run the auto-gas pipeline system."""
    import sys

    monitor = PipelineMonitorIntegration()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "start":
            # Start perpetual motion!
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            monitor.start_perpetual_motion(interval=interval)

        elif command == "status":
            # Show current pipeline status
            print(monitor.get_status_dashboard())

        elif command == "force-gas":
            # Manually send gas
            agent_id = sys.argv[2] if len(sys.argv) > 2 else "Agent-1"
            monitor.pipeline.force_gas_send(agent_id, "MANUAL_OVERRIDE")
            print(f"⛽ Manual gas sent from {agent_id}")

    else:
        print("""
🚀 AUTO-GAS PIPELINE SYSTEM

Usage:
  python -m src.core.auto_gas_pipeline_system start [interval]
    - Start perpetual motion engine
    - interval: seconds between checks (default: 60)
  
  python -m src.core.auto_gas_pipeline_system status
    - Show current pipeline status dashboard
  
  python -m src.core.auto_gas_pipeline_system force-gas [agent_id]
    - Manually send gas from agent (emergency use)

Examples:
  python -m src.core.auto_gas_pipeline_system start 30
    - Monitor every 30 seconds, auto-send gas
  
  python -m src.core.auto_gas_pipeline_system status
    - Check current pipeline state

🔥 PERPETUAL MOTION - UNLIMITED GAS - SWARM NEVER STOPS! 🐝⚡
""")


if __name__ == "__main__":
    main()
