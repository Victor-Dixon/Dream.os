#!/usr/bin/env python3
"""
Full Swarm Coordination Example
===============================

This example demonstrates how to coordinate all agents (1-8) in a full swarm operation.
It shows advanced swarm intelligence patterns, task distribution, and collective decision making.

Usage:
    python examples/full_swarm.py

Requirements:
    - .env file with DISCORD_BOT_TOKEN and DISCORD_GUILD_ID
    - All agent workspaces (Agent-1 through Agent-8)
    - Messaging system operational
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_cli import MessagingCLI
from src.core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority
from src.services.unified_messaging_service import UnifiedMessagingService


class SwarmCoordinator:
    """Coordinates full swarm operations."""

    def __init__(self):
        self.messaging_service = UnifiedMessagingService()
        self.agents = [f"Agent-{i}" for i in range(1, 9)]  # Agent-1 through Agent-8
        self.active_tasks = {}
        self.swarm_status = {}

    async def initialize_swarm(self) -> bool:
        """Initialize all agents in the swarm."""
        print("🚀 INITIALIZING FULL SWARM...")

        success_count = 0
        for agent in self.agents:
            workspace = Path(f"agent_workspaces/{agent}")
            if not workspace.exists():
                print(f"❌ {agent} workspace missing")
                continue

            # Send initialization message
            init_success = await self.messaging_service.send_message(
                agent=agent,
                message=f"""SYSTEM: {agent} activated for full swarm operation.
SWARM STATUS: All agents online and synchronized.
PROTOCOL: A2A coordination enabled, task distribution active.
COORDINATION: Respond to swarm commands and coordinate with neighboring agents.""",
                priority="high",
                use_pyautogui=True,
                message_category="c2a"
            )

            if init_success:
                success_count += 1
                self.swarm_status[agent] = "INITIALIZED"
                print(f"✅ {agent} initialized")
            else:
                print(f"❌ {agent} initialization failed")

        print(f"\n📊 Swarm initialization: {success_count}/{len(self.agents)} agents ready")
        return success_count == len(self.agents)

    async def distribute_swarm_tasks(self) -> bool:
        """Distribute specialized tasks across the swarm."""
        print("\n📋 DISTRIBUTING SWARM TASKS...")

        # Define specialized roles for each agent
        swarm_roles = {
            "Agent-1": {
                "role": "Code Quality Lead",
                "tasks": ["Code review", "Testing", "Documentation"],
                "specialty": "Quality Assurance"
            },
            "Agent-2": {
                "role": "System Architecture Lead",
                "tasks": ["Design patterns", "System integration", "Performance optimization"],
                "specialty": "System Design"
            },
            "Agent-3": {
                "role": "Database & Data Lead",
                "tasks": ["Data modeling", "Query optimization", "Data validation"],
                "specialty": "Data Management"
            },
            "Agent-4": {
                "role": "Captain & Coordination Lead",
                "tasks": ["Swarm coordination", "Task assignment", "Status monitoring"],
                "specialty": "Leadership"
            },
            "Agent-5": {
                "role": "Frontend & UI Lead",
                "tasks": ["User interface", "User experience", "Responsive design"],
                "specialty": "Frontend Development"
            },
            "Agent-6": {
                "role": "Testing & QA Lead",
                "tasks": ["Automated testing", "Performance testing", "Bug tracking"],
                "specialty": "Quality Engineering"
            },
            "Agent-7": {
                "role": "Documentation & CLI Lead",
                "tasks": ["API documentation", "CLI tools", "User guides"],
                "specialty": "Technical Writing"
            },
            "Agent-8": {
                "role": "DevOps & Infrastructure Lead",
                "tasks": ["CI/CD pipelines", "Infrastructure", "Deployment automation"],
                "specialty": "DevOps"
            }
        }

        success_count = 0
        for agent, role_info in swarm_roles.items():
            task_message = f"""TASK ASSIGNMENT: {role_info['role']}
Specialty: {role_info['specialty']}
Assigned tasks: {', '.join(role_info['tasks'])}
Timeline: Active swarm operation
Priority: P0 - Critical for swarm intelligence
Capabilities required: {role_info['specialty']} expertise, swarm coordination, A2A communication
Coordinate with: All swarm agents for collective intelligence"""

            task_success = await self.messaging_service.send_message(
                agent=agent,
                message=task_message,
                priority="urgent",
                use_pyautogui=True,
                message_category="c2a"
            )

            if task_success:
                success_count += 1
                self.active_tasks[agent] = role_info
                self.swarm_status[agent] = "TASK_ASSIGNED"
                print(f"✅ {agent} assigned: {role_info['role']}")
            else:
                print(f"❌ {agent} task assignment failed")

        print(f"\n📊 Task distribution: {success_count}/{len(self.agents)} agents assigned")
        return success_count == len(self.agents)

    async def initiate_swarm_intelligence(self) -> bool:
        """Initiate collective swarm intelligence operations."""
        print("\n🧠 INITIATING SWARM INTELLIGENCE...")

        # Send swarm intelligence activation to all agents
        swarm_activation = """SWARM INTELLIGENCE ACTIVATION:
🐝 WE. ARE. SWARM. ⚡️🔥

All agents now operating in collective intelligence mode:
- A2A communication protocols active
- Task specialization engaged
- Consensus-driven decision making
- Parallel processing enabled
- Cross-agent coordination online

Swarm objectives:
1. Collective problem solving
2. Distributed task execution
3. Quality assurance through consensus
4. Continuous improvement cycles
5. Emergent intelligence patterns

