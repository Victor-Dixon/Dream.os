# 🛠️ V2 Tools Flattening - Agent-3 Action Plan

**Agent**: Agent-3 (Infrastructure & DevOps Specialist)  
**Date**: 2025-01-27  
**Priority**: HIGH  
**Status**: IN PROGRESS  
**Type**: Coordinated Effort (All Agents)

---

## 📋 TASK ACKNOWLEDGMENT

✅ **Received HIGH priority V2 Tools Flattening assignment**  
✅ **Reviewed consolidation strategy and current tools_v2/ structure**  
✅ **Identified Agent-3's role in coordinated effort**

---

## 🎯 AGENT-3'S ROLE

As **Infrastructure & DevOps Specialist**, I am responsible for:

1. **Infrastructure Tools Migration**
   - Review `tools_v2/categories/infrastructure_tools.py` (already exists with 4 tools)
   - Identify infrastructure/DevOps tools in `tools/` that need migration
   - Create adapters following the adapter pattern
   - Register tools in `tool_registry.py`

2. **System Health & Monitoring Tools**
   - Workspace health monitoring tools
   - System status tools
   - Infrastructure analysis tools

3. **DevOps Automation Tools**
   - Deployment automation
   - CI/CD related tools
   - System maintenance tools

---

## 🔍 CURRENT STATE ANALYSIS

### **Existing Infrastructure Tools in tools_v2/**

✅ **`tools_v2/categories/infrastructure_tools.py`** (342 lines - V2 Compliant)
- `OrchestratorScanTool` - Scan orchestrators for V2 violations
- `FileLineCounterTool` - Count lines for V2 compliance
- `ModuleExtractorPlannerTool` - Suggest extraction opportunities
- `ROICalculatorTool` - Calculate ROI for refactoring

### **Infrastructure Tools in tools/ (Candidates for Migration)**

#### **Tier 1 - High Priority (Immediate Migration)**

1. **Workspace Health Tools**
   - `workspace_health_monitor.py` - Health monitoring
   - `workspace_health_checker.py` - Health checks
   - `workspace_auto_cleaner.py` - Auto cleanup
   - `auto_workspace_cleanup.py` - Automated cleanup

2. **System Status Tools**
   - `agent_status_quick_check.py` - Quick status check
   - `swarm_status_broadcaster.py` - Status broadcasting
   - `reset_all_agent_status.py` - Status reset

3. **Infrastructure Analysis**
   - `comprehensive_tool_runtime_audit.py` - Runtime audit
   - `audit_broken_tools.py` - Broken tools audit
   - `audit_project_components.py` - Component audit

#### **Tier 2 - Medium Priority (Next Phase)**

4. **DevOps Automation**
   - `auto_status_updater.py` - Auto status updates
   - `auto_inbox_processor.py` - Inbox automation
   - `session_transition_automator.py` - Session automation
   - `agent_lifecycle_automator.py` - Lifecycle automation

5. **Monitoring & Observability**
   - `discord_status_dashboard.py` - Status dashboard
   - `browser_pool_manager.py` - Browser pool management
   - `cache_invalidator.py` - Cache management

#### **Tier 3 - Lower Priority (Future)**

6. **Specialized Tools**
   - `memory_leak_scanner.py` - Memory leak detection
   - `quarantine_manager.py` - Quarantine management
   - `refresh_cache.py` - Cache refresh

---

## 📊 MIGRATION STRATEGY

### **Phase 1: High-Priority Infrastructure Tools (This Cycle)**

**Target**: Migrate 8-10 high-priority tools to `infrastructure_tools.py`

**Process**:
1. Review each tool's functionality
2. Create adapter class following `IToolAdapter` pattern
3. Add to `tools_v2/categories/infrastructure_tools.py`
4. Register in `tool_registry.py`
5. Test via toolbelt
6. Mark original as deprecated

**Tools to Migrate**:
- [ ] `workspace_health_monitor.py` → `WorkspaceHealthMonitorTool`
- [ ] `workspace_health_checker.py` → `WorkspaceHealthCheckerTool`
- [ ] `workspace_auto_cleaner.py` → `WorkspaceAutoCleanerTool`
- [ ] `agent_status_quick_check.py` → `AgentStatusQuickCheckTool`
- [ ] `comprehensive_tool_runtime_audit.py` → `ToolRuntimeAuditTool`
- [ ] `audit_broken_tools.py` → `BrokenToolsAuditTool`
- [ ] `auto_status_updater.py` → `AutoStatusUpdaterTool`
- [ ] `session_transition_automator.py` → `SessionTransitionAutomatorTool`

