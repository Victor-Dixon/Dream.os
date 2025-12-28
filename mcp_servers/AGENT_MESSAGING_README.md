# Agent Messaging MCP Server

A Model Context Protocol (MCP) server that provides a complete messaging system for agent-to-agent communication with coordinate management.

## Overview

This MCP server is a clone of the core messaging system, designed to allow:

- **Coordinate Management**: Set, update, and remove agent screen coordinates
- **Agent-to-Agent Messaging (A2A)**: Direct messaging between agents
- **Captain-to-Agent Messaging (C2A)**: Messages from the Captain to agents
- **Broadcast Messaging**: Send messages to all configured agents
- **Message History**: Track and query message history

## Installation

The server is already included in the `mcp_servers/` directory. To register it with your MCP client, add to your configuration:

```json
{
  "mcpServers": {
    "agent-messaging": {
      "command": "python",
      "args": ["path/to/mcp_servers/agent_messaging_mcp_server.py"],
      "description": "Agent-to-agent messaging with coordinate management"
    }
  }
}
```

## Tools Available

### 1. `set_agent_coordinates`

Set or update coordinates for an agent. Required for PyAutoGUI-based messaging.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | Agent identifier (e.g., "Agent-1") |
| `x` | integer | Yes | X coordinate for chat input |
| `y` | integer | Yes | Y coordinate for chat input |
| `description` | string | No | Agent description |
| `onboarding_x` | integer | No | X coordinate for onboarding |
| `onboarding_y` | integer | No | Y coordinate for onboarding |
| `active` | boolean | No | Whether agent is active (default: true) |

**Example:**
```json
{
  "agent_id": "Agent-1",
  "x": -1269,
  "y": 481,
  "description": "Integration Specialist",
  "active": true
}
```

### 2. `get_agent_coordinates`

Get coordinates for one or all agents.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | No | Specific agent ID, or omit for all |

**Example Response:**
```json
{
  "success": true,
  "agent_id": "Agent-1",
  "chat_coordinates": [-1269, 481],
  "onboarding_coordinates": [-1269, 431],
  "description": "Integration Specialist",
  "active": true
}
```

### 3. `remove_agent_coordinates`

Remove coordinates for an agent.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | Yes | Agent identifier to remove |

### 4. `send_agent_message`

Send a message from one agent to another.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sender` | string | Yes | Sender agent ID |
| `recipient` | string | Yes | Recipient agent ID |
| `message` | string | Yes | Message content |
| `priority` | string | No | "regular" or "urgent" |
| `message_type` | string | No | Override message type |

**Example:**
```json
{
  "sender": "Agent-1",
  "recipient": "Agent-2",
  "message": "Coordination request for task #123",
  "priority": "regular"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "abc12345",
  "sender": "Agent-1",
  "recipient": "Agent-2",
  "priority": "regular",
  "message_type": "agent_to_agent",
  "coordinates": [-308, 480],
  "delivered": true,
  "timestamp": "2025-12-28T10:30:00+00:00"
}
```

### 5. `broadcast_message`

Broadcast a message to all configured agents.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `sender` | string | Yes | Sender agent ID |
| `message` | string | Yes | Message content |
| `priority` | string | No | "regular" or "urgent" |
| `exclude_agents` | array | No | Agent IDs to exclude |

**Example:**
```json
{
  "sender": "CAPTAIN",
  "message": "System update: New task assignments available",
  "priority": "regular",
  "exclude_agents": ["Agent-4"]
}
```

### 6. `get_message_history`

Get message history with optional filters.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `agent_id` | string | No | Filter by agent (as sender or recipient) |
| `limit` | integer | No | Max messages (default: 50) |
| `sender_filter` | string | No | Filter by sender |
| `recipient_filter` | string | No | Filter by recipient |

### 7. `list_agents`

List all configured agents with their status.

**Response:**
```json
{
  "success": true,
  "total_agents": 8,
  "active_agents": 8,
  "agents": [
    {
      "agent_id": "Agent-1",
      "description": "Integration Specialist",
      "active": true,
      "has_coordinates": true
    }
  ]
}
```

### 8. `import_coordinates_from_config`

Import coordinates from the main `config/coordinates.json` file.

## Message Types

The server automatically determines message types:

| Tag | Type | Description |
|-----|------|-------------|
| `[A2A]` | Agent-to-Agent | Between two agents |
| `[C2A]` | Captain-to-Agent | From Captain/Agent-4 |
| `[A2C]` | Agent-to-Captain | To Captain/Agent-4 |
| `[S2A]` | System-to-Agent | System messages |
| `[MSG]` | Generic | Default fallback |

## Storage Files

The server uses two storage files in `config/`:

- `mcp_agent_coordinates.json` - Agent coordinates storage
- `mcp_message_history.json` - Message history (last 1000 messages)

## Quick Start

1. **Import existing coordinates:**
   ```
   import_coordinates_from_config
   ```

2. **Or set coordinates manually:**
   ```json
   {
     "tool": "set_agent_coordinates",
     "arguments": {
       "agent_id": "Agent-1",
       "x": -1269,
       "y": 481,
       "description": "Integration Specialist"
     }
   }
   ```

3. **Send a message:**
   ```json
   {
     "tool": "send_agent_message",
     "arguments": {
       "sender": "Agent-1",
       "recipient": "Agent-2",
       "message": "Hello from Agent-1!"
     }
   }
   ```

## PyAutoGUI Delivery

When PyAutoGUI is available, messages are delivered by:

1. Moving cursor to recipient's coordinates
2. Clicking to focus the input field
3. Clearing any existing content
4. Pasting the formatted message
5. Pressing Enter to send

If PyAutoGUI is not available, messages are logged but not delivered (indicated in the response).

## Dependencies

- Python 3.9+
- `pyautogui` (optional, for actual delivery)
- `pyperclip` (optional, for clipboard operations)

## Error Handling

All responses include a `success` boolean. On failure:

```json
{
  "success": false,
  "error": "Error description"
}
```

Common errors:
- Recipient not found (set coordinates first)
- Coordinates out of bounds
- PyAutoGUI not available

## Version History

- **1.0.0** - Initial release with full messaging capabilities
