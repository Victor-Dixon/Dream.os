#!/usr/bin/env python3
"""
🎯 System Awareness Campaign Launcher
===================================

Automated system discovery and training campaign for Agent Cellphone V2.
Launches daily system highlights and utilization tracking.

Usage:
    python system_awareness_campaign.py --launch
    python system_awareness_campaign.py --status
    python system_awareness_campaign.py --survey Agent-X
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from services.messaging_cli import MessagingCLI


class SystemAwarenessCampaign:
    """
    Automated system awareness and utilization campaign.

    Features:
    - Daily system highlights
    - Utilization tracking
    - Agent surveys and assessments
    - Progress monitoring
    """

    def __init__(self):
        self.campaign_file = Path(__file__).parent / 'campaign_data.json'
        self.systems_catalog = self._load_systems_catalog()
        self.campaign_data = self._load_campaign_data()

    def _load_systems_catalog(self) -> Dict[str, Any]:
        """Load the comprehensive system catalog."""
        return {
            "messaging": {
                "name": "A2A Messaging System",
                "description": "Agent-to-agent coordination and communication",
                "difficulty": "Basic",
                "usage": "python -m src.services.messaging_cli --agent Agent-X --message 'Hello'",
                "benefits": ["Real-time coordination", "Status updates", "Issue escalation"],
                "owner": "Agent-6"
            },
            "plugins": {
                "name": "Plugin Ecosystem",
                "description": "Modular functionality extensions",
                "difficulty": "Intermediate",
                "usage": "python demo_plugin_system.py",
                "benefits": ["Custom functionality", "Rapid prototyping", "Scalable architecture"],
                "owner": "Agent-6"
            },
            "qa": {
                "name": "Quality Assurance Framework",
                "description": "Automated testing and validation",
                "difficulty": "Intermediate",
                "usage": "pytest tests/ -v",
                "benefits": ["Automated validation", "Quality assurance", "Regression prevention"],
                "owner": "Agent-8"
            },
            "trading": {
                "name": "Trading Analytics",
                "description": "Real-time market data and trading intelligence",
                "difficulty": "Basic",
                "usage": "python -m src.trading.analytics --dashboard",
                "benefits": ["Market insights", "Performance tracking", "Risk management"],
                "owner": "Agent-2"
            },
            "devops": {
                "name": "DevOps Pipeline",
                "description": "Deployment, monitoring, and infrastructure",
                "difficulty": "Advanced",
                "usage": "python -m src.devops.pipeline --status",
                "benefits": ["Automated deployment", "System monitoring", "Rollback safety"],
                "owner": "Agent-1"
            },
            "ai_orchestration": {
                "name": "AI Orchestration Framework",
                "description": "Multi-model coordination and optimization",
                "difficulty": "Advanced",
                "usage": "python -m src.ai.orchestrator --analyze",
                "benefits": ["Model optimization", "Resource efficiency", "Parallel processing"],
                "owner": "Agent-2"
            },
            "docs": {
                "name": "Documentation System (SSOT)",
                "description": "Single source of truth documentation",
                "difficulty": "Basic",
                "usage": "python -m src.docs.generator --update",
                "benefits": ["Knowledge management", "Automated docs", "Version control"],
                "owner": "Agent-8"
            }
        }

    def _load_campaign_data(self) -> Dict[str, Any]:
        """Load campaign progress data."""
        if self.campaign_file.exists():
            with open(self.campaign_file, 'r') as f:
                return json.load(f)

        # Initialize default campaign data
        return {
            "campaign_start": datetime.now().isoformat(),
            "daily_highlights": [],
            "agent_surveys": {},
            "utilization_metrics": {},
            "last_highlight": None
        }

    def _save_campaign_data(self):
        """Save campaign progress data."""
        with open(self.campaign_file, 'w') as f:
            json.dump(self.campaign_data, f, indent=2, default=str)

    def launch_daily_highlight(self) -> str:
        """
        Launch daily system highlight campaign.

        Returns:
            str: Highlight message content
        """
        # Select random system not highlighted recently
        available_systems = [s for s in self.systems_catalog.keys()
                           if s != self.campaign_data.get('last_highlight')]

        if not available_systems:
            available_systems = list(self.systems_catalog.keys())

        featured_system = random.choice(available_systems)
        system_data = self.systems_catalog[featured_system]

        # Create highlight message
        highlight = f"""
🔥 **DAILY SYSTEM HIGHLIGHT: {system_data['name'].upper()}** 🔥

**What it does:** {system_data['description']}
**Difficulty:** {system_data['difficulty']}
**Why use it:** {', '.join(system_data['benefits'][:2])}

**Quick Start:**
```bash
{system_data['usage']}
```

**Owner:** {system_data['owner']}
**Learn more:** Check `system_inventory_catalog.md`

**Challenge:** Try using this system in your next task! 🚀

