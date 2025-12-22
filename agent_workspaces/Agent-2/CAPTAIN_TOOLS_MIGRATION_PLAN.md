# 🎯 Captain Tools Migration Plan

**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-01-27  
**Priority:** HIGH  
**Status:** IN PROGRESS  
**Task:** V2 Tools Flattening - Captain Tools Consolidation

---

## 📊 EXECUTIVE SUMMARY

**Current State:**
- 15+ `captain_*.py` files scattered in `tools/` directory
- `tools/categories/captain_coordination_tools.py` exists but uses wrong pattern (not IToolAdapter)
- Need to migrate all captain tools to proper adapters in `tools/`

**Objective:**
- Migrate all captain tools to `tools/` using IToolAdapter pattern
- Consolidate into appropriate category files
- Register all tools in tool_registry.py
- Deprecate old files

---

## 🔍 CAPTAIN TOOLS INVENTORY

### **Tools in `tools/` Directory:**

1. ✅ `captain_check_agent_status.py` → Already has `captain.status_check`
2. ⏳ `captain_message_all_agents.py` → Needs adapter
3. ⏳ `captain_self_message.py` → Needs adapter
4. ⏳ `captain_find_idle_agents.py` → Needs adapter
5. ⏳ `captain_gas_check.py` → Needs adapter
6. ⏳ `captain_architectural_checker.py` → Needs adapter
7. ⏳ `captain_coordinate_validator.py` → Needs adapter
8. ⏳ `captain_import_validator.py` → Needs adapter
9. ⏳ `captain_morning_briefing.py` → Needs adapter
10. ✅ `captain_completion_processor.py` → Partially migrated (wrong pattern)
11. ✅ `captain_leaderboard_update.py` → Already has `captain.update_leaderboard`
12. ✅ `captain_next_task_picker.py` → Partially migrated (wrong pattern)
13. ✅ `captain_roi_quick_calc.py` → Partially migrated (wrong pattern)
14. ⏳ `captain_update_log.py` → Needs adapter
15. ⏳ `captain_hard_onboard_agent.py` → Needs adapter
16. ⏳ `captain_toolbelt_help.py` → Needs adapter
17. ✅ `captain_snapshot.py` → Already has `health.snapshot`

**Total:** 17 captain tools
- ✅ **Already migrated:** 6 tools (but some need pattern fix)
- ⏳ **Need migration:** 11 tools

---

## 🏗️ MIGRATION STRATEGY

### **Category Assignment:**

**A. Core Operations (→ captain_tools.py):**
- `captain_message_all_agents.py` → `captain.message_all`
- `captain_self_message.py` → `captain.self_message`
- `captain_find_idle_agents.py` → `captain.find_idle`
- `captain_gas_check.py` → `captain.gas_check`

**B. Analysis (→ captain_tools_advanced.py):**
- `captain_architectural_checker.py` → `captain.arch_check`
- `captain_coordinate_validator.py` → `captain.coord_validate`
- `captain_import_validator.py` → `captain.import_validate`
- `captain_morning_briefing.py` → `captain.briefing`

**C. Workflow (→ captain_coordination_tools.py - FIX PATTERN):**
- `captain_completion_processor.py` → `captain.process_completion` (fix pattern)
- `captain_next_task_picker.py` → `captain.pick_task` (fix pattern)
- `captain_roi_quick_calc.py` → `captain.roi_calc` (fix pattern)
- `captain_update_log.py` → `captain.update_log`
- `captain_hard_onboard_agent.py` → `captain.hard_onboard`

**D. Help/UI (→ coordination_tools.py):**
- `captain_toolbelt_help.py` → `coord.toolbelt_help`

---

## 🔧 ADAPTER PATTERN DESIGN

### **Standard IToolAdapter Pattern:**