Report swarm readiness and begin coordinated operations."""

        success_count = 0
        for agent in self.agents:
            activation_success = await self.messaging_service.send_message(
                agent=agent,
                message=swarm_activation,
                priority="urgent",
                use_pyautogui=True,
                message_category="c2a"
            )

            if activation_success:
                success_count += 1
                self.swarm_status[agent] = "SWARM_ACTIVE"
                print(f"✅ {agent} swarm intelligence activated")
            else:
                print(f"❌ {agent} swarm activation failed")

        print(f"\n📊 Swarm intelligence: {success_count}/{len(self.agents)} agents activated")
        return success_count == len(self.agents)

    async def monitor_swarm_status(self) -> Dict[str, Any]:
        """Monitor the current status of all swarm agents."""
        print("\n📊 MONITORING SWARM STATUS...")

        status_results = {}

        for agent in self.agents:
            status_request = await self.messaging_service.send_message(
                agent=agent,
                message="SWARM STATUS REQUEST: Report current operational status, active tasks, and any coordination needs.",
                priority="regular",
                use_pyautogui=True,
                message_category="c2a"
            )

            status_results[agent] = {
                "status_requested": status_request,
                "last_known_status": self.swarm_status.get(agent, "UNKNOWN"),
                "assigned_role": self.active_tasks.get(agent, {}).get("role", "UNASSIGNED")
            }

        return status_results

    async def demonstrate_swarm_consensus(self) -> bool:
        """Demonstrate swarm consensus decision making."""
        print("\n🤝 DEMONSTRATING SWARM CONSENSUS...")

        consensus_topic = """CONSENSUS TOPIC: Code Review Process Standardization

Proposal: Standardize code review process across all agents with:
1. Automated linting checks
2. Peer review requirements
3. Documentation standards
4. Testing coverage minimums

Vote: APPROVE or REJECT with reasoning."""

        # Send consensus topic to all agents
        consensus_votes = []
        for agent in self.agents:
            vote_request = await self.messaging_service.send_message(
                agent=agent,
                message=consensus_topic,
                priority="high",
                use_pyautogui=True,
                message_category="c2a"
            )

            if vote_request:
                consensus_votes.append(agent)
                print(f"✅ {agent} received consensus topic")
            else:
                print(f"❌ {agent} consensus delivery failed")

        print(f"\n📊 Consensus initiated: {len(consensus_votes)}/{len(self.agents)} agents notified")
        return len(consensus_votes) > 0

    def generate_swarm_report(self) -> str:
        """Generate a comprehensive swarm status report."""
        active_agents = sum(1 for status in self.swarm_status.values() if status != "UNKNOWN")
        assigned_agents = len(self.active_tasks)

        report = f"""
🐝 FULL SWARM COORDINATION REPORT
{'='*50}

SWARM STATUS OVERVIEW:
• Total Agents: {len(self.agents)}
• Active Agents: {active_agents}
• Task Assigned: {assigned_agents}
• Swarm Intelligence: {'ACTIVE' if active_agents == len(self.agents) else 'PARTIAL'}

AGENT STATUS BREAKDOWN:
"""

        for agent in self.agents:
            status = self.swarm_status.get(agent, "UNKNOWN")
            role = self.active_tasks.get(agent, {}).get("role", "UNASSIGNED")
            report += f"• {agent}: {status} - {role}\n"

        report += f"""
COORDINATION PROTOCOLS:
• A2A Communication: {'✅ ACTIVE' if active_agents > 0 else '❌ INACTIVE'}
• Task Distribution: {'✅ COMPLETE' if assigned_agents == len(self.agents) else '❌ INCOMPLETE'}
• Swarm Intelligence: {'✅ ACTIVATED' if active_agents == len(self.agents) else '❌ PARTIAL'}
• Consensus Engine: {'✅ READY' if active_agents > 0 else '❌ OFFLINE'}

NEXT STEPS:
1. Monitor agent inboxes for responses
2. Track task completion through messaging system
3. Coordinate consensus decisions
4. Maintain swarm synchronization

🐝 WE. ARE. SWARM. ⚡️🔥
"""
        return report


async def main():
    """Main swarm coordination demonstration."""
    print("🐝 FULL SWARM COORDINATION EXAMPLE")
    print("=" * 60)

    coordinator = SwarmCoordinator()

    try:
        # Phase 1: Initialize swarm
        init_success = await coordinator.initialize_swarm()
        if not init_success:
            print("❌ Swarm initialization failed")
            return 1

        # Phase 2: Distribute tasks
        task_success = await coordinator.distribute_swarm_tasks()
        if not task_success:
            print("❌ Task distribution failed")
            return 1

        # Phase 3: Activate swarm intelligence
        intelligence_success = await coordinator.initiate_swarm_intelligence()
        if not intelligence_success:
            print("❌ Swarm intelligence activation failed")
            return 1

        # Phase 4: Monitor status
        status_results = await coordinator.monitor_swarm_status()

        # Phase 5: Demonstrate consensus
        consensus_success = await coordinator.demonstrate_swarm_consensus()

        # Phase 6: Generate report
        final_report = coordinator.generate_swarm_report()
        print(final_report)

        print("🎉 FULL SWARM COORDINATION DEMONSTRATION COMPLETE!")
        print("\n💡 To continue the swarm operation:")
        print("   1. Check agent inboxes: agent_workspaces/*/inbox/")
        print("   2. Monitor responses through messaging system")
        print("   3. Use consensus_demo.py for decision making")
        print("   4. Track progress with: python -m src.services.messaging_cli --queue-stats")

        return 0

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    print("\n🐝 WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)