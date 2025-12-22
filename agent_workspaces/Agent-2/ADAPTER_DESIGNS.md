# 🔧 V2 Tools Flattening - Adapter Designs

**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-01-27  
**Priority:** HIGH  
**Status:** IN PROGRESS  
**Task:** V2 Tools Flattening - Adapter Designs

---

## 📊 EXECUTIVE SUMMARY

**Objective:** Design IToolAdapter implementations for remaining captain tools that need migration.

**Priority Tools:**
1. ✅ `captain.message_all` - Message all agents (HIGH PRIORITY)
2. ✅ `captain.find_idle` - Find idle agents (HIGH PRIORITY)
3. ✅ `captain.gas_check` - Check agent gas levels (HIGH PRIORITY)
4. ⏳ `captain.self_message` - Self-message tool
5. ⏳ `captain.architectural_checker` - Architecture validation
6. ⏳ `captain.coordinate_validator` - Coordinate validation
7. ⏳ `captain.import_validator` - Import validation
8. ⏳ `captain.morning_briefing` - Morning briefing generator
9. ⏳ `captain.update_log` - Update log tool
10. ⏳ `captain.hard_onboard` - Hard onboarding tool
11. ⏳ `captain.toolbelt_help` - Toolbelt help generator

---

## 🎯 ADAPTER DESIGNS

### **1. MessageAllAgentsTool** ⭐⭐ HIGH PRIORITY

**Source:** `tools/captain_message_all_agents.py`  
**Target:** `tools/categories/captain_tools.py`  
**Name:** `captain.message_all`

**Design:**
```python
class MessageAllAgentsTool(IToolAdapter):
    """Send message to all swarm agents including Captain."""
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="captain.message_all",
            version="1.0.0",
            category="captain",
            summary="Send message to all swarm agents",
            required_params=["message"],
            optional_params={
                "priority": "regular",
                "include_captain": True,
                "tags": []
            },
        )
    
    def execute(self, params, context=None) -> ToolResult:
        # Call messaging_cli for each agent
        # Return aggregated results
```

**Integration:**
- Add to `tools/categories/captain_tools.py`
- Register in `tool_registry.py` as `captain.message_all`
- Deprecate `tools/captain_message_all_agents.py`

---

### **2. FindIdleAgentsTool** ⭐⭐ HIGH PRIORITY

**Source:** `tools/captain_find_idle_agents.py`  
**Target:** `tools/categories/captain_tools.py`  
**Name:** `captain.find_idle`

**Design:**
```python
class FindIdleAgentsTool(IToolAdapter):
    """Find agents that are idle or need task assignment."""
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="captain.find_idle",
            version="1.0.0",
            category="captain",
            summary="Find idle agents needing task assignment",
            required_params=[],
            optional_params={"hours_threshold": 1},
        )
    
    def execute(self, params, context=None) -> ToolResult:
        # Check all agent status.json files
        # Identify idle agents (no current_task or "idle" status)
        # Return list of idle agents with reasons
```

**Integration:**
- Add to `tools/categories/captain_tools.py`
- Register in `tool_registry.py` as `captain.find_idle`
- Deprecate `tools/captain_find_idle_agents.py`

---

### **3. GasCheckTool** ⭐⭐ HIGH PRIORITY

**Source:** `tools/captain_gas_check.py`  
**Target:** `tools/categories/captain_tools.py`  
**Name:** `captain.gas_check`

**Design:**
```python
class GasCheckTool(IToolAdapter):
    """Check when agents last received messages (gas levels)."""
    
    def get_spec(self) -> ToolSpec:
        return ToolSpec(
            name="captain.gas_check",
            version="1.0.0",
            category="captain",
            summary="Check agent message gas levels",
            required_params=[],
            optional_params={"threshold_hours": 2},
        )
    
    def execute(self, params, context=None) -> ToolResult:
        # Check inbox timestamps for all agents
        # Identify low gas agents (no recent messages)
        # Return gas status for all agents
```

**Integration:**
- Add to `tools/categories/captain_tools.py`
- Register in `tool_registry.py` as `captain.gas_check`
- Deprecate `tools/captain_gas_check.py`

---

## 📋 IMPLEMENTATION PLAN

### **Phase 1: High Priority Tools** (IMMEDIATE)
1. ✅ Design MessageAllAgentsTool adapter
2. ✅ Design FindIdleAgentsTool adapter
3. ✅ Design GasCheckTool adapter
4. ⏳ Implement adapters in `captain_tools.py`
5. ⏳ Register in `tool_registry.py`
6. ⏳ Test adapters
7. ⏳ Deprecate old files

### **Phase 2: Medium Priority Tools** (NEXT)
1. ⏳ Design remaining captain tool adapters
2. ⏳ Implement in appropriate category files
3. ⏳ Register in tool registry
4. ⏳ Test and deprecate

### **Phase 3: Validation & Coordination** (FINAL)
1. ⏳ Validate all adapters follow IToolAdapter pattern
2. ⏳ Coordinate with Agent-1, Agent-7, Agent-8
3. ⏳ Update documentation
4. ⏳ Final review and merge

---

## 🎯 SUCCESS CRITERIA

- [x] Adapter designs created for priority tools
- [ ] All adapters implement IToolAdapter pattern
- [ ] All adapters registered in tool_registry.py
- [ ] All adapters tested and working
- [ ] Old files deprecated with migration notes
- [ ] Team coordination complete

---

**WE. ARE. SWARM.** 🐝⚡🔥

