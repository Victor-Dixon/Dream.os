# MCP Server Debugging Guide

## Current Status

All 6 MCP servers are configured and have valid Python syntax:
- ✅ swarm-messaging
- ✅ task-manager  
- ✅ website-manager
- ✅ swarm-brain
- ✅ git-operations
- ✅ v2-compliance

## Issue: MCP Servers Not Available

When calling `list_mcp_resources()`, no resources are returned. This indicates the MCP servers are not connected to Cursor.

## Root Cause

MCP servers need to be registered in Cursor's MCP configuration. The configuration file `mcp_servers/all_mcp_servers.json` exists, but Cursor needs to be configured to use it.

## Solution Steps

### 1. Verify Cursor MCP Configuration

Cursor MCP servers are configured in one of these locations:
- Cursor Settings → MCP Servers
- `.cursor/mcp.json` (workspace-specific)
- Global Cursor settings

### 2. Register MCP Servers in Cursor

The MCP server configuration is in `mcp_servers/all_mcp_servers.json`. You need to:

1. Open Cursor Settings
2. Navigate to MCP Servers section
3. Add each server from `all_mcp_servers.json`:
   ```json
   {
     "mcpServers": {
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

### 3. Verify Server Startup

Test each server manually:
```bash
python mcp_servers/task_manager_server.py
```

Expected: Server should output JSON-RPC initialization message and wait for input.

### 4. Check Cursor MCP Logs

Check Cursor's MCP server logs for connection errors:
- Cursor → View → Output → Select "MCP" channel
- Look for connection errors or startup failures

### 5. Verify Dependencies

Ensure all Python dependencies are installed:
```bash
pip install -r requirements.txt
```

## Debugging Tool

Use the debugging tool to check server status:
```bash
python tools/debug_mcp_servers.py
```

This will:
- Verify all server files exist
- Check Python syntax validity
- Test server startup (timeout is expected - servers wait for JSON-RPC)

## Common Issues

1. **Servers not appearing in Cursor**
   - Check Cursor MCP settings are configured
   - Restart Cursor after adding servers
   - Verify paths are absolute and correct

2. **Import errors**
   - Ensure project root is in Python path
   - Check all dependencies are installed

3. **Timeout on startup**
   - This is expected! MCP servers wait for JSON-RPC input
   - Timeout in test is normal behavior

4. **Connection refused**
   - Check Cursor MCP logs
   - Verify Python executable path is correct
   - Ensure no firewall blocking

## Next Steps

1. ✅ Created debugging tool (`tools/debug_mcp_servers.py`)
2. ⏳ Verify Cursor MCP configuration
3. ⏳ Test server connections
4. ⏳ Document any Cursor-specific configuration needed

