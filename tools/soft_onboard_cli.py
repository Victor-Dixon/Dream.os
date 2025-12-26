#!/usr/bin/env python3
"""
Soft Onboard CLI Tool
=====================

Command-line interface for soft onboarding agents.
Used by Discord bot commands.

V2 Compliance | Author: Agent-6 | Date: 2025-12-25
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.soft_onboarding_service import (
    soft_onboard_agent,
    soft_onboard_multiple_agents,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Soft onboard agent(s) - Agent activation protocol"
    )
    parser.add_argument(
        '--agent',
        type=str,
        help='Single agent ID (e.g., Agent-1)'
    )
    parser.add_argument(
        '--agents',
        type=str,
        help='Comma-separated list of agent IDs (e.g., Agent-1,Agent-2,Agent-3)'
    )
    parser.add_argument(
        '--message',
        type=str,
        default="🚀 SOFT ONBOARD - Agent activation initiated. Check your inbox and begin autonomous operations.",
        help='Onboarding message (optional)'
    )
    parser.add_argument(
        '--generate-cycle-report',
        action='store_true',
        help='Generate cycle accomplishments report after onboarding'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.agent and not args.agents:
        print("❌ ERROR: Must specify either --agent or --agents")
        parser.print_help()
        sys.exit(1)

    if args.agent and args.agents:
        print("❌ ERROR: Cannot use both --agent and --agents")
        parser.print_help()
        sys.exit(1)

    # Process single agent
    if args.agent:
        agent_id = args.agent.strip()
        if not agent_id.startswith('Agent-'):
            # Convert numeric ID to Agent-X format
            if agent_id.isdigit():
                agent_id = f"Agent-{agent_id}"
            else:
                print(f"❌ ERROR: Invalid agent ID format: {agent_id}")
                sys.exit(1)

        print(f"🚀 Soft onboarding {agent_id}...")
        success = soft_onboard_agent(
            agent_id=agent_id,
            message=args.message
        )

        if success:
            print(f"✅ {agent_id} soft onboarded successfully!")
            sys.exit(0)
        else:
            print(f"❌ Failed to soft onboard {agent_id}")
            sys.exit(1)

    # Process multiple agents
    if args.agents:
        agent_list = [aid.strip() for aid in args.agents.split(',') if aid.strip()]
        
        # Convert numeric IDs to Agent-X format
        formatted_agents = []
        for agent_id in agent_list:
            if agent_id.isdigit():
                formatted_agents.append(f"Agent-{agent_id}")
            elif agent_id.lower().startswith('agent-'):
                formatted_agents.append(agent_id)
            else:
                formatted_agents.append(agent_id)  # Keep as-is

        if not formatted_agents:
            print("❌ ERROR: No valid agents specified")
            sys.exit(1)

        print(f"🚀 Soft onboarding {len(formatted_agents)} agent(s)...")
        # Format as list of (agent_id, message) tuples
        agents_list = [(agent_id, args.message) for agent_id in formatted_agents]
        results = soft_onboard_multiple_agents(
            agents=agents_list,
            generate_cycle_report=args.generate_cycle_report
        )

        # Print results
        successful = [agent for agent, success in results.items() if success]
        failed = [agent for agent, success in results.items() if not success]

        if successful:
            print(f"\n✅ Successful ({len(successful)}/{len(formatted_agents)}):")
            for agent in successful:
                print(f"  ✅ {agent}")

        if failed:
            print(f"\n❌ Failed ({len(failed)}/{len(formatted_agents)}):")
            for agent in failed:
                print(f"  ❌ {agent}")

        # Exit with error if any failed
        if failed:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()

