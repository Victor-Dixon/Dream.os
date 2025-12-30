#!/usr/bin/env python3
"""
MCP Server for Coordination & Status Operations
Consolidates scattered coordination and status management tools into centralized MCP server

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

PROJECT_ROOT = Path(__file__).parent.parent

# Try to import coordination tools
try:
    from tools.a2a_coordination_queue import CoordinationQueue
    HAS_COORDINATION_QUEUE = True
except ImportError:
    HAS_COORDINATION_QUEUE = False
    CoordinationQueue = None


def send_coordination_message(
    recipient: str,
    message: str,
    priority: str = "normal",
    sender: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send A2A coordination message to an agent.
    
    Consolidates: a2a_coordination_queue.py, a2a_coordination_validator.py
    
    Args:
        recipient: Target agent ID (Agent-1 through Agent-8)
        message: Message content
        priority: Message priority (normal, urgent)
        sender: Sender agent ID (optional)
        category: Message category (optional)
        
    Returns:
        Coordination message result
    """
    try:
        if HAS_COORDINATION_QUEUE:
            queue = CoordinationQueue()
            result = queue.add_message(
                recipient=recipient,
                message=message,
                priority=priority,
                sender=sender or "Agent-3",
                category=category or "a2a"
            )
            return {
                "success": True,
                "recipient": recipient,
                "message_id": result.get("message_id"),
                "priority": priority,
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Fallback: Use messaging CLI
            import subprocess
            cmd = [
                sys.executable, "-m", "src.services.messaging_cli",
                "--agent", recipient,
                "--message", message,
                "--priority", priority,
                "--category", category or "a2a"
            ]
            if sender:
                cmd.extend(["--sender", sender])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            return {
                "success": result.returncode == 0,
                "recipient": recipient,
                "priority": priority,
                "output": result.stdout,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "recipient": recipient,
            "timestamp": datetime.now().isoformat()
        }


def get_coordination_status(
    agent_filter: Optional[str] = None,
    status_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get coordination status dashboard.
    
    Consolidates: coordination_status_dashboard.py
    
    Args:
        agent_filter: Filter by agent ID (optional)
        status_filter: Filter by status (optional)
        
    Returns:
        Coordination status dashboard
    """
    try:
        # Read all agent status.json files
        agent_workspaces = PROJECT_ROOT / "agent_workspaces"
        if not agent_workspaces.exists():
            return {
                "success": False,
                "error": "agent_workspaces directory not found"
            }
        
        coordinations = []
        agents_data = {}
        
        for agent_dir in agent_workspaces.iterdir():
            if not agent_dir.is_dir() or not agent_dir.name.startswith("Agent-"):
                continue
            
            agent_id = agent_dir.name
            status_file = agent_dir / "status.json"
            
            if status_file.exists():
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                    
                    agents_data[agent_id] = {
                        "status": status.get("status"),
                        "fsm_state": status.get("fsm_state"),
                        "current_phase": status.get("current_phase"),
                        "last_updated": status.get("last_updated"),
                        "current_tasks": status.get("current_tasks", [])
                    }
                    
                    # Extract coordination information
                    current_tasks = status.get("current_tasks", [])
                    for task in current_tasks:
                        if isinstance(task, str) and ("coordination" in task.lower() or "blocked" in task.lower()):
                            coordinations.append({
                                "agent": agent_id,
                                "task": task,
                                "status": status.get("status"),
                                "last_updated": status.get("last_updated")
                            })
                except Exception as e:
                    continue
        
        # Apply filters
        if agent_filter:
            coordinations = [c for c in coordinations if c["agent"] == agent_filter]
            agents_data = {k: v for k, v in agents_data.items() if k == agent_filter}
        
        if status_filter:
            coordinations = [c for c in coordinations if status_filter.lower() in c.get("status", "").lower()]
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(agents_data),
            "active_coordinations": len(coordinations),
            "agents": agents_data,
            "coordinations": coordinations
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def track_coordination(
    coordination_id: Optional[str] = None,
    updates: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Track coordination progress.
    
    Consolidates: coordination_status_tracker.py
    
    Args:
        coordination_id: Coordination identifier (optional)
        updates: Updates to track (optional)
        
    Returns:
        Tracking result
    """
    try:
        # This would integrate with coordination tracking system
        # For now, return structure
        return {
            "success": True,
            "coordination_id": coordination_id or f"coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "updates": updates or {},
            "timestamp": datetime.now().isoformat(),
            "message": "Coordination tracking (implementation needed)"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def identify_coordination_opportunities() -> Dict[str, Any]:
    """
    Identify coordination opportunities across agents.
    
    Consolidates: identify_coordination_opportunities.py
    
    Returns:
        List of coordination opportunities
    """
    try:
        # Read agent statuses to find coordination needs
        agent_workspaces = PROJECT_ROOT / "agent_workspaces"
        opportunities = []
        
        if not agent_workspaces.exists():
            return {
                "success": False,
                "error": "agent_workspaces directory not found"
            }
        
        agent_statuses = {}
        for agent_dir in agent_workspaces.iterdir():
            if not agent_dir.is_dir() or not agent_dir.name.startswith("Agent-"):
                continue
            
            status_file = agent_dir / "status.json"
            if status_file.exists():
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)
                    agent_statuses[agent_dir.name] = status
                except Exception:
                    continue
        
        # Look for blockers that might need coordination
        for agent_id, status in agent_statuses.items():
            tasks = status.get("current_tasks", [])
            for task in tasks:
                if isinstance(task, str):
                    # Check for blockers
                    if "blocked" in task.lower() or "waiting" in task.lower():
                        opportunities.append({
                            "agent": agent_id,
                            "task": task,
                            "type": "blocker",
                            "priority": "high"
                        })
                    
                    # Check for coordination mentions
                    if "coordination" in task.lower() or "coordinate" in task.lower():
                        opportunities.append({
                            "agent": agent_id,
                            "task": task,
                            "type": "coordination",
                            "priority": "medium"
                        })
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "opportunities_found": len(opportunities),
            "opportunities": opportunities
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


def get_agent_status(agent_id: str) -> Dict[str, Any]:
    """
    Get current status for an agent.
    
    Consolidates: debug_status_check.py
    
    Args:
        agent_id: Agent ID (Agent-1 through Agent-8)
        
    Returns:
        Agent status information
    """
    try:
        status_file = PROJECT_ROOT / "agent_workspaces" / agent_id / "status.json"
        
        if not status_file.exists():
            return {
                "success": False,
                "error": f"Status file not found for {agent_id}"
            }
        
        with open(status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "status": status.get("status"),
            "fsm_state": status.get("fsm_state"),
            "current_phase": status.get("current_phase"),
            "last_updated": status.get("last_updated"),
            "current_mission": status.get("current_mission"),
            "current_tasks": status.get("current_tasks", []),
            "completed_tasks": status.get("completed_tasks", []),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }


def update_agent_status(
    agent_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update agent status.json with new information.
    
    Consolidates: Status management operations
    
    Args:
        agent_id: Agent ID
        updates: Dictionary of fields to update
        
    Returns:
        Update result
    """
    try:
        status_file = PROJECT_ROOT / "agent_workspaces" / agent_id / "status.json"
        
        if not status_file.exists():
            return {
                "success": False,
                "error": f"Status file not found for {agent_id}"
            }
        
        # Read current status
        with open(status_file, 'r', encoding='utf-8') as f:
            status = json.load(f)
        
        # Apply updates
        for key, value in updates.items():
            if key in status:
                status[key] = value
        
        # Update timestamp
        status["last_updated"] = datetime.now().isoformat()
        
        # Write back
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
        
        return {
            "success": True,
            "agent_id": agent_id,
            "updated_fields": list(updates.keys()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat()
        }


def main():
    """MCP server main loop."""
    print(
        json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "initialize",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {
                            "send_coordination_message": {
                                "description": "Send A2A coordination message to an agent",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "recipient": {"type": "string", "description": "Target agent ID"},
                                        "message": {"type": "string", "description": "Message content"},
                                        "priority": {"type": "string", "enum": ["normal", "urgent"], "default": "normal"},
                                        "sender": {"type": "string", "description": "Sender agent ID (optional)"},
                                        "category": {"type": "string", "description": "Message category (optional)"}
                                    },
                                    "required": ["recipient", "message"]
                                }
                            },
                            "get_coordination_status": {
                                "description": "Get coordination status dashboard",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "agent_filter": {"type": "string", "description": "Filter by agent ID (optional)"},
                                        "status_filter": {"type": "string", "description": "Filter by status (optional)"}
                                    }
                                }
                            },
                            "track_coordination": {
                                "description": "Track coordination progress",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "coordination_id": {"type": "string", "description": "Coordination identifier (optional)"},
                                        "updates": {"type": "object", "description": "Updates to track (optional)"}
                                    }
                                }
                            },
                            "identify_coordination_opportunities": {
                                "description": "Identify coordination opportunities across agents",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {}
                                }
                            },
                            "get_agent_status": {
                                "description": "Get current status for an agent",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "agent_id": {"type": "string", "description": "Agent ID (Agent-1 through Agent-8)"}
                                    },
                                    "required": ["agent_id"]
                                }
                            },
                            "update_agent_status": {
                                "description": "Update agent status.json with new information",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "agent_id": {"type": "string", "description": "Agent ID"},
                                        "updates": {
                                            "type": "object",
                                            "description": "Dictionary of fields to update"
                                        }
                                    },
                                    "required": ["agent_id", "updates"]
                                }
                            }
                        }
                    }
                }
            }
        )
    )
    
    # Main loop - read JSON-RPC requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            
            if request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                arguments = request.get("params", {}).get("arguments", {})
                
                result = None
                if tool_name == "send_coordination_message":
                    result = send_coordination_message(**arguments)
                elif tool_name == "get_coordination_status":
                    result = get_coordination_status(**arguments)
                elif tool_name == "track_coordination":
                    result = track_coordination(**arguments)
                elif tool_name == "identify_coordination_opportunities":
                    result = identify_coordination_opportunities(**arguments)
                elif tool_name == "get_agent_status":
                    result = get_agent_status(**arguments)
                elif tool_name == "update_agent_status":
                    result = update_agent_status(**arguments)
                else:
                    result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                
                print(
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request.get("id"),
                            "result": {"content": [{"type": "text", "text": json.dumps(result)}]},
                        }
                    )
                )
        except Exception as e:
            print(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": request.get("id") if 'request' in locals() else None,
                        "error": {"code": -32603, "message": str(e)},
                    }
                )
            )


if __name__ == "__main__":
    main()



