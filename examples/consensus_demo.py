#!/usr/bin/env python3
"""
Swarm Consensus Demonstration
=============================

This example demonstrates swarm consensus decision-making processes.
It shows how agents can collectively reach decisions through voting,
discussion, and consensus building.

Usage:
    python examples/consensus_demo.py

Requirements:
    - .env file with DISCORD_BOT_TOKEN and DISCORD_GUILD_ID
    - Active swarm (run full_swarm.py first)
    - Messaging system operational
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import time

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.messaging_cli import MessagingCLI
from src.core.messaging_core import send_message, UnifiedMessageType, UnifiedMessagePriority
from src.services.unified_messaging_service import UnifiedMessagingService


class ConsensusEngine:
    """Manages swarm consensus decision-making processes."""

    def __init__(self):
        self.messaging_service = UnifiedMessagingService()
        self.agents = [f"Agent-{i}" for i in range(1, 9)]
        self.active_consensus = {}
        self.consensus_history = []

    async def initiate_consensus_process(self, topic: str, options: List[str],
                                       deadline_minutes: int = 30) -> str:
        """
        Initiate a consensus decision-making process.

        Args:
            topic: The decision topic
            options: List of voting options
            deadline_minutes: Time limit for consensus

        Returns:
            Consensus ID for tracking
        """
        consensus_id = f"CONSENSUS_{int(time.time())}"

        deadline = datetime.now() + timedelta(minutes=deadline_minutes)

        consensus_message = f"""🐝 SWARM CONSENSUS INITIATED
Consensus ID: {consensus_id}

TOPIC: {topic}

OPTIONS:
{chr(10).join(f"{i+1}. {option}" for i, option in enumerate(options))}

VOTING INSTRUCTIONS:
- Reply with your vote: "VOTE: [option_number] - [reasoning]"
- Discuss with other agents using A2A messaging
- Consensus reached when majority agrees or deadline reached

DEADLINE: {deadline.strftime('%H:%M UTC')}
TIME REMAINING: {deadline_minutes} minutes

🐝 WE. ARE. SWARM. Collective intelligence activated."""

        print(f"\n🗳️ INITIATING CONSENSUS: {topic}")
        print(f"Consensus ID: {consensus_id}")
        print(f"Deadline: {deadline.strftime('%H:%M UTC')}")

        # Send consensus initiation to all agents
        success_count = 0
        for agent in self.agents:
            success = await self.messaging_service.send_message(
                agent=agent,
                message=consensus_message,
                priority="high",
                use_pyautogui=True,
                message_category="c2a"
            )

            if success:
                success_count += 1
                print(f"✅ {agent} notified")
            else:
                print(f"❌ {agent} notification failed")

        if success_count > 0:
            self.active_consensus[consensus_id] = {
                "topic": topic,
                "options": options,
                "deadline": deadline,
                "votes": {},
                "status": "ACTIVE",
                "agents_notified": success_count
            }

            print(f"\n📊 Consensus initiated: {success_count}/{len(self.agents)} agents notified")
            return consensus_id
        else:
            print("\n❌ Consensus initiation failed - no agents notified")
            return None

    async def collect_votes(self, consensus_id: str) -> Dict[str, Any]:
        """
        Collect and analyze votes for a consensus process.

        In a real implementation, this would monitor agent responses
        through the messaging system inbox monitoring.
        """
        if consensus_id not in self.active_consensus:
            print(f"❌ Consensus {consensus_id} not found")
            return {}

        consensus = self.active_consensus[consensus_id]

        # Simulate vote collection (in reality, this would monitor inboxes)
        print(f"\n🗳️ COLLECTING VOTES for: {consensus['topic']}")

        # Mock votes for demonstration (replace with actual inbox monitoring)
        mock_votes = {
            "Agent-1": {"vote": 1, "reasoning": "Best practice alignment"},
            "Agent-2": {"vote": 1, "reasoning": "Performance benefits"},
            "Agent-3": {"vote": 2, "reasoning": "Data integrity concerns"},
            "Agent-4": {"vote": 1, "reasoning": "Team consensus"},
            "Agent-5": {"vote": 1, "reasoning": "User experience improvement"},
            "Agent-6": {"vote": 2, "reasoning": "Testing overhead"},
            "Agent-7": {"vote": 1, "reasoning": "Documentation standards"},
            "Agent-8": {"vote": 1, "reasoning": "Infrastructure compatibility"}
        }

        consensus["votes"] = mock_votes

        # Analyze results
        vote_counts = {}
        for vote_data in mock_votes.values():
            option = vote_data["vote"]
            vote_counts[option] = vote_counts.get(option, 0) + 1

        total_votes = len(mock_votes)
        majority_threshold = total_votes // 2 + 1

        # Check for consensus
        consensus_reached = False
        winning_option = None
        winning_count = 0

        for option, count in vote_counts.items():
            if count >= majority_threshold:
                consensus_reached = True
                winning_option = option
                winning_count = count
                break

        consensus["vote_analysis"] = {
            "total_votes": total_votes,
            "vote_counts": vote_counts,
            "consensus_reached": consensus_reached,
            "winning_option": winning_option,
            "winning_count": winning_count,
            "majority_threshold": majority_threshold
        }

        return consensus

    async def announce_consensus_result(self, consensus_id: str) -> bool:
        """Announce the consensus result to all agents."""
        if consensus_id not in self.active_consensus:
            print(f"❌ Consensus {consensus_id} not found")
            return False

        consensus = self.active_consensus[consensus_id]

        if "vote_analysis" not in consensus:
            print("❌ No vote analysis available")
            return False

        analysis = consensus["vote_analysis"]

        if analysis["consensus_reached"]:
            result_message = f"""🐝 CONSENSUS REACHED!

