# 🛠️ V2 Tools Flattening Plan - Agent-7

**Agent**: Agent-7 (Web Development Specialist)  
**Date**: 2025-01-27  
**Priority**: HIGH  
**Status**: IN PROGRESS

---

## 📊 CURRENT STATE ANALYSIS

### Tools_v2 Registry Status
- **Current Tools**: 100 tools registered
- **Category Files**: 37 category modules
- **Tool Classes**: 127 tool adapter classes

### Web-Related Tools Audit

#### Tools in `tools/` Directory (Need Migration):
1. **Dashboard Tools**:
   - `compliance_dashboard.py` - Main dashboard generator
   - `dashboard_html_generator_refactored.py` - HTML generation (245 lines)
   - `dashboard_charts.py` - JavaScript charts (180 lines)
   - `dashboard_styles.py` - CSS generation (69 lines)
   - `dashboard_data_aggregator.py` - Data aggregation
   - `discord_status_dashboard.py` - Discord status dashboard

2. **Web/UI Tools**:
   - `browser_pool_manager.py` - Browser management
   - (Other web-related tools to be identified)

#### Tools Already in tools_v2:
- ✅ `compliance_tools.py` - Has `ComplianceHistoryTool` and `PolicyCheckTool`
- ✅ `discord_webhook_tools.py` - Discord webhook tools
- ✅ `discord_tools.py` - Discord bot tools

---

## 🎯 MIGRATION PLAN

### Phase 1: Dashboard Tools Migration (HIGH PRIORITY)

#### 1.1 Create Dashboard Tools Category
**File**: `tools_v2/categories/dashboard_tools.py`

**Tools to Create**:
- `DashboardGenerateTool` - Main dashboard generation
- `DashboardDataAggregateTool` - Data aggregation
- `DashboardHTMLTool` - HTML generation
- `DashboardChartsTool` - Chart generation
- `DashboardStylesTool` - Style generation
- `DiscordStatusDashboardTool` - Discord status dashboard

**Adapter Pattern**:
```python
class DashboardGenerateTool(IToolAdapter):
    """Generate compliance dashboards."""
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="dashboard.generate",
            version="1.0.0",
            category="dashboard",
            summary="Generate compliance dashboard",
            required_params=["directory"],
            optional_params={"pattern": "**/*.py", "include_history": True}
        )
    
    def execute(self, params: dict[str, Any], context: dict[str, Any] | None = None) -> ToolResult:
        # Call tools/compliance_dashboard.py via subprocess or direct import
        ...
```

#### 1.2 Update Tool Registry
Add to `tools_v2/tool_registry.py`:
```python
# Dashboard tools
"dashboard.generate": ("tools_v2.categories.dashboard_tools", "DashboardGenerateTool"),
"dashboard.data": ("tools_v2.categories.dashboard_tools", "DashboardDataAggregateTool"),
"dashboard.html": ("tools_v2.categories.dashboard_tools", "DashboardHTMLTool"),
"dashboard.charts": ("tools_v2.categories.dashboard_tools", "DashboardChartsTool"),
"dashboard.styles": ("tools_v2.categories.dashboard_tools", "DashboardStylesTool"),
"dashboard.discord": ("tools_v2.categories.dashboard_tools", "DiscordStatusDashboardTool"),
```

### Phase 2: Browser/Web Tools Migration

#### 2.1 Browser Tools Category
**File**: `tools_v2/categories/browser_tools.py`

**Tools to Create**:
- `BrowserPoolManagerTool` - Browser pool management

### Phase 3: Integration with Existing Tools

#### 3.1 Enhance Compliance Tools
- Add dashboard generation to existing `compliance_tools.py`
- Or create separate dashboard category (preferred for separation of concerns)

---

## 📋 IMPLEMENTATION CHECKLIST

### Dashboard Tools
- [ ] Create `tools_v2/categories/dashboard_tools.py`
- [ ] Implement `DashboardGenerateTool` adapter
- [ ] Implement `DashboardDataAggregateTool` adapter
- [ ] Implement `DashboardHTMLTool` adapter
- [ ] Implement `DashboardChartsTool` adapter
- [ ] Implement `DashboardStylesTool` adapter
- [ ] Implement `DiscordStatusDashboardTool` adapter
- [ ] Register all tools in `tool_registry.py`
- [ ] Test all dashboard tools via toolbelt
- [ ] Update documentation

### Browser Tools
- [ ] Create `tools_v2/categories/browser_tools.py`
- [ ] Implement `BrowserPoolManagerTool` adapter
- [ ] Register in tool registry
- [ ] Test browser tools

### Coordination
- [ ] Coordinate with Agent-1 (Integration & Core Systems)
- [ ] Coordinate with Agent-8 (SSOT & System Integration)
- [ ] Share progress with all agents
- [ ] Update consolidation strategy document

---

## 🔄 COORDINATION NOTES

### With Agent-1:
- Share dashboard tools migration plan
- Coordinate on integration tools overlap
- Review adapter patterns

### With Agent-8:
- Ensure SSOT compliance for tool registry
- Verify no duplicate tool implementations
- Review tool categorization

### With All Agents:
- Share progress updates
- Coordinate on shared tool dependencies
- Report completion status

---

## 📊 SUCCESS METRICS

- [ ] All web-related tools migrated to tools_v2
- [ ] All tools follow adapter pattern
- [ ] All tools registered in tool registry
- [ ] All tools accessible via toolbelt CLI
- [ ] V2 compliance maintained (<400 lines per file)
- [ ] No duplicate tool implementations
- [ ] Documentation updated

---

## 🚀 NEXT STEPS

1. **Immediate**: Create `dashboard_tools.py` category file
2. **This Cycle**: Implement dashboard tool adapters
3. **Next Cycle**: Test and register all tools
4. **Coordination**: Share progress with Agent-1 and Agent-8

---

**WE. ARE. SWARM.** 🐝⚡🔥

