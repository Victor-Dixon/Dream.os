# 🔧 V2 COMPLIANCE SPLIT PLAN - infrastructure_tools.py

**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-01-27  
**Priority:** CRITICAL  
**Status:** ⏳ IN PROGRESS

---

## 🎯 OBJECTIVE

Split `infrastructure_tools.py` (748 lines) into 3 V2-compliant files (<400 lines each).

---

## 📊 SPLIT STRATEGY

### **File 1: infrastructure_workspace_tools.py** (~250 lines)
**Tools (6):**
- WorkspaceHealthMonitorTool
- WorkspaceAutoCleanerTool
- AgentStatusQuickCheckTool
- AutoStatusUpdaterTool
- SessionTransitionAutomatorTool
- SwarmStatusBroadcasterTool

### **File 2: infrastructure_audit_tools.py** (~300 lines)
**Tools (5):**
- OrchestratorScanTool
- FileLineCounterTool
- ToolRuntimeAuditTool
- BrokenToolsAuditTool
- ProjectComponentsAuditTool

### **File 3: infrastructure_utility_tools.py** (~200 lines)
**Tools (3):**
- ModuleExtractorPlannerTool
- ROICalculatorTool
- BrowserPoolManagerTool

### **File 4: infrastructure_tools.py** (Backward Compatibility)
- Re-export all tools from split files
- Maintain backward compatibility
- ~50 lines

---

## 🔄 TOOL REGISTRY UPDATES

**Registry entries to update:**
- `infra.workspace_health` → `infrastructure_workspace_tools`
- `infra.workspace_cleanup` → `infrastructure_workspace_tools`
- `infra.agent_status_check` → `infrastructure_workspace_tools`
- `infra.auto_status_updater` → `infrastructure_workspace_tools`
- `infra.session_transition` → `infrastructure_workspace_tools`
- `infra.swarm_broadcast` → `infrastructure_workspace_tools`
- `infra.orchestrator_scan` → `infrastructure_audit_tools`
- `infra.file_lines` → `infrastructure_audit_tools`
- `infra.tool_runtime_audit` → `infrastructure_audit_tools`
- `infra.broken_tools_audit` → `infrastructure_audit_tools`
- `infra.project_components_audit` → `infrastructure_audit_tools`
- `infra.extract_planner` → `infrastructure_utility_tools`
- `infra.roi_calc` → `infrastructure_utility_tools`
- `browser.pool` → `infrastructure_utility_tools`

---

## ✅ SUCCESS CRITERIA

- [ ] All 3 new files <400 lines
- [ ] All tools maintain adapter pattern
- [ ] Tool registry updated
- [ ] Backward compatibility maintained
- [ ] No breaking changes

---

**WE. ARE. SWARM. SPLITTING. COMPLYING. 🐝⚡🔥**




