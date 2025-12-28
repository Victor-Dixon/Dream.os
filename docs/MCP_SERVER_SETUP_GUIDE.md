# MCP Server Setup Guide for Cursor IDE

## Problem
MCP servers are functional but not accessible via `list_mcp_resources()` in Cursor.

## Solution Steps

### Step 1: Locate Cursor MCP Configuration

Cursor stores MCP server configuration in one of these locations:

**Windows:**
- User settings: `%APPDATA%\Cursor\User\settings.json` or `%APPDATA%\Cursor\User\globalStorage\mcp.json`
- Workspace settings: `.cursor/mcp.json` or `.vscode/settings.json`

**macOS:**
- `~/Library/Application Support/Cursor/User/settings.json`
- `~/.cursor/mcp.json`

**Linux:**
- `~/.config/Cursor/User/settings.json`
- `~/.cursor/mcp.json`

### Step 2: Add MCP Configuration

#### Option A: Workspace Configuration (Recommended)

Create `.cursor/mcp.json` in your workspace root:

```json
{
  "mcpServers": {
    "swarm-messaging": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/messaging_server.py"
      ]
    },
    "task-manager": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/task_manager_server.py"
      ]
    },
    "website-manager": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/website_manager_server.py"
      ]
    },
    "swarm-brain": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/swarm_brain_server.py"
      ]
    },
    "git-operations": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/git_operations_server.py"
      ]
    },
    "v2-compliance": {
      "command": "python",
      "args": [
        "D:/Agent_Cellphone_V2_Repository/mcp_servers/v2_compliance_server.py"
      ]
    }
  }
}
```

#### Option B: User Settings

Add to Cursor User Settings (`Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)"):

```json
{
  "mcp.servers": {
    "swarm-messaging": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/messaging_server.py"]
    },
    "task-manager": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/task_manager_server.py"]
    },
    "website-manager": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/website_manager_server.py"]
    },
    "swarm-brain": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/swarm_brain_server.py"]
    },
    "git-operations": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/git_operations_server.py"]
    },
    "v2-compliance": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/v2_compliance_server.py"]
    }
  }
}
```

### Step 3: Verify Python Path

Ensure `python` command is in your PATH. Test with:

```bash
python --version
```

If `python` doesn't work, use full path:

```json
"command": "C:/Python311/python.exe"
```

### Step 4: Restart Cursor

**CRITICAL:** After adding/updating MCP configuration:
1. Completely quit Cursor (not just close window)
2. Restart Cursor
3. MCP servers should auto-start

### Step 5: Verify Connection

After restart, test MCP server access:

```python
# In Cursor AI chat or Python script
from mcp import list_mcp_resources
resources = list_mcp_resources()
print(f"Found {len(resources)} MCP resources")
```

Or use the diagnostic tool:

```bash
python tools/test_mcp_server_connectivity.py
```

### Step 6: Check MCP Server Logs

If servers still don't connect:

1. **Open Cursor Developer Tools:**
   - `Ctrl+Shift+P` → "Developer: Toggle Developer Tools"
   - Check Console tab for MCP errors

2. **Check MCP Server Output:**
   - Look for server startup errors
   - Verify Python can execute server files
   - Check for missing dependencies

3. **Test Server Manually:**
   ```bash
   python mcp_servers/task_manager_server.py
   ```
   - Should start and wait for stdin input
   - If it errors, fix the issue before Cursor can connect

## Troubleshooting

### Issue: "No MCP resources found"

**Solutions:**
1. Verify `.cursor/mcp.json` exists and is valid JSON
2. Check file paths are correct (use forward slashes `/` or escaped backslashes `\\`)
3. Ensure Python is accessible from Cursor's PATH
4. Restart Cursor completely (not just reload window)
5. Check Cursor Developer Tools console for errors

### Issue: "Server failed to start"

**Solutions:**
1. Test server manually: `python mcp_servers/task_manager_server.py`
2. Check Python dependencies are installed
3. Verify file paths are absolute and correct
4. Check file permissions (server files must be readable)

### Issue: "Module not found" errors

**Solutions:**
1. Install missing Python packages
2. Verify `sys.path` includes project root (servers do this automatically)
3. Check Python version compatibility

## Alternative: Direct Python Imports

If MCP protocol still doesn't work, servers can be used directly:

```python
# Direct import (works without MCP protocol)
from mcp_servers import task_manager_server
result = task_manager_server.get_tasks('INBOX')
```

This bypasses MCP protocol but provides same functionality.

## Configuration Reference

See `mcp_servers/all_mcp_servers.json` for the canonical server configuration.

## Last Updated

2025-12-27 by Agent-6


