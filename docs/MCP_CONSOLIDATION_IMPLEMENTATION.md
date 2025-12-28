# MCP Tool Consolidation Implementation Guide

## Overview

**Problem:** 1444+ tools scattered across 63+ categories  
**Solution:** Unified MCP server architecture with category-specific servers

## Architecture

### Core MCP Servers (7)

1. **unified-tools** - Single entry point for all tools via tool registry
2. **swarm-messaging** - Agent messaging and coordination
3. **task-manager** - Task management operations
4. **website-manager** - WordPress and website operations
5. **swarm-brain** - Knowledge base operations
6. **git-operations** - Git verification and operations
7. **v2-compliance** - V2 compliance validation

### Unified Tool Server Features

The `unified-tool-server.py` provides:

- **Dynamic Tool Discovery:** Uses `tool_registry.py` to discover all tools
- **Unified Interface:** Single MCP endpoint for all tools
- **Tool Metadata:** Get tool info, parameters, examples
- **Tool Execution:** Execute any tool via MCP protocol
- **Tool Search:** Search tools by name or description

## Usage

### List All Tools

```python
# Via MCP
list_mcp_resources()  # Returns unified-tools server
# Then call: list_all_tools
```

### Execute Tool

```python
# Via MCP unified-tools server
execute_tool(
    tool_name="vector.search",
    query="find agent status",
    limit=10
)
```

### Get Tool Info

```python
# Via MCP unified-tools server
get_tool_info(tool_name="vector.search")
```

## Migration Strategy

### Phase 1: Unified Server (Complete ✅)
- ✅ Created `unified_tool_server.py`
- ✅ Integrated with tool registry
- ✅ Added to MCP configuration

### Phase 2: Category Servers (Next)
Create focused servers for major categories:
- `agent-operations-server.py` - Agent ops, onboarding, workflow
- `infrastructure-server.py` - Infrastructure, system, health
- `documentation-server.py` - Documentation tools
- `testing-server.py` - Testing and validation
- `business-intelligence-server.py` - BI, dashboards, observability

### Phase 3: Tool Migration
- Migrate high-priority tools to MCP servers
- Update tool registry with MCP metadata
- Create tool wrappers for MCP access

### Phase 4: Deprecation
- Mark standalone scripts as deprecated
- Add deprecation notices pointing to MCP servers
- Update documentation

## Benefits

1. **Single Entry Point:** All tools accessible via unified server
2. **Dynamic Discovery:** Tools automatically discovered via registry
3. **Type Safety:** Consistent interface across all tools
4. **Error Handling:** Centralized error handling
5. **Documentation:** Automatic tool documentation
6. **Extensibility:** Easy to add new tools

## Next Steps

1. **Test Unified Server:**
   ```bash
   python mcp_servers/unified_tool_server.py
   ```

2. **Add to Cursor Config:**
   Run `python tools/add_mcp_to_cursor_settings.py` to add unified-tools

3. **Verify Integration:**
   ```bash
   python tools/test_mcp_server_connectivity.py
   ```

4. **Create Category Servers:**
   Use migration script to generate category-specific servers

5. **Migrate High-Priority Tools:**
   Start with agent operations and coordination tools

## Configuration

Add to `mcp_servers/all_mcp_servers.json`:

```json
{
  "mcpServers": {
    "unified-tools": {
      "command": "python",
      "args": ["D:/Agent_Cellphone_V2_Repository/mcp_servers/unified_tool_server.py"],
      "description": "Unified tool server exposing all tools via tool registry"
    }
  }
}
```

Then run:
```bash
python tools/add_mcp_to_cursor_settings.py
```

## Status

- ✅ Unified tool server created
- ✅ Tool registry integration
- ✅ MCP configuration updated
- ⏳ Category servers (pending)
- ⏳ Tool migration (pending)
- ⏳ Documentation update (pending)

