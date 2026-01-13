#!/usr/bin/env python3
"""
AI Orchestration CLI - Intelligent Coordination Assistant
=======================================================

Command-line interface for AI-powered agent coordination and task allocation.
Integrates with the swarm messaging system to provide intelligent coordination recommendations.

USAGE:
    python scripts/ai_orchestrate.py --analyze-task "Build user authentication system"
    python scripts/ai_orchestrate.py --coordinate-agents "agent-1,agent-7" --task "API + frontend integration"
    python scripts/ai_orchestrate.py --generate-message --task "Database optimization" --recipients "agent-1,agent-8"

FEATURES:
- AI-powered task analysis and decomposition
- Intelligent agent selection based on expertise
- Coordination message generation with AI insights
- Integration with swarm messaging system
- Risk assessment and mitigation recommendations

Author: Agent-5 (Infrastructure Automation Specialist)
Date: 2026-01-13
"""

import argparse
import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.orchestration.ai_orchestrator_factory import (
    AIOrchestratorFactory,
    create_smart_orchestrator
)
from core.orchestration.registry import StepRegistry


class AIOrchestrationCLI:
    """CLI for AI-powered agent coordination."""

    def __init__(self):
        self.factory = AIOrchestratorFactory()

    def analyze_task(self, task_description: str, available_agents: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze a task using AI orchestration intelligence.

        Args:
            task_description: Description of the task to analyze
            available_agents: List of available agent IDs (optional)

        Returns:
            AI analysis with recommendations
        """
        # Default agents if not specified
        if available_agents is None:
            available_agents = ['agent-1', 'agent-2', 'agent-3', 'agent-5', 'agent-6', 'agent-7', 'agent-8']

        # Create mock agent data with expertise mapping
        agent_expertise = {
            'agent-1': ['integration', 'core-systems', 'api', 'backend'],
            'agent-2': ['architecture', 'design', 'planning', 'system-design'],
            'agent-3': ['infrastructure', 'devops', 'deployment', 'monitoring'],
            'agent-5': ['business-intelligence', 'ai', 'orchestration', 'analytics'],
            'agent-6': ['coordination', 'communication', 'messaging', 'facilitation'],
            'agent-7': ['web-development', 'frontend', 'ui', 'user-experience'],
            'agent-8': ['ssot', 'system-integration', 'data-management', 'validation']
        }

        agents = []
        for agent_id in available_agents:
            if agent_id in agent_expertise:
                agents.append({
                    'id': agent_id,
                    'agent_id': agent_id,
                    'specialties': agent_expertise[agent_id],
                    'capacity': 5,  # Default capacity
                    'status': 'available'
                })

        # Create coordination context
        coordination_context = {
            'agents': agents,
            'tasks': [{
                'id': 'current_task',
                'task_id': 'current_task',
                'description': task_description,
                'priority': 3,
                'estimated_complexity': 'medium',
                'required_domains': self._extract_domains_from_task(task_description)
            }],
            'coordination_state': {
                'phase': 'analysis',
                'goal': 'Determine optimal coordination strategy'
            }
        }

        # Get orchestrator selection recommendation
        orchestrator_type = self.factory.select_orchestrator_type(coordination_context)

        # Get orchestrator info
        registry = StepRegistry()
        orchestrator = self.factory.create_orchestrator(registry, ['analyze'], coordination_context)
        orchestrator_info = self.factory.get_orchestrator_info(orchestrator)

        # Generate analysis report
        analysis = {
            'task_description': task_description,
            'available_agents': available_agents,
            'recommended_orchestrator': orchestrator_type.value,
            'orchestrator_capabilities': orchestrator_info,
            'coordination_strategy': self._recommend_coordination_strategy(task_description, agents),
            'risk_assessment': self._assess_coordination_risks(task_description, agents),
            'message_templates': self._generate_coordination_messages(task_description, agents)
        }

        return analysis

    def _extract_domains_from_task(self, task_description: str) -> List[str]:
        """Extract technical domains from task description."""
        domains = []
        description_lower = task_description.lower()

        domain_keywords = {
            'ai': ['ai', 'machine learning', 'neural', 'gpt', 'llm', 'intelligence'],
            'web': ['web', 'frontend', 'ui', 'html', 'css', 'javascript', 'react', 'vue'],
            'api': ['api', 'backend', 'server', 'endpoint', 'rest', 'graphql'],
            'database': ['database', 'sql', 'data', 'schema', 'migration'],
            'infrastructure': ['infrastructure', 'devops', 'deployment', 'docker', 'kubernetes'],
            'architecture': ['architecture', 'design', 'system', 'planning'],
            'integration': ['integration', 'messaging', 'coordination', 'orchestration'],
            'testing': ['test', 'qa', 'validation', 'quality']
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in description_lower for keyword in keywords):
                domains.append(domain)

        return domains if domains else ['general']

    def _recommend_coordination_strategy(self, task_description: str, agents: List[Dict]) -> Dict[str, Any]:
        """Recommend coordination strategy based on task and agents."""
        domains = self._extract_domains_from_task(task_description)

        # Strategy selection logic
        if len(domains) > 2:
            strategy = "swarm_coordination"
            recommended_agents = self._select_agents_for_domains(domains, agents, max_agents=4)
            reasoning = f"Multi-domain task ({len(domains)} domains) requires swarm coordination"
        elif len(domains) == 2:
            strategy = "bilateral_coordination"
            recommended_agents = self._select_agents_for_domains(domains, agents, max_agents=2)
            reasoning = f"Dual-domain task requires bilateral coordination between specialists"
        elif len(agents) > 1 and any(agent.get('capacity', 0) < 3 for agent in agents):
            strategy = "delegated_execution"
            recommended_agents = [agents[0]]  # Primary agent
            reasoning = "Task complexity suggests delegation to specialized agent"
        else:
            strategy = "solo_execution"
            recommended_agents = [agents[0]] if agents else []
            reasoning = "Task can be handled by single agent"

        return {
            'strategy': strategy,
            'recommended_agents': [agent['id'] for agent in recommended_agents],
            'reasoning': reasoning,
            'estimated_effort': self._estimate_effort(domains, recommended_agents)
        }

    def _select_agents_for_domains(self, domains: List[str], agents: List[Dict], max_agents: int = 4) -> List[Dict]:
        """Select best agents for required domains."""
        selected_agents = []

        # Domain to agent mapping
        domain_experts = {
            'ai': ['agent-5', 'agent-2'],
            'web': ['agent-7', 'agent-1'],
            'api': ['agent-1', 'agent-2'],
            'database': ['agent-8', 'agent-1'],
            'infrastructure': ['agent-3', 'agent-5'],
            'architecture': ['agent-2', 'agent-1'],
            'integration': ['agent-6', 'agent-8'],
            'testing': ['agent-1', 'agent-7']
        }

        for domain in domains:
            if len(selected_agents) >= max_agents:
                break

            expert_ids = domain_experts.get(domain, [])
            for agent in agents:
                if agent['id'] in expert_ids and agent not in selected_agents:
                    selected_agents.append(agent)
                    break

        # Fill remaining slots with available agents
        for agent in agents:
            if len(selected_agents) >= max_agents:
                break
            if agent not in selected_agents:
                selected_agents.append(agent)

        return selected_agents[:max_agents]

    def _estimate_effort(self, domains: List[str], agents: List[Dict]) -> Dict[str, Any]:
        """Estimate coordination effort."""
        base_effort = len(domains) * 2  # Base effort per domain
        agent_multiplier = max(1, len(agents))  # More agents can parallelize

        return {
            'estimated_cycles': max(1, base_effort // agent_multiplier),
            'parallelization_factor': agent_multiplier,
            'communication_overhead': len(agents) - 1 if len(agents) > 1 else 0
        }

    def _assess_coordination_risks(self, task_description: str, agents: List[Dict]) -> Dict[str, Any]:
        """Assess risks in the coordination approach."""
        risks = []

        if len(agents) > 4:
            risks.append("High coordination complexity - consider breaking into smaller tasks")

        domains = self._extract_domains_from_task(task_description)
        if len(domains) > 3:
            risks.append("Multi-domain task - ensure clear ownership boundaries")

        # Check for single points of failure
        agent_specialties = {}
        for agent in agents:
            for specialty in agent.get('specialties', []):
                if specialty not in agent_specialties:
                    agent_specialties[specialty] = []
                agent_specialties[specialty].append(agent['id'])

        single_points = [specialty for specialty, agents_list in agent_specialties.items() if len(agents_list) == 1]
        if single_points:
            risks.append(f"Single points of failure in: {', '.join(single_points)}")

        return {
            'risk_level': 'high' if len(risks) > 2 else 'medium' if risks else 'low',
            'identified_risks': risks,
            'mitigation_suggestions': [
                "Establish clear communication protocols",
                "Set up regular status checkpoints",
                "Document integration points clearly"
            ] if risks else []
        }

    def _generate_coordination_messages(self, task_description: str, agents: List[Dict]) -> Dict[str, str]:
        """Generate coordination message templates."""
        agent_ids = [agent['id'] for agent in agents]

        if len(agent_ids) == 1:
            return {
                'solo_execution': f"Task: {task_description}\\nI'll handle this solo as it fits my expertise area."
            }

        elif len(agent_ids) == 2:
            return {
                'bilateral_request': f"""A2A COORDINATION REQUEST
From: Agent-{agent_ids[0].split('-')[1]}
To: Agent-{agent_ids[1].split('-')[1]}

COORDINATION REQUEST:
Task: {task_description}
Proposed approach: {agent_ids[0]} leads technical implementation, {agent_ids[1]} handles integration
Synergy: Combined expertise for complete solution
Next steps: {agent_ids[0]} starts implementation, {agent_ids[1]} prepares integration points
Capabilities: Technical implementation + system integration
Timeline: Complete within 2-3 cycles

ETA: Task completion within 3 cycles""",

                'bilateral_acceptance': f"""A2A REPLY to [message_id]:
✅ ACCEPT: Proposed approach: {agent_ids[0]} leads implementation + {agent_ids[1]} handles integration. Synergy: Technical + integration expertise. Next steps: Start implementation immediately. Capabilities: Full-stack delivery. Timeline: 2-3 cycles.
| ETA: Complete within 3 cycles"""
            }

        else:
            # Swarm coordination
            assignments = []
            for i, agent_id in enumerate(agent_ids):
                assignments.append(f"Agent-{agent_id.split('-')[1]}: Component {i+1}")

            agent_list = ', '.join([f'Agent-{id.split("-")[1]}' for id in agent_ids])

            return {
                'swarm_request': f"""SWARM COORDINATION REQUEST
To: {agent_list}

COORDINATION REQUEST:
Task: {task_description}

Assignments:
{chr(10).join(f'• {assignment}' for assignment in assignments)}

Next steps: Start parallel execution
Timeline: Complete within 2 cycles

ETA: All components complete within 2 cycles"""
            }

    def generate_coordination_message(self, task: str, recipients: List[str]) -> str:
        """Generate a complete coordination message for the given task and recipients."""
        # Analyze the task
        analysis = self.analyze_task(task, recipients)

        # Generate appropriate message based on strategy
        strategy = analysis['coordination_strategy']['strategy']

        if strategy == 'solo_execution':
            return f"Task: {task}\\nI'll handle this solo as it fits within my expertise area."

        elif strategy == 'bilateral_coordination' and len(recipients) == 2:
            recipient_numbers = [r.split('-')[1] for r in recipients]
            return f"""A2A COORDINATION REQUEST
From: Agent-{recipient_numbers[0]}
To: Agent-{recipient_numbers[1]}

COORDINATION REQUEST:
Task: {task}
Proposed approach: Agent-{recipient_numbers[0]} leads technical implementation, Agent-{recipient_numbers[1]} handles integration
Synergy: Combined expertise for complete solution
Next steps: Agent-{recipient_numbers[0]} starts implementation, Agent-{recipient_numbers[1]} prepares integration points
Capabilities: Technical implementation + system integration
Timeline: Complete within 2-3 cycles

ETA: Task completion within 3 cycles"""

        elif strategy == 'swarm_coordination':
            agent_numbers = [r.split('-')[1] for r in recipients]
            agent_list = ', '.join([f'Agent-{num}' for num in agent_numbers])
            assignments = [f"Agent-{agent_numbers[i]}: Component {i+1}" for i in range(len(recipients))]

            return f"""SWARM COORDINATION REQUEST
To: {agent_list}

COORDINATION REQUEST:
Task: {task}

Assignments:
{chr(10).join(f'• {assignment}' for assignment in assignments)}

Next steps: Start parallel execution
Timeline: Complete within 2 cycles

ETA: All components complete within 2 cycles"""

        else:
            return f"Task: {task}\\nRecommended strategy: {strategy}\\nPlease coordinate with team."


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered agent coordination assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a task for coordination recommendations
  python scripts/ai_orchestrate.py --analyze-task "Build user authentication system"

  # Generate coordination message for specific agents
  python scripts/ai_orchestrate.py --generate-message --task "API + frontend integration" --recipients "agent-1,agent-7"

  # Get orchestration advice for current work
  python scripts/ai_orchestrate.py --analyze-task "Debug failing tests" --agents "agent-1,agent-7"
        """
    )

    parser.add_argument(
        '--analyze-task',
        help='Analyze a task and provide coordination recommendations'
    )

    parser.add_argument(
        '--generate-message',
        action='store_true',
        help='Generate a coordination message based on task analysis'
    )

    parser.add_argument(
        '--task',
        help='Task description for message generation'
    )

    parser.add_argument(
        '--recipients', '--agents',
        help='Comma-separated list of agent IDs (e.g., "agent-1,agent-7")'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )

    args = parser.parse_args()

    if not args.analyze_task and not (args.generate_message and args.task):
        parser.print_help()
        return

    cli = AIOrchestrationCLI()

    try:
        if args.analyze_task:
            # Parse agents if provided
            available_agents = None
            if args.agents:
                available_agents = [a.strip() for a in args.agents.split(',')]

            # Analyze the task
            analysis = cli.analyze_task(args.analyze_task, available_agents)

            if args.json:
                print(json.dumps(analysis, indent=2))
            else:
                print("🤖 AI ORCHESTRATION ANALYSIS")
                print("=" * 50)
                print(f"Task: {analysis['task_description']}")
                print(f"Available Agents: {', '.join(analysis['available_agents'])}")
                print(f"Recommended Orchestrator: {analysis['recommended_orchestrator'].upper()}")
                print()

                strategy = analysis['coordination_strategy']
                print("🎯 COORDINATION STRATEGY")
                print(f"Strategy: {strategy['strategy'].replace('_', ' ').title()}")
                print(f"Recommended Agents: {', '.join(strategy['recommended_agents'])}")
                print(f"Reasoning: {strategy['reasoning']}")
                print()

                effort = strategy['estimated_effort']
                print("⏱️  EFFORT ESTIMATION")
                print(f"Estimated Cycles: {effort['estimated_cycles']}")
                print(f"Parallelization Factor: {effort['parallelization_factor']}x")
                print(f"Communication Overhead: {effort['communication_overhead']} agents")
                print()

                risks = analysis['risk_assessment']
                print("⚠️  RISK ASSESSMENT")
                print(f"Risk Level: {risks['risk_level'].upper()}")
                if risks['identified_risks']:
                    print("Identified Risks:")
                    for risk in risks['identified_risks']:
                        print(f"  • {risk}")
                if risks['mitigation_suggestions']:
                    print("Mitigation Suggestions:")
                    for suggestion in risks['mitigation_suggestions']:
                        print(f"  • {suggestion}")
                print()

                if analysis['message_templates']:
                    print("📨 RECOMMENDED MESSAGES")
                    for msg_type, template in analysis['message_templates'].items():
                        print(f"{msg_type.replace('_', ' ').title()}:")
                        print(f"  {template}")
                        print()

        elif args.generate_message and args.task:
            # Parse recipients
            recipients = []
            if args.recipients:
                recipients = [r.strip() for r in args.recipients.split(',')]

            # Generate message
            message = cli.generate_coordination_message(args.task, recipients)

            if args.json:
                result = {
                    'task': args.task,
                    'recipients': recipients,
                    'generated_message': message
                }
                print(json.dumps(result, indent=2))
            else:
                print("📨 GENERATED COORDINATION MESSAGE")
                print("=" * 50)
                print(message)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()