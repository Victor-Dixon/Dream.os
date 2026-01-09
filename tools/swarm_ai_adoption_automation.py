#!/usr/bin/env python3
"""
Swarm-Wide AI Adoption Automation Tool
Automated deployment of AI capabilities across entire agent swarm

Usage:
python tools/swarm_ai_adoption_automation.py --deploy-all
python tools/swarm_ai_adoption_automation.py --status
python tools/swarm_ai_adoption_automation.py --validate-rollout
"""

import sys
import json
import time
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class SwarmAIAdoptionAutomation:
    """Automated AI adoption across entire agent swarm"""

    def __init__(self):
        self.repo_root = Path(__file__).parent.parent
        self.status_file = self.repo_root / "swarm_ai_adoption_status.json"
        self.max_workers = 4  # Parallel deployment limit

    def get_all_agents(self) -> List[str]:
        """Get list of all agents in the swarm"""
        agent_workspaces = self.repo_root / "agent_workspaces"
        if not agent_workspaces.exists():
            return []

        agents = []
        for item in agent_workspaces.iterdir():
            if item.is_dir() and item.name.startswith("Agent-"):
                agents.append(item.name)

        return sorted(agents)

    def deploy_ai_to_agent(self, agent_id: str) -> Dict[str, Any]:
        """Deploy AI integration to a specific agent"""
        try:
            # Use standalone AI integration to avoid module dependency issues
            from tools.standalone_ai_integration import deploy_to_agent_workspace
            success = deploy_to_agent_workspace(agent_id)

            return {
                "agent_id": agent_id,
                "success": success,
                "timestamp": time.time(),
                "error": None if success else "Deployment failed"
            }

        except Exception as e:
            return {
                "agent_id": agent_id,
                "success": False,
                "timestamp": time.time(),
                "error": str(e)
            }

    def deploy_ai_to_all_agents(self) -> Dict[str, Any]:
        """Deploy AI integration to all agents sequentially (for compatibility)"""
        agents = self.get_all_agents()

        if not agents:
            return {"error": "No agents found", "deployments": []}

        print(f"🚀 Starting swarm-wide AI adoption for {len(agents)} agents...")
        print(f"Agents: {', '.join(agents)}")

        results = []

        # Deploy sequentially to avoid multiprocessing import issues
        for agent in agents:
            try:
                result = self.deploy_ai_to_agent(agent)
                results.append(result)
                status = "✅" if result["success"] else "❌"
                print(f"{status} {agent}: {'Success' if result['success'] else result.get('error', 'Failed')}")
            except Exception as e:
                results.append({
                    "agent_id": agent,
                    "success": False,
                    "timestamp": time.time(),
                    "error": str(e)
                })
                print(f"❌ {agent}: Exception - {e}")

        # Summarize results
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]

        summary = {
            "total_agents": len(agents),
            "successful_deployments": len(successful),
            "failed_deployments": len(failed),
            "success_rate": f"{len(successful)}/{len(agents)} ({len(successful)/len(agents)*100:.1f}%)",
            "timestamp": time.time(),
            "deployments": results
        }

        # Update global status
        self._update_swarm_status(summary)

        return summary

    def validate_swarm_ai_adoption(self) -> Dict[str, Any]:
        """Validate AI adoption across the entire swarm"""
        agents = self.get_all_agents()

        if not agents:
            return {"error": "No agents found", "validations": []}

        print(f"🔍 Validating AI adoption for {len(agents)} agents...")

        validations = []

        # Validate each agent
        for agent_id in agents:
            try:
                from tools.standalone_ai_integration import verify_ai_integration
                validation = verify_ai_integration(agent_id)
                validations.append(validation)

                status = "✅" if validation.get("functionality_test", False) else "⚠️"
                print(f"{status} {agent_id}: {'Functional' if validation.get('functionality_test', False) else 'Needs attention'}")

            except Exception as e:
                validations.append({
                    "agent_id": agent_id,
                    "ai_available": False,
                    "files_created": False,
                    "functionality_test": False,
                    "error": str(e)
                })
                print(f"❌ {agent_id}: Validation error - {e}")

        # Summarize validations
        functional = [v for v in validations if v.get("functionality_test", False)]
        partial = [v for v in validations if v.get("files_created", False) and not v.get("functionality_test", False)]
        none = [v for v in validations if not v.get("files_created", False)]

        summary = {
            "total_agents": len(agents),
            "fully_functional": len(functional),
            "partially_deployed": len(partial),
            "not_deployed": len(none),
            "overall_adoption_rate": f"{len(functional)}/{len(agents)} ({len(functional)/len(agents)*100:.1f}%)",
            "timestamp": time.time(),
            "validations": validations
        }

        return summary

    def get_swarm_ai_status(self) -> Dict[str, Any]:
        """Get comprehensive swarm AI adoption status"""
        if self.status_file.exists():
            with open(self.status_file, 'r') as f:
                return json.load(f)

        return {"status": "no_swarm_status", "deployments": [], "validations": []}

    def _update_swarm_status(self, deployment_summary: Dict[str, Any]):
        """Update swarm-wide AI adoption status"""
        current_status = self.get_swarm_ai_status()

        # Update deployment history
        if "deployments" not in current_status:
            current_status["deployments"] = []

        current_status["deployments"].append(deployment_summary)
        current_status["last_deployment"] = deployment_summary
        current_status["last_updated"] = time.time()

        # Keep only last 10 deployments
        current_status["deployments"] = current_status["deployments"][-10:]

        with open(self.status_file, 'w') as f:
            json.dump(current_status, f, indent=2, default=str)

