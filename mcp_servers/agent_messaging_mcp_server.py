#!/usr/bin/env python3
"""
Agent Messaging MCP Server
==========================

A Model Context Protocol (MCP) server that provides a complete messaging system
for agent-to-agent communication with coordinate management.

Features:
- Set/update agent coordinates for PyAutoGUI-based messaging
- Agent-to-agent messaging (A2A)
- Captain-to-agent messaging (C2A)
- Broadcast messaging to all agents
- Message history tracking
- Coordinate validation and management

Author: Agent Swarm
Version: 1.0.0
"""

import json
import sys
import uuid
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Coordinates storage path
COORDINATES_FILE = PROJECT_ROOT / "config" / "mcp_agent_coordinates.json"
MESSAGE_HISTORY_FILE = PROJECT_ROOT / "config" / "mcp_message_history.json"

# Thread lock for file operations
_file_lock = threading.Lock()


# =============================================================================
# Data Models
# =============================================================================

class MessagePriority:
    REGULAR = "regular"
    URGENT = "urgent"


class MessageType:
    AGENT_TO_AGENT = "agent_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    BROADCAST = "broadcast"
    SYSTEM = "system"


# =============================================================================
# Coordinate Management
# =============================================================================

def _load_coordinates() -> dict[str, Any]:
    """Load coordinates from the SSOT file."""
    with _file_lock:
        if not COORDINATES_FILE.exists():
            # Initialize with default structure
            default_coords = {
                "agents": {},
                "metadata": {
                    "description": "MCP Agent Messaging Coordinates",
                    "version": "1.0",
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                },
                "validation_rules": {
                    "coordinate_bounds": {
                        "min_x": -5000,
                        "max_x": 5000,
                        "min_y": -2000,
                        "max_y": 5000
                    }
                }
            }
            COORDINATES_FILE.parent.mkdir(parents=True, exist_ok=True)
            COORDINATES_FILE.write_text(json.dumps(default_coords, indent=2))
            return default_coords
        
        try:
            return json.loads(COORDINATES_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError) as e:
            return {"agents": {}, "error": str(e)}


def _save_coordinates(data: dict[str, Any]) -> bool:
    """Save coordinates to the SSOT file."""
    with _file_lock:
        try:
            data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            COORDINATES_FILE.parent.mkdir(parents=True, exist_ok=True)
            COORDINATES_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return True
        except (IOError, OSError) as e:
            return False


def _validate_coordinates(x: int, y: int, data: dict[str, Any]) -> tuple[bool, str]:
    """Validate coordinates against bounds."""
    bounds = data.get("validation_rules", {}).get("coordinate_bounds", {})
    min_x = bounds.get("min_x", -5000)
    max_x = bounds.get("max_x", 5000)
    min_y = bounds.get("min_y", -2000)
    max_y = bounds.get("max_y", 5000)
    
    if x < min_x or x > max_x:
        return False, f"X coordinate {x} out of bounds ({min_x} to {max_x})"
    if y < min_y or y > max_y:
        return False, f"Y coordinate {y} out of bounds ({min_y} to {max_y})"
    
    return True, "Valid"


# =============================================================================
# Message History
# =============================================================================

