#!/usr/bin/env python3
"""
Unified Captain Tools - Consolidated Captain Operations
========================================================

<!-- SSOT Domain: core -->

Consolidates all Captain tools into a single unified tool.
Replaces 23+ individual captain tools with modular captain system.

Captain Categories:
- inbox: Inbox management operations
- coordination: Swarm coordination
- monitoring: Status monitoring
- tasks: Task assignment
- cleanup: Workspace cleanup

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-06
V2 Compliant: Yes (<400 lines)
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UnifiedCaptain:
    """Unified captain system consolidating all captain capabilities."""
    
    def __init__(self):
        """Initialize unified captain."""
        self.project_root = project_root
        self.agent_workspaces = project_root / "agent_workspaces"
        
    def handle_inbox(self, action: str = "analyze", **kwargs) -> Dict[str, Any]:
        """Handle inbox operations."""
        try:
            from tools.captain_inbox_manager import analyze_inbox, categorize_message
            
            inbox_path = self.agent_workspaces / "Agent-4" / "inbox"
            
            if action == "analyze":
                result = analyze_inbox(inbox_path)
                return {
                    "category": "inbox",
                    "action": "analyze",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "categorize":
                file_path = kwargs.get("file")
                if file_path:
                    msg_file = inbox_path / file_path
                    if msg_file.exists():
                        result = categorize_message(msg_file)
                        return {
                            "category": "inbox",
                            "action": "categorize",
                            "result": result,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "category": "inbox",
                            "action": "categorize",
                            "error": f"File not found: {file_path}",
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    return {
                        "category": "inbox",
                        "action": "categorize",
                        "error": "File path required",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "category": "inbox",
                    "error": f"Unknown action: {action}",
                    "available_actions": ["analyze", "categorize"],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Inbox operation failed: {e}")
            return {
                "category": "inbox",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_coordination(self, action: str = "status", **kwargs) -> Dict[str, Any]:
        """Handle swarm coordination operations."""
        try:
            from tools.captain_swarm_coordinator import CaptainSwarmCoordinator
            
            coordinator = CaptainSwarmCoordinator()
            
            if action == "status":
                statuses = coordinator.check_all_agent_statuses()
                return {
                    "category": "coordination",
                    "action": "status",
                    "statuses": statuses,
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "open-loops":
                coordinator.check_all_agent_statuses()  # Populate cache
                loops = coordinator.identify_open_loops()
                return {
                    "category": "coordination",
                    "action": "open-loops",
                    "loops": loops,
                    "count": len(loops),
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "assign-task":
                agent_id = kwargs.get("agent")
                task = kwargs.get("task")
                priority = kwargs.get("priority", "NORMAL")
                
                if agent_id and task:
                    result = coordinator.assign_task_to_agent(
                        agent_id=agent_id,
                        task=task,
                        priority=priority,
                        description=kwargs.get("description", "")
                    )
                    return {
                        "category": "coordination",
                        "action": "assign-task",
                        "result": result,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "category": "coordination",
                        "action": "assign-task",
                        "error": "Agent ID and task required",
                        "timestamp": datetime.now().isoformat()
                    }
            else:
                return {
                    "category": "coordination",
                    "error": f"Unknown action: {action}",
                    "available_actions": ["status", "open-loops", "assign-task"],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Coordination operation failed: {e}")
            return {
                "category": "coordination",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_monitoring(self, action: str = "snapshot", **kwargs) -> Dict[str, Any]:
        """Handle monitoring operations."""
        try:
            if action == "snapshot":
                from tools.captain_snapshot import generate_snapshot
                snapshot = generate_snapshot()
                return {
                    "category": "monitoring",
                    "action": "snapshot",
                    "snapshot": snapshot,
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "find-idle":
                from tools.captain_find_idle_agents import find_idle_agents
                idle = find_idle_agents()
                return {
                    "category": "monitoring",
                    "action": "find-idle",
                    "idle_agents": idle,
                    "count": len(idle),
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "progress":
                from tools.captain_progress_dashboard import generate_dashboard
                dashboard = generate_dashboard()
                return {
                    "category": "monitoring",
                    "action": "progress",
                    "dashboard": dashboard,
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "gas-check":
                from tools.captain_gas_check import check_gas_levels
                gas = check_gas_levels()
                return {
                    "category": "monitoring",
                    "action": "gas-check",
                    "gas_levels": gas,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "category": "monitoring",
                    "error": f"Unknown action: {action}",
                    "available_actions": ["snapshot", "find-idle", "progress", "gas-check"],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Monitoring operation failed: {e}")
            return {
                "category": "monitoring",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_tasks(self, action: str = "assign", **kwargs) -> Dict[str, Any]:
        """Handle task assignment operations."""
        try:
            from tools.captain_task_assigner import CaptainTaskAssigner
            
            assigner = CaptainTaskAssigner()
            
            if action == "assign":
                assigner.assign_critical_tasks()
                return {
                    "category": "tasks",
                    "action": "assign",
                    "message": "Critical tasks assigned",
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "next":
                from tools.captain_next_task_picker import pick_next_task
                task = pick_next_task()
                return {
                    "category": "tasks",
                    "action": "next",
                    "task": task,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "category": "tasks",
                    "error": f"Unknown action: {action}",
                    "available_actions": ["assign", "next"],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Task operation failed: {e}")
            return {
                "category": "tasks",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def handle_cleanup(self, action: str = "workspace", **kwargs) -> Dict[str, Any]:
        """Handle cleanup operations."""
        try:
            if action == "workspace":
                from tools.captain_workspace_cleanup import cleanup_workspace
                result = cleanup_workspace()
                return {
                    "category": "cleanup",
                    "action": "workspace",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            elif action == "archive-inbox":
                from tools.archive_captain_inbox import archive_old_messages
                result = archive_old_messages()
                return {
                    "category": "cleanup",
                    "action": "archive-inbox",
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "category": "cleanup",
                    "error": f"Unknown action: {action}",
                    "available_actions": ["workspace", "archive-inbox"],
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Cleanup operation failed: {e}")
            return {
                "category": "cleanup",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for unified captain."""
    parser = argparse.ArgumentParser(
        description="Unified Captain Tools - Consolidated Captain Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--category",
        choices=["inbox", "coordination", "monitoring", "tasks", "cleanup", "all"],
        default="all",
        help="Category of captain operations"
    )
    
    parser.add_argument(
        "--action",
        type=str,
        help="Specific action to perform (varies by category)"
    )
    
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent ID for task assignment"
    )
    
    parser.add_argument(
        "--task",
        type=str,
        help="Task description"
    )
    
    parser.add_argument(
        "--priority",
        type=str,
        default="NORMAL",
        help="Task priority (NORMAL, HIGH, CRITICAL)"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="File path for file-specific operations"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    captain = UnifiedCaptain()
    results = []
    
    categories = ["inbox", "coordination", "monitoring", "tasks", "cleanup"] if args.category == "all" else [args.category]
    
    for category in categories:
        action = args.action or {
            "inbox": "analyze",
            "coordination": "status",
            "monitoring": "snapshot",
            "tasks": "assign",
            "cleanup": "workspace"
        }.get(category, "status")
        
        kwargs = {
            "agent": args.agent,
            "task": args.task,
            "priority": args.priority,
            "file": args.file,
            "description": args.task  # Use task as description if provided
        }
        
        if category == "inbox":
            result = captain.handle_inbox(action=action, **kwargs)
        elif category == "coordination":
            result = captain.handle_coordination(action=action, **kwargs)
        elif category == "monitoring":
            result = captain.handle_monitoring(action=action, **kwargs)
        elif category == "tasks":
            result = captain.handle_tasks(action=action, **kwargs)
        elif category == "cleanup":
            result = captain.handle_cleanup(action=action, **kwargs)
        else:
            result = {
                "category": category,
                "error": "Unknown category",
                "timestamp": datetime.now().isoformat()
            }
        
        results.append(result)
    
    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            if "error" in result:
                print(f"❌ {result['category']}: {result['error']}")
            else:
                print(f"✅ {result['category']}: {result.get('action', 'completed')}")
                if "count" in result:
                    print(f"   Count: {result['count']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