TOPIC: {consensus['topic']}
RESULT: Option {analysis['winning_option']} - {consensus['options'][analysis['winning_option']-1]}

VOTE SUMMARY:
• Total Votes: {analysis['total_votes']}
• Majority Threshold: {analysis['majority_threshold']}
• Winning Votes: {analysis['winning_count']}

DETAILED VOTES:
"""

            for agent, vote_data in consensus["votes"].items():
                option_text = consensus["options"][vote_data["vote"]-1]
                result_message += f"• {agent}: {option_text} - {vote_data['reasoning']}\n"

            result_message += "\n🐝 WE. ARE. SWARM. Decision made through collective intelligence."
        else:
            result_message = f"""🤝 CONSENSUS PENDING

TOPIC: {consensus['topic']}
STATUS: No majority reached yet

Current vote distribution: {analysis['vote_counts']}
Continue discussion and A2A coordination.

🐝 WE. ARE. SWARM. Collective intelligence in progress."""

        print("\n📢 ANNOUNCING CONSENSUS RESULT...")
        # Send result to all agents
        success_count = 0
        for agent in self.agents:
            success = await self.messaging_service.send_message(
                agent=agent,
                message=result_message,
                priority="high",
                use_pyautogui=True,
                message_category="c2a"
            )

            if success:
                success_count += 1

        print(f"✅ Consensus result announced to {success_count}/{len(self.agents)} agents")

        # Archive consensus
        consensus["status"] = "COMPLETED" if analysis["consensus_reached"] else "PENDING"
        consensus["completed_at"] = datetime.now()
        self.consensus_history.append(consensus)

        return success_count > 0

    async def demonstrate_code_review_consensus(self) -> str:
        """Demonstrate consensus on code review process standardization."""
        topic = "Code Review Process Standardization"
        options = [
            "Implement automated linting + peer review + documentation requirements",
            "Focus on critical path reviews only + automated testing",
            "Maintain current process with minor improvements",
            "Adopt pair programming model for complex changes"
        ]

        consensus_id = await self.initiate_consensus_process(topic, options, deadline_minutes=15)
        return consensus_id

    async def demonstrate_architecture_consensus(self) -> str:
        """Demonstrate consensus on system architecture decisions."""
        topic = "Microservices vs Monolithic Architecture Migration"
        options = [
            "Gradual migration to microservices over 6 months",
            "Stay monolithic with modular refactoring",
            "Hybrid approach: core services + micro frontends",
            "Complete rewrite with new architecture"
        ]

        consensus_id = await self.initiate_consensus_process(topic, options, deadline_minutes=20)
        return consensus_id

    async def demonstrate_deployment_consensus(self) -> str:
        """Demonstrate consensus on deployment strategy."""
        topic = "CI/CD Pipeline Enhancement Strategy"
        options = [
            "Implement comprehensive automated testing + staging environments",
            "Focus on blue-green deployments + feature flags",
            "Add performance testing + security scanning",
            "Multi-region deployment with failover automation"
        ]

        consensus_id = await self.initiate_consensus_process(topic, options, deadline_minutes=10)
        return consensus_id

    def generate_consensus_report(self) -> str:
        """Generate a report of all consensus activities."""
        report = f"""
