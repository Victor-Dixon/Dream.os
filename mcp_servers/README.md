# MCP Servers

Centralized Model Context Protocol (MCP) servers for the Agent Cellphone V2 system.

## Available Servers

### Core Servers

| Server | Description | Tools |
|--------|-------------|-------|
| `task-manager` | MASTER_TASK_LOG.md operations | `add_task_to_inbox`, `mark_task_complete`, `move_task_to_waiting`, `get_tasks` |
| `swarm-messaging` | PyAutoGUI-based agent messaging | `send_agent_message`, `broadcast_message`, `get_agent_coordinates` |
| `swarm-brain` | Knowledge base access | `share_learning`, `record_decision`, `search_swarm_knowledge`, `take_note`, `get_agent_notes` |
| `website-manager` | WordPress/website operations | Site management, deployment, content updates |
| `git-operations` | Git operations and verification | Commit tracking, work verification |
| `v2-compliance` | V2 compliance validation | Compliance checking, standard enforcement |

### Consolidated Servers (NEW)

These servers consolidate functionality from scattered standalone tools:

| Server | Replaces | Tools |
|--------|----------|-------|
| `devlog-manager` | `devlog_*.py` (6 files) | `post_devlog`, `validate_devlog`, `create_devlog`, `list_devlogs`, `generate_devlog_feed` |
| `discord-integration` | `discord_*.py`, `webhook_*.py` (7 files) | `post_to_webhook`, `post_agent_update`, `validate_webhook`, `send_embed`, `get_configured_webhooks`, `post_build_notification` |
| `cleanup-manager` | `cleanup_*.py`, `session_*.py` (10 files) | `cleanup_agent_inbox`, `cleanup_all_inboxes`, `session_cleanup`, `archive_completed_tasks`, `get_workspace_status`, `consolidate_documentation` |
| `deployment-manager` | `deploy_*.py`, `verify_*.py` (4 files) | `check_deployment_status`, `verify_deployment`, `list_deployable_sites`, `get_deployment_history`, `record_deployment`, `check_all_sites`, `get_sftp_credentials` |

## Configuration

MCP servers are configured in:
- **Project config**: `mcp_servers/all_mcp_servers.json`
- **Cursor config**: `~/.cursor/mcp.json`

## Usage

### Via Cursor MCP Tools

After configuring in Cursor, MCP tools are available directly:

```
mcp_task-manager_add_task_to_inbox(task="New task", agent_id="Agent-1")
mcp_devlog-manager_create_devlog(agent_id="Agent-3", title="Status Update", content="...")
mcp_discord-integration_post_to_webhook(webhook_url="...", message="Hello!")
```

### Direct Python Usage

```python
from mcp_servers.devlog_manager_server import create_devlog, post_devlog

result = create_devlog("Agent-3", "My Devlog", "Content here...")
print(result)
```

## Deprecated Standalone Tools

The following tools are now **DEPRECATED** in favor of MCP servers:

### Devlog Tools → `devlog-manager` MCP
- `tools/devlog_manager.py` → Use `mcp_devlog-manager_*`
- `tools/devlog_poster.py` → Use `mcp_devlog-manager_post_devlog`
- `tools/devlog_poster_agent_channel.py` → Use `mcp_devlog-manager_post_devlog`
- `tools/devlog_compliance_validator.py` → Use `mcp_devlog-manager_validate_devlog`
- `tools/devlog_auto_poster.py` → Use `mcp_devlog-manager_post_devlog`
- `tools/generate_devlog_feed.py` → Use `mcp_devlog-manager_generate_devlog_feed`

### Discord Tools → `discord-integration` MCP
- `tools/discord_webhook_validator.py` → Use `mcp_discord-integration_validate_webhook`
- `tools/post_agent*_devlog_to_discord.py` → Use `mcp_discord-integration_post_agent_update`
- `tools/start_discord_system.py` → Still needed for bot startup
- `tools/test_discord_commands.py` → Use for testing only

### Cleanup Tools → `cleanup-manager` MCP
- `tools/cleanup_agent_workspaces.py` → Use `mcp_cleanup-manager_cleanup_all_inboxes`
- `tools/cleanup_inbox.py` → Use `mcp_cleanup-manager_cleanup_agent_inbox`
- `tools/session_cleanup_manager.py` → Use `mcp_cleanup-manager_session_cleanup`
- `tools/archive_completed_tasks.py` → Use `mcp_cleanup-manager_archive_completed_tasks`
- `tools/post_session_cleanup.py` → Use `mcp_cleanup-manager_session_cleanup`
- `tools/consolidate_documentation.py` → Use `mcp_cleanup-manager_consolidate_documentation`

### Deployment Tools → `deployment-manager` MCP
- `tools/deployment_status_checker.py` → Use `mcp_deployment-manager_check_deployment_status`
- `tools/deployment_verification_tool.py` → Use `mcp_deployment-manager_verify_deployment`
- `tools/verify_deployment_integration.py` → Use `mcp_deployment-manager_verify_deployment`

## Adding New MCP Servers

1. Create server file: `mcp_servers/<name>_server.py`
2. Implement MCP protocol (see existing servers for template)
3. Add to `all_mcp_servers.json`
4. Update Cursor config: `~/.cursor/mcp.json`
5. Restart Cursor

## Testing

```bash
# Test all server imports
python tools/test_mcp_server_connectivity.py

# Debug MCP servers
python tools/debug_mcp_servers.py
```