#SystemAwareness #SwarmIntelligence #AgentTraining
        """.strip()

        # Record highlight
        self.campaign_data['daily_highlights'].append({
            'date': datetime.now().isoformat(),
            'system': featured_system,
            'message': highlight
        })
        self.campaign_data['last_highlight'] = featured_system
        self._save_campaign_data()

        return highlight

    def send_highlight_broadcast(self):
        """Send daily highlight to all agents."""
        highlight_message = self.launch_daily_highlight()

        # Send to all agents
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-7", "Agent-8"]

        for agent in agents:
            try:
                # Use messaging CLI to send highlight
                import subprocess
                cmd = [
                    sys.executable, "-m", "src.services.messaging_cli",
                    "--agent", agent,
                    "--message", highlight_message,
                    "--category", "training",
                    "--sender", "Agent-6",
                    "--tags", "system-awareness,daily-highlight"
                ]
                subprocess.run(cmd, capture_output=True, timeout=10)
                print(f"✅ Highlight sent to {agent}")

            except Exception as e:
                print(f"❌ Failed to send to {agent}: {e}")

    def create_agent_survey(self, agent_id: str) -> str:
        """
        Create personalized system utilization survey for agent.

        Args:
            agent_id: Agent to survey

        Returns:
            str: Survey message
        """
        survey = f"""
📊 **SYSTEM UTILIZATION SURVEY - {agent_id}**

Help us improve system utilization across the swarm!

**Quick Assessment (1-5 scale):**

**Core Systems:**
1. A2A Messaging: ____ (1=Never, 5=Daily)
2. Plugin Ecosystem: ____ (1=Never, 5=Daily)
3. Quality Assurance: ____ (1=Never, 5=Daily)
4. Trading Analytics: ____ (1=Never, 5=Daily)

**Specialized Systems:**
5. DevOps/Infrastructure: ____ (1=Never, 5=Daily)
6. AI Orchestration: ____ (1=Never, 5=Daily)
7. Documentation (SSOT): ____ (1=Never, 5=Daily)

**Open Feedback:**
- What system would you like training on?
- What's preventing you from using available systems?
- Any system integrations you'd find valuable?

**Reply Format:**
```
SYSTEM SURVEY RESULTS:
Agent: {agent_id}
Messaging: X/5
Plugins: X/5
QA: X/5
Trading: X/5
DevOps: X/5
AI: X/5
Docs: X/5
Training Request: [system name]
Barriers: [your feedback]
Integration Ideas: [suggestions]
```

This helps us create personalized training plans! 🎯

#SystemUtilization #AgentTraining #SwarmOptimization
        """.strip()

        return survey

    def get_campaign_status(self) -> Dict[str, Any]:
        """Get comprehensive campaign status."""
        total_agents = 8  # Agent-1 through Agent-8 (excluding Agent-6)
        surveyed_agents = len(self.campaign_data.get('agent_surveys', {}))
        highlights_sent = len(self.campaign_data.get('daily_highlights', []))

        return {
            "campaign_duration_days": (datetime.now() - datetime.fromisoformat(self.campaign_data['campaign_start'])).days,
            "highlights_sent": highlights_sent,
            "agents_surveyed": surveyed_agents,
            "survey_completion_rate": f"{surveyed_agents}/{total_agents} ({surveyed_agents/total_agents*100:.1f}%)",
            "last_highlight": self.campaign_data.get('last_highlight', 'None'),
            "systems_covered": len(set(h['system'] for h in self.campaign_data.get('daily_highlights', [])))
        }

    def run_campaign_command(self, command: str, *args):
        """Run campaign command."""
        if command == "launch":
            print("🚀 Launching Daily System Highlight Campaign...")
            self.send_highlight_broadcast()
            print("✅ Daily highlights sent to all agents!")

        elif command == "status":
            status = self.get_campaign_status()
            print("📊 Campaign Status:")
            for key, value in status.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")

        elif command == "survey":
            if not args:
                print("❌ Please specify agent ID: python system_awareness_campaign.py --survey Agent-X")
                return

            agent_id = args[0]
            survey = self.create_agent_survey(agent_id)

            # Send survey to agent
            try:
                import subprocess
                cmd = [
                    sys.executable, "-m", "src.services.messaging_cli",
                    "--agent", agent_id,
                    "--message", survey,
                    "--category", "training",
                    "--sender", "Agent-6",
                    "--tags", "system-survey,utilization-assessment"
                ]
                subprocess.run(cmd, capture_output=True, timeout=10)
                print(f"✅ Survey sent to {agent_id}")

            except Exception as e:
                print(f"❌ Failed to send survey to {agent_id}: {e}")

        elif command == "inventory":
            print("🔧 System Inventory Catalog:")
            print(f"Total Systems: {len(self.systems_catalog)}")
            for sys_id, system in self.systems_catalog.items():
                print(f"  • {system['name']} ({sys_id}) - Owner: {system['owner']}")

        else:
            print("❌ Unknown command. Available commands:")
            print("  --launch    Send daily system highlight to all agents")
            print("  --status    Show campaign status and metrics")
            print("  --survey    Send utilization survey to specific agent")
            print("  --inventory Show available systems")


def main():
    """Main campaign launcher."""
    if len(sys.argv) < 2:
        print("Usage: python system_awareness_campaign.py <command>")
        print("Commands: --launch, --status, --survey <agent>, --inventory")
        return

    command = sys.argv[1].lstrip('-')
    args = sys.argv[2:]

    campaign = SystemAwarenessCampaign()
    campaign.run_campaign_command(command, *args)


if __name__ == "__main__":
    main()