def _load_message_history() -> list[dict[str, Any]]:
    """Load message history from file."""
    with _file_lock:
        if not MESSAGE_HISTORY_FILE.exists():
            MESSAGE_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
            MESSAGE_HISTORY_FILE.write_text("[]")
            return []
        
        try:
            return json.loads(MESSAGE_HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return []


def _save_message_to_history(message: dict[str, Any]) -> bool:
    """Append message to history file."""
    with _file_lock:
        try:
            history = _load_message_history()
            # Keep only last 1000 messages
            if len(history) >= 1000:
                history = history[-999:]
            history.append(message)
            MESSAGE_HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")
            return True
        except (IOError, OSError):
            return False


# =============================================================================
# MCP Tool Implementations
# =============================================================================

def set_agent_coordinates(
    agent_id: str,
    x: int,
    y: int,
    description: Optional[str] = None,
    onboarding_x: Optional[int] = None,
    onboarding_y: Optional[int] = None,
    active: bool = True
) -> dict[str, Any]:
    """
    Set or update coordinates for an agent.
    
    Args:
        agent_id: Agent identifier (e.g., "Agent-1", "Agent-2")
        x: X coordinate for chat input
        y: Y coordinate for chat input
        description: Optional agent description
        onboarding_x: Optional X coordinate for onboarding (defaults to x)
        onboarding_y: Optional Y coordinate for onboarding (defaults to y-50)
        active: Whether the agent is active
    
    Returns:
        Result dictionary with success status
    """
    try:
        data = _load_coordinates()
        
        # Validate coordinates
        valid, error_msg = _validate_coordinates(x, y, data)
        if not valid:
            return {"success": False, "error": error_msg}
        
        # Set onboarding coordinates if not provided
        if onboarding_x is None:
            onboarding_x = x
        if onboarding_y is None:
            onboarding_y = y - 50  # Default offset
        
        # Validate onboarding coordinates
        valid, error_msg = _validate_coordinates(onboarding_x, onboarding_y, data)
        if not valid:
            return {"success": False, "error": f"Onboarding coordinates: {error_msg}"}
        
        # Update agent entry
        data["agents"][agent_id] = {
            "chat_input_coordinates": [x, y],
            "onboarding_coordinates": [onboarding_x, onboarding_y],
            "description": description or f"Agent {agent_id}",
            "active": active,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }
        
        if _save_coordinates(data):
            return {
                "success": True,
                "agent_id": agent_id,
                "coordinates": {
                    "chat": [x, y],
                    "onboarding": [onboarding_x, onboarding_y]
                },
                "active": active
            }
        else:
            return {"success": False, "error": "Failed to save coordinates"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_agent_coordinates(agent_id: Optional[str] = None) -> dict[str, Any]:
    """
    Get coordinates for one or all agents.
    
    Args:
        agent_id: Optional specific agent ID. If not provided, returns all agents.
    
    Returns:
        Dictionary with agent coordinates and status
    """
    try:
        data = _load_coordinates()
        agents = data.get("agents", {})
        
        if agent_id:
            if agent_id in agents:
                agent_data = agents[agent_id]
                return {
                    "success": True,
                    "agent_id": agent_id,
                    "chat_coordinates": agent_data.get("chat_input_coordinates"),
                    "onboarding_coordinates": agent_data.get("onboarding_coordinates"),
                    "description": agent_data.get("description", ""),
                    "active": agent_data.get("active", True),
                    "last_updated": agent_data.get("last_updated")
                }
            else:
                return {"success": False, "error": f"Agent {agent_id} not found"}
        else:
            # Return all agents
            result = {"success": True, "agents": {}}
            for aid, agent_data in agents.items():
                result["agents"][aid] = {
                    "chat_coordinates": agent_data.get("chat_input_coordinates"),
                    "onboarding_coordinates": agent_data.get("onboarding_coordinates"),
                    "description": agent_data.get("description", ""),
                    "active": agent_data.get("active", True)
                }
            return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def remove_agent_coordinates(agent_id: str) -> dict[str, Any]:
    """
    Remove coordinates for an agent.
    
    Args:
        agent_id: Agent identifier to remove
    
    Returns:
        Result dictionary with success status
    """
    try:
        data = _load_coordinates()
        
        if agent_id not in data.get("agents", {}):
            return {"success": False, "error": f"Agent {agent_id} not found"}
        
        del data["agents"][agent_id]
        
        if _save_coordinates(data):
            return {"success": True, "message": f"Agent {agent_id} coordinates removed"}
        else:
            return {"success": False, "error": "Failed to save changes"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_agent_message(
    sender: str,
    recipient: str,
    message: str,
    priority: str = "regular",
    message_type: Optional[str] = None
) -> dict[str, Any]:
    """
    Send a message from one agent to another.
    
    Args:
        sender: Sender agent ID (e.g., "Agent-1", "CAPTAIN")
        recipient: Recipient agent ID (e.g., "Agent-2")
        message: Message content
        priority: Message priority ("regular" or "urgent")
        message_type: Optional message type override
    
    Returns:
        Result dictionary with delivery status
    """
    try:
        # Validate priority
        if priority not in [MessagePriority.REGULAR, MessagePriority.URGENT]:
            priority = MessagePriority.REGULAR
        
        # Determine message type
        if message_type is None:
            if sender.upper() in ["CAPTAIN", "AGENT-4"]:
                message_type = MessageType.CAPTAIN_TO_AGENT
            elif sender.startswith("Agent-") and recipient.startswith("Agent-"):
                message_type = MessageType.AGENT_TO_AGENT
            else:
                message_type = MessageType.SYSTEM
        
        # Load coordinates to validate recipient exists
        data = _load_coordinates()
        agents = data.get("agents", {})
        
        if recipient not in agents:
            return {
                "success": False,
                "error": f"Recipient {recipient} not found in coordinates. Set coordinates first.",
                "available_agents": list(agents.keys())
            }
        
        recipient_coords = agents[recipient].get("chat_input_coordinates", [0, 0])
        
        # Create message record
        message_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now(timezone.utc).isoformat()
        
        message_record = {
            "message_id": message_id,
            "sender": sender,
            "recipient": recipient,
            "content": message,
            "priority": priority,
            "message_type": message_type,
            "timestamp": timestamp,
            "coordinates": recipient_coords,
            "delivered": False,
            "delivery_method": "pyautogui"
        }
        
        # Try to deliver via PyAutoGUI if available
        delivery_success = False
        delivery_error = None
        
        try:
            # Attempt PyAutoGUI delivery
            import pyautogui
            import pyperclip
            
            x, y = recipient_coords
            
            # Format the message with proper tag
            tag = _get_message_tag(sender, recipient)
            formatted_message = f"{tag} {recipient}\n\n{message}"
            if priority == MessagePriority.URGENT:
                formatted_message = f"🚨 URGENT MESSAGE 🚨\n\n{formatted_message}"
            
            # PyAutoGUI delivery sequence
            pyautogui.moveTo(x, y, duration=0.3)
            pyautogui.click()
            import time
            time.sleep(0.3)
            
            # Clear and paste
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(0.1)
            
            pyperclip.copy(formatted_message)
            time.sleep(0.3)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.3)
            pyautogui.press('enter')
            
            delivery_success = True
            message_record["delivered"] = True
            
        except ImportError:
            delivery_error = "PyAutoGUI not available - message logged but not delivered"
            message_record["delivery_method"] = "logged_only"
        except Exception as e:
            delivery_error = f"Delivery failed: {str(e)}"
        
        # Save to history
        _save_message_to_history(message_record)
        
        result = {
            "success": True,
            "message_id": message_id,
            "sender": sender,
            "recipient": recipient,
            "priority": priority,
            "message_type": message_type,
            "coordinates": recipient_coords,
            "delivered": delivery_success,
            "timestamp": timestamp
        }
        
        if delivery_error:
            result["delivery_note"] = delivery_error
        
        return result
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def broadcast_message(
    sender: str,
    message: str,
    priority: str = "regular",
    exclude_agents: Optional[list[str]] = None
) -> dict[str, Any]:
    """
    Broadcast a message to all agents.
    
    Args:
        sender: Sender agent ID
        message: Message content
        priority: Message priority
        exclude_agents: Optional list of agent IDs to exclude
    
    Returns:
        Result dictionary with broadcast status
    """
    try:
        data = _load_coordinates()
        agents = data.get("agents", {})
        
        if not agents:
            return {"success": False, "error": "No agents configured. Set coordinates first."}
        
        exclude_list = set(exclude_agents or [])
        results = {}
        success_count = 0
        
        for agent_id in agents.keys():
            if agent_id in exclude_list:
                results[agent_id] = {"status": "skipped", "reason": "excluded"}
                continue
            
            result = send_agent_message(
                sender=sender,
                recipient=agent_id,
                message=message,
                priority=priority,
                message_type=MessageType.BROADCAST
            )
            
            if result.get("success"):
                success_count += 1
                results[agent_id] = {
                    "status": "sent",
                    "delivered": result.get("delivered", False),
                    "message_id": result.get("message_id")
                }
            else:
                results[agent_id] = {
                    "status": "failed",
                    "error": result.get("error")
                }
        
        return {
            "success": success_count > 0,
            "total_agents": len(agents),
            "successful": success_count,
            "excluded": len(exclude_list),
            "results": results
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_message_history(
    agent_id: Optional[str] = None,
    limit: int = 50,
    sender_filter: Optional[str] = None,
    recipient_filter: Optional[str] = None
) -> dict[str, Any]:
    """
    Get message history with optional filters.
    
    Args:
        agent_id: Optional agent ID to filter (as sender or recipient)
        limit: Maximum number of messages to return
        sender_filter: Filter by sender
        recipient_filter: Filter by recipient
    
    Returns:
        Dictionary with message history
    """
    try:
        history = _load_message_history()
        
        # Apply filters
        filtered = history
        
        if agent_id:
            filtered = [
                m for m in filtered 
                if m.get("sender") == agent_id or m.get("recipient") == agent_id
            ]
        
        if sender_filter:
            filtered = [m for m in filtered if m.get("sender") == sender_filter]
        
        if recipient_filter:
            filtered = [m for m in filtered if m.get("recipient") == recipient_filter]
        
        # Sort by timestamp (newest first) and limit
        filtered = sorted(filtered, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
        
        return {
            "success": True,
            "count": len(filtered),
            "messages": filtered
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def list_agents() -> dict[str, Any]:
    """
    List all configured agents with their status.
    
    Returns:
        Dictionary with agent list and status
    """
    try:
        data = _load_coordinates()
        agents = data.get("agents", {})
        
        agent_list = []
        for agent_id, agent_data in agents.items():
            agent_list.append({
                "agent_id": agent_id,
                "description": agent_data.get("description", ""),
                "active": agent_data.get("active", True),
                "has_coordinates": bool(agent_data.get("chat_input_coordinates"))
            })
        
        # Sort by agent ID
        agent_list = sorted(agent_list, key=lambda x: x["agent_id"])
        
        return {
            "success": True,
            "total_agents": len(agent_list),
            "active_agents": sum(1 for a in agent_list if a["active"]),
            "agents": agent_list
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def import_coordinates_from_config() -> dict[str, Any]:
    """
    Import coordinates from the main config/coordinates.json file.
    
    Returns:
        Result dictionary with import status
    """
    try:
        source_file = PROJECT_ROOT / "config" / "coordinates.json"
        
        if not source_file.exists():
            return {"success": False, "error": "Source coordinates.json not found"}
        
        source_data = json.loads(source_file.read_text(encoding="utf-8"))
        source_agents = source_data.get("agents", {})
        
        if not source_agents:
            return {"success": False, "error": "No agents found in source file"}
        
        imported_count = 0
        for agent_id, agent_data in source_agents.items():
            chat_coords = agent_data.get("chat_input_coordinates", [0, 0])
            onboarding_coords = agent_data.get("onboarding_coordinates", chat_coords)
            
            result = set_agent_coordinates(
                agent_id=agent_id,
                x=chat_coords[0],
                y=chat_coords[1],
                description=agent_data.get("description", ""),
                onboarding_x=onboarding_coords[0],
                onboarding_y=onboarding_coords[1],
                active=agent_data.get("active", True)
            )
            
            if result.get("success"):
                imported_count += 1
        
        return {
            "success": True,
            "imported": imported_count,
            "total_in_source": len(source_agents)
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# =============================================================================
# Helper Functions
# =============================================================================

def _get_message_tag(sender: str, recipient: str) -> str:
    """Determine the correct message tag based on sender and recipient."""
    sender_upper = sender.upper()
    
    if sender_upper in ["CAPTAIN", "AGENT-4"]:
        return "[C2A]"
    elif sender_upper == "SYSTEM":
        return "[S2A]"
    elif sender.startswith("Agent-") and recipient.startswith("Agent-"):
        return "[A2A]"
    elif recipient.upper() in ["CAPTAIN", "AGENT-4"]:
        return "[A2C]"
    else:
        return "[MSG]"


# =============================================================================
# MCP Server Protocol Implementation
# =============================================================================

def get_tool_definitions() -> dict:
    """Return MCP tool definitions."""
    return {
        "set_agent_coordinates": {
            "description": "Set or update coordinates for an agent. Required for PyAutoGUI-based messaging.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Agent identifier (e.g., 'Agent-1', 'Agent-2')"
                    },
                    "x": {
                        "type": "integer",
                        "description": "X coordinate for chat input"
                    },
                    "y": {
                        "type": "integer",
                        "description": "Y coordinate for chat input"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional agent description"
                    },
                    "onboarding_x": {
                        "type": "integer",
                        "description": "Optional X coordinate for onboarding"
                    },
                    "onboarding_y": {
                        "type": "integer",
                        "description": "Optional Y coordinate for onboarding"
                    },
                    "active": {
                        "type": "boolean",
                        "description": "Whether the agent is active",
                        "default": True
                    }
                },
                "required": ["agent_id", "x", "y"]
            }
        },
        "get_agent_coordinates": {
            "description": "Get coordinates for one or all agents",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Optional specific agent ID. If not provided, returns all agents."
                    }
                }
            }
        },
        "remove_agent_coordinates": {
            "description": "Remove coordinates for an agent",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Agent identifier to remove"
                    }
                },
                "required": ["agent_id"]
            }
        },
        "send_agent_message": {
            "description": "Send a message from one agent to another via PyAutoGUI",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "string",
                        "description": "Sender agent ID (e.g., 'Agent-1', 'CAPTAIN')"
                    },
                    "recipient": {
                        "type": "string",
                        "description": "Recipient agent ID (e.g., 'Agent-2')"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content to send"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["regular", "urgent"],
                        "description": "Message priority level",
                        "default": "regular"
                    },
                    "message_type": {
                        "type": "string",
                        "description": "Optional message type override"
                    }
                },
                "required": ["sender", "recipient", "message"]
            }
        },
        "broadcast_message": {
            "description": "Broadcast a message to all configured agents",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "string",
                        "description": "Sender agent ID"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content to broadcast"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["regular", "urgent"],
                        "description": "Message priority",
                        "default": "regular"
                    },
                    "exclude_agents": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of agent IDs to exclude"
                    }
                },
                "required": ["sender", "message"]
            }
        },
        "get_message_history": {
            "description": "Get message history with optional filters",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Optional agent ID to filter (as sender or recipient)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of messages to return",
                        "default": 50
                    },
                    "sender_filter": {
                        "type": "string",
                        "description": "Filter by sender"
                    },
                    "recipient_filter": {
                        "type": "string",
                        "description": "Filter by recipient"
                    }
                }
            }
        },
        "list_agents": {
            "description": "List all configured agents with their status",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        },
        "import_coordinates_from_config": {
            "description": "Import coordinates from the main config/coordinates.json file",
            "inputSchema": {
                "type": "object",
                "properties": {}
            }
        }
    }