```python
from tools.adapters.base_adapter import IToolAdapter, ToolSpec, ToolResult

class CaptainMessageAllTool(IToolAdapter):
    """Send message to all agents including Captain."""
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="captain.message_all",
            version="1.0.0",
            category="captain",
            summary="Send message to all 8 agents including Captain",
            required_params=["message"],
            optional_params={
                "priority": "normal",
                "include_captain": True
            }
        )
    
    def validate(self, params: dict) -> tuple[bool, list[str]]:
        spec = self.get_spec()
        return spec.validate_params(params)
    
    def execute(self, params: dict, context: dict | None) -> ToolResult:
        from tools.captain_message_all_agents import message_all_agents
        
        try:
            message = params["message"]
            priority = params.get("priority", "normal")
            include_captain = params.get("include_captain", True)
            
            result = message_all_agents(message, priority, include_captain)
            
            return ToolResult(
                success=True,
                output=f"Messaged {len(result)} agents successfully",
                data=result
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error_message=str(e)
            )
```

---

## 📋 MIGRATION CHECKLIST

### **Phase 1: Fix Existing Adapters (Immediate)**

**captain_coordination_tools.py:**
- [ ] Convert `CompletionProcessor` to `ProcessCompletionTool(IToolAdapter)`
- [ ] Convert `LeaderboardUpdater` to `UpdateLeaderboardTool(IToolAdapter)`
- [ ] Convert `NextTaskPicker` to `PickNextTaskTool(IToolAdapter)`
- [ ] Convert `ROIQuickCalculator` to `ROICalculatorTool(IToolAdapter)`
- [ ] Register all in `tool_registry.py`

### **Phase 2: Core Operations (Next)**

**captain_tools.py:**
- [ ] Create `CaptainMessageAllTool` adapter
- [ ] Create `CaptainSelfMessageTool` adapter
- [ ] Create `CaptainFindIdleTool` adapter
- [ ] Create `CaptainGasCheckTool` adapter
- [ ] Register all in `tool_registry.py`

### **Phase 3: Analysis Tools (Next)**

**captain_tools_advanced.py:**
- [ ] Create `CaptainArchitecturalCheckerTool` adapter
- [ ] Create `CaptainCoordinateValidatorTool` adapter
- [ ] Create `CaptainImportValidatorTool` adapter
- [ ] Create `CaptainMorningBriefingTool` adapter
- [ ] Register all in `tool_registry.py`

### **Phase 4: Workflow Tools (Next)**

**captain_coordination_tools.py:**
- [ ] Create `CaptainUpdateLogTool` adapter
- [ ] Create `CaptainHardOnboardTool` adapter
- [ ] Register all in `tool_registry.py`

### **Phase 5: Help Tools (Next)**

**coordination_tools.py:**
- [ ] Create `ToolbeltHelpTool` adapter
- [ ] Register in `tool_registry.py`

### **Phase 6: Deprecation (Final)**

- [ ] Add deprecation warnings to all old `captain_*.py` files
- [ ] Point to tools adapters
- [ ] Update documentation

---

## 🎯 IMMEDIATE ACTION ITEMS

### **This Cycle:**

1. **Fix captain_coordination_tools.py pattern** (2 hours)
   - Convert existing classes to IToolAdapter
   - Register in tool_registry.py
   - Test via toolbelt

2. **Create 4 core operation adapters** (3 hours)
   - CaptainMessageAllTool
   - CaptainSelfMessageTool
   - CaptainFindIdleTool
   - CaptainGasCheckTool

3. **Coordinate with team** (1 hour)
   - Share migration plan
   - Get feedback
   - Update status

**Total Estimated Time:** 6 hours

---

## 📊 SUCCESS METRICS

**Coverage:**
- [ ] 100% captain tools migrated to adapters
- [ ] 100% tools registered in tool_registry.py
- [ ] 100% tools testable via toolbelt

**Quality:**
- [ ] All adapters follow IToolAdapter pattern
- [ ] All tools have proper ToolSpec
- [ ] All tools have error handling

**Documentation:**
- [ ] Migration plan complete ✅
- [ ] Adapter designs documented
- [ ] Deprecation warnings added

---

## 🤝 COORDINATION

**With Agent-7 (Web Development):**
- Update tool_registry.py
- Review registry structure
- Ensure proper categorization

**With Agent-8 (SSOT):**
- Ensure SSOT compliance
- Review scattered tools
- Validate consolidation

**Communication:**
- Update status file
- Send progress to Captain inbox
- Coordinate via messaging system

---

**WE. ARE. SWARM.** 🐝⚡🔥

**Status:** Migration plan complete, ready for implementation

