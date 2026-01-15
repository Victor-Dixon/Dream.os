# MCP Tool Consolidation Plan

## Problem Statement

Tools are scattered across the codebase:
- **Standalone scripts** in `tools/` directory (100+ files)
- **Category-organized tools** in `tools/categories/` (50+ files)
- **Existing MCP servers** in `mcp_servers/` (6 servers)
- **Tool registry system** (`tool_registry.py`) managing dynamic tool discovery

**Goal:** Consolidate all tools into centralized MCP servers for unified access.

## Current State Analysis

### Existing MCP Servers (6)
1. **swarm-messaging** - PyAutoGUI-based agent messaging
2. **task-manager** - MASTER_TASK_LOG.md operations
3. **website-manager** - WordPress and website management
4. **swarm-brain** - Knowledge base operations
5. **git-operations** - Git verification and commit checking
6. **v2-compliance** - V2 compliance validation

### Scattered Tools Categories

#### 1. Agent Operations Tools
- `tools/categories/agent_ops_tools.py`
- `tools/categories/agent_activity_tools.py`
- `tools/categories/autonomous_workflow_tools.py`
- `tools/categories/onboarding_tools.py`
- **Target:** New MCP server `agent-operations`

#### 2. Coordination & Communication Tools
- `tools/categories/communication_tools.py`
- `tools/categories/coordination_tools.py`
- `tools/categories/messaging_tools.py`
- `tools/categories/discord_tools.py`
- `tools/devlog_manager.py`
- **Target:** Enhance `swarm-messaging` server

#### 3. Website & WordPress Tools
- `tools/categories/web_tools.py`
=======
- `mcp_servers/wp_cli_manager_server.py` (canonical replacement)
>>>>>>> origin/codex/build-tsla-morning-report-system
- `tools/create_icp_definitions.py`
- `tools/deploy_*.py` scripts
- **Target:** Enhance `website-manager` server

#### 4. Analysis & Validation Tools
- `tools/categories/analysis_tools.py`
- `tools/categories/validation_tools.py`
- `tools/categories/v2_tools.py`
- `tools/categories/compliance_tools.py`
- `tools/categories/ssot_validation_tools.py`
- **Target:** Enhance `v2-compliance` server + new `analysis` server

#### 5. Infrastructure & DevOps Tools
- `tools/categories/infrastructure_tools.py`
- `tools/categories/infrastructure_audit_tools.py`
- `tools/categories/system_tools.py`
- `tools/categories/health_tools.py`
- **Target:** New MCP server `infrastructure`

#### 6. Documentation Tools
- `tools/categories/docs_tools.py`
- `tools/cleanup_documentation.py`
- `tools/enhance_documentation_navigation.py`
- **Target:** New MCP server `documentation`

#### 7. Testing Tools
- `tools/categories/testing_tools.py`
- `tools/categories/test_generation_tools.py`
- **Target:** New MCP server `testing`

#### 8. Business Intelligence Tools
- `tools/categories/bi_tools.py`
- `tools/categories/dashboard_tools.py`
- `tools/categories/observability_tools.py`
- **Target:** New MCP server `business-intelligence`

## Consolidation Strategy

### Phase 1: Create Unified Tool MCP Server
Create a single MCP server that exposes all tools through a unified interface, using the existing tool registry.

### Phase 2: Migrate Tools to MCP Servers
Gradually migrate tools from standalone scripts to MCP-accessible functions.

### Phase 3: Deprecate Standalone Scripts
Mark standalone scripts as deprecated and redirect to MCP servers.

## Implementation Plan

### Step 1: Create Unified Tool Server
- **File:** `mcp_servers/unified_tool_server.py`
- **Purpose:** Single entry point for all tools via tool registry
- **Features:**
  - Dynamic tool discovery via `tool_registry.py`
  - Tool execution via adapter pattern
  - Error handling and validation
  - Tool metadata and documentation

### Step 2: Create Category-Specific MCP Servers
Create focused MCP servers for major categories:
- `agent-operations-server.py`
- `infrastructure-server.py`
- `documentation-server.py`
- `testing-server.py`
- `business-intelligence-server.py`
- `analysis-server.py`

### Step 3: Update Existing MCP Servers
Enhance existing servers with additional tools from their domains.

### Step 4: Create Migration Script
- **File:** `tools/migrate_tools_to_mcp.py`
- **Purpose:** Automatically migrate tool functions to MCP servers
- **Features:**
  - Scan tools directory
  - Identify tool functions
  - Generate MCP server code
  - Update tool registry

## Unified Tool Server Architecture

```python
# mcp_servers/unified_tool_server.py
"""
Unified Tool MCP Server
Exposes all tools through a single MCP interface using tool registry
"""

from tools.tool_registry import ToolRegistry

def list_tools():
    """List all available tools"""
    registry = ToolRegistry()
    return registry.list_tools()

def execute_tool(tool_name: str, **kwargs):
    """Execute a tool by name"""
    registry = ToolRegistry()
    tool_class = registry.get_tool_class(tool_name)
    tool_instance = tool_class()
    return tool_instance.execute(**kwargs)

def get_tool_info(tool_name: str):
    """Get tool metadata and documentation"""
    registry = ToolRegistry()
    tool_class = registry.get_tool_class(tool_name)
    tool_instance = tool_class()
    spec = tool_instance.get_spec()
    return {
        "name": spec.name,
        "description": spec.description,
        "category": spec.category,
        "parameters": spec.parameters,
        "examples": spec.examples
    }
```

## Benefits

1. **Unified Access:** All tools accessible via single MCP interface
2. **Dynamic Discovery:** Tools automatically discovered via registry
3. **Type Safety:** Consistent interface across all tools
4. **Error Handling:** Centralized error handling and validation
5. **Documentation:** Automatic tool documentation generation
6. **Extensibility:** Easy to add new tools without modifying servers

## Migration Timeline

- **Week 1:** Create unified tool server + migration script
- **Week 2:** Migrate high-priority tools (agent ops, coordination)
- **Week 3:** Migrate remaining tools
- **Week 4:** Deprecate standalone scripts, update documentation

## Success Criteria

- ✅ All tools accessible via MCP servers
- ✅ Tool registry integrated with MCP
- ✅ Standalone scripts deprecated
- ✅ Documentation updated
- ✅ No breaking changes to existing workflows