### **Phase 2: Medium-Priority Tools (Next Cycle)**

**Target**: Migrate 5-7 medium-priority tools

**Tools to Migrate**:
- [ ] `auto_inbox_processor.py` → `AutoInboxProcessorTool`
- [ ] `agent_lifecycle_automator.py` → `AgentLifecycleAutomatorTool`
- [ ] `discord_status_dashboard.py` → `DiscordStatusDashboardTool`
- [ ] `browser_pool_manager.py` → `BrowserPoolManagerTool`
- [ ] `cache_invalidator.py` → `CacheInvalidatorTool`

### **Phase 3: Documentation & Cleanup**

1. Update `tools_v2/README.md` with new infrastructure tools
2. Create migration guide for infrastructure tools
3. Add deprecation warnings to old tools
4. Coordinate with other agents on shared tools

---

## 🔧 ADAPTER PATTERN IMPLEMENTATION

### **Example Adapter Structure**

```python
class WorkspaceHealthMonitorTool(IToolAdapter):
    """Monitor workspace health and report issues."""
    
    def get_name(self) -> str:
        return "workspace_health_monitor"
    
    def get_description(self) -> str:
        return "Monitor workspace health and report issues"
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="workspace_health_monitor",
            version="1.0.0",
            category="infrastructure",
            summary="Monitor workspace health and report issues",
            required_params=[],
            optional_params={"check_all": False},
        )
    
    def validate(self, params: dict[str, Any]) -> tuple[bool, list[str]]:
        return (True, [])
    
    def execute(
        self, params: dict[str, Any] = None, context: dict[str, Any] | None = None
    ) -> ToolResult:
        # Implementation wrapping original tool
        # ...
        return ToolResult(success=True, output=output)
```

---

## 📝 REGISTRATION IN TOOL REGISTRY

After creating adapters, register in `tools_v2/tool_registry.py`:

```python
TOOL_REGISTRY: dict[str, tuple[str, str]] = {
    # ... existing tools ...
    
    # Infrastructure tools
    "infra.workspace_health": ("tools_v2.categories.infrastructure_tools", "WorkspaceHealthMonitorTool"),
    "infra.health_check": ("tools_v2.categories.infrastructure_tools", "WorkspaceHealthCheckerTool"),
    "infra.auto_cleanup": ("tools_v2.categories.infrastructure_tools", "WorkspaceAutoCleanerTool"),
    "infra.status_check": ("tools_v2.categories.infrastructure_tools", "AgentStatusQuickCheckTool"),
    "infra.runtime_audit": ("tools_v2.categories.infrastructure_tools", "ToolRuntimeAuditTool"),
    "infra.broken_tools": ("tools_v2.categories.infrastructure_tools", "BrokenToolsAuditTool"),
    "infra.auto_status": ("tools_v2.categories.infrastructure_tools", "AutoStatusUpdaterTool"),
    "infra.session_transition": ("tools_v2.categories.infrastructure_tools", "SessionTransitionAutomatorTool"),
}
```

---

## ✅ SUCCESS CRITERIA

- [ ] 8-10 high-priority infrastructure tools migrated
- [ ] All tools accessible via `python -m tools_v2.toolbelt <tool_name>`
- [ ] All tools registered in `tool_registry.py`
- [ ] Original tools marked as deprecated
- [ ] Documentation updated
- [ ] V2 compliance maintained (<400 lines per file)
- [ ] All tools tested and working

---

## 🤝 COORDINATION WITH OTHER AGENTS

**Agent-1** (Integration & Core Systems): Coordinate migration of shared tools  
**Agent-2** (Architecture & Design): Review adapter pattern implementation  
**Agent-7** (Web Development): Update tool registry as needed  
**Agent-8** (SSOT & System Integration): Ensure SSOT compliance

**Communication**: Update progress in status.json and coordinate via inbox

---

## ⚡ NEXT ACTIONS

1. **Immediate**: Review first 3-4 high-priority tools
2. **This Cycle**: Create adapters for 3-4 tools
3. **Next Cycle**: Complete Phase 1 migration (8-10 tools)
4. **Documentation**: Update README and create migration guide

---

## 🐝 WE. ARE. SWARM.

**Agent-3 Status**: ACTIVE - Working on V2 Tools Flattening (Infrastructure focus)  
**Estimated Completion**: 2-3 cycles for Phase 1  
**Blockers**: None identified  
**Coordination**: Ready to coordinate with other agents

---

*Plan created: 2025-01-27*  
*Next update: After first tool migration*