def main():
    parser = argparse.ArgumentParser(description="Swarm-Wide AI Adoption Automation Tool")

    parser.add_argument("--deploy-all", action="store_true",
                       help="Deploy AI integration to all agents in parallel")
    parser.add_argument("--status", action="store_true",
                       help="Show comprehensive swarm AI adoption status")
    parser.add_argument("--validate-rollout", action="store_true",
                       help="Validate AI adoption across the entire swarm")

    args = parser.parse_args()

    automation = SwarmAIAdoptionAutomation()

    if args.deploy_all:
        print("\\n🤖 Swarm-Wide AI Adoption Deployment Starting...")
        summary = automation.deploy_ai_to_all_agents()

        print(f"\\n📊 Deployment Summary:")
        print(f"Total Agents: {summary['total_agents']}")
        print(f"Successful: {summary['successful_deployments']}")
        print(f"Failed: {summary['failed_deployments']}")
        print(f"Success Rate: {summary['success_rate']}")

        if summary['successful_deployments'] > 0:
            print("\\n✅ AI adoption deployment completed!")
            print("Run 'python tools/swarm_ai_adoption_automation.py --validate-rollout' to verify.")
        else:
            print("\\n❌ All deployments failed. Check AI infrastructure availability.")

    elif args.validate_rollout:
        print("\\n🔍 Swarm-Wide AI Adoption Validation...")
        validation = automation.validate_swarm_ai_adoption()

        print(f"\\n📊 Validation Summary:")
        print(f"Total Agents: {validation['total_agents']}")
        print(f"Fully Functional: {validation['fully_functional']}")
        print(f"Partially Deployed: {validation['partially_deployed']}")
        print(f"Not Deployed: {validation['not_deployed']}")
        print(f"Overall Adoption Rate: {validation['overall_adoption_rate']}")

        if validation['fully_functional'] == validation['total_agents']:
            print("\\n🎉 100% AI adoption achieved across swarm!")
        elif validation['fully_functional'] > 0:
            print(f"\\n✅ {{validation['fully_functional']}}/{{validation['total_agents']}} agents have functional AI integration.")
        else:
            print("\\n⚠️ No agents currently have functional AI integration.")

    elif args.status:
        status = automation.get_swarm_ai_status()

        print("\\n📈 Swarm AI Adoption Status:")

        if status.get("last_deployment"):
            last = status["last_deployment"]
            print(f"\\nLast Deployment: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last['timestamp']))}")
            print(f"Success Rate: {last['success_rate']}")
            print(f"Successful Deployments: {last['successful_deployments']}/{last['total_agents']}")

        if status.get("deployments"):
            print(f"\\nTotal Deployments: {len(status['deployments'])}")
            print(f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status.get('last_updated', 0)))}")

        # Show current agent status
        agents = automation.get_all_agents()
        if agents:
            print(f"\\nCurrent Swarm: {len(agents)} agents")
            print(f"Agents: {', '.join(agents)}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()