🐝 SWARM CONSENSUS REPORT
{'='*50}

ACTIVE CONSENSUS PROCESSES: {len(self.active_consensus)}
COMPLETED PROCESSES: {len(self.consensus_history)}

ACTIVE PROCESSES:
"""

        for consensus_id, consensus in self.active_consensus.items():
            if consensus["status"] == "ACTIVE":
                remaining_time = consensus["deadline"] - datetime.now()
                report += f"• {consensus_id}: {consensus['topic']}\n"
                report += f"  Deadline: {consensus['deadline'].strftime('%H:%M UTC')}\n"
                report += f"  Time remaining: {max(0, int(remaining_time.total_seconds() / 60))} minutes\n"
                report += f"  Agents notified: {consensus.get('agents_notified', 0)}\n\n"

        if self.consensus_history:
            report += "COMPLETED PROCESSES:\n"
            for consensus in self.consensus_history[-5:]:  # Show last 5
                status_emoji = "✅" if consensus.get("vote_analysis", {}).get("consensus_reached") else "⏳"
                report += f"• {status_emoji} {consensus['topic']}\n"

        report += """
🐝 WE. ARE. SWARM. Collective intelligence through consensus.
"""
        return report


async def main():
    """Demonstrate swarm consensus processes."""
    print("🐝 SWARM CONSENSUS DEMONSTRATION")
    print("=" * 60)

    engine = ConsensusEngine()

    try:
        # Demonstrate multiple consensus scenarios
        print("🎭 DEMONSTRATING DIFFERENT CONSENSUS SCENARIOS...")

        # Scenario 1: Code Review Process
        print("\n📋 SCENARIO 1: Code Review Standardization")
        consensus1_id = await engine.demonstrate_code_review_consensus()
        if consensus1_id:
            await asyncio.sleep(2)  # Simulate discussion time
            await engine.collect_votes(consensus1_id)
            await engine.announce_consensus_result(consensus1_id)

        # Scenario 2: Architecture Decision
        print("\n🏗️ SCENARIO 2: Architecture Migration")
        consensus2_id = await engine.demonstrate_architecture_consensus()
        if consensus2_id:
            await asyncio.sleep(2)  # Simulate discussion time
            await engine.collect_votes(consensus2_id)
            await engine.announce_consensus_result(consensus2_id)

        # Scenario 3: Deployment Strategy
        print("\n🚀 SCENARIO 3: CI/CD Enhancement")
        consensus3_id = await engine.demonstrate_deployment_consensus()
        if consensus3_id:
            await asyncio.sleep(2)  # Simulate discussion time
            await engine.collect_votes(consensus3_id)
            await engine.announce_consensus_result(consensus3_id)

        # Generate final report
        final_report = engine.generate_consensus_report()
        print(final_report)

        print("🎉 CONSENSUS DEMONSTRATION COMPLETE!")
        print("\n💡 Consensus Process Summary:")
        print("   1. Topic initiation with voting options")
        print("   2. Agent notification and discussion period")
        print("   3. Vote collection and analysis")
        print("   4. Consensus determination (majority rule)")
        print("   5. Result announcement to all agents")
        print("   6. Process archival for future reference")
        print()
        print("🔄 In production, consensus monitoring would:")
        print("   • Continuously monitor agent inboxes")
        print("   • Parse vote responses automatically")
        print("   • Trigger re-votes for tied decisions")
        print("   • Escalate stalled consensus processes")

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
