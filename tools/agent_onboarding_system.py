#!/usr/bin/env python3
"""
Agent Soft Onboarding System
Manages the soft onboarding process for all swarm agents
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

class AgentOnboardingSystem:
    """Manages soft onboarding for all agents"""

    def __init__(self):
        self.repo_root = Path(__file__).resolve().parents[1]
        self.agent_workspaces = self.repo_root / "agent_workspaces"
        self.templates = self.repo_root / "templates"

    def get_all_agents(self) -> List[str]:
        """Get list of all agent IDs"""
        agents = []
        if self.agent_workspaces.exists():
            for item in self.agent_workspaces.iterdir():
                if item.is_dir() and item.name.startswith("Agent-") and not item.name.startswith("Agent-Agent"):
                    agents.append(item.name)
        return sorted(agents)

    def validate_agent_workspace(self, agent_id: str) -> Dict[str, Any]:
        """Validate an agent's workspace structure"""
        workspace = self.agent_workspaces / agent_id

        validation = {
            "agent_id": agent_id,
            "workspace_exists": workspace.exists(),
            "has_status": False,
            "has_inbox": False,
            "has_devlogs": False,
            "inbox_messages": 0,
            "devlog_count": 0,
            "status_valid": False
        }

        if workspace.exists():
            # Check status.json
            status_file = workspace / "status.json"
            if status_file.exists():
                validation["has_status"] = True
                try:
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                        if "agent_id" in status_data and status_data["agent_id"] == agent_id:
                            validation["status_valid"] = True
                except:
                    pass

            # Check inbox
            inbox_dir = workspace / "inbox"
            if inbox_dir.exists():
                validation["has_inbox"] = True
                validation["inbox_messages"] = len(list(inbox_dir.glob("*")))

            # Check devlogs
            devlogs_dir = workspace / "devlogs"
            if devlogs_dir.exists():
                validation["has_devlogs"] = True
                validation["devlog_count"] = len(list(devlogs_dir.glob("*.md")))

        return validation

    def create_standard_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Create a standard agent status structure"""
        return {
            "agent_id": agent_id,
            "agent_name": f"{agent_id} Agent",
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "ONBOARDED",
            "last_updated": datetime.now().isoformat(),
            "current_mission": "Swarm Coordination & Task Execution",
            "mission_priority": "HIGH",
            "current_tasks": ["Ready for swarm assignments"],
            "completed_tasks": ["Soft onboarding completed"],
            "achievements": ["Agent workspace initialized", "Onboarding protocols engaged"],
            "next_actions": ["Await swarm coordination directives", "Monitor inbox for assignments"],
            "last_activity": {
                "timestamp": datetime.now().isoformat(),
                "message_id": None,
                "category": "onboarding",
                "recipient": "CAPTAIN"
            }
        }

    def onboard_agent(self, agent_id: str) -> Dict[str, Any]:
        """Onboard a single agent"""
        workspace = self.agent_workspaces / agent_id

        # Create workspace structure
        workspace.mkdir(exist_ok=True)
        (workspace / "inbox").mkdir(exist_ok=True)
        (workspace / "devlogs").mkdir(exist_ok=True)

        # Create/update status.json
        status_file = workspace / "status.json"
        status_data = self.create_standard_agent_status(agent_id)

        with open(status_file, 'w') as f:
            json.dump(status_data, f, indent=2)

        # Copy onboarding message if it doesn't exist
        onboarding_msg = workspace / "inbox" / "soft_onboarding_message_full.txt"
        if not onboarding_msg.exists():
            template_msg = self.repo_root / "agent_workspaces" / "Agent-7" / "inbox" / "soft_onboarding_message_full.txt"
            if template_msg.exists():
                import shutil
                shutil.copy2(template_msg, onboarding_msg)

                # Update the message to be specific to this agent
                with open(onboarding_msg, 'r') as f:
                    content = f.read()
                content = content.replace("Agent-7", agent_id)
                with open(onboarding_msg, 'w') as f:
                    f.write(content)

        return {
            "agent_id": agent_id,
            "status": "ONBOARDED",
            "workspace_created": True,
            "status_file_created": True,
            "onboarding_message_copied": True
        }

    def onboard_all_agents(self) -> List[Dict[str, Any]]:
        """Onboard all agents in the swarm"""
        agents = self.get_all_agents()
        results = []

        print(f"🐝 Starting soft onboarding for {len(agents)} agents...")
        print("=" * 60)

        for agent_id in agents:
            print(f"📋 Onboarding {agent_id}...")
            try:
                result = self.onboard_agent(agent_id)
                results.append(result)
                print(f"✅ {agent_id} onboarded successfully")
            except Exception as e:
                error_result = {
                    "agent_id": agent_id,
                    "status": "FAILED",
                    "error": str(e)
                }
                results.append(error_result)
                print(f"❌ {agent_id} onboarding failed: {e}")

        print("=" * 60)
        print("🎯 Soft onboarding complete!")

        return results

    def validate_all_agents(self) -> List[Dict[str, Any]]:
        """Validate all agent workspaces"""
        agents = self.get_all_agents()
        validations = []

        print(f"🔍 Validating {len(agents)} agent workspaces...")
        print("=" * 60)

        for agent_id in agents:
            validation = self.validate_agent_workspace(agent_id)
            validations.append(validation)

            status_icon = "✅" if validation["workspace_exists"] and validation["status_valid"] else "❌"
            print(f"{status_icon} {agent_id}: Workspace={'✅' if validation['workspace_exists'] else '❌'}, Status={'✅' if validation['status_valid'] else '❌'}")

        print("=" * 60)
        return validations

def main():
    """Main onboarding execution"""
    onboarding_system = AgentOnboardingSystem()

    print("🚀 AGENT SOFT ONBOARDING SYSTEM")
    print("=" * 60)

    # Validate current state
    print("\n📊 CURRENT AGENT STATUS:")
    validations = onboarding_system.validate_all_agents()

    valid_count = sum(1 for v in validations if v["workspace_exists"] and v["status_valid"])
    total_count = len(validations)

    print(f"\n📈 Validation Results: {valid_count}/{total_count} agents properly configured")

    if valid_count < total_count:
        print("\n🔄 Executing soft onboarding for missing/invalid agents...")

        # Onboard missing agents
        onboarding_results = onboarding_system.onboard_all_agents()

        # Final validation
        print("\n📊 POST-ONBOARDING VALIDATION:")
        final_validations = onboarding_system.validate_all_agents()

        final_valid_count = sum(1 for v in final_validations if v["workspace_exists"] and v["status_valid"])
        print(f"\n🎯 Final Results: {final_valid_count}/{total_count} agents successfully onboarded")

        if final_valid_count == total_count:
            print("\n🎉 ALL AGENTS SUCCESSFULLY ONBOARDED!")
            print("🐝 Swarm is ready for coordinated operations.")
        else:
            print(f"\n⚠️ {total_count - final_valid_count} agents still need attention.")
    else:
        print("\n✅ All agents already properly onboarded!")

if __name__ == "__main__":
    main()