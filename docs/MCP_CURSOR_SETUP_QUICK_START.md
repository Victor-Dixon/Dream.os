# Quick Start: Fix MCP Server Connection in Cursor

## The Problem
MCP servers work but aren't connected to Cursor's MCP system.

## The Solution (3 Steps)

### Step 1: Open Cursor Settings
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type: `Preferences: Open User Settings (JSON)`
3. Press Enter

### Step 2: Add MCP Configuration
Add this to your `settings.json` file:

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

**Important:** If you already have settings in `settings.json`, add `"mcp.servers"` to the existing JSON object (don't replace the whole file).

### Step 3: Restart Cursor
1. **Completely quit Cursor** (File → Exit, or close all windows)
2. **Restart Cursor**
3. MCP servers should auto-start

### Verify It Works

After restart, test with:

```bash
python tools/test_mcp_server_connectivity.py
```

Or check Cursor Developer Tools (`Ctrl+Shift+I`) for MCP server startup messages.

## Troubleshooting

### Still Not Working?

1. **Check Python Path:**
   ```bash
   python --version
   ```
   If `python` doesn't work, use full path in config:
   ```json
   "command": "C:/Python311/python.exe"
   ```

2. **Test Server Manually:**
   ```bash
   python mcp_servers/task_manager_server.py
   ```
   Should start and wait for input (press Ctrl+C to stop)

3. **Check Cursor Logs:**
   - `Ctrl+Shift+I` → Console tab
   - Look for MCP errors

4. **Verify File Paths:**
   - Ensure paths use forward slashes `/` or escaped backslashes `\\`
   - Paths must be absolute (full path from drive letter)

## Alternative: Use Direct Imports

If MCP still doesn't work, servers can be used directly:

```python
from mcp_servers import task_manager_server
result = task_manager_server.get_tasks('INBOX')
```

This bypasses MCP protocol but provides same functionality.

## Generated Config File

Run `python tools/setup_cursor_mcp.py` to generate `CURSOR_MCP_CONFIG.json` with the exact configuration needed.