def handle_tool_call(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Route tool calls to appropriate handlers."""
    handlers = {
        "set_agent_coordinates": set_agent_coordinates,
        "get_agent_coordinates": get_agent_coordinates,
        "remove_agent_coordinates": remove_agent_coordinates,
        "send_agent_message": send_agent_message,
        "broadcast_message": broadcast_message,
        "get_message_history": get_message_history,
        "list_agents": list_agents,
        "import_coordinates_from_config": import_coordinates_from_config,
    }
    
    handler = handlers.get(tool_name)
    if handler:
        return handler(**arguments)
    else:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}


def main():
    """MCP server main loop."""
    # Send initialization response
    tools = get_tool_definitions()
    
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": tools
            },
            "serverInfo": {
                "name": "agent-messaging-mcp-server",
                "version": "1.0.0",
                "description": "Agent-to-agent messaging with coordinate management"
            }
        }
    }))
    sys.stdout.flush()
    
    # Handle incoming requests
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "tools/list":
                # Return tool list
                tool_list = [
                    {"name": name, **definition}
                    for name, definition in tools.items()
                ]
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tool_list}
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                result = handle_tool_call(tool_name, arguments)
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps(result, indent=2)
                        }]
                    }
                }
            
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"}
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in dir() else None,
                "error": {"code": -32603, "message": f"Internal error: {e}"}
            }))
            sys.stdout.flush()


if __name__ == "__main__":
    main